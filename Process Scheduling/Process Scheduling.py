import sys
import random
import copy
from collections import deque

if sys.stdin.isatty(): sys.exit()

input = ""
    
for line in sys.stdin:
   input += line

def convert(input):
    st = []
    list_str = input.strip(' ').strip('\n').split('\n')

    for i in list_str:
        list_aux = i.split(' ')
        list_int = list(map(int, list_aux))
        st.append(list_int)
    
    return st

def dynamic_priority(st):
    avg_return = 0
    avg_arrival = 0
    avg_waiting = 0

    num_of_proc = len(st)
    end_t = 0

    for i in range(num_of_proc):
        end_t += st[i][1]
        st[i].append(5)
        st[i].append(False)

    i = 0

    while i <= end_t:
        exc = 0
        flag = False
        for j in range(len(st)):
            if(st[j][0] <= i and (st[j][2] > st[exc][2] or not flag)):
                exc = j
                flag = True
            st[j][2] += 1
            if(st[j][0] <= i):
                avg_waiting += 1

        if not flag:
            i += 1
            continue
        
        st[exc][1] -= 1
        st[exc][2] -= 2
        avg_waiting -= 1

        if not st[exc][3]:
            st[exc][3] = True
            avg_arrival += (i - st[exc][0])

        i += 1

        if st[exc][1] == 0:
            avg_return += (i - st[exc][0])
            st.pop(exc)
            if len(st) == 0:
                break
        
    avg_return /= num_of_proc
    avg_arrival /= num_of_proc
    avg_waiting /= num_of_proc

    print('PRI    {:.2f}       {:.2f}         {:.2f}'.format(avg_return, avg_arrival, avg_waiting))

def lottery(st):
    avg_return = 0
    avg_arrival = 0
    avg_waiting = 0
    
    num_of_proc = len(st)
    end_t = 0
    
    for i in range(num_of_proc):
        end_t += st[i][1]
        st[i].append(False)

    i = 0

    while i <= end_t:
        count = 0
        flag = False
        
        while count < len(st)*3:
            exc = random.randrange(0, len(st))
            if(st[exc][0] <= i):
                flag = True
                break
            count += 1
        
        if not flag:
            i += 1
            continue
        
        if st[exc][1] > 1:
            exc_time = 2
        else: 
            exc_time = 1

        st[exc][1] -= exc_time

        if not st[exc][2]:
            st[exc][2] = True
            avg_arrival += (i - st[exc][0])

        for j in range(len(st)):
            if(j != exc):
                if(st[j][0] <= i):
                    avg_waiting += exc_time
                if(exc_time == 2 and st[j][0] == i + 1):
                    avg_waiting += 1

        i += exc_time

        if st[exc][1] == 0:
            avg_return += (i - st[exc][0])
            st.pop(exc)
            if(len(st) == 0):
                break
        
    avg_return /= num_of_proc
    avg_arrival /= num_of_proc
    avg_waiting /= num_of_proc

    print('LOT    {:.2f}       {:.2f}         {:.2f}'.format(avg_return, avg_arrival, avg_waiting))

def round_robin(st):
    avg_return = 0
    avg_arrival = 0
    avg_waiting = 0
    
    num_of_proc = len(st)
    end_t = 0
    circular_queue = deque()
    
    for i in range(num_of_proc):
        end_t += st[i][1]
        st[i].append(False)
        circular_queue.append(st[i])

    i = 0

    while i <= end_t:
        flag = False
        for j in range(len(circular_queue)):
            if(circular_queue[0][0] <= i):
                flag = True
                break
            else:
                circular_queue.rotate(-1)

        if not flag:
            i += 1
            continue
        
        if circular_queue[0][1] > 1:
            exc_time = 2
        else: 
            exc_time = 1

        circular_queue[0][1] -= exc_time

        if not circular_queue[0][2]:
            circular_queue[0][2] = True
            avg_arrival += (i - circular_queue[0][0])

        for j in range(1, len(circular_queue)):
            if(circular_queue[j][0] <= i):
                avg_waiting += exc_time
            if(exc_time == 2 and circular_queue[j][0] == i + 1):
                avg_waiting += 1

        i += exc_time

        if circular_queue[0][1] == 0:
            avg_return += (i - circular_queue[0][0])
            circular_queue.rotate(-1)
            circular_queue.pop()
            if len(circular_queue) == 0:
                break
        else:
            circular_queue.rotate(-1)

    avg_return /= num_of_proc
    avg_arrival /= num_of_proc
    avg_waiting /= num_of_proc

    print('RR     {:.2f}       {:.2f}         {:.2f}'.format(avg_return, avg_arrival, avg_waiting))


st_proc = convert(input)

print('    AVG RETURN  AVG ARRIVAL  AVG WAITING')

dynamic_priority(copy.deepcopy(st_proc))

lottery(copy.deepcopy(st_proc))

round_robin(copy.deepcopy(st_proc))