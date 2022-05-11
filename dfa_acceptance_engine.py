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
        states.append(line.strip())
    
    if check_transitions==1:
        transitions.append(line.strip())

transition_dict={}

for transition in transitions:
    transition_list=transition.split(", ")
    if transition_list[0] in transition_dict:
        transition_dict[transition_list[0]][transition_list[1]]=transition_list[2]
    else:
        transition_dict[transition_list[0]]={}
        transition_dict[transition_list[0]][transition_list[1]]=transition_list[2]

final_states=[]

for i in states:
    if i[len(i)-1]=='S' or (len(i.split(', '))==3 and (i.split(', ')[2]=='S' or i.split(', ')[1]=='S')):
        starting_state=i
    if i[len(i)-1]=='F' or (len(i.split(', '))==3 and (i.split(', ')[2]=='F' or i.split(', ')[1]=='F')):
        final_states.append(i.split(',')[0])
starting_state=starting_state.split(',')[0]

word_to_test=input("Input the word: ")

def accepts(letters,transition_dict,starting_state,final_states,word_to_test):
    for letter in word_to_test:
        if letter not in letters:
            return False
    state = starting_state
    for c in word_to_test:
        state = transition_dict[state][c]
    return state in final_states

if accepts(letters,transition_dict,starting_state,final_states,word_to_test):
    print("This word is accepted by the DFA")
else:
    print("This word is not accepted by the DFA")