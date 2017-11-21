regex = """
keywords: {if else while}
datatype: {bool int float}
letter = [a-zA-Z]
digit = [0-9]
digits = digit+
id: letter(letter|digit)*
num: digit+ |(digit+ \. digits (\L | (E digits)))
relop: (\=\=) | (\!\=) | (\>) | (\>\=) | (\<) | (\<\=)
assign: \=
punct: [\;\,\(\)\{\}]
addop:\+ | \-
mulop: \* | \/
"""
import string
i = 1
inside_square_bracket=False
def priority(c):
    return " ([.|+?*-".find(c)
def new_state():
    global i
    x = i
    i += 1
    return x
def linetype(line):
    for c in line:
        if c.isalnum() or c.isspace():
            continue
        elif c == "=":
            return "REP"
        elif c == ":":
            return "END"
        else:
            return "ERR"
def curly_to_paren(string):
    return "((" + ")|(".join(filter(None, string[1:-1].split(" "))) + "))"
def handle_curly_brackets(string):
    #import pdb
    #pdb.set_trace()
    while '{' in string and '\\{' not in string:
        l = len(string)
        i = 0
        while i < l:
            if string[i] != '{' or (i>0 and string[i - 1] == '\\'):
                i += 1
                continue
            j = i
            while j < l:
                if string[j] != '}' or (j>0 and string[j-1] =='\\'):
                    j += 1
                    continue
                string = string.replace(string[i: j+1], curly_to_paren(string[i:j+1]))
                j = l
                i = l
    return string

def get_patterns(regex):
    lines = filter(None, [line for line in regex.split("\n")])
    rep_list = {}
    patterns = {}
    ordered_end_states = []
    for line in lines:
        t = linetype(line)
        if t == "ERR":
            print("Error in get_pattenrs")
            return
        if t == "END":
            ordered_end_states.append(line[:line.find(":")].strip())
            patterns[line[:line.find(":")].strip()] = handle_curly_brackets(line[line.find(":") + 1:].strip())
        else:
            rep_list[line[:line.find("=")].strip()] = handle_curly_brackets(line[line.find("=") + 1:].strip())
    l = list(rep_list.keys())
    l.sort(key=len, reverse=True)
    for key in l:
        for key2 in patterns.keys():
            patterns[key2] = patterns[key2].replace(key, "(" + rep_list[key] + ")")
    return ordered_end_states, patterns

def process_single(character):
    start = new_state()
    accept= new_state()
    nfa = {start:[(accept, character)]}
    return (start, accept, nfa)

def append_if_exist(nfa, key, value):
    if key in nfa.keys():
        nfa[key].append(value)
    else:
        nfa[key] = [value]

def process_append(nfas):
    s_start, s_end, s_nfa = nfas.pop(-1)
    f_start, f_end, f_nfa = nfas.pop(-1)
    start = f_start
    end = s_end
    nfa = f_nfa.copy()
    nfa.update(s_nfa)
    append_if_exist(nfa, f_end, (s_start, None))
    nfas.append((start, end, nfa))

def process_or(nfas):
    f_start, f_end, f_nfa = nfas.pop(-1)
    s_start, s_end, s_nfa = nfas.pop(-1)
    start = new_state()
    end = new_state()
    nfa = f_nfa.copy()
    nfa.update(s_nfa)
    nfa[start] = [
            (s_start, None),
            (f_start, None)
            ]
    append_if_exist(nfa, f_end, (end, None))
    append_if_exist(nfa, s_end, (end, None))
    nfas.append((start, end, nfa))

def process_range(nfas):
    endv = nfas.pop(-1)
    endv = ord(endv[2][endv[0]][0][1])
    startv = nfas.pop(-1)
    startv = ord(startv[2][startv[0]][0][1])
    start = new_state()
    nfa = {start: []}
    if inside_square_bracket:
        end = new_state()
        for i in range(startv, endv + 1):
            nfa[start].append((end, chr(i)))
        nfas.append((start,end, nfa))
    else:
        end = start
        for i in range(startv, endv + 1):
            append_if_exist(nfa, end, (new_state(), chr(i)))
            end = nfa[end][0][0]
        nfas.append((start,end, nfa))

