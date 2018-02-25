from mpi4py import MPI

lst_sta = [-1.0] * 100
lst_end = [-1.0] * 100
lst_elapse = []
lst_comment = [""] * 100

def timer_sta(i, comment):
    lst_sta[i] = MPI.Wtime()
    lst_comment[i] = comment

def timer_end(i):
    lst_end[i] = MPI.Wtime()

def get_lst_elapse():
    for sta, end, comment in zip(lst_sta, lst_end, lst_comment):
        if sta >= 0.0 and end >= 0.0:
            elapse = end - sta
            d = {comment : elapse}
            lst_elapse.append(d)
    return lst_elapse
