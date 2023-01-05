def pos_tagging(R, S, T, E):
    
    """
    Parameters
    ----------
    R : tuple 
        roles
    S : tuple
        words
    T : dictionary
        whose keys are the roles in R plus the special role Start and values are dictionaries T[r] such that
        - the keys of T[r] are the roles in R plus the special role End
        - the values of T[r] are the transition probabilities between r and the corresponding role defined by the key
    E : dictionary
        whose keys are the strings in S and value are dictionaries E[s] such that
        - the keys of E[s] are the roles in R
        - the values in E[s] are the emission probabilities between s and the corresponding role defined by the key
        
    Returns
    -------
    tags : dictionary 
        whose keys are the words in S and the values are the roles assigned to these words, 
        so that the selected assignment is the one of maximum likelihood.
    """
    
    result = viterbi(R, S, T, E)
    
    i = 0
    tags = dict()
    for s in S:
        tags[s] = result[i]
        i += 1
        
    return tags

def viterbi(R, S, T, E):
    
    """ 
    This function is the implementation of the Viterbi algorithm for the POS tagging problem. It is a dynamic
    programming algorithm for finding the most likely sequence of hidden states - called the Viterbi path - 
    that results in a sequence of observed events.
    
    Parameters
    ----------
    R : tuple 
        roles
    S : tuple
        words
    T : dictionary
        whose keys are the roles in R plus the special role Start and values are dictionaries T[r] such that
        - the keys of T[r] are the roles in R plus the special role End
        - the values of T[r] are the transition probabilities between r and the corresponding role defined by the key
    E : dictionary
        whose keys are the strings in S and value are dictionaries E[s] such that
        - the keys of E[s] are the roles in R
        - the values in E[s] are the emission probabilities between s and the corresponding role defined by the key
    
    Returns
    -------
    bestPath : list
        the most likely sequence of roles

    Time Complexity
    ---------------
    Assuming that K is the number of states and T is the number of observations, the time complexity of this algorithm is O(K^2 * T).
    First of all, the algorithm builds two tables of size K*T: one to hold the probability of each state given each observation, 
    and one to hold the backpointer to the best prior state. It is necessary to determine each hidden state's probability at time 0,
    so the time complexity is O(K). Then, for each observation, the algorithm needs to determine the probability of each state given
    the previous observation, so the time complexity is O(K^2). Finally, the algorithm needs to determine the most likely path, so the
    time complexity is O(T). Therefore, the total time complexity is O(K^2 * T).
    """
    
    # We consider two tables: one to hold the probability of each state given each observation, 
    # and one to hold the backpointer to the best prior state.
    probs = dict() 
    backs = dict() 
    
    # Determine each hidden state's probability at time 0
    for i in range(len(R)):
        probs[R[i]] = {0: T["Start"][R[i]] * E[S[0]][R[i]]}
        backs[R[i]] = {0: 0}
        
    # Tracking each state's most likely prior state and probability
    for j in range(1,len(S)):
        for i in range(len(R)):
            maxProb = probs[R[0]][j-1] * T[R[0]][R[i]] * E[S[j]][R[i]]
            maxState = R[0]
            for k in range(1,len(R)):
                prob = probs[R[k]][j-1] * T[R[k]][R[i]] * E[S[j]][R[i]]
                if prob > maxProb:
                    maxProb = prob
                    maxState = R[k]
            probs[R[i]][j] = maxProb
            backs[R[i]][j] = maxState
    
    # Find the most likely final state
    maxProb = probs[R[0]][len(S)-1] * T[R[0]]["End"]
    maxState = R[0]
    for k in range(1,len(R)):
        prob = probs[R[k]][len(S)-1] * T[R[k]]["End"]
        if prob > maxProb:
            maxProb = prob
            maxState = R[k]
    probs["End"] = {len(S)-1: maxProb}
    backs["End"] = {len(S)-1: maxState}
    
    bestPath = []
            
    # Backtrack from last observation
    for j in range(len(S)-1,-1,-1): 
        bestPath.insert(0, maxState) # insert best state at beginning of list
        maxState = backs[maxState][j] # set maxState to best prior state
        
    return bestPath
        
        
        

            

    
    
    
    

    