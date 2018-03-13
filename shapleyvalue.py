import itertools
from pprint import pprint as pprint
from timeit import default_timer as timer

def shapleyvalue(playerset,v):
    ''' input,  set, the player set
                function, TU game which assigns to every coalition a worth i.e. a set function f:2^n -> R
        output, dict, stores the Shapley values
    ''' 
    n = len(playerset)
    SV = {}    # dict storing the Shapley values
    potCur = {}    # stores potential values of coalition with size k

    for player in playerset:
        player_as_singleton_set = frozenset([player])
        potCur[player_as_singleton_set]=v(player_as_singleton_set) # set pot of singletons to worth of singletons

    for coalition_Size in range(1,n-1):
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

EU27POP = [289714776,8772865,11351727,7101859,4154213,854802,10578820,5748769,1315635,5503297,66989083,82521653,10768193,9797561,4784383,60589445,1950116,2847904,590667,460297,17081507,37972964,10309573,19644350,5435343,2065895,46528966,9995153]
def EU27(coalition):
    ''' input, a set containing players out of the player set {1,...,27}
        output, 1 if 
                coalition size > 24 
                or
                coalition size > 15 and sum of player's population surpasses 0.65* 445715040 = 289714776
    '''
    if len(coalition)<16: return 0
    elif len(coalition)>24: return 1
    elif  sum([EU27POP[i] for i in coalition]  ) <289714776: return 0 #here we know that between 16 and 24 countries support and check for population threshold
    else: return 1
##################################################################################################################


start = timer()
### lets try the example function (very quick)
result = shapleyvalue({1,2,3},v)

###### uncomment this for calculation of Shapley Shubik of the UN Security Council (takes a second)
# result = shapleyvalue(frozenset(['US', 'CH', 'RUS', 'FR','UK']).union(frozenset(range(1,11))), UN_security_council ) 
######

###### uncomment this for calculation of Shapley Shubik of the EU Council without England  (takes about an hour)
# result = shapleyvalue( frozenset(range(27)), EU27)  
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