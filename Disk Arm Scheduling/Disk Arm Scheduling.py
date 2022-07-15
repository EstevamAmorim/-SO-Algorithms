import sys
import copy
from collections import deque

if sys.stdin.isatty(): sys.exit()

input = ""

for line in sys.stdin:
    input += line

def convert(input):
    access_req = []

    list_str = input.strip(' ').strip('\n').split('\n')
    outermost_cyl = int(list_str[0])
    start_position = int(list_str[1])

    if start_position > outermost_cyl:
        exit("Error: invalid start position")

    list_str.pop(0)
    list_str.pop(0)

    for i in list_str:
        req = int(i)

        if req > outermost_cyl:
            exit("Error: invalid request")

        access_req.append(req)
    
    return (access_req, start_position)

def FCFS(access_req, start_position):
    prev_access = start_position
    total_cyl = 0

    for i in access_req:
        total_cyl += abs(i - prev_access)
        prev_access = i

    print('FCFS           {}'.format(total_cyl))

def SSTF(access_req, start_position):
    prev_access = start_position
    total_req = len(access_req)
    total_cyl = 0

    for i in range(total_req):
        closest_position = 0
        old_diff = abs(access_req[closest_position] - prev_access)

        for j in range(len(access_req)):
            new_diff = abs(access_req[j] - prev_access)

            if new_diff < old_diff and new_diff > 0:
                old_diff = new_diff
                closest_position = j

        total_cyl += old_diff
        prev_access = access_req[closest_position]
        access_req.pop(closest_position)

    print('SSTF           {}'.format(total_cyl))
        
def elevator(access_req, start_position):
    prev_access = start_position
    access_req.sort()
    first_access = 0
    total_cyl = 0

    for i in range(len(access_req)):
        first_access = i

        if access_req[i] > prev_access:
            break
    
    if first_access == (len(access_req) - 1):
        first_access += 1
    else:
        for i in range(first_access, len(access_req)):
            total_cyl += abs(access_req[i] - prev_access)
            prev_access = access_req[i]

    if first_access > 0:
        for i in range(first_access - 1, -1, -1):
            total_cyl += abs(access_req[i] - prev_access)
            prev_access = access_req[i]

    print('ELVTR          {}'.format(total_cyl))


access_req, start_position = convert(input)

print('         CYLINDERS TRAVELED')

FCFS(copy.deepcopy(access_req), start_position)

SSTF(copy.deepcopy(access_req), start_position)

elevator(copy.deepcopy(access_req), start_position)




