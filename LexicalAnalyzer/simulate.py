def simulate(dfa, start, accept_list, string):
    import pdb
    #pdb.set_trace()
    internal_state = start
    string_start = 0
    string_end = 0
    last_accepting_state = None
    token_list = []
    i = 0
    stuck = None
    string = string+" "*10
    while i < len(string):
        if internal_state not in dfa.keys() or stuck == True:
            token_list.append((''.join([i for i in last_accepting_state if not i.isdigit()]), string[string_start:string_end+1]))
            i = string_end + 1
            while string[i].isspace():
                if i == len(string) -1:
                    return token_list
                i += 1
            string_start = i
            internal_state = start
        stuck = True
        for next_state, c in dfa[internal_state]:
            if c == string[i]:
                stuck = False
                internal_state = next_state
                if internal_state in accept_list:
                    last_accepting_state = internal_state
                    string_end = i
                break;
        i += 1 
    return token_list

