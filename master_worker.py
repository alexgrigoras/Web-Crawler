import glob
import json

from mpi4py import MPI

from map_reduce import MapReduce


def transmit_data(data_queue, nr_nodes, comm, phase):
    dest_rank = 1
    temp_data = []

    confirmation = 30

    while data_queue and dest_rank < nr_nodes:
        data = data_queue.pop()
        temp_data.append(data)
        comm.isend(data, dest=dest_rank, tag=phase)
        dest_rank += 1

    status = MPI.Status()

    is_finished = False

    # mapping phase
    while not is_finished:
        received_data = comm.recv(source=MPI.ANY_SOURCE, tag=MPI.ANY_TAG, status=status)
        source = status.Get_source()
        tag = status.Get_tag()
        if tag == confirmation:
            if received_data in temp_data:
                temp_data.remove(received_data)
            if data_queue:
                data = data_queue.pop()
                comm.isend(data, dest=source, tag=phase)
                temp_data.append(data)
            else:
                is_finished = True

    return temp_data


def main():
    comm = MPI.COMM_WORLD
    nr_nodes = comm.Get_size()
    rank = comm.Get_rank()
    map_phase = 10
    reduce_phase = 20
    confirmation = 30
    stop_phase = 100
    master = 0

    # master node
    if rank == master:

        # mapping phase
        file_name = 'output/adjacency_list.json'
        with open(file_name, 'r', encoding='utf-8') as infile:
            json_data = json.load(infile)

        keys = []
        data_queue = []

        for data in json_data:
            keys.append(data)

        for key in keys:
            for value in json_data[key]:
                data = {"k": key, "v": value}
                data_queue.append(data)

        # transmit data
        temp_data = transmit_data(data_queue, nr_nodes, comm, map_phase)
        while temp_data:
            temp_data = transmit_data(temp_data, nr_nodes, comm, map_phase)

        # reduction phase
        path = 'output/map/*.json'
        files = glob.glob(path)
        for file in files:
            with open(file, 'r', encoding='utf-8') as infile:
                json_data = json.load(infile)

            keys = []
            data_queue = []

            for data in json_data:
                keys.append(data)

            for key in keys:
                for value in json_data[key]:
                    data = {"k": key, "v": value}
                    data_queue.append(data)

            # transmit data
            temp_data = transmit_data(data_queue, nr_nodes, comm, reduce_phase)
            #while temp_data:
            #    temp_data = transmit_data(temp_data, nr_nodes, comm, reduce_phase)

        # stopping phase
        for dest_rank in range(1, nr_nodes):
            data = {"k": "", "v": ""}
            comm.isend(data, dest=dest_rank, tag=stop_phase)

        print("[" + str(rank) + "] - TERMINATED ")

    # worker nodes
    else:
        is_terminated = False
        mr = MapReduce(rank)

        while not is_terminated:
            status = MPI.Status()
            data = comm.recv(source=0, tag=MPI.ANY_TAG, status=status)
            tag = status.Get_tag()
            if tag == map_phase:
                key = data["k"]
                value = data["v"]
                mr.map(key, value)
            elif tag == reduce_phase:
                key = data["k"]
                value = data["v"]
                mr.reduce(key, value)
            elif tag == stop_phase:
                print("[" + str(rank) + "] - TERMINATED")
                is_terminated = True
            else:
                print("[" + str(rank) + "] - INCORRECT TAG RECEIVED")

            comm.isend(data, dest=master, tag=confirmation)

        mr.store_values()


if __name__ == "__main__":
    main()
