from collections import OrderedDict

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

states_nr=len(states)

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
            transition_dict[transition_list[0]][transition_list[1]]=transition_list[2]
        else:
            print(transition_dict)
            transition_dict[transition_list[0]][transition_list[1]].append(transition_list[2])
    else:
        transition_dict[transition_list[0]]={}
        transition_dict[transition_list[0]][transition_list[1]]=transition_list[2]


def matrix(x,y,value):
    return [[value for i in range(x)] for j in range(y)]

pairs_of_states=matrix(states_nr, states_nr, 0)

for i in range(states_nr):
    for j in range(states_nr):
        if i>j and ((states[i] in final_states and states[j] not in final_states) or (states[i] not in final_states and states[j] in final_states)):
            pairs_of_states[i][j]=1
        #if i==j:
            #pairs_of_states[i][j]=0

for i in range(states_nr):
    print(transition_dict[str(i)])

check_if_made=1
while check_if_made==1:
    check_if_made=0
    for i in range(states_nr):
        for j in range(states_nr):
            if pairs_of_states[i][j]==0 and i>j:
                if pairs_of_states[int(transition_dict[str(i)][str(letters[1])])][int(transition_dict[str(j)][str(letters[1])])]==1:
                    pairs_of_states[i][j]=1
                    check_if_made=1

combined_states=[]

new_transition_dict={}

for i in range(states_nr):
    for j in range(states_nr):
        if pairs_of_states[i][j]==0 and i>j:
            combined_states.append(''.join(sorted(states[i]+states[j])))

combined_states_n=[]

for i in combined_states:
    for char in i:    
        combined_states_n.append(char)

for i in range(len(combined_states_n)):
    cnt=0
    index=-1
    for j in range(len(combined_states)): 
        if cnt==0 and combined_states_n[i] in combined_states[j]:
           cnt=1
           index = j
        elif cnt==1 and combined_states_n[i] in combined_states[j]:
            combined_states[index]=combined_states[index]+combined_states[j]
            combined_states[j]='x'
for i in range(len(combined_states)):
    combined_states[i]="".join(OrderedDict.fromkeys(combined_states[i]))

while 'x' in combined_states:
    combined_states.remove('x')

combined_states_n=[]

for i in combined_states:
    new_transition_dict[i]={}
    for char in i:    
        combined_states_n.append(char)

print(combined_states)

for i in range(states_nr):
    print(pairs_of_states[i])

for i in transition_dict.keys():
    if i not in combined_states_n:
        new_transition_dict[i]={}

for i in transition_dict.keys():
    for j in transition_dict[i].keys():
        if i not in combined_states_n and transition_dict[i][j] in combined_states_n:
            index=0
            for k in range(len(combined_states)):
                if transition_dict[i][j] in combined_states[k]:
                    index=k

            new_transition_dict[i][j] =  combined_states[index]
        if i not in combined_states_n and transition_dict[i][j] not in combined_states_n:
            new_transition_dict[i][j]=transition_dict[i][j]
        pass

for i in combined_states:
    for j in letters:
        new_transition_dict[i][j]=''


for i in combined_states:
    for j in letters:            
        for l in combined_states_n:
            if transition_dict[l][j] in combined_states_n:
                #index=0
                for k in range(len(combined_states)):
                    if l in i and transition_dict[l][j] in combined_states[k]:
                        print(transition_dict[l][j], combined_states[k])
                        #index=k
                        print(new_transition_dict[i][j])
                        new_transition_dict[i][j]=combined_states[k]
            else:
                new_transition_dict[i][j]=transition_dict[i[0]][j]

new_final_states=[]

for i in final_states:
    for j in new_transition_dict.keys():
        if i in j:
            new_final_states.append(j)

print(new_transition_dict)

f = open("dfa_result",'w')

f.write("SIGMA:\n")
for i in letters:
    f.write(f"    {i}\n")

f.write("END\n\n")

f.write("STATES:\n")

for i in new_transition_dict.keys():
    f.write(f"    {i}")
    if i in new_final_states:
        f.write(", F")
    if i == combined_states[0]:
        f.write(", S")
    f.write("\n")

f.write("END\n\n")

f.write("TRANSITIONS:\n")

for i in new_transition_dict.keys():
    for j in letters:
        f.write(f"    {i}")
        f.write(f", {j}")
        f.write(f", {new_transition_dict[i][j]}\n")
    f.write("\n")

f.write("END\n")