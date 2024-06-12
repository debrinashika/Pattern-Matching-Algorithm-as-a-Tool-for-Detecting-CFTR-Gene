from pattern import *

print("Welcome to The Protein Motifs Searcher!")
print("Here's you can do a Pattern Matching Algorithm as a Tool for Detecting CFTR Gene Mutations in Cystic Fibrosis Disease")
print("Choose an input do you want to choose:")
print("1. File (.txt)")
print("2. Terminal")

while True:
    try:
        choice = int(input("Input: "))
        if choice not in [1, 2]:
            print("Invalid input! Please enter 1 or 2.")
        else:
            break
    except ValueError:
        print("Invalid input! Please enter a number (1 or 2).")

if choice == 1:
    loc = input("Enter file name: ")
    file_path = 'test/' + loc

    try:
        with open(file_path, 'r') as file:
            cftr_sequence = file.read().replace('\n', '')  # Remove newlines if present
    except FileNotFoundError:
        print("File not found. Please check the file path.")
        exit()
else:
    cftr_sequence = input("Enter CFTR sequences: ")

# Now call the search_disorder function with cftr_sequence
search_disorder(cftr_sequence)
