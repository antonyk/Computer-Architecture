# part 1
data = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0]

# data2 = data[-1::-1]

# print(data2)

for i in range(len(data)):

  print(data[(-1-i)])


# part 2
"""
Given a hashmap where the keys are integers, print out all of the values of the hashmap in reverse order, ordered by the keys.
For example, given the following hashmap:
{
  14: "vs code",
  3: "window",
  9: "alloc",
  26: "views",
  4: "bottle",
  15: "inbox",
  79: "widescreen",
  16: "coffee",
  19: "tissue",
}
The expected output is:
widescreen
views
tissue
coffee
inbox
vs code
alloc
bottle
window
"""

dic = {
  14: "vs code",
  3: "window",
  9: "alloc",
  26: "views",
  4: "bottle",
  15: "inbox",
  79: "widescreen",
  16: "coffee",
  19: "tissue",
}

keys = list(dic.keys())
keys.sort(reverse=True)
for key in keys:
  print(dic[key])

