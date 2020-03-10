from mpi4py import MPI


def main():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()

    if rank == 0:
        req = comm.isend(data, dest=1, tag=11)
        req.wait()
        print(data)
    elif rank == 1:
        req = comm.irecv(source=0, tag=11)
        data = req.wait()
        print(data)


if __name__ == "__main__":
    main()
