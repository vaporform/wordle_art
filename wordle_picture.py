keyword = "curry"
lines = [
    "BBBBB",
    "BBYBB",
    "BYYYB",
    "BBYBB",
    "BYBYB",
    "GGGGG",
]

def wordcheck(word:str,key:str):
    output = ''
    # make temp word
    temp_word = key

    for i in range(len(word)):
        if word[i] == temp_word[i]:
            output += 'G'
            temp_word = temp_word[:i] + '0' + temp_word[i+1:]
        else:
            # find if it's even in the word at all
            res =  temp_word.find(word[i])
            if res == -1:
                output += "B"
            else:
                output += "Y"
                temp_word = temp_word[:res] + '0' + temp_word[res+1:]
        #print(temp_word)
    return output

# word find
possible = {
    0:[],1:[],2:[],3:[],4:[],5:[]
}

match_true = True
for i in range(len(lines)):
    tex = lines[i]
    # bruteforce lol
    with open('possible.txt','r') as f:
        wordle_poss = f.read().splitlines()
        for word in wordle_poss:
            if match_true:
                if wordcheck(word,keyword) == tex:
                    possible[i].append(word)
            else:
                if wordcheck(word,keyword).replace('Y','1').replace('G','1') == tex.replace('Y','1').replace('G','1'):
                    possible[i].append(word)
        
        if len(possible[i]) == len(wordle_poss):
            possible[i] = "Any"


#print(possible)
for key,value in possible.items():
    print("LINE",key+1)
    print("POSSIBLE:", value)
#print(wordcheck("nanny",keyword))
