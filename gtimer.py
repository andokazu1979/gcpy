from mpi4py import MPI

lst_sta = [-1.0] * 100
lst_end = [-1.0] * 100
lst_elapse = []

def timer_sta(i):
    lst_sta[i] = MPI.Wtime()

def timer_end(i):
    lst_end[i] = MPI.Wtime()

def get_lst_elapse():
    for sta, end in zip(lst_sta, lst_end):
        if sta >= 0.0 and end >= 0.0:
            elapse = end - sta
            lst_elapse.append(elapse)
    return lst_elapse
