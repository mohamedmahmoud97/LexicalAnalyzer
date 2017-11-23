"""
# DFA and nfa will be represented by automata
# automata = {node_id: [nodes_transitions]}
# nodes_transitions = (node, transition)
# example:
"""
testnfa = {
    0: [
        (1, None),
        (7, None),
        ],
    1: [
        (2, None),
        (4, None)
        ],
    2: [
        (3, 'a')
        ],
    3: [
        (6, None)
        ],
    4: [
        (5, 'b')
        ],
    5: [
        (6, None)
        ],
    6: [
        (7, None),
        (1, None)
        ],
    7: [
        (8, 'a')
        ],
    8: [
        (9, 'b')
        ],
    9: [
        (10, 'b')
        ],
    10: [
        ]
    }

def move(nfa, T, a):
    ret = set()
    for s in T:
        if s not in nfa.keys():
            continue
        for dest, transition in nfa[s]:
            if transition is a:
                ret.add(dest)
    if len(ret) == 0:
        return set([None])
    return ret

def eclosure(nfa, states):
    x = states
    while True:
        s = move(nfa, x, None)
        s.update(x)
        if x == s:
            return s
        else:
            x = s

def get_all_syms(nfa):
    syms = set()
    for i in nfa.values():
        for _,j in i:
            syms.add(j)
    if None in syms:
        syms.remove(None)
    return syms

def most_important(items, real):
    minimum = len(real)
    item = None
    for i in items:
        if real.index(i) < minimum:
            minimum = real.index(i)
            item = i
    return item
def ordered_insert(accept_list, state, old_accept_list):
    if len(accept_list) == 0:
        accept_list.append(state)
        return
    old_state = ''.join([i for i in state if not i.isdigit()])
    i = 0
    done = False
    while i < len(accept_list) and not done:
        current_state = ''.join([j for j in accept_list[i] if not j.isdigit()])
        if old_accept_list.index(current_state) > old_accept_list.index(old_state):
            accept_list.insert(i, state)
            done = True
        i += 1
    if not done:
        accept_list.append(state)

def nfa2dfa(nfa, start_state, accept_list):
    #import pdb
    #pdb.set_trace()
    symbol_set = get_all_syms(nfa)
    state_list = {}
    counter = 1
    ss = eclosure(nfa, set([start_state]))
    state_list[0] = ss
    visit_list = []
    visit_list.append(0)
    dfa = {}
    while len(visit_list) != 0:
       ntv = visit_list.pop()
       for sym in symbol_set:
            u = eclosure(nfa, move(nfa, state_list[ntv], sym))
            dest_id = -1
            if u == set([None]):
                continue;
            if u not in state_list.values():
                accept_subset = []
                for x in u:
                    if x in accept_list:
                        accept_subset.append(x)
                if len(accept_subset) == 0:
                    state_list[counter] = u
                    visit_list.append(counter)
                    dest_id = counter
                    counter += 1
                else:
                    name = most_important(accept_subset, accept_list) + str(counter)
                    state_list[name] = u
                    visit_list.append(name)
                    dest_id = name
                    counter += 1 
                
            else:
                dest_id = [k for k in state_list.keys() if state_list[k] == u][0]
            if ntv not in dfa.keys():
                dfa[ntv] = []
            dfa[ntv].append((dest_id, sym))

    acs = []
    #import pdb
    #pdb.set_trace()
    for k in state_list.keys():
        if len(state_list[k].intersection(set(accept_list))) != 0:
            ordered_insert(acs, k, accept_list)
    return [k for k in state_list.keys() if state_list[k] == ss][0], acs, dfa
