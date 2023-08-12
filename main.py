import difflib
import os.path
import re
from datetime import datetime


# Function to validate user input for the primary menu option.
def get_menu():
    while True:
        try:
            print()
            print(('\u00AB'*2), ('\u2261'*60), ('\u00BB'*2))
            print(('\u00AB' * 2), ('\u2261' * 60), ('\u00BB' * 2))
            print(('\u00AB'*2), ('\u2591'*10), "SPELL", ('\u2591'*10), "CHECK", ('\u2591'*10), "MENU", ('\u2591'*10),
                  ('\u00BB'*2))
            print(('\u00AB' * 2), ('\u2261' * 60), ('\u00BB' * 2))
            print(('\u00AB'*2), ('\u2248'*7), "<<<<<<", '\u007C'*2, "1. Spell check a sentence",  '\u007C'*2, ">>>>>>",
                  ('\u2248'*6), ('\u00BB'*2))
            print(('\u00AB' * 2), ('\u2248' * 7), "<<<<<<", '\u007C'*2, "2. Spell check a file", ' '*3, '\u007C'*2,
                  ">>>>>>", ('\u2248' * 6),
                  ('\u00BB' * 2))
            print(('\u00AB' * 2), ('\u2248' * 7), "<<<<<<", '\u007C'*2, "0. Quit", ' '*17, '\u007C'*2, ">>>>>>",
                  ('\u2248' * 6), ('\u00BB' * 2))
            print(('\u00AB' * 2), ('\u2261' * 60), ('\u00BB' * 2))
            print(('\u00AB' * 2), ('\u2591' * 12), "END", ('\u2591' * 12), "OF", ('\u2591' * 11), "MENU",
                  ('\u2591' * 10), ('\u00BB' * 2))
            print(('\u00AB' * 2), ('\u2261' * 60), ('\u00BB' * 2))
            print(('\u00AB' * 2), ('\u2261' * 60), ('\u00BB' * 2))
            print()

            user_input = int(input("Enter your choice: "))
            if user_input not in (0, 1, 2):
                raise ValueError
            return user_input
        except ValueError:
            print("Invalid input! Please enter a valid choice (0, 1, or 2).")


# Loading English words from the provided (EnglishWords.txt) text file and making it set.
with open("EnglishWords.txt", "r") as f:
    set_of_words = set(f.read().splitlines())


# Function to suggest similar/likely words
def suggested_corrections(word):
    suggestions = difflib.get_close_matches(word, set_of_words, n=3)
    return suggestions


# function to check the filename that user entered
def get_users_filename():
    while True:
        filename = input("Enter the filename: ")
        if os.path.isfile(filename):
            return filename
        else:
            print("File not found. Please enter a valid filename.")
            print()
            print(('\u00AB' * 2), ('\u2261' * 60), ('\u00BB' * 2))
            print(('\u00AB' * 2), ('\u2261' * 60), ('\u00BB' * 2))


