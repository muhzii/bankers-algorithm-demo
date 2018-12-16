import random

NUM_OF_PROCESSES = 0
NUM_OF_RESOURCES_TYPES = 0


class Banker(object):
    def __init__(self, avail, Max):
        self.Need = Max
        self.avail = avail
        self.Allocation = [[0] * NUM_OF_RESOURCES_TYPES for _ in range(NUM_OF_PROCESSES)]

    def request_resource(self, process, type, quantity):
        self.avail[type] -= quantity
        self.Need[process][type] -= quantity
        self.Allocation[process][type] += quantity

        if self.is_safe_state():
            return True
        else:
            self.Need[process][type] += quantity
			self.release_resource(process, type, quantity)
            return False

    def release_resource(self, process, type, quantity):
        self.avail[type] += quantity
        self.Allocation[process][type] -= quantity

    def is_safe_state(self):
        Work = self.avail
        Finish = NUM_OF_PROCESSES * [False]

        for i in range(NUM_OF_PROCESSES):
            if not Finish[i]:
                if self.Need[i] <= Work:
                    Work = [x + y for x, y in zip(Work, self.Allocation[i])]
                    Finish[i] = True
                    i = 0

        for i in range(NUM_OF_PROCESSES):
            if not Finish[i]:
                return False
        return True


def get_inputs_and_init():
    global NUM_OF_PROCESSES
    global NUM_OF_RESOURCES_TYPES

    print("Enter number of processes & number of processes types")
    NUM_OF_PROCESSES, NUM_OF_RESOURCES_TYPES = list(map(int, input().split()))
    print("Enter number of resources available for each type")
    avail = list(map(int, input().split()))
    print("")

    Max = [[0] * NUM_OF_RESOURCES_TYPES for _ in range(NUM_OF_PROCESSES)]
    for i in range(NUM_OF_PROCESSES):
        for j in range(NUM_OF_RESOURCES_TYPES):
            Max[i][j] = random.randint(0, avail[j])

    return Banker(avail, Max)


def main():
    banker = get_inputs_and_init()

    for i in range(NUM_OF_PROCESSES):
        print("Process no." + str(i + 1), end=': ')
        for j in range(NUM_OF_RESOURCES_TYPES):
            print(banker.Need[i][j], end=' ')
        print("")
    print("")

    proc_pool = [x for x in range(NUM_OF_PROCESSES)]
    while True:
        if len(proc_pool) == 0:
            print("")
            print("Done")
            break

        msg = ''
        rand_proc_num = random.choice(proc_pool)
        for res_type in range(NUM_OF_RESOURCES_TYPES):
            req = random.randint(0, 1)
            if req:
                rand_res_quantity = random.randint(0, banker.Need[rand_proc_num][res_type])
                if rand_res_quantity == 0:
                    continue
                flag = banker.request_resource(rand_proc_num, res_type, rand_res_quantity)
                msg += "Process with number %s's request for %s instance/s of resource type %s, is "
                msg %= rand_proc_num + 1, rand_res_quantity, res_type + 1
                if flag:
                    msg += "granted.\n"
                else:
                    msg += "denied.\n"
            else:
                rand_res_quantity = random.randint(0, banker.Allocation[rand_proc_num][res_type])
                if rand_res_quantity == 0:
                    continue
                banker.release_resource(rand_proc_num, res_type, rand_res_quantity)
                msg += "Process with number %s released %s instance/s of resource type %s.\n"
                msg %= rand_proc_num + 1, rand_res_quantity, res_type + 1

        print(msg, end='')

        is_finished = True
        for i, j in zip(banker.Need[rand_proc_num], banker.Allocation[rand_proc_num]):
            if i > 0 or j > 0:
                is_finished = False
                break
        if is_finished:
            proc_pool.remove(rand_proc_num)
            print("Process no." + str(rand_proc_num+1) + " is finished.")

        if len(msg) != 0:
            print("")


main()
