# Ask user to enter sentence
str_manip = str(input("Enter the sentence: "))

# Calculating the length of sentence
length = len(str_manip)
print("length of sentence:", length)

# Finding the last letter and replacing with @
last_letter = str_manip[-1]

for i in str_manip:
    if i == last_letter:
        i = "@"
        replaced = str_manip.replace(last_letter, i)
print("Replacing sentence with last character: ", replaced)

# Reversing last three characters
last_three = str_manip[-3:]
rev = last_three[::-1]
print("Last three characters Reversed: ", rev)

five_words = str_manip[0:3] + str_manip[-2:]
print("Word made from First three and last two_words: ", five_words)
