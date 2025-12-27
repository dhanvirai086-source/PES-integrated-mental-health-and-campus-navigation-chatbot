import random
name=input("enter your name:")
def sevenup(person):
    cash=50
    def game():
        nonlocal cash
        print("you have",cash,"in your hand")
        call=int(input("how much money do you want to put(lesser than or equal to cash in hand): "))
        a=int(input("choose 1 for 7up, 2 for 7down, and 0 for lucky 7: "))
        x=0
        b=random.randint(1,6)
        c=random.randint(1,6)
        print("Dice one rolled",b,"and dice two rolled",c)
        if b+c<7:
            x=2
        elif b+c>7:
            x=1
        else:
            x=0

        if a==x:
            print("yay you won",2*call)
            cash+=2*call
        else:
            print("haha loser")
            cash-=call

    return game

player=sevenup(name)
n=int(input("how many times do you want to play"))
for i in range(n):
    player()