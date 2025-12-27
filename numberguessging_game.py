import random
target_number = random.randint(1 ,100)
print("welcome to the number guessing game!")
attempts = int(5)
while attempts > 0:
    guess = int(input("enter ur guess!!"))
    if guess == target_number:
        print("OMG thats right ;)")
        (exit)
    elif guess > target_number:
        print("oh no too high ><")
        attempts = attempts-1
    elif guess < target_number:
        print("oh no too less :(")
        attempts = attempts-1
    if attempts == 0:
        print("game over,no attempts left,the number was",target_number)
