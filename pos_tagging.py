"""
This function takes in input:
• a tuple R of roles,
• a tuple S of strings,
• a dictionary T whose keys are the roles in R plus the special role Start and values are dictionaries T[r] such that
    - the keys of T[r] are the roles in R plus the special role End
    - the values of T[r] are the transition probabilities between r and the corresponding role defined by the key
• a dictionary E whose keys are the strings in S and value are dictionaries E[s] such that
    - the keys of E[s] are the roles in R
    - the values in E[s] are the emission probabilities between s and the corresponding role defined by the key
The function returns a dictionary whose keys are the words in S and the values are the roles assigned to these words, so that the selected assignment is the one of maximum likelihood.
"""

def pos_tagging(R, S, T, E):
    
    result = viterbi(R,S,T,E)
    
    i = 0
    tags = dict()
    for s in S:
        tags[s] = result[i]
        i += 1
        
    return tags

def viterbi(R, S, T, E):
    
    trellis = dict() # table to hold probability of each state given each observation
    pointers = dict() # table to hold backpointer to best prior state
    
    # Determine each hidden state's probability at time 0
    for i in range(len(R)):
        trellis[R[i]] = {0: T["Start"][R[i]] * E[S[0]][R[i]]}
        pointers[R[i]] = {0: 0}
        
    # Tracking each state's most likely prior state and probability
    for j in range(1,len(S)):
        for i in range(len(R)):
            maxProb = trellis[R[0]][j-1] * T[R[0]][R[i]] * E[S[j]][R[i]]
            maxState = R[0]
            for k in range(1,len(R)):
                prob = trellis[R[k]][j-1] * T[R[k]][R[i]] * E[S[j]][R[i]]
                if prob > maxProb:
                    maxProb = prob
                    maxState = R[k]
            trellis[R[i]][j] = maxProb
            pointers[R[i]][j] = maxState
                
    bestPath = []
    
    # Find the most likely final state
    maxProb = trellis[R[0]][len(S)-1] * T[R[0]]["End"]
    maxState = R[0]
    for k in range(1,len(R)):
        prob = trellis[R[k]][len(S)-1] * T[R[k]]["End"]
        if prob > maxProb:
            maxProb = prob
            maxState = R[k]
    trellis["End"] = {len(S)-1: maxProb}
    pointers["End"] = {len(S)-1: maxState}
            
    # Backtrack from last observation
    for j in range(len(S)-1,-1,-1): 
        bestPath.insert(0,maxState) # insert best state at beginning of list
        maxState = pointers[maxState][j] # set maxState to best prior state
        
    return bestPath
        
        
        

            

    
    
    
    

    