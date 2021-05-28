import math
import sys


## Function: for converting number to string

def numbertowords(x):
    ## Number dictionary ##
    s = {0: 'ZERO', 1: 'ONE', 2: 'TWO', 3: 'THREE', 4: 'FOUR', 5: 'FIVE', 6: 'SIX', 7: 'SEVEN', 8: 'EIGHT', 9: 'NINE'}

    ## Last four digits of the given ID
    a = x[-4:]
    string = ''

    ## Convert the last four digits to their corresponding string form
    for i in a:
        d = int(i)
        if d in s:
            string += s[d]

    return 'MYIDIS' + string


## Function: for computing the Huffman prefix code

def PrefixCode(IdStr):
    ## Computing the frequency initialization with zero.
    freq = {}
    for ch in IdStr:
        if ch in freq:
            freq[ch] += 1
        else:
            freq[ch] = 1

            ## Sorting the frequency in Descending order
    freq = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    lenId = len(IdStr)

    ## Computing the probabilities based on the frequencies of the letter
    count = 0
    charLoc = {}
    probabilities = []
    for ch, fr in freq:
        charLoc[ch] = count;
        probabilities.append(float("{:.2f}".format(fr / lenId)))
        count += 1

    num = len(probabilities)

    ## List of the huffman prefix codes for each letter
    huffmanPreCode = [''] * num

    ## Traversing the number of probabilities to compute the prefix codes
    for i in range(num - 2):

        ## Considering the 2 smallest probabilities in the list
        val = probabilities[num - i - 1] + probabilities[num - i - 2]

        ## If both nodes (left and right) already have existing binary trees
        if (huffmanPreCode[num - i - 1] != '' and huffmanPreCode[num - i - 2] != ''):
            huffmanPreCode[-1] = ['1' + code for code in huffmanPreCode[-1]]
            huffmanPreCode[-2] = ['0' + code for code in huffmanPreCode[-2]]

        ## If the left node has an existing binary tree
        elif (huffmanPreCode[num - i - 1] != ''):
            huffmanPreCode[num - i - 2] = '0'
            huffmanPreCode[-1] = ['1' + code for code in huffmanPreCode[-1]]

        ## If the right node has an existing binary tree
        elif (huffmanPreCode[num - i - 2] != ''):
            huffmanPreCode[num - i - 1] = '1'
            huffmanPreCode[-2] = ['0' + code for code in huffmanPreCode[-2]]

        ## If the node is a new node without existing left and right nodes
        else:
            huffmanPreCode[num - i - 1] = '1'
            huffmanPreCode[num - i - 2] = '0'

        ## Find position for the new combined probability
        pos = findPosNewProb(val, i, probabilities)
        probabilities.insert(pos, val)

        ## Consider the rest of the probabilities
        probabilities = probabilities[0:(len(probabilities) - 2)]

        ## Temporary prefix code for the newly combined probability ##

        ## Temporary prefix code: Both left and right nodes have existing trees
        if (isinstance(huffmanPreCode[num - i - 2], list) and isinstance(huffmanPreCode[num - i - 1], list)):
            combineCode = huffmanPreCode[num - i - 1] + huffmanPreCode[num - i - 2]

        ## Temporary prefix code: Only left node has existing tree
        elif (isinstance(huffmanPreCode[num - i - 2], list)):
            combineCode = huffmanPreCode[num - i - 2] + [huffmanPreCode[num - i - 1]]

        ## Temporary prefix code: Only right node has existing tree
        elif (isinstance(huffmanPreCode[num - i - 1], list)):
            combineCode = huffmanPreCode[num - i - 1] + [huffmanPreCode[num - i - 2]]

        ## Temporary prefix code: No node has existing trees
        else:
            combineCode = [huffmanPreCode[num - i - 2], huffmanPreCode[num - i - 1]]

        ## Considering the prefix codes for the rest of the chars
        huffmanPreCode = huffmanPreCode[0:(len(huffmanPreCode) - 2)]
        huffmanPreCode.insert(pos, combineCode)

    ## Root node for the final binary tree. '0' is added for all the left side and '1' is added for the
    ## right side of the binary tree.
    huffmanPreCode[0] = ['0' + code for code in huffmanPreCode[0]]
    huffmanPreCode[1] = ['1' + code for code in huffmanPreCode[1]]

    count = 0
    completeCode = [''] * num

    ## Merging all the prefix codes from the left and right sides of the final binary trees
    for i in range(2):
        for j in range(len(huffmanPreCode[i])):
            completeCode[count] = huffmanPreCode[i][j]
            count += 1

    ## Sorting all the prefix codes in ascending order based on the length of the codes
    completeCode = sorted(completeCode, key=len)

    print('Step #3. Prefix Codes (Generated Using Huffman Coding):')

    ## Displaying the prefix code for the unique chars
    for ch in IdStr:
        if ch in charLoc.keys():
            print('{:>10} {:>1} {:<0} {:<5}'.format(ch, ':', '', completeCode[charLoc[ch]]))
            del charLoc[ch]


## Find the position in probabilities array for the new combined probability
def findPosNewProb(val, ind, probabilities):
    for j in range(len(probabilities)):
        if (val >= probabilities[j]):
            return j
    return ind - 1


## Taking input from the user
stuId = input("Step #1. Enter Student ID:")

## Calling function to convert the ID to string
IdStr = numbertowords(stuId)
print("Step #2. Generated String: " + IdStr)

## Finally computing the Huffman coding for each characters for the previous string
## and displying all the codes.
PrefixCode(IdStr)