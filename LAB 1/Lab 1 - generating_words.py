# This programs generates all possible words with length less than 20 characters
# and compare them with the searched words

# grammar declaration
d = dict()
d["S"] = "aD"
d["D"] = "dE,bJ,aE"
d["J"] = "cS"
d["E"] = "e,aE"

# words to search for
search = ["adaaae", "abcade", "abcadae", "abcabcadaae", "aaaaae"]

def generate(letter, interm_str):
    # make an array with possible replacements for nonterminal characters
    try:
        options = d[letter].split(",")
    except:
        options = d[letter]

    # loop through replacement options
    for i in range(len(options)):
        # limit the words at 20 charaters
        if len(interm_str)>20:
            return
        
        temp_str = ""
        for idx_letter in range(len(interm_str)):
            # keep the terminal characters and replace the nonterminal ones    
            if letter == interm_str[idx_letter]:
                temp_str += options[i]
            else:
                temp_str += interm_str[idx_letter]

        # search for new nonterminal characters
        upper_letter = ""
        for up_letter in temp_str:
            if up_letter == up_letter.upper():
                upper_letter = up_letter
        
        if len(upper_letter) != 0:
            generate(upper_letter, temp_str)
        # there aren't any nontermial characters
        else:
            if temp_str in search:
                print(temp_str)


print("Founded words:")               
# the start string is "S" and the character to be replaced is "S"
generate("S", "S")