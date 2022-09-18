from random import randint as rand

with open('Laborator LFA\het.txt', 'r') as f:
    s = open('Laborator LFA\hes.txt','w')
    pos = ['PG', 'SG', 'C', 'G', 'SF', 'PF']
    i = 100
    x=0
    a = 800
    
    while x<50:
        i = rand(0,100)
        y = rand(0,100)
        j, k = rand(300,329), rand(300,329)
        while k==j:
            k=rand(300,329)
        s.write(f"INSERT INTO joaca VALUES({a}, {j}, {k}); \n")

        x+=1
        a+=1