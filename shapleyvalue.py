import itertools
from pprint import pprint as pprint
from timeit import default_timer as timer

def shapleyvalue(playerset,v,minimalWinningCoalitionSize=1):
    ''' input,  set, the player set
                function, TU game which assigns to every coalition a worth i.e. a set function f:2^n -> R
        output, dict, stores the Shapley values
    ''' 
    n = len(playerset)
    SV = {}    # dict storing the Shapley values
    potCur = {}    # stores potential values of coalition with size k

    for coalition in itertools.combinations(playerset, minimalWinningCoalitionSize):
        potCur[frozenset(coalition)]=v(frozenset(coalition))/(minimalWinningCoalitionSize) # pot(S \cup i) = v(S \cup i)/ (s+1)   + 0 if pot(S \setminus i) = 0 for all i \in S 


    for coalition_Size in range(minimalWinningCoalitionSize,n-1):
        potNext = {}    # stores next potential values of coalition with size coalition_Size+1
        for coalition in itertools.combinations(playerset, coalition_Size+1):
            potNext[frozenset(coalition)]=v(frozenset(coalition))/(coalition_Size+1) # pot(S \cup i) = v(S \cup i)/ (s+1)   +...
        for coalition in potCur:
            for player in playerset.difference(coalition):
                potNext[ frozenset(coalition.union(frozenset( [player]))) ] += potCur[coalition]/(coalition_Size+1)  # pot(S \cup i) = ...+ pot(S)\ (s+1)
        potCur = potNext

    potN=v(playerset)/n # calculate pot(N) separate without losing potCur
    for coalition in potCur:
        potN += potCur[coalition]/n # pot(N) separate without deleting potCur
    for player in playerset:
        playerset_without_player = frozenset(playerset.difference(frozenset([player])))
        SV[player] = potN - potCur[playerset_without_player]
        
    return SV
    
######## We now define three example TU games  ###################################################################  
#1st: call with playerset {1,2,3}
def v(coalition):
    ''' input, a set containing players
        output, a float that represents the worth of 
            this coalition
    '''
    if coalition=={0}: return 0
    elif coalition=={1}: return 12
    elif coalition=={2}: return 6
    elif coalition=={3}: return 9
    elif coalition=={1,2}: return 24
    elif coalition=={1,3}: return 27
    elif coalition=={2,3}: return 15
    elif coalition=={1,2,3}: return 36

#2nd: call with playerset including {'US', 'CH', 'RUS', 'FR','UK'} , 
# e.g. frozenset(['US', 'CH', 'RUS', 'FR','UK']).union(frozenset(range(1,11)))   
def UN_security_council(coalition):
    ''' input, a set containing players out of the player set {1,...,15}
            where the players 1,...,5 are the permanent members
        output, 1 if nine members are in this coalition including 
            the veto power 1,...,5; otherwise 0
    '''
    if len(coalition)<9: return 0
    elif not coalition.issuperset({ 'CH', 'FR','RUS','UK', 'US'}): return 0
    else: return 1    



start = timer()
### lets try the example function (very quick)
result = shapleyvalue({1,2,3},v)

###### uncomment this for calculation of Shapley Shubik of the UN Security Council (takes a second)
result = shapleyvalue(frozenset(['US', 'CH', 'RUS', 'FR','UK']).union(frozenset(range(1,11))), UN_security_council, minimalWinningCoalitionSize=9) 
######


end = timer()
ctime = end - start
print('Time needed to compute: {:04.2f} minutes '.format(ctime/60))
print('Shapley values: ')
pprint(result, width=1)
##### uncomment the following to get results printed into a file output.txt
# with open('output.txt', 'a') as f:   
#     f.write('Time needed to compute: {}h {}min {:04.2f}sec  \n {} \n'.format(ctime//3600, (ctime%3600)//60 , (ctime%3600)%60 , result))
# #####