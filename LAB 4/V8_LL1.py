import numpy as np


stack = ['$']
word = str()

class Tree(object):
    def __init__(self):
        self.children = list()
        self.data = None
        self.level = None
        self.ls = None

max_level = 0
matrix = 0

def print_productions(joined_productions):
    count = 1
    for (key, value) in joined_productions.items():
        for result in value:
            print(str(count) + '.', key + '->' + result)
            count += 1

class DisplayTree():
    def __init__(self): 
        self.matrix = np.array([[' '] * (3*max_level)] * (8*max_level))
        self.i = 0

    def build_representation(self, node, left, right):
        for (idx, c) in enumerate(node.children):
            if(idx < len(node.children)/2):
                self.build_representation(c, 1, 0)
        
        self.matrix[self.i*2,node.level*2] = node.data
        self.matrix[self.i*2,node.level*2-1] = '/'*left + '\\'*right
        self.i += 1

        for (idx, c) in enumerate(node.children):
            if(idx >= len(node.children)/2):
                self.build_representation(c, 0, 1)

    def print_tree(self, tree):
        self.build_representation(tree, 0, 0)
        for x in range(self.matrix.shape[1]):
            for y in range(self.matrix.shape[0]):
                print(self.matrix[y,x], end='')
            print()

def get_first(prod):
    first = dict()
    for (key, value) in prod.items():
        first[key] = dict()
        for result in value:
            to_add = list()
            if(result[0] == result[0].lower() or result[0] == '-'):
                to_add.append((result[0], result))
            else:
                to_add = get_first_from_string(result[0], prod)

            if(len(to_add) != 0): 
                for (letter, r) in to_add:
                    first[key][letter] = result
            elif(to_add[0][0] == '_'):
                raise Exception('FAILED to compute FIRST('+key+'). Grammar is left-recursive.')

    return first

def get_first_from_string(c, prod):
    value = prod[c]
    found = list()
    for result in value:
        if(result[0] == result[0].lower() or result[0] == '-'):
            found.append((result[0], result))
        else:
            if(c == result[0]):
                found.append(('_', ''))
                
            new_found = get_first_from_string(result[0], prod)
            for (letter, r) in new_found:
                found.append((letter, r))

    return found

def search_follow(prod, word, i):
    follow = dict()
    for (idx, symbol) in enumerate(word):
        if(symbol == symbol.upper()):
            for result in prod[symbol]:
                if(result != '-'):
                    last_nt = word[-1:]
                    if(last_nt == last_nt.upper() and i!= 0):
                        if(not last_nt in follow.keys()):
                            follow[last_nt] = list()

                        follow[last_nt].append('$')

                    new_word = word[:idx] + result + word[idx+1:]
                    new_prod = dict()
                    for (k, v) in prod.items():
                        new_prod[k] = list()
                        for y in v:
                            if(y != result):
                                new_prod[k].append(y)

                    returned = search_follow(new_prod, new_word, i+1)
                    for (k, v) in returned.items():
                        for y in v:
                            if(not k in follow.keys()):
                                follow[k] = list()

                            if(not y in follow[k]):
                                follow[k].append(y)

    for (idx, symbol) in enumerate(word):
        if(idx+1 < len(word)):
            if(symbol == symbol.upper() and word[idx+1] == word[idx+1].lower()):
                if(not symbol in follow.keys()):
                    follow[symbol] = list()

                if(not word[idx+1] in follow[symbol]):
                    follow[symbol].append(word[idx+1])
    
    return follow
    
def get_follow(prod, start):
    follow = search_follow(prod, start, 0)

    for k in prod.keys():
        if(not k in follow.keys()):
            follow[k] = ['$']
    
    return follow

def print_F(data):
    for x in data:
        print(x, '- ', end='')
        for y in data[x]:
            print(y, end=',')
        print()

def print_pt(table, terminals):
    print(end='    ') 
    for t in terminals:
        print(t, '   ', end='')
    print()
    for x in table.keys():
        print(x, end='   ')
        for y in terminals:
            if y in table[x].keys():
                print(table[x][y], ' '*(5-len(table[x][y])), sep='', end='')
            else:
                print('     ', end='')
        print()

def build_parsing_table(first, follow):
    parsing_table = dict()
    for (key1, terminals) in first.items():
        parsing_table[key1] = dict()
        for (key2, production) in terminals.items():
            if(key2 == '-'):
                for symbol in follow[key1]:
                    parsing_table[key1][symbol] = '_'
            
            parsing_table[key1][key2] = production

    return parsing_table

def parse(parsing_table, follow, i):
    global word
    global stack
    global max_level

    node = Tree()
    if(i>max_level):
        max_level = i

    stack_first = stack[-1:][0][0]
    
    if(stack_first == stack_first.lower()):
        node.data = word[0]
        node.level = i
        node.ls = stack_first
        del stack[-1:]
        word = word[1:]
        
        return (node, True)

    else:
        rules = parsing_table[stack_first]
        if(word[0] in rules.keys()):
            node.data = stack[-1:][0][0]
            node.level = i
            node.ls = stack[-1:][0][1]
            deleted = stack[-1:]
            del stack[-1:]

            if rules[word[0]] == '_':
                empty_node = Tree()
                empty_node.data = '-'
                empty_node.level = i+1
                empty_node.ls = stack[-1:][0][1]

                node.children.append(empty_node)
                return (node, True)

            for (idx, c) in enumerate(reversed(rules[word[0]])):
                stack.append((c, len(rules[word[0]])-idx+1))
            
            # building the tree
            for c in rules[word[0]]:                
                (new_children, state) = parse(parsing_table, follow, i+1)
                if(state):
                    node.children.append(new_children)
                else:
                    return (node, False)
        else:
            return (node, False)

    return (node, True)

def analyze(prod, start, nonterminals, terminals, string_to_parse):
    global word
    word = str(string_to_parse)
    
    stack.append((start,0))
    
    print('Initial productions:')
    print_productions(prod)

    print('\nFISRT:')
    first = get_first(prod)
    print_F(first)

    print('\nFOLLOW:')
    follow = get_follow(prod, start)
    print_F(follow)
        
    print('\nParsing table:')
    parsing_table = build_parsing_table(first, follow)
    print_pt(parsing_table, terminals)

    (tree, status) = parse(parsing_table, follow, 1)    
    
    print('\nString:', string_to_parse)
    if(status):    
        x = DisplayTree()
        x.print_tree(tree)
    else:
        print("Parsing failed!")

if __name__ == "__main__":
    start = 'S'

    print('analisys of provided example')
    prod = {'S':['E'], 'E':['FcA'], 'A':['b', 'dD'], 'D': ['Fe'], 'F':['aX'], 'X':['-', 'baX']}
    nonterminals = ['S', 'A', 'F', 'E', 'D', 'X']
    terminals = ['a', 'b', 'c', 'd', 'e']
    string_to_parse = 'ababacdabae'

    analyze(prod, start, nonterminals, terminals, string_to_parse)

    print('individual task analisys')
    prod = {'S':['LdX'], 'X':['D'], 'L':['ca', 'aL'], 'D': ['eDb','b']}
    nonterminals = ['S', 'X', 'L', 'D']
    terminals = ['a', 'b', 'c', 'd', 'e']
    string_to_parse = 'aaaacadeebbb'

    analyze(prod, start, nonterminals, terminals, string_to_parse)

    

    
    
    
    