# function to spell check a file and make suggestions
def check_file():
    filename = get_users_filename()
    with open(filename, "r") as file:
        file_content = file.read()

    # Clean and tokenize the content of the file
    updated_sentence = re.sub(r'[^\w\s]', '', file_content).lower()
    words = re.findall(r'\b\w+\b', updated_sentence)

    # Initialise variables to track spell check statistics
    total_words = len(words)
    correct_words = 0
    incorrect_words = 0
    added_to_dictionary = 0
    changed_words = 0
    marked_words = []

    # Record the start time for spell checking
    start_time = datetime.now()

    # Iterate through each word in the file
    for word in words:
        cleaned_word = re.sub(r'[^\w]', '', word.lower())

        # Function for marking the misspelt word
        def mark():
            nonlocal incorrect_words
            print(f"?{word}?")
            marked_words.append(f"?{word}?")
            incorrect_words += 1

        # Function to add the misspelt word in the dictionary
        def add_to_dictionary():
            nonlocal added_to_dictionary, correct_words
            set_of_words.add(cleaned_word)
            added_to_dictionary += 1
            correct_words += 1
            print("Word is added to the dictionary.")

        # Function for ignoring the misspelt word
        def ignore():
            nonlocal incorrect_words
            incorrect_words += 1

        # Function for suggesting likely/similar words for the misspelt word
        def suggest_likely_word():
            nonlocal correct_words, changed_words
            print(f"Suggested corrections: {suggested_corrections(word)}\n")
            user_action = input("Enter the number(1, 2, or 3) to choose the suggestion and"
                                " accept it or enter 'R' or 'r' to reject: ")
            print(f"You entered : {user_action}")
            if user_action.isdigit():
                index_suggestion = int(user_action) - 1
                if 0 <= index_suggestion < len(suggestions):
                    corrected_word = suggestions[index_suggestion]
                    print(f"Accepted suggestion: {corrected_word}")
                    correct_words += 1
                    changed_words += 1
                else:
                    print("Invalid selection. Please enter a valid suggestion number.")
            elif user_action.lower() == 'r':
                print("Suggestion rejected.")
            else:
                print("Invalid input. Please enter a valid option.")

        # Check if the word is in the set of English words
        if cleaned_word not in set_of_words:
            suggestions = suggested_corrections(cleaned_word)
            if suggestions:
                print(('\u00AB' * 2), ('\u2261' * 60), ('\u00BB' * 2))
                print(('\u00AB' * 2), ('\u2261' * 60), ('\u00BB' * 2))
                print()
                print(f"'{word}' is not spelled correctly.")
                # Prompt for the user input to select options
                user_input_action = input("Enter one of the options.\n 1 Ignore\n"
                                          " 2 Mark\n"
                                          " 3 Add to dictionary\n"
                                          " 4 Suggest likely word\n ")
                print(f"You selected : {user_input_action}")
                print(('\u00AB' * 2), ('\u2261' * 60), ('\u00BB' * 2))

                # Switch statement for the options
                switch_actions = {
                    '1': ignore,
                    '2': mark,
                    '3': add_to_dictionary,
                    '4': suggest_likely_word
                }

                selected_action = switch_actions.get(user_input_action)
                if selected_action is not None:
                    selected_action()
            else:
                marked_words.append(f"?{word}?")
                incorrect_words += 1
        else:
            correct_words += 1

    # Record the end time for spell checking
    end_time = datetime.now()

    print(('\u00AB' * 2), ('\u2261' * 60), ('\u00BB' * 2))
    # Display summary statistics
    print("\nSummary Statistics:")
    print(f"Total words: {total_words}")
    print(f"Correctly spelled words: {correct_words}")
    print(f"Incorrectly spelled words: {incorrect_words}")
    print(f"Words added to dictionary: {added_to_dictionary}")
    print(f"Words changed by the user: {changed_words}")
    print(f"Time and date: {start_time}")
    print(f"Time elapsed: {end_time - start_time}")
    print()
    print(('\u00AB' * 2), ('\u2261' * 60), ('\u00BB' * 2))
    print(('\u00AB' * 2), ('\u2261' * 60), ('\u00BB' * 2))
    print()

    # Save the spell-checked input to a new file
    save_file2 = input("Do you want to save the statistics for this process? (y/n) ")
    print(f"You selected : {save_file2}")
    if save_file2.lower() == 'y':
        new_filename = input("Enter the filename to save the spell-checked input: ")
        print(f"You entered : {new_filename}")
        with open(new_filename, "w") as file_inner1:
            file_inner1.write(f"Summary Statistics:\n")
            file_inner1.write(f"Total words: {total_words}\n")
            file_inner1.write(f"Correctly spelled words: {correct_words}\n")
            file_inner1.write(f"Incorrectly spelled words: {incorrect_words}\n")
            file_inner1.write(f"Words added to dictionary: {added_to_dictionary}\n")
            file_inner1.write(f"Words changed by the user: {changed_words}\n")
            file_inner1.write(f"Time and date: {start_time}\n")
            file_inner1.write(f"Time elapsed: {end_time - start_time}\n\n")
            file_inner1.write(" ".join(marked_words))
            file_inner1.write("\n")
            file_inner1.write(file_content)
            print("Spell checked input is saved in the file.")

        print()
        print(('\u00AB' * 2), ('\u2261' * 60), ('\u00BB' * 2))
        print(('\u00AB' * 2), ('\u2261' * 60), ('\u00BB' * 2))
        print()
        # Prompt user for further action
        option_check = input("Select <Q> or <q> to quit, <M> or <m> to return to the menu: ")
        print(f"You entered : {option_check}")
        if option_check.lower() == "q":
            print("You are quitting the program. Thank you!")
            print()
            print(('\u00AB' * 2), ('\u2261' * 60), ('\u00BB' * 2))
            print(('\u00AB' * 2), ('\u2261' * 60), ('\u00BB' * 2))
            print()
            raise SystemExit
        elif option_check.lower() == "m":
            print("Directing to the menu")
            return get_menu()
        else:
            print("Invalid input. Enter a valid option.")
        print()
        print(('\u00AB' * 2), ('\u2261' * 60), ('\u00BB' * 2))
        print(('\u00AB' * 2), ('\u2261' * 60), ('\u00BB' * 2))

    # Do not save the file and jump to menu or quit program
    elif save_file2.lower() == "n":
        option_check2 = input("Select <Q> or <q> to quit , <M> or <m> to return to menu ")
        print(f"You entered : {option_check2}")
        if option_check2.lower() == "m":
            print("Directed to the menu")
            return get_menu()
        elif option_check2.lower() == "q":
            print("You are quitting the program. Thank you!")
            print()
            print(('\u00AB' * 2), ('\u2261' * 60), ('\u00BB' * 2))
            print(('\u00AB' * 2), ('\u2261' * 60), ('\u00BB' * 2))
            print()
            raise SystemExit
        else:
            print("Invalid input. Enter valid input.")

    else:
        print("Invalid input! Please select correct options.")
    print()
    print(('\u00AB' * 2), ('\u2261' * 60), ('\u00BB' * 2))
    print(('\u00AB' * 2), ('\u2261' * 60), ('\u00BB' * 2))


