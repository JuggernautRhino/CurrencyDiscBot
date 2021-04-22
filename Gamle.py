import random

def rand_card():
    speccards=['Jack','Queen','King','Ace']
    card = str(random.randint(0,12))
    if int(card) >= 10:
        card=speccards[int(card)-10]
    elif int(card) == 0: 
        card = speccards[3]
    else:
        card=int(card)+1
    return card

def checkcard(card,card2,ace=0):
    cardval = 0
    speccards={'Jack': 10, 'Queen': 10, 'King': 10}
    for i in range(2):    
        try:
            cardval = int(card) + cardval
        except:
            if card != 'Ace':
                cardval = speccards[card] + cardval 
        if ace == 0: continue
        elif ace != 0:
            if ace == 1:
                cardval=cardval+1
            elif ace == 11:
                cardval=cardval+11
        card=str(card2)
    return cardval