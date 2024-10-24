import random
import string
from random import choice
def getpassword(): #mmouse generates entropy?
    frequncy = random.randint(1,5) # used for the frequency of random nums and syms
    symbols = "!£$%^&*():@?><.,|¬`#][@}]" # can be expanded
    numbers = "1234567890"
    parts = [ # takes one work from each word list and then splits it
        string.capwords(random.choice(open("verbs.txt").read().split())),
        string.capwords(random.choice(open("adjects.txt").read().split())),
        string.capwords(random.choice(open("nouns.txt").read().split()))
    ]

    random.shuffle(parts) #random shuffle 

    password = ''.join(parts) #joins them back to gether

    passwordl = list(password)
    for _ in range(frequncy):#takes the fequency num which is how many times the for is set
        symbol = random.choice(symbols) # gets a sym
        num = random.choice(numbers) #gets a num
        positionnum = random.randint(0, len(passwordl))  #gets a random int position between the start and end of passlist
        passwordl.insert(positionnum, num) #inserts the number in
        positionsym = random.randint(0, len(passwordl)) 
        passwordl.insert(positionsym, symbol)
    return ''.join(passwordl)

print(getpassword())

