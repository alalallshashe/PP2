#With the break statement we can stop the loop before it has looped through all the items:

#1
fruits = ["apple", "banana", "cherry"]
for x in fruits:
  print(x)
  if x == "banana":
    break

#2
fruits = ["apple", "banana", "cherry"]
for x in fruits:
  if x == "banana":
    break
  print(x)

#3
for ch in "hello":
    if ch == "l":
        break
    print(ch)

#4
for i in range(10):
    if i > 5:
        break
    print(i)

#5
for x in range(1, 10):
    if x == 7:
        break
    print(x)