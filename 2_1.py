import sys

input_file = sys.argv[1]
word_to_test = sys.argv[2]
f = open(input_file)



valid=1

check_symbols=0
check_tape=0
check_states=0
check_transitions=0
check_blank=0

symbols=[]
tape_symbols=[]
states=[]
transitions=[]
reject=[]
accept=[]
start=''
blank=''

#f=open('tm_config_input',"r")
#l=f.readlines()

#loading input file

for line in f:
    if line[0]=='#':
        continue
    if 'BLANK' in line:
        check_blank = 1
    if 'TAPESYMBOLS' in line:
        check_tape=1
        continue
    if 'SYMBOLS' in line:
        check_symbols=1
        continue
    if 'STATES' in line:
        check_states=1
        continue
    if 'TRANSITIONS' in line:
        check_transitions=1
        continue
    if 'END' in line:
        check_states, check_transitions, check_symbols, check_tape, check_blank = 0, 0, 0, 0, 0

    if check_symbols==1:
        symbols.append(line.strip())
    
    if check_states==1:
        states.append(line.strip().split(',',1)[0])
        if ',' in line:
            if 'R' in line:
                reject.append(line.strip().split(',',1)[0])
            elif 'A' in line:
                accept.append(line.strip().split(',',1)[0])
            elif 'S' in line:
                start = line.strip().split(',',1)[0]
    if check_transitions==1:
        transitions.append(line.strip())
    
    if check_tape==1:
        tape_symbols.append(line.strip())
    if check_blank==1:
        blank=line.strip()

for transition in transitions:
    transition_list=transition.replace(' -> ', ', ').split(", ")
    if transition_list[0] not in states:
        print(f'Invalid TM input file: Invalid state(There is no state "{transition_list[0]}" in States)')
        valid=0
        break
    if transition_list[2] not in states:
        print(f'Invalid TM input file: Invalid state(There is no state "{transition_list[2]}" in States)')
        valid=0
        break
    if transition_list[1] not in tape_symbols and transition_list[1]!=blank:
        print(f'Invalid TM input file: Invalid symbol(There is no symbol "{transition_list[1]}" in Symbols)')
        valid=0
        break
    if transition_list[3] not in tape_symbols and transition_list[3]!=blank and len(transition_list)==5:
        print(f'Invalid TM input file: Invalid state(There is no symbol "{transition_list[3]}" in Symbols)')
        valid=0
        break

transition_dict={}

for transition in transitions:
    transition_list=transition.replace(" -> ",", ").split(", ")
    if transition_list[0] in transition_dict:
        if transition_list[1] not in transition_dict[transition_list[0]].keys():
            transition_dict[transition_list[0]][transition_list[1]]=[transition_list[2]]
        else:
            transition_dict[transition_list[0]][transition_list[1]].append(transition_list[2])
            print(f'Invalid TM input file: Test for determinism fail')
            valid=0
    else:
        transition_dict[transition_list[0]]={}
        transition_dict[transition_list[0]][transition_list[1]]=[transition_list[2]]


if(valid==1):
    print("Valid TM")