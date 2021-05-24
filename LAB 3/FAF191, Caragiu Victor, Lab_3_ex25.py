def search_epsilon_states(cfg):
	epsilon_states = list()
	for (key, value) in cfg.items():
		for result in value:
			if result == '-':
				epsilon_states.append(key)
	
	return epsilon_states
	
	
def generate_productions(epsilon_states):
	productions = dict()
	occurences = int()
	for (key, value) in cfg.items():
		productions[key] = dict()
		for result in value:
			occurences = 0
			for character in result:
				if character in epsilon_states:
					occurences += 1
			if occurences > 0:
				productions[key][result] = occurences
		if len(productions[key]) == 0:
			del productions[key]
			
	new_productions = dict()
	for e_state in epsilon_states:
		for (key, value) in productions.items():
			new_productions[key] = eliminate_epsilon(value, e_state)			
	
	return new_productions
	
	
def eliminate_epsilon(value,  e_state):
	resulted_productions = list()
	for (result, occurences) in value.items():
		for i in range(occurences):
			word = result
			for y in range(occurences-i):
				word = remove_char(word, e_state, i) 
				resulted_productions.append(word)
	
	return resulted_productions


def remove_char(word, character, start):
	resulted_word = ""
	count = 0
	remove = True
	for letter in word:
		if letter == character:
			if remove and count >= start:
				remove = False
				continue
			count += 1
		resulted_word += letter
	
	return resulted_word

	
def join_productions(cfg, new_productions):
	result = dict()
	for (key, value) in cfg.items():
		if key in new_productions:
			result[key] = cfg[key] + new_productions[key]
		else:
			if '-' in cfg[key]:
				list_without_e = cfg[key]
				list_without_e.remove('-')
				result[key] = list_without_e
			else:
				result[key] = cfg[key]
			
	return result
	

def check_one_nt_symbol(c):
	if len(c) == 1 and c >= 'A' and c <= 'Z':
		return True
	else:
		return False


def search_symbols(joined_productions):
	symbols_to_replace = list()
	for (key, value) in joined_productions.items():
		for result in value:
			if check_one_nt_symbol(result):
				symbols_to_replace.append(result)

	return symbols_to_replace

	
def elliminate_renaming(joined_productions, symbols_to_replace):
	elliminated_renaming = dict()
	for symbol_to_replace in symbols_to_replace:
		for (key, value) in elliminated_renaming.items():
			if symbol_to_replace in value:
				value.remove(symbol_to_replace)
				elliminated_renaming[key] = elliminated_renaming[key] + joined_productions[symbol_to_replace]
		
		for (key, value) in joined_productions.items():
			if symbol_to_replace in value:
				value.remove(symbol_to_replace)
				elliminated_renaming[key] = joined_productions[key] + joined_productions[symbol_to_replace]
		
	for (key, value) in joined_productions.items():
		if not key in elliminated_renaming:
			elliminated_renaming[key] = joined_productions[key]
	
	return elliminated_renaming
		

def search_productive_symbols(elliminated_renaming, terminals):
	productive_symbols = list()
	for (key, value) in elliminated_renaming.items():
		for result in value:
			if result in terminals:
				productive_symbols.append(key)
				
	productive_symbols = search_productive_rules(elliminated_renaming, productive_symbols, terminals)

	return productive_symbols
	

def search_productive_rules(elliminated_renaming, productive_symbols, terminals):
	search_again = False
	for (key, value) in elliminated_renaming.items():
		productive = False
		if not key in productive_symbols:
			for result in value:
				productive_result = True
				for symbol in result:
					if not symbol in productive_symbols and not symbol in terminals:
						productive_result = False
				if productive_result:
					productive = True
		if productive:
			productive_symbols.append(key)
			search_again = True
			
	if search_again:
		productive_symbols = search_productive_rules(elliminated_renaming, productive_symbols, terminals)	
	
	return productive_symbols
	
	
def elliminate_unproductive_symbols(elliminated_renaming, productive_symbols):
	productive_productions = dict()
	for (key, value) in elliminated_renaming.items():
		if key in productive_symbols:
			productive_productions[key] = elliminated_renaming[key]
	
	return productive_productions
	
	
