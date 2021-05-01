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
    return card #idk why but seeing a red cursor just sitting here was terrifying

def checkcard(card,card2,ace:str):
    cardval = 0
    temp = card
    cards={'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'10':10,'Jack': 10, 'Queen': 10, 'King': 10}
    for i in range(2):
        if 'Ace' in temp:
            cardval = cardval + int(ace)
        else:
            cardval = cardval + cards[temp]
        temp = card2
    return cardval