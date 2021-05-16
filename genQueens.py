# -*- coding: utf-8 -*-
"""
Created on Sat May 15 17:12:08 2021

@author: Miguelsancerv
"""

import numpy as np
import random
import math

def evalDIAG(arr, ind, RSC,RIC,ROW):
    val = arr[ind]
    add = 1;
    rsc,ric,rwc = [],[],[]
    
    sup = True
    inf = True
    row = True
    
    if ind in RSC:
        sup = False
        
    if ind in RIC:
        inf = False
        
    if ind in ROW:
        row = False
        
        
    if not (sup or inf or row) :
        return rsc,ric,rwc
    
    for i in range(ind+1,len(arr)):
        if (sup and arr[i] == val + add):
            rsc.append(i)
        if (inf and arr[i] == val - add):
            ric.append(i)
        if (row and arr[i] == val):
            rwc.append(i)
        add += 1
    if (sup and len(rsc) > 0):
        rsc.append(ind)
    if (inf and len(ric) > 0):
        ric.append(ind)
    if (row and len(rwc) > 0):
        rwc.append(ind)
    return rsc,ric,rwc

def solEval(arr):   
    RSC = []
    RIC = []
    RWC = []
    for i in range(0,len(arr)):
        RSCm,RICm,RWCm = evalDIAG(arr,i,RSC,RIC,RWC)
        RSC = np.concatenate((RSC,RSCm))
        RIC = np.concatenate((RIC,RICm))
        RWC = np.concatenate((RWC,RWCm))
    RES = np.unique(np.concatenate((RSC,RIC,RWC)))       
    return len(RES)

def evalAll(pop):
    res = []
    score= [] 
    for item in pop:
        score.append(solEval(item))
        res.append(item)
    return res,score


def checkBackwards(arr,ind,val):
    add = 1
    conf = 0
    i=ind - 1
    while(i>=0):
        # print(val,arr[i],i)
        if(val == arr[i] or val == arr[i] - add or val == arr[i] + add):
            conf += 1
        add +=1
        i -= 1
    return conf


def reduceConflicts(arr):
    for i in range(len(arr)):
        prop = []
        # print("elem",i,arr[i])
        if(checkBackwards(arr,i,arr[i]) > 0):
            for j in range(len(arr)):
                prop.append(checkBackwards(arr,i,j))
            prop = np.array(prop)
            idx = prop.argsort()
            prop = prop[idx]
            arr[i] = idx[0]
            # print(idx,prop)
    return arr
#--------------------------------------------------------------

def initPop(n,q):
    pop = []
    arr = np.arange(0,q)
    for i in range(n):
        pop.append(np.random.permutation(arr))
    return pop

def vs(p1,p2):
    r1 = solEval(p1)
    r2 = solEval(p2)
    
    return p1 if r1<r2 else p2

def tournament(pop,k):
    winners = []
    if(k==0):
        return pop
    while(len(pop)>0):
        if(len(pop) == 1):
            winners.append(pop[0])
            break
        ind1 = random.randint(0,len(pop)-1)
        p1 = pop.pop(ind1)
        ind2 = random.randint(0,len(pop)-1)
        p2 = pop.pop(ind2)
        
        winners.append(vs(p1,p2))
    
    return tournament(winners,k-1)

def Ncross(p1,p2,crosspoints):
    cross = [0]
    cross += crosspoints
    cross += [len(p2)]
    np1,np2 = p1,p2
    res = []
    for i in range(len(cross)-1):
        res = np.concatenate((res,np1[cross[i]:cross[i+1]]))
        np1,np2 = np2,np1
    return res

def elite(pop,n):
    res,score = evalAll(pop)
    
    idx = np.argsort(score)
    res = np.array(res)
    res = res.take(idx,0)
    
    return res[:n]

def mutation(p1,mutp):
    prob = random.random()
    
    if prob > mutp :
        return p1
    
    i1 = random.randint(0,len(p1)-1)
    i2 = random.randint(0,len(p1)-1)
    while(i1==i2):
        i2 = random.randint(0,len(p1)-1)
    p1[i1],p1[i2] = p1[i2],p1[i1]
    return p1

def newPop(pop,n,elit,crossp,mutp):
    nextGen = []
    for i in range(n):
        ind1 = random.randint(0,len(pop)-1)
        ind2 = random.randint(0,len(pop)-1)
        
        nextGen.append(Ncross(pop[ind1],pop[ind2],crossp))
        
    best = elite(pop,elit)
    for cand in best:
        nextGen.append(cand)
    # print(nextGen)
    for i in range(len(nextGen)):
        # nextGen[i] = mutation(nextGen[i],mutp)
        nextGen[i] = reduceConflicts(mutation(nextGen[i],mutp))
    return nextGen

def GeneticQueens(queens,ngen,ntour,crossPoints,mutp,popLim,nelit):
    pop = initPop(popLim,queens)
    for i in range(ngen):
        res = tournament(pop,ntour)
        newGen = newPop(res,popLim-nelit,nelit,crossPoints,mutp)
        pop = newGen
        verify = elite(pop,1)[0]
        score = solEval(verify)
        if(score == 0):
            print("solution found before the end of algorithm")
            return verify,score
        
    res = elite(pop,1)[0]
    score = solEval(res)
    return res,score

def Queens(queens):
    ngen = 20 * queens
    ntour = 2
    crossPoints = [int(math.ceil(queens/3)),int(math.ceil(2*queens/3))]
    mutp = 0.05
    popLim = 10 * queens
    nelit = 2
    
    return GeneticQueens(queens,ngen,ntour,crossPoints,mutp,popLim,nelit)

def exhaustiveTest(n):
    res = 0
    for i in range(n):
        r = Queens(50)
        print(r)
        res += r[1]
        
    res /= n
    print(res)

print(Queens(20))

# exhaustiveTest(10)
    