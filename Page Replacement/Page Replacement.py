import sys
import copy
from collections import deque

if sys.stdin.isatty(): sys.exit()

input = ""

for line in sys.stdin:
    input += line

def convert(input):
    page_ref = []
    
    list_str = input.strip(' ').strip('\n').split('\n')
    page_frame = int(list_str[0])
    list_str.pop(0)

    for i in list_str:
        page_ref.append(int(i))
    
    return (page_ref, page_frame)

def second_chance(pag_ref, pag_frame):
    pag_fault = 0
    ref_count = 0
    memory = [[None, 0] for _ in range(pag_frame)]

    circular_queue = deque()
    
    for i in range(len(pag_ref)):
        success = False
        for j in range(pag_frame):
            if memory[j][0] == None:
                memory[j][0] = pag_ref[i]
                memory[j][1] = 1
                circular_queue.append(j)
                pag_fault += 1
                success = True
                break
            
            if memory[j][0] == pag_ref[i]:
                memory[j][1] = 1
                success = True
                break
        
        if not success:
            index = circular_queue[0]
            
            while memory[index][1] != 0:
                circular_queue.rotate(-1)
                index = circular_queue[0]
            
            circular_queue.rotate(-1)

            memory[index][0] = pag_ref[i]
            memory[index][1] = 1
            pag_fault += 1

        ref_count += 1
        if ref_count == 4:
            ref_count = 0
            
            for j in range(pag_frame):
                memory[j][1] = 0

    print('SC       {}'.format(pag_fault))

def optimal_algorithm(pag_ref, pag_frame):
    pag_fault = 0
    memory = [[None, 0] for _ in range(pag_frame)]
    
    for i in range(len(pag_ref)):
        success = False
        for j in range(pag_frame):
            if memory[j][0] == None:
                memory[j][0] = pag_ref[i]
                pag_fault += 1
                success = True
                break
            
            if memory[j][0] == pag_ref[i]:
                success = True
                break
        
        if not success:
            last_ref = 0
            ref_count = 0
            
            for j in range(pag_frame):
                will_be_ref = False

                for k in range(i, len(pag_ref)):
                    if pag_ref[k] == memory[j][0]:
                        will_be_ref = True
                        break
                    ref_count += 1
                
                if will_be_ref:
                    memory[j][1] = ref_count
                else:
                    memory[j][1] = None

            for j in range(pag_frame):
                if memory[j][1] == None:
                    last_ref = j
                    break
                if memory[j][1] > memory[last_ref][1]:
                    last_ref = j

            memory[last_ref][0] = pag_ref[i]
            pag_fault += 1

    print('OPT      {}'.format(pag_fault))

def working_set(pag_ref, pag_frame):
    pag_fault = 0
    ref_count = 0
    virtual_time = 0
    threshold = int(pag_frame/2) + 1
    memory = [[None, 0, 0] for _ in range(pag_frame)]
    
    for i in range(len(pag_ref)):
        virtual_time += 1
        success = False
        for j in range(pag_frame):
            if memory[j][0] == None:
                memory[j][0] = pag_ref[i]
                memory[j][1] = 1
                memory[j][2] = virtual_time
                pag_fault += 1
                success = True
                break
            
            if memory[j][0] == pag_ref[i]:
                memory[j][1] = 1
                memory[j][2] = virtual_time
                success = True
                break
        
        if not success:
            replaced = 0
            
            for j in range(pag_frame):
                if memory[j][1] == 0:
                    age = virtual_time - memory[j][2]
                    if age > threshold:
                        replaced = j
                        break
                    if age > (virtual_time - memory[replaced][2]):
                        replaced = j
                         
            memory[replaced][0] = pag_ref[i]
            memory[replaced][1] = 1
            memory[replaced][2] = virtual_time

            pag_fault += 1

        ref_count += 1
        if ref_count == 4:
            ref_count = 0
            
            for j in range(pag_frame):
                memory[j][1] = 0

    print('WS       {}'.format(pag_fault))


pag_ref, pag_frame = convert(input)

print('    PAGE FAULTS')

second_chance(copy.deepcopy(pag_ref), pag_frame)

optimal_algorithm(copy.deepcopy(pag_ref), pag_frame)

working_set(copy.deepcopy(pag_ref), pag_frame)