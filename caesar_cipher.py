'''
Task:
Implement a Caesar cipher, both encoding and decoding. The key is an integer from 1 to 25. This cipher rotates 
the letters of the alphabet (A to Z). The encoding replaces each letter with the 1st to 25th next letter in the 
alphabet (wrapping Z to A). So key 2 encrypts "HI" to "JK", but key 20 encrypts "HI" to "BC". This simple 
"monoalphabetic substitution cipher" provides almost no security, because an attacker who has the encoded message 
can either use frequency analysis to guess the key, or just try all 25 keys.

Solution:
Two functions:
- caesar(string, integer)
- caesar_decrypt(string, integer)
That encrypt and decrypt strings as required. Note that they are the same except the decrypt version just uses 
negative the integer specified.

Approach:
Create two dictionaries:
- (A) one to map lower-case letters to integers
- (B) one to map integers to lower-case letters

For each letter in the string we are trying to encrypt/decrypt, find the integer it corresponds to (i.e. the
letter's index in the alphabet) from (A), shift that by the number required (e.g. add 5), and then see which 
letter it now corresponds to using (B). Then add that letter to the encrypted/decrypted string. Also use an if
statement to retain the capitalisation of each character.

Do this for all characters in the string (retaining spaces, punctuation, and numbers as they were), and then 
return the completed string.
'''

IntegerToLetterDictionary = {}
IntegerToLetterDictionary[0] = 'a'
IntegerToLetterDictionary[1] = 'b'
IntegerToLetterDictionary[2] = 'c'
IntegerToLetterDictionary[3] = 'd'
IntegerToLetterDictionary[4] = 'e'
IntegerToLetterDictionary[5] = 'f'
IntegerToLetterDictionary[6] = 'g'
IntegerToLetterDictionary[7] = 'h'
IntegerToLetterDictionary[8] = 'i'
IntegerToLetterDictionary[9] = 'j'
IntegerToLetterDictionary[10] = 'k'
IntegerToLetterDictionary[11] = 'l'
IntegerToLetterDictionary[12] = 'm'
IntegerToLetterDictionary[13] = 'n'
IntegerToLetterDictionary[14] = 'o'
IntegerToLetterDictionary[15] = 'p'
IntegerToLetterDictionary[16] = 'q'
IntegerToLetterDictionary[17] = 'r'
IntegerToLetterDictionary[18] = 's'
IntegerToLetterDictionary[19] = 't'
IntegerToLetterDictionary[20] = 'u'
IntegerToLetterDictionary[21] = 'v'
IntegerToLetterDictionary[22] = 'w'
IntegerToLetterDictionary[23] = 'x'
IntegerToLetterDictionary[24] = 'y'
IntegerToLetterDictionary[25] = 'z'

LetterToIntegerDictionary = {}
for x in range (0,26):
    LetterToIntegerDictionary[IntegerToLetterDictionary[x]] = x

def caesar(text,shift_by):
    '''
    Takes in a string, and creates a 'Caesar' cipher by shifting each letter by the number of letters set out by the 'shift_by' argument. Output is the encoded string.
    '''
    shifted_string = ''
    for x in text:
        try:
            if x == x.lower():
                y = IntegerToLetterDictionary[(LetterToIntegerDictionary[x] + shift_by)%26]
            elif x == x.upper():
                y = IntegerToLetterDictionary[(LetterToIntegerDictionary[x.lower()] + shift_by)%26].upper()
            shifted_string = shifted_string + y
        except: 
            shifted_string = shifted_string + x
    return shifted_string

def caesar_decrypt(text, shifted_by):
    '''
    Takes in a string that has been 'Casear ciphered' and the number of letters it was shifted by, and outputs the original, decrypted string
    '''
    return caesar(text, -shifted_by)
