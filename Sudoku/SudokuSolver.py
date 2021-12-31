import timeit, sys

global N, SYMSET, subBlockHeight, subBlockWidth, CONSTRAINTS, NEIGHBORS


def setGlobals(pzl):
    global N, SYMSET, subBlockHeight, subBlockWidth, CONSTRAINTS, NEIGHBORS
    N = int(len(pzl)**0.5 + 0.5)
    assert N**2 == len(pzl)

    labels = "123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    SYMSET = set()
    i = 0
    while len(SYMSET)!=N:
        SYMSET.add(labels[i])
        i+=1
    SYMSET = set(sorted([*SYMSET]))
    
    for char in pzl:
        assert char in SYMSET or char == "."

    subBlockHeight = [i for i in range(int(N**0.5),0,-1) if N%i == 0][0]
    subBlockWidth = N//subBlockHeight
    rowConstraints = [list(range(i,i+N)) for i in range(0,len(pzl),N)]
    colConstraints = [[row[i] for row in rowConstraints] for i in range(N)]
    blockConstraints = []
    for r in range(0,N,subBlockWidth):
        for c in range(0,N,subBlockHeight):
            spot = r + c*N #top left of each block
            now = []
            for i in range(subBlockHeight):
                now+=list(range(spot,spot+subBlockWidth))
                spot += N
            blockConstraints.append(now)

    CONSTRAINTS = [set(x) for x in rowConstraints+colConstraints+blockConstraints]
    constraints3 = []
    for p in range(len(pzl)):
        constraints3.append([i for i in range(len(CONSTRAINTS)) if p in CONSTRAINTS[i]])
    NEIGHBORS = []
    for p in range(len(pzl)):
        cons = constraints3[p]
        NEIGHBORS.append(CONSTRAINTS[cons[0]].union(CONSTRAINTS[cons[1]], CONSTRAINTS[cons[2]]))
        NEIGHBORS[p].remove(p)


def isInvalid(pzl):
    global NEIGHBORS
    for p in range(len(pzl)):
        if(pzl[p] in {pzl[x] for x in NEIGHBORS[p]}):
            return True
    return False

def checkSum(pzl):
    return sum(ord(x) for x in pzl) - 81*ord("0")

def bruteForce(pzl,psbll):
    global N, SYMSET, subBlockHeight, subBlockWidth, CONSTRAINTS, NEIGHBORS

    psbl = [x.copy() for x in psbll]
    next = [(len(x),p,x) for p,x in enumerate(psbl) if(x)]
    if(not (next)):
        if("." in pzl):
            return ""
        return pzl
    length,poss1,sym1 = min(next)

    if(len(sym1) <= 1):
        sym,poss = sym1,{poss1}
    else:
        poss2Len = N**2
        #nbrVals = [set() if sym!="." else {pzl[nbrPos] for nbrPos in NEIGHBORS[p]} for p,sym in enumerate(pzl)]
        for tempSym in SYMSET:
            if(poss2Len == 1):
                break
            setAllPosForSym = {p for p,x in enumerate(psbl) if(tempSym in x)}
            for cs in CONSTRAINTS:
                setAllPosForSymInCs = cs.intersection(setAllPosForSym)
                if(len(setAllPosForSymInCs) < poss2Len and len(setAllPosForSymInCs) > 0):
                    sym2,poss2,poss2Len = tempSym,setAllPosForSymInCs,len(setAllPosForSymInCs)
                    if(poss2Len == 1):
                        break

        #print(poss2,sym2)
        if(len(poss2)<len(sym1)):
            sym,poss = {sym2},poss2
        else:
            sym,poss = sym1,{poss1}


    for label in sym:
        for pos in poss:
            newPzl = list(pzl)
            newPzl[pos] = label
            tempPsbl = [x.copy() for x in psbl]
            for nbr in NEIGHBORS[pos]:
                if(label in tempPsbl[nbr]): tempPsbl[nbr].remove(label)
            tempPsbl[pos].clear()
            bf = bruteForce(''.join(newPzl), tempPsbl)
            if bf: return bf
    return ""


pzl = sys.argv[1] if len(sys.argv)>1 else ""
if (not pzl):
    pzl = input("What is the given puzzle: ")
    
start = timeit.default_timer()

setGlobals(pzl)
nbrVals = [set() if sym!="." else {pzl[nbrPos] for nbrPos in NEIGHBORS[p]} for p,sym in enumerate(pzl)]
psbl = [SYMSET.difference(nbrVals[p]) if(nbrVals[p]) else set() for p in range(len(pzl))]
sol = bruteForce(pzl,psbl)

print()
print("SOLUTION:")
# print("\n\n".join(["\n".join(["\t".join(
#     [sol[c:c+subBlockWidth] for c in range(r, r+N, subBlockWidth)]) 
#                             for r in range(s, s + subBlockHeight*N, N)]) 
#                             for s in range(0, N**2, subBlockHeight*N)]))

for r in range(N):
    if (r % subBlockHeight == 0):
        print()
    for c in range(N):
        if (c % subBlockWidth == 0):
            print("\t", end="")
        loc = r*N + c
        print(sol[loc], end="")
    print()
    
print()
print("Time:",timeit.default_timer()-start, "seconds")
        