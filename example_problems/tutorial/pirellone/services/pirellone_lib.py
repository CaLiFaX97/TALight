#!/usr/bin/env python3import randomimport copydef random_pirellone(m, n, seed="any", solvable=False):    if seed=="any":        random.seed()        seed = random.randrange(0,1000000)    else:        seed = int(seed)    random.seed(seed)            line = [random.randint(0, 1) for _ in range(n)]    inv = [int(not x) for x in line]    pirellone = []    for _ in range(m):        if random.randint(0, 1) == 0:            pirellone.append(line[:])        else:            pirellone.append(inv[:])    if not solvable:        row = random.randrange(0, n)        col = random.randrange(0, m)        pirellone[row][col] = 1-pirellone[row][col]    return pirellone, seeddef switch_row(i,pirellone):    for j in range(len(pirellone[0])):        pirellone[i][j] = int(not pirellone[i][j])def switch_col(j,pirellone):    for i in range(len(pirellone)):        pirellone[i][j] = int(not pirellone[i][j])def is_solvable(pirellone, m, n):    for i in range(m):        inv = pirellone[0][0] != pirellone[i][0]        for j in range(n):            v = not pirellone[i][j] if inv else pirellone[i][j]            if v != pirellone[0][j]:                return False    return True def print_pirellone(pirellone):    for l in pirellone:        print(*l)         def off_lista(pirellone,solu,TAc, LANG):    l=len(solu)    empty=[[0 for j in range(0,len(pirellone[0]))] for i in range(0,len(pirellone))]    for i in range(0,l):        if solu[i][0]=='r':            if len(solu[i])>2:                switch_row(int(solu[i][1])*10+int(solu[i][2])-1,pirellone)            else:                switch_row(int(solu[i][1])-1,pirellone)        elif solu[i][0]=='c':            if len(solu[i])>2:                switch_col(int(solu[i][1])*10+int(solu[i][2])-1,pirellone)            else:                switch_col(int(solu[i][1])-1,pirellone)        if is_solvable(pirellone, len(pirellone), len(pirellone[0])):        if empty==pirellone:            TAc.OK()            TAc.print("This sequence turns off all lights", "green", ["bold"])            return         else:            TAc.NO()            TAc.print("This sequence doesn't turn off all lights see what happens using your solution:", "red", ["bold"])            print_pirellone(pirellone)            return     else:        check_numberlight(pirellone,count(pirellone),TAc, LANG)        return    def off(pirellone,rs,cs,TAc, LANG): #sapendo sottoinsieme    m=len(rs)    n=len(cs)    empty=[[0 for j in range(0,n)] for i in range(0,m)]    for i in range(0,m):        if rs[i]:            switch_row(i,pirellone)    for j in range(0,n):        if cs[j]:            switch_col(j,pirellone)    if is_solvable(pirellone, len(pirellone), len(pirellone[0])):        if empty==pirellone:            TAc.OK()            TAc.print("This subset turns off all lights", "green", ["bold"])            return         else:            TAc.NO()            TAc.print("This subset doesn't turn off all lights see what happens using your solution:", "red", ["bold"])            print_pirellone(pirellone)            return     else:        check_numberlight(pirellone,count(pirellone),TAc, LANG)        return    def check_numberlight(a,answer,TAc, LANG):    s=[]    for i in range(1,len(a),2):        s.append(i)    up=0    down=1    matrix=0    index=[]    while up<len(a) and down<len(a):            for i in range(len(a[0])-1):                for j in range(i+1,len(a[0])):                    if j not in index and i not in index:                        if a[up][i]==0 and a[down][i]==0:                            if (a[up][j]==1 and a[down][j]==0) or (a[up][j]==0 and a[down][j]==1):                                matrix+=1                                #print("matrice di colonne: "+str(i)+","+str(j)+" e righe: "+str(up)+","+str(down))                                index.append(j)                                index.append(i)                        if (a[up][i]==1 and a[down][i]==0) or (a[up][i]==0 and a[down][i]==1):                            if a[up][j]==0 and a[down][j]==0:                                matrix+=1                                #print("matrice di colonne: "+str(i)+","+str(j)+" e righe: "+str(up)+","+str(down))                                index.append(j)                                index.append(i)                        if a[up][i]==1 and a[down][i]==1:                            if (a[up][j]==1 and a[down][j]==0) or (a[up][j]==0 and a[down][j]==1):                                matrix+=1                                #print("matrice di colonne: "+str(i)+","+str(j)+" e righe: "+str(up)+","+str(down))                                index.append(j)                                index.append(i)                        if (a[up][i]==1 and a[down][i]==0) or (a[up][i]==0 and a[down][i]==1):                            if a[up][j]==1 and a[down][j]==1:                                matrix+=1                                #print("matrice di colonne: "+str(i)+","+str(j)+" e righe: "+str(up)+","+str(down))                                index.append(j)                                index.append(i)            up+=1            down+=1            if down in s:                index=[]    if answer==matrix:        TAc.OK()        TAc.print("You can not turn off more lights", "green", ["bold"])        return     elif answer>matrix:        TAc.NO()        TAc.print("You can turn off more lights, check it: ", "red", ["bold"])        print_pirellone(a)        return     def count(p):    m=len(p)    s=0    for i in range(m):        s+=sum(p[i])    return(s)def off_lista_noprint(pirellone,solu):    l=len(solu)    empty=[[0 for j in range(0,len(pirellone[0]))] for i in range(0,len(pirellone))]    for i in range(0,l):        if solu[i][0]=='r':            if len(solu[i])>2:                switch_row(int(solu[i][1])*10+int(solu[i][2])-1,pirellone)            else:                switch_row(int(solu[i][1])-1,pirellone)        elif solu[i][0]=='c':            if len(solu[i])>2:                switch_col(int(solu[i][1])*10+int(solu[i][2])-1,pirellone)            else:                switch_col(int(solu[i][1])-1,pirellone)                    if empty==pirellone:               return True    else:        return False    def soluzione(pirellone,m,n):    if is_solvable(pirellone, m, n):        R=[0]*len(pirellone)        C=[0]*len(pirellone[0])    for i in range(0,m):            for j in range(0,n):            if pirellone[i][j]:                C[j] = 1                switch_col(j,pirellone)    for i in range(0,m):         if pirellone[i][0]:            R[i] = 1            switch_row(i,pirellone)    lista=[]    for i in range(m):        if R[i]:            lista.append(f"r{i+1}")    for j in range(n):        if C[j]:            lista.append(f"c{j+1}")    return listadef soluzione_min(pirellone,m,n):    pirellone1=copy.deepcopy(pirellone)    if is_solvable(pirellone, m, n):        R1=[0]*len(pirellone)        C1=[0]*len(pirellone[0])        R2=[0]*len(pirellone)        C2=[0]*len(pirellone[0])    for j in range(0,n):        if pirellone1[0][j]:            C1[j] = 1            switch_col(j,pirellone1)    for i in range(0,m):         if pirellone1[i][0]:            R1[i] = 1            switch_row(i,pirellone1)    pirellone2=copy.deepcopy(pirellone)        for i in range(0,m):        if pirellone2[i][0]:            R2[i] = 1            switch_row(i,pirellone2)    for j in range(0,n):        if pirellone2[0][j]:            C2[j] = 1            switch_col(j,pirellone2)    lista=[]    if (sum(R1)+sum(C1))<=(sum(R2)+sum(C2)):        for i in range(m):            if R1[i]:                lista.append(f"r{i+1}")        for j in range(n):            if C1[j]:                lista.append(f"c{j+1}")    else:        for i in range(m):            if R2[i]:                lista.append(f"r{i+1}")        for j in range(n):            if C2[j]:                lista.append(f"c{j+1}")    return listadef soluzione_min_step(pirellone,m,n):    lista=[]    if is_solvable(pirellone, m, n):        R1=[0]*len(pirellone)        C1=[0]*len(pirellone[0])    for j in range(0,n):        if pirellone[0][j]:            C1[j] = 1            lista.append(f"c{j+1}")            switch_col(j,pirellone)            print_pirellone(pirellone)            return stampa_lista(lista)    for i in range(0,m):         if pirellone[i][0]:            R1[i] = 1            switch_row(i,pirellone)            lista.append(f"r{i+1}")            print_pirellone(pirellone)            return stampa_lista(lista)        return def solution_toolong(sol,m,n):    longsol=sol    #stampa_lista(sol)    for i in range(random.randint(0,int(len(sol)/2)-1 )):        num=sol[random.randint(0, len(sol)-1)]        longsol.append(num)        longsol.append(num)    if random.randint(0,1)==1:        num=f"r{random.randint(1,m)}"         if num  not in sol:            longsol.append(num)            longsol.append(num)    if random.randint(0,2)==1:        num=f"c{random.randint(1,n)}"        if num  not in sol:            longsol.append(num)            longsol.append(num)          random.shuffle(longsol)    return(longsol)                    def stampa_lista(lista):    s=''    for i in range(len(lista)):        s+=f'{lista[i]} '    print(s)    return 