# Function to spell check a sentence and make suggestions
def check_sentence():
    # Get the sentence input from the user
    users_sentence = input("Enter the sentence to spell check: ")
    print(f"You entered : {users_sentence}")
    words = re.findall(r'\b\w+\b', users_sentence)

    # Initialize variables to track spell check statistics
    total_words = len(words)
    correct_words = 0
    incorrect_words = 0
    added_to_dictionary = 0
    changed_words = 0
    marked_words = []

    # Record the start time for spell checking
    start_time = datetime.now()

    # Iterate through each word in the sentence
    for word in words:
        word_lower_case = word.lower()
        cleaned_word = re.sub(r'[^\w]', '', word_lower_case)

        # Check if the word is in the set of English words
        if cleaned_word not in set_of_words:
            suggestions = suggested_corrections(cleaned_word)
            if suggestions:
                while True:
                    print(('\u00AB' * 2), ('\u2261' * 60), ('\u00BB' * 2))
                    print(f"'{word}' is not spelled correctly.")
                    user_input_action = input("Enter one of the options.\n 1 Ignore\n"
                                              " 2 Mark\n"
                                              " 3 Add to dictionary\n"
                                              " 4 Suggest likely word\n ")
                    print(f"You selected : {user_input_action}")
                    print(('\u00AB' * 2), ('\u2261' * 60), ('\u00BB' * 2))

                    # Function to add the misspelt word to the dictionary
                    def add_to_dictionary():
                        nonlocal added_to_dictionary, correct_words
                        set_of_words.add(cleaned_word)
                        added_to_dictionary += 1
                        correct_words += 1
                        print("word is added to the dictionary.")

                    # Function marking the misspelt word
                    def mark():
                        nonlocal incorrect_words
                        print(f"?{word}?")
                        marked_words.append(f"?{word}?")
                        incorrect_words += 1

                    # Function ignoring the misspelt word
                    def ignore():
                        nonlocal incorrect_words
                        incorrect_words += 1

                    # Function to suggest likely/similar words for the misspelt word
                    def suggest_likely_word():
                        nonlocal correct_words, changed_words
                        print(f"Suggested corrections: {suggested_corrections(word)}\n")

                        # Prompt for the user input for accepting or rejecting the word
                        user_action = input("Enter\n A Accept suggestion\n B Reject suggestion\n ")
                        print(f"You selected : {user_action}")
                        print(('\u00AB' * 2), ('\u2261' * 60), ('\u00BB' * 2))
                        print(('\u00AB' * 2), ('\u2261' * 60), ('\u00BB' * 2))
                        print()
                        if user_action.lower() == 'a':
                            switch_suggestions = {
                                'a': suggestions[0],
                                'b': suggestions[1],
                                'c': suggestions[2]
                            }
                            # Prompt for accepting one of the three suggestions
                            word_suggested = input("Enter one of the alphabet to select a particular word.\n"
                                                   " A - suggestion 1\n B - suggestion 2\n C - suggestion 3\n")
                            print(f"You selected : {word_suggested}")
                            selected_suggestion = switch_suggestions.get(word_suggested.lower())
                            if selected_suggestion is not None:
                                correct_words += 1
                                changed_words += 1
                                print(f"Here is selected suggestion : {selected_suggestion}")
                            else:
                                print("Invalid selection. Please select correctly. Try again ")
                        elif user_action.lower() == 'b':
                            nonlocal incorrect_words
                            incorrect_words += 1
                            print(f"You rejected the suggested word for : {word}")

                    # Switch statement for the provided options
                    switch_actions = {
                        '1': ignore,
                        '2': mark,
                        '3': add_to_dictionary,
                        '4': suggest_likely_word
                    }

                    selected_action = switch_actions.get(user_input_action)
                    if selected_action is not None:
                        selected_action()
                        break

            else:
                marked_words.append(f"?{word}?")
                incorrect_words += 1
        else:
            correct_words += 1

    # Record the end time for spell checking
    end_time = datetime.now()

    print(('\u00AB' * 2), ('\u2261' * 60), ('\u00BB' * 2))
    # Display summary statistics
    print("\nSummary Statistics:")
    print(f"Total words: {total_words}")
    print(f"Correctly spelled words: {correct_words}")
    print(f"Incorrectly spelled words: {incorrect_words}")
    print(f"Words added to dictionary: {added_to_dictionary}")
    print(f"Words changed by the user: {changed_words}")
    print(f"Time and date: {start_time}")
    print(f"Time elapsed: {end_time - start_time}")
    print()
    print(('\u00AB' * 2), ('\u2261' * 60), ('\u00BB' * 2))
    print(('\u00AB' * 2), ('\u2261' * 60), ('\u00BB' * 2))
    print()

    # Save the spell-checked input to a new file
    save_file1 = input("Do you want to save the statistics for this process? (y/n) ")
    print(f"You selected : {save_file1}")
    if save_file1.lower() == "y":
        new_filename = input("Enter the New filename to save the spell-checked input: ")
        with open(new_filename, "w") as file_inner2:
            file_inner2.write(f"Summary Statistics:\n")
            file_inner2.write(f"Total words: {total_words}\n")
            file_inner2.write(f"Correctly spelled words: {correct_words}\n")
            file_inner2.write(f"Incorrectly spelled words: {incorrect_words}\n")
            file_inner2.write(f"Words added to dictionary: {added_to_dictionary}\n")
            file_inner2.write(f"Words changed by the user: {changed_words}\n")
            file_inner2.write(f"Time and date: {start_time}\n")
            file_inner2.write(f"Time elapsed: {end_time - start_time}\n\n")
            file_inner2.write(" ".join(marked_words))
            file_inner2.write("\n")
            file_inner2.write(users_sentence)
            print("Spell checked input is saved in the file.")

        print()
        print(('\u00AB' * 2), ('\u2261' * 60), ('\u00BB' * 2))
        print(('\u00AB' * 2), ('\u2261' * 60), ('\u00BB' * 2))
        print()
        # Prompt user for further action
        option_check1 = input("Select <Q> or <q> to quit , <M> or <m> to return to menu ")
        print(f"You selected : {option_check1}")
        if option_check1.lower() == "m":
            print("You are directed to the menu.")
            return get_menu()
        elif option_check1.lower() == "q":
            print(f"You selected : {option_check1}")
            print("You are quitting the program. Thank you!")
            print()
            print(('\u00AB' * 2), ('\u2261' * 60), ('\u00BB' * 2))
            print(('\u00AB' * 2), ('\u2261' * 60), ('\u00BB' * 2))
            print()
            raise SystemExit
        else:
            print("Invalid input. Enter valid input.")
        print()
        print(('\u00AB' * 2), ('\u2261' * 60), ('\u00BB' * 2))
        print(('\u00AB' * 2), ('\u2261' * 60), ('\u00BB' * 2))

    # Do not save the file and jump to menu or quit program
    elif save_file1.lower() == "n":
        option_check2 = input("Select <Q> or <q> to quit , <M> or <m> to return to menu ")
        if option_check2.lower() == "m":
            print("You are directed to the menu.")
            return get_menu()
        elif option_check2.lower() == "q":
            print("You are quitting the program. Thank you!")
            print()
            print(('\u00AB' * 2), ('\u2261' * 60), ('\u00BB' * 2))
            print(('\u00AB' * 2), ('\u2261' * 60), ('\u00BB' * 2))
            print()
            raise SystemExit
        else:
            print("Invalid input. Enter valid input.")

    else:
        print("Invalid input! Please select correct options.")
    print()
    print(('\u00AB' * 2), ('\u2261' * 60), ('\u00BB' * 2))
    print(('\u00AB' * 2), ('\u2261' * 60), ('\u00BB' * 2))


# Main program
if __name__ == "__main__":
    while True:
        user_choice_input = get_menu()

        if user_choice_input == 1:
            check_sentence()
        elif user_choice_input == 2:
            check_file()
        else:
            print("You are quitting. Thank You!")
            print()
            print(('\u00AB' * 2), ('\u2261' * 60), ('\u00BB' * 2))
            print(('\u00AB' * 2), ('\u2261' * 60), ('\u00BB' * 2))
            raise SystemExit
