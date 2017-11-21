#from DFA_Optimizer import *
from nfa2dfa import *
from visualize import *
from regex2nfa import *
from simulate import *
import pdb
#pdb.set_trace()
f = raw_input("Grammer file Name: ")
grammer = open(f).read()
nfa_start, nfa_end, nfa = regex2nfa(grammer)
dfa_start, dfa_end, dfa = nfa2dfa(nfa, nfa_start, nfa_end)
#dfa_start_min, dfa_end_min, dfa_min = minimizeDFA(dfa, dfa_end, dfa_start)
f = raw_input("Code file name:")
code = open(f).read()
token_list = simulate(dfa, dfa_start, dfa_end, code)
for token, lexeme in token_list:
    if len(token) >= 8:
        print (token+"\t"+lexeme)
    else:
        print(token+"\t\t"+lexeme)
