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

print(symbols)
print(tape_symbols)
print(states)
print(transitions)
print(reject)
print(accept)
print(start)
print(blank)


transition_dict={}

for transition in transitions:
    transition_list=transition.split(", ")
    if transition_list[0] in transition_dict:
        if transition_list[1] not in transition_dict[transition_list[0]].keys():
            
            transition_dict[transition_list[0]][transition_list[1]]=[transition_list[i] for i in range(len(transition_list)) if i>=2]
        else:
            transition_dict[transition_list[0]][transition_list[1]].append(transition_list[i] for i in range(len(transition_list)) if i>=2)

    else:
        transition_dict[transition_list[0]]={}
        transition_dict[transition_list[0]][transition_list[1]]=[transition_list[i] for i in range(len(transition_list)) if i>=2]

print(transition_dict)



tape = [blank for i in range(len(word_to_test)+20000)]
tape_copy = tape

def accepts(symbols,word_to_test, transition_dict, reject, accept, start):
    #print(symbols)
    for symbol in word_to_test: 
        
        if symbol not in symbols:
            return 'Rejected'
    state = start
    head = 10000
    posi=head
    for i in range(len(word_to_test)):
        tape[posi]=word_to_test[i]
        tape_copy[posi]=word_to_test[i]
        posi+=1
    
    while True:
        #print(head)
        
        print(list(tape[i] for i in range(10000,10020)))
        print(state)
        print(tape[head])
        print(head)
        state = transition_dict[state][tape[head]][0]
        print(list(tape[i] for i in range(10000,10020)))
        print(state)
        print(tape[head])
        if state in accept:

            return 'Accepted'
        
        if state in reject:
            
            return 'Rejected'
        
        if transition_dict[state][tape[head]][len(transition_dict[state][tape[head]])-1]=='R':
            head+=1
        elif transition_dict[state][tape[head]][len(transition_dict[state][tape[head]])-1]=='L':

            head-=1

        elif transition_dict[state][tape[head]][len(transition_dict[state][tape[head]])-1]=='L' and tape[head-1]==blank:
            if len(transition_dict[state][tape[head]])==3:
                tape[head]=transition_dict[state][tape[head]][1]
                tape_copy[head]=transition_dict[state][tape_copy[head]][1]
                if tape!=tape_copy:
                    return 'EROARE: TAPEURI DIFERITE'
            continue
        if len(transition_dict[state][tape[head-1]])==3:
            tape[head-1]=transition_dict[state][tape[head-1]][1]
            print(tape_copy[head-1])
            print(tape[head-1])
            tape_copy[head-1]=transition_dict[state][tape_copy[head-1]][1]
            if tape!=tape_copy:
                return 'EROARE: TAPEURI DIFERITE'

v = accepts(tape_symbols, word_to_test, transition_dict, reject, accept, start)

print(v)
