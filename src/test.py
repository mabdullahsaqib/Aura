from word2number import w2n

string = "145"
print(string[0])
print(string[1:])

# string = "one fourty five"
# print(string[0])
# print(string[1:])
# print(w2n.word_to_num(string[0]))
# print(w2n.word_to_num(string[1:]))

string = "one forty five"
string = string.split()
print(string)
print(w2n.word_to_num(string[0]))
s = ''.join(string[1:])
print(s)
print(w2n.word_to_num(s))

string = "one forty-five"
string = string.split()
print(string)
print(w2n.word_to_num(string[0]))
s = ''.join(string[1:])
print(s)
print(w2n.word_to_num(s))