def eliminate_inaccessible(elliminated_unproductive_symbols, start_symbol, nonterminals):
	nonterminals.remove(start_symbol)
	for (key, value) in elliminated_unproductive_symbols.items():
		for result in value:
			for symbol in result:
				if symbol in nonterminals:
					nonterminals.remove(symbol)
	
	for key in nonterminals:
		del elliminated_unproductive_symbols[key]
	
	return elliminated_unproductive_symbols
	
	
def check_two_nt_symbols(symbols):
	uppers = 0
	for symbol in symbols:
		if symbol >= 'A' and symbol <= 'Z':
			uppers += 1
		elif symbol >= 'a' and symbol <= 'z':
			return False
	
	if uppers == 2:
		return True
	else:
		return False
	
	
def check_t_and_nt_and_build(symbols, terminals, new_from_terminals):
	if len(symbols) == 2:
		if (check_one_nt_symbol(symbols[0]) and symbols[1] in terminals):
			nonterminal = list(new_from_terminals.keys())[list(new_from_terminals.values()).index(list(symbols[1]))]
			return (True, symbols[0] + nonterminal)
		if (check_one_nt_symbol(symbols[1]) and symbols[0] in terminals):
			nonterminal = list(new_from_terminals.keys())[list(new_from_terminals.values()).index(list(symbols[0]))]
			return (True, nonterminal + symbols[1])
	
	return (False, "")
	

def join_dicts(d1, d2):
	for key, value in d2.items():
		if key in list(d1.keys()):
			d1[key] = d1[key] + value
		else:
			d1[key] = value
	
	return d1
	
	
def filter_productions(productions_left, already_following, terminals):
	for (key, value) in productions_left.items():
		productions = list()
		current_productions = value.copy()
		for result in value:
			if result in terminals or check_two_nt_symbols(result):
				productions.append(result)
				current_productions.remove(result)	
		productions_left[key] = current_productions
		if len(productions) > 0:
			if key in already_following:
				already_following[key] = already_following[key] + productions
			else:
				already_following[key] = productions
	return (productions_left, already_following)
	
			
def check_more_than_two_nt(result):
	uppers = 0
	for symbol in result:
		if symbol >= 'A' and symbol <= 'Z':
			uppers += 1
	
	if uppers > 2:
		return True
	else:
		return False
		
def group_nontermials(productions_left, made_productions_keys, made_productions_values, key_idx):
	productive_itteration = False
	for (key, value) in productions_left.items():
		for (idx_result, result) in enumerate(value):	
			if check_more_than_two_nt(result):		
				uppers = 0
				new_result = ""
				two_nt = ""
				for (idx, symbol) in enumerate(result):
					new_result += symbol
					is_letter = symbol >= 'A' and symbol <= 'Z'
					is_number = symbol >= '0' and symbol <= '9'
					if is_letter:
						uppers += 1

					if is_letter or is_number:
						two_nt += symbol
					
					
					next_is_letter_or_end = True if idx+1 == len(result) else False
					if not next_is_letter_or_end:
						next_is_letter_or_end = result[idx+1] >= 'A' and result[idx+1] <= 'Z'
					if uppers == 2 and next_is_letter_or_end:
						
						if not result[idx+1-len(two_nt):idx+1] in made_productions_values:
							key_idx += 1
							productive_itteration = True
							made_productions_keys.append('Z'+str(key_idx))
							made_productions_values.append(result[idx+1-len(two_nt):idx+1])
							
							new_result = new_result[:-len(two_nt)] + 'Z' + str(key_idx)
						else: 
							new_result = new_result[:-len(two_nt)] + made_productions_keys[made_productions_values.index(two_nt)]
						
						uppers = 0
						two_nt = ""
						
				value[idx_result] = new_result
				
	if productive_itteration:
		(productions_left, made_productions_keys, made_productions_values) = group_nontermials(productions_left, made_productions_keys, made_productions_values, len(made_productions_keys))
	
	return (productions_left, made_productions_keys, made_productions_values)
	
	
