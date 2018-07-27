from mpi4py import MPI

lst_sta = [-1.0] * 100
lst_end = [-1.0] * 100
lst_elapse = [0.0] * 100
lst_comment = [""] * 100

def timer_sta(i, comment):
    lst_sta[i] = MPI.Wtime()
    lst_comment[i] = comment

def timer_end(i):
    lst_end[i] = MPI.Wtime()
    lst_elapse[i] += (lst_end[i] - lst_sta[i])

def get_lst_elapse():
    lst = []
    for sta, end, elapse, comment in zip(lst_sta, lst_end, lst_elapse, lst_comment):
        if sta >= 0.0 and end >= 0.0:
            d = {comment : elapse}
            lst.append(d)
    return lst
