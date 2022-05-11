#variables for identifying what section are we on
valid=1

check_sigma=0
check_states=0
check_transitions=0

letters=[]
states=[]
transitions=[]

f=open('dfa_config_file',"r")
l=f.readlines()

#loading input file

for line in l:
    if line[0]=='#':
        continue
    if 'Sigma' in line:
        check_sigma=1
        continue
    if 'States' in line:
        check_states=1
        continue
    if 'Transitions' in line:
        check_transitions=1
        continue
    if 'End' in line:
        check_states, check_transitions, check_sigma = 0, 0, 0

    if check_sigma==1:
        letters.append(line.strip())
    
    if check_states==1:
        states.append(line.strip().split(',',1)[0])
    
    if check_transitions==1:
        transitions.append(line.strip())



#checking if the transition section is valid
#making another states list in case the state is followed by 'S' or 'F'

for transition in transitions:
    transition_list=transition.split(", ")
    if transition_list[0] not in states:
        print(f'Invalid DFA input file: Invalid state(There is no state "{transition_list[0]}" in States)')
        valid=0
        break
    if transition_list[2] not in states:
        print(f'Invalid DFA input file: Invalid state(There is no state "{transition_list[2]}" in States)')
        valid=0
        break
    if transition_list[1] not in letters:
        print(f'Invalid DFA input file: Invalid letter(There is no letter "{transition_list[1]}" in Sigma)')
        valid=0
        break

#testing for determinism

transition_dict={}

for transition in transitions:
    transition_list=transition.split(", ")
    if transition_list[0] in transition_dict:
        if transition_list[1] not in transition_dict[transition_list[0]].keys():
            transition_dict[transition_list[0]][transition_list[1]]=[transition_list[2]]
        else:
            transition_dict[transition_list[0]][transition_list[1]].append(transition_list[2])
            print(f'Invalid DFA input file: Test for determinism fail')
            valid=0
    else:
        transition_dict[transition_list[0]]={}
        transition_dict[transition_list[0]][transition_list[1]]=[transition_list[2]]



if valid==1:
    print('Valid DFA input file')