def follow_cnf_rules(productions_left, nonterminals, terminals):
	already_following = dict()
	(productions_left, already_following) = filter_productions(productions_left, already_following, terminals)
	
	
	new_from_terminals = dict()
	for (idx, terminal) in enumerate(terminals):
		new_from_terminals['X' + str(idx)] = list(terminal)

	terminals_and_nonterminals = dict()
	for (key, value) in productions_left.items():
		productions = list()
		current_productions = list(value)
		for result in value:
			(t_and_nt_symbols, new_result) = check_t_and_nt_and_build(result, terminals, new_from_terminals)
			if t_and_nt_symbols:
				productions.append(new_result)
				current_productions.remove(result)
		productions_left[key] = current_productions
		if len(productions) > 0:
			terminals_and_nonterminals[key] = productions
	
	new_productions = join_dicts(join_dicts(already_following, new_from_terminals), terminals_and_nonterminals)

	# searching two innitial nonterminals side by side
	new_keys = list()
	new_values = list()
	key_idx_1 = -1
	for (key, value) in productions_left.items():
		for (idx_result, result) in enumerate(value):
			symbol_type = 0
			for (idx, symbol) in enumerate(result):
				if check_one_nt_symbol(symbol):
					if symbol_type == 1:
						if not result[idx-1:idx+1] in new_values:
							key_idx_1 += 1
							new_keys.append('Y'+str(key_idx_1))
							new_values.append(result[idx-1:idx+1])
							
						value[idx_result] = result[:idx-1] + 'Y' + str(key_idx_1) + result[idx+1:]
					symbol_type = 1
				
				else:
					symbol_type = 2
				
	for (idx, key) in enumerate(new_keys):
		new_productions[key] = [new_values[idx]]
	
	
	(productions_left, new_productions) = filter_productions(productions_left, new_productions, terminals)
	
	# converting terminals to nonterminals
	for (key, value) in productions_left.items():
		for (idx_result, result) in enumerate(value):
			new_result = str()
			for (idx, symbol) in enumerate(result):
				if symbol in terminals:
					nonterminal = list(new_from_terminals.keys())[list(new_from_terminals.values()).index(list(symbol))]
					new_result = new_result + nonterminal
				else:
					new_result = new_result + symbol
			value[idx_result] = new_result

	(productions_left, new_productions) = filter_productions(productions_left, new_productions, terminals)

	(productions_left, made_productions_keys, made_productions_values) = group_nontermials(productions_left, list(), list(), 0)
	
	(productions_left, new_productions) = filter_productions(productions_left, new_productions, terminals)
	
	for (idx, key) in enumerate(made_productions_keys):
		new_productions[key] = [made_productions_values[idx]]
		
	print("CNF:")
	print_productions(new_productions)
	
def print_productions(joined_productions):
	count = 1
	for (key, value) in joined_productions.items():
		for result in value:
			print(str(count) + '.', key + '->' + result)
			count += 1

if __name__ == "__main__":
	cfg = {'S': ['bA', 'BC'], 'A': ['a', 'aS', 'bCaCa'], 'B': ['A', 'bS', 'bCAa'], 'C': ['-', 'AB'], 'D': ['AB']}
	start_symbol = 'S'
	nonterminals = ['S', 'A', 'B', 'C', 'D']
	terminals = ['a', 'b']
	
	print("Initial productions:")
	print_productions(cfg)

	# remove epsilon productions

	epsilon_states = search_epsilon_states(cfg)
	
	new_productions = generate_productions(epsilon_states)
	
	joined_productions = join_productions(cfg, new_productions)

	print("Epsilon-free productions:")
	print_productions(joined_productions)

	# elimination of renaming
	
	symbols_to_replace = search_symbols(joined_productions)
	
	elliminated_renaming = elliminate_renaming(joined_productions, symbols_to_replace)
	
	print("Renaming-free productions:")
	print_productions(elliminated_renaming)
	
	# elimination of unproductive symbols
	
	productive_symbols = search_productive_symbols(elliminated_renaming, terminals)
	
	elliminated_unproductive_symbols = elliminate_unproductive_symbols(elliminated_renaming, productive_symbols)
	print("Elliminated unproductive symbols:")
	print_productions(elliminated_unproductive_symbols)
	
	# elimination of inaccessible symbols
	
	accessible_productions = eliminate_inaccessible(elliminated_unproductive_symbols, start_symbol, nonterminals.copy())

	print("Elliminated inaccessible productions:")
	print_productions(accessible_productions)
	
	# transform to follow the CNF ruses
	cnf = follow_cnf_rules(accessible_productions, nonterminals, terminals)
	
	
