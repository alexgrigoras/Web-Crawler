import json
from mpi4py import MPI
from map_reduce import MapReduce

def main():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()

    MAP = 10
    REDUCE = 20
    STOP = 100
    NR_NODES = 12

    # master node
    if rank == 0:
        file_name = 'output/adjacency_list.json'
        with open(file_name, 'r', encoding='utf-8') as infile:
            json_data = json.load(infile)

        keys = []
        dest_rank = 1

        for data in json_data:
            keys.append(data)

        for key in keys:
            for value in json_data[key]:
                data = {"k": key, "v": value}
                comm.isend(data, dest=dest_rank, tag=MAP)
                dest_rank += 1
                if dest_rank > (NR_NODES - 1):
                    dest_rank = 1

        for dest_rank in range(1, NR_NODES):
            data = {"k": "", "v": ""}
            comm.isend(data, dest=dest_rank, tag=STOP)

        print("[" + str(rank) + "] - TERMINATED ")

    # worker nodes
    else:
        is_terminated = False
        mr = MapReduce(rank)

        while not is_terminated:
            status = MPI.Status()
            data = comm.recv(source=0, tag=MPI.ANY_TAG, status=status)
            tag = status.Get_tag()
            if tag == MAP:
                key = data["k"]
                value = data["v"]
                mr.map(key, value)
            elif tag == REDUCE:
                print("[" + str(rank) + "] - REDUCE")
            elif tag == STOP:
                print("[" + str(rank) + "] - TERMINATED")
                is_terminated = True
            else:
                print("[" + str(rank) + "] - INCORRECT TAG RECEIVED")

        mr.store_values()



if __name__ == "__main__":
    main()
