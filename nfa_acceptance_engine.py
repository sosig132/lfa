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

states_list=states[:]


for i in range(len(states)):
    if ', F' in states[i] and ', S' in states[i]:
        states[i]=str(i)+", S"+", F"
    if states[i][-1]=='F':
        states[i]=str(i)+", F"
    if states[i][-1]=='S':
        states[i]=str(i)+", S"
    if states[i][-1] != 'F' and states[i][-1] != 'S':
        states[i]=str(i)


final_states=[]

for i in states:
    if ', S' in i:
        starting_state=i
    if ', F' in i:
        final_states.append(i.split(',')[0])
starting_state=starting_state.split(',')[0]

for i in range(len(states)):
    states[i]=states[i].split(',')[0]

for i in range(len(states_list)):
    states_list[i]=states_list[i].split(',')[0]


#print(states[states_list.index(transitions[0].split(', ')[0])])
for i in range(len(transitions)):
    transitions[i]=f"{states[states_list.index(transitions[i].split(', ')[0])]}, {letters[letters.index(transitions[i].split(', ')[1])]}, {states[states_list.index(transitions[i].split(', ')[2])]}"

transition_dict={}

for transition in transitions:
    transition_list=transition.split(", ")
    if transition_list[0] in transition_dict:
        if transition_list[1] not in transition_dict[transition_list[0]].keys():
            transition_dict[transition_list[0]][transition_list[1]]=[transition_list[2]]
        else:
            transition_dict[transition_list[0]][transition_list[1]].append(transition_list[2])
    else:
        transition_dict[transition_list[0]]={}
        transition_dict[transition_list[0]][transition_list[1]]=[transition_list[2]]




dfa_transition_dict={}

additional_states=[]
list_of_keys = list(list(transition_dict.keys())[0])

dfa_transition_dict[list_of_keys[0]]={}

for i in range(len(letters)):
    combined_states="".join(transition_dict[list_of_keys[0]][letters[i]])
    dfa_transition_dict[list_of_keys[0]][letters[i]]=combined_states

    if combined_states not in list_of_keys:
        additional_states.append(combined_states)
        list_of_keys.append(combined_states)


def checkAnag(s1, s2):
    if(sorted(s1)==sorted(s2)):
        return 1
    return 0

n=1
while len(additional_states) != 0:
    dfa_transition_dict[additional_states[0]]={}
    for i in range(len(additional_states[0])):
        for j in range(len(letters)):
            aux=[]
            for k in range(len(additional_states[0])):
                check =  all(item in aux for item in transition_dict[additional_states[0][k]][letters[j]])
                if check is False:
                    for l in transition_dict[additional_states[0][k]][letters[j]]:
                        if l not in aux:
                            aux+=l
                           # print(f"t:{t}")
            s=""
            s=s.join(aux)
            if s not in list_of_keys:
                additional_states.append(s)
                list_of_keys.append(s)
            dfa_transition_dict[additional_states[0]][letters[j]]=s
        
    additional_states.remove(additional_states[0])
    n+=1

for i in list(dfa_transition_dict.keys()):
    for j in list(dfa_transition_dict.keys()):
        if i!=j and checkAnag(i,j)==1:
            dfa_transition_dict.pop(i, None)
for i in list(dfa_transition_dict.keys()):
    if len(set(i))!=len(i):
        dfa_transition_dict.pop(i)

dfa_sttes = list(dfa_transition_dict.keys())

dfa_final_state=[]

for i in dfa_sttes:
    for j in i:
        if j in final_states:
            dfa_final_state.append(i)
            break

word_to_test=input()

print(dfa_transition_dict)

def accepts(letters,transition_dict,starting_state,final_states,word_to_test):
    for letter in word_to_test:
        if letter not in letters:
            return False
    state = starting_state
    for c in word_to_test:
        print(state)
        state = transition_dict[state][c]
    return state in final_states

if accepts(letters,dfa_transition_dict,starting_state,dfa_final_state,word_to_test):
    print("This word is accepted by the NFA")
else:
    print("This word is not accepted by the NFA")