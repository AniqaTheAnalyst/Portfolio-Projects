
print("Welcome to the game")

playing = input("Do you want to play? : ")

total = 0
if playing.lower() != "yes":

    quit()


print("okay lets play :)")
answer = input("what dose CPU stand for? ")
# 1
if answer.lower() == "central processing unit":
    print("Correct!")
    total += 1
else:
    print("Wrong! Try again")

answer = input("what dose GPU stand for? ")
# 2
if answer.lower() == "graphics processing unit":
    print("Correct!")
    total += 1

else:
    print("Wrong! Try again")
# 3
answer = input("what dose RAM stand for? ")

if answer.lower() == "random access memory":
    print("Correct!")
    total += 1
else:
    print("Wrong! Try again")
# 4
answer = input("what dose PSU stand for? ")

if answer.lower() == "power supply unit":
    print("Correct!")
    total += 1
else:
    print("Wrong! Try again")


print(f"You got {int((total*100)/4)}% correct")
