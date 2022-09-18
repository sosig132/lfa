valid=1

check_var=0
check_sigma=0
check_start=0
check_rules=0

var=[]
sigma=[]
start =''
rules=[]

f=open('cfg_config_input',"r")
l=f.readlines()

#loading input file

for line in l:
    if line[0]=='#':
        continue
    if 'SIGMA' in line:
        check_sigma=1
        continue
    if 'START' in line:
        check_start=1
        continue
    if 'VARIABLES' in line:
        check_var=1
        continue
    if 'RULE' in line:
        check_rules=1
        continue
    if 'END' in line:
        check_sigma, check_start, check_var, check_rules= 0, 0, 0, 0

    if check_sigma==1:
        sigma.append(line.strip())
    
    if check_start==1:
        start = line.strip()

    if check_var==1:
        var.append(line.strip())
    
    if check_rules==1:
        rules.append(line.strip())

for rule in rules:
    rule_list=rule.split(" -> ")
    if rule_list[0] not in var:
        print(f'Invalid CFG input file: Invalid variable(There is no variable "{rule_list[0]}" in Variables)')
        valid=0
        break
    for i in rule_list[1]:
        if i not in sigma and i not in var:
            valid=0
            print(f'Invalid CFG input file: Invalid variable/terminal(There is no variable/terminal "{i}" in Variables or in Sigma)')

if start not in var:
    
    valid=0
    print(f'Invalid CFG input file: Invalid starting state')

if(valid==1):
    print("Valid CFG")