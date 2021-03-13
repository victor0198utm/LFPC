nfa = {'0': {'a': ['0', '1']}, '1': {'a': ['2'], 'b': ['1']}, '2': {'a': ['3']}, '3': {'a': ['1']}}   

states = ['0','1','2','3']             
terminal_symbols = ['a','b','c']
nfa_initial_state = '0'
nfa_final_state = '3'         
                       
dfa = dict()                                  

def bulid_state(current_state, symbol):
    new_key_states = dfa[current_state][symbol]
    new_key = dict()

    for key in new_key_states:
        if key in nfa:
            for state_to_add in nfa[key]:
                if state_to_add in new_key:
                    new_str = str(new_key[state_to_add])

                    for symbols in nfa[key][state_to_add]:
                        if not symbols in new_str:
                            new_str+=symbols

                    new_key[state_to_add] = new_str
                else:
                    new_key[state_to_add] = "".join(nfa[key][state_to_add])
            
    dfa[new_key_states] = new_key
    
    for transition in dfa[new_key_states]:
        if (not dfa[new_key_states][transition] in dfa) and (not dfa[new_key_states][transition] in nfa):
            bulid_state(new_key_states, transition)


for current_state in states:
    dfa[current_state] = dict()
    for symbol in terminal_symbols:
        if symbol in nfa[current_state]:
            for s in nfa[current_state][symbol]:
                if current_state in dfa and symbol in dfa[current_state]:
                    dfa[current_state][symbol] = dfa[current_state][symbol] + s
                else:
                    dfa[current_state][symbol] = s
                
                if not dfa[current_state][symbol] in states:
                    bulid_state(current_state, symbol)
                

print("", end="\t")
for ts in terminal_symbols:
    print("|",ts, end="\t")
print("")
for key in dfa:
    
    if nfa_initial_state in key:
        print("->"+key, end="\t")
    elif nfa_final_state in key:
        print("*"+key, end="\t")
    else:
        print(key, end="\t")
    for ts in terminal_symbols:
        if ts in dfa[key]:
            print("|",dfa[key][ts], end="\t")
        else:
            print("|", end="\t")
    print("")