def process_optional(nfas):
    start, end, nfa = nfas.pop(-1)
    append_if_exist(nfa, start, (end, None))
    nfas.append((start, end, nfa))

def process_one_or_more(nfas):
    start, end, nfa = nfas.pop(-1)
    append_if_exist(nfa, end, (start, None))
    nfas.append((start, end, nfa))

def process_zero_or_more(nfas):
    start, end, nfa = nfas.pop(-1)
    append_if_exist(nfa, end, (start, None))
    append_if_exist(nfa,start, (end, None))
    nfas.append((start, end, nfa))

def push(nfas, operands, op):
    global inside_square_bracket
    plist = {
            '.': process_append,
            '|': process_or,
            '-': process_range,
            '?': process_optional,
            '*': process_zero_or_more,
            '+': process_one_or_more
            }
    if op == ')':
        while operands[-1] != '(':
            operand = operands.pop(-1)
            plist[operand](nfas)
        operands.pop(-1)
        return
    elif op == '(':
        operands.append(op)
        return
    elif op == '[':
        operands.append(op)
        inside_square_bracket=True
        return
    elif op == ']':
        while operands[-1] != '[':
            operand = operands.pop(-1)
            plist[operand](nfas)
        operands.pop(-1)
        inside_square_bracket=False
        return
    while len(operands) > 0 and priority(op) <= priority(operands[-1]):
        operand = operands.pop(-1)
        plist[operand](nfas)
    operands.append(op)
    
def process(regex):
    nfas = []  #stack
    operands = [] #another stack
    i = 0
    l = len(regex)
    append = False
    #import pdb
    #pdb.set_trace()
    while i < l:
        if regex[i] in string.ascii_lowercase+string.ascii_uppercase+string.digits+'\\':
            if append:
                if inside_square_bracket:
                    push(nfas, operands, '|')
                else:
                    push(nfas, operands, '.')
            append = True
            if regex[i] == '\\':
                if regex[i+1] == 'L':
                    nfas.append(process_single(None))
                else:
                    nfas.append(process_single(regex[i+1]))
                i += 2
            else:
                nfas.append(process_single(regex[i]))
                i += 1
        elif regex[i] in "([":
            if append:
                push(nfas, operands, '.')
            push(nfas, operands, regex[i])
            append = False
            i += 1
        elif regex[i] in "+?*)]":
            push(nfas, operands, regex[i])
            append = True
            i += 1
        elif regex[i] in "|-":
            push(nfas, operands, regex[i])
            append = False
            i += 1
        elif regex[i].isspace():
            i += 1
            continue
        else:
            print ("Error in parse at " + regex[i:])
            print ("                  ^")
            return
    push(nfas, operands, " ")
    return nfas[0]

def rename_state(nfa, old_name, new_name):
    for key in nfa.keys():
        for name, transition in nfa[key]:
            if name == old_name:
                nfa[key].remove((name,transition))
                nfa[key].append((new_name, transition))
        if key == old_name:
            nfa[new_name] = nfa[key]
            del nfa[key]
def merge_nfas(nfas):
    final_start = new_state()
    end_list = []
    final_nfa = {}
    for start, end, nfa in nfas.values():
        end_list.append(end);
        final_nfa.update(nfa)
        append_if_exist(final_nfa, final_start, (start, None))
    return final_start, end_list, final_nfa

def regex2nfa(regex):
    global i
    i = 0
    import pdb
    #pdb.set_trace()
    end, patterns = get_patterns(regex)
    nfas = {}
    for token in patterns.keys():
        nfas[token] = process(patterns[token])
        rename_state(nfas[token][2], nfas[token][1], token)
        nfas[token] = (nfas[token][0], token, nfas[token][2])
    a,b,c = merge_nfas(nfas)
    return a,end,c
#regex2nfa(regex)
