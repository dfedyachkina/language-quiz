import random
import time
import os
import gspread
from google.oauth2.service_account import Credentials
import colorama
from colorama import Fore, Back, Style


# Define the scope for Google Sheets and Drive API
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

# Authenticate using the service account credentials
CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('language_quiz')
USERNAME = None
colorama.init(autoreset=True)


def clear():
    """
    Clear function to clean-up the terminal so things don't get messy.
    """
    os.system("cls" if os.name == "nt" else "clear")


def get_username():
    """
    Prompts the user to create a username.
    Ensures the username is at least 4 characters long.
    Returns:
        username (str): The validated username entered by the user.
    """
    clear()
    print("Welcome to the Language Quiz!\n")
    while True:
        print(
            "Before the game starts - you need to create a username."
            "Username should be more than 4 letters.\n"
            )
        USERNAME = input("Enter a username: \n")

        if validate_username(USERNAME):
            clear()
            break
    return USERNAME


def validate_username(username):
    """
    Validates the length of the username.
    Args:
        username (str): The username to validate.
    Returns:
        bool: True if the username is valid, False otherwise.
    """
    try:
        if len(username) < 4:
            raise ValueError(
                f'{Fore.RED}The username should contain at least 4 letters.'
                f'{Fore.RED}Your username contains just '
                f'{len(username)} letters.'
            )
    except ValueError as e:
        print(f'Invalid data: {e}, please try again. \n')
        return False

    return True


def user_action():
    """
    Prompts the user to select an action from the menu.
    Returns:
        number_action (int): The validated number of the user's action.
    """
    while True:
        number_action = input(
            "Please enter the number of the action you want to do: \n"
            )

        if validate_user_action(number_action):
            clear()
            break
    number_action = int(number_action)
    return number_action


def validate_user_action(number):
    """
    Validates the user's action selection.
    Args:
        number (str): The user's input to validate.
    Returns:
        bool: True if the input is valid, False otherwise.
    """
    try:
        number = int(number)
        if number > 3:
            raise ValueError(
                f'Sorry, but the number of action {number} doesn\'t exist.'
            )
    except ValueError as e:
        print(
            f"{Fore.RED}Invalid data: {e}. "
            f"{Fore.RED}Please choose a number of action from 1 to 3."
            )
        return False

    return True


def start_quiz():
    """
    Starts the quiz by asking the user to choose a language.
    Returns:
        result (list): The user's score and selected language.
    """
    print("Choose a language:\n")
    print(" (1) Russian\n")
    print(" (2) Spanish\n")
    print(" (3) French\n")
    print(" (4) German\n")
    while True:
        number_language = int(
            input("Enter the number of the selected language:\n")
            )

        if validate_lan_answer(number_language):
            break

    if number_language == 1:
        result = show_questions("russian")
    elif number_language == 2:
        result = show_questions("spanish")
    elif number_language == 3:
        result = show_questions("french")
    else:
        result = show_questions("german")
    return result


def validate_lan_answer(number):
    """
    Validation of user's answer to choose language
    """
    try:
        number = int(number)
        if number > 4:
            raise ValueError(
                f'Sorry, but the number of action {number} doesn\'t exist.'
            )
    except ValueError as e:
        print(
            f"{Fore.RED}Invalid data: {e}. "
            f"{Fore.RED}Please choose a number of action from 1 to 3."
            )
        return False

    return True


def show_questions(language):
    """
    Displays all questions in the selected language,
    Collects user answers, and calculates the score.
    Args:
        language (str): The selected language for the quiz.
    Returns:
        score_data (list): A list containing the user's score and the language.
    """
    clear()
    print(f"You chose {language.capitalize()} language.")
    lan_sheet = SHEET.worksheet(language)
    all_data = lan_sheet.get_all_values()
    questions = all_data[1:]
    user_score = 0
    number_correct_answers = 0
    for row in questions:
        question_number = row[0]
        word = row[1]
        options = [row[2], row[3], row[4]]
        correct_answer = row[5]
        random.shuffle(options)
        print(
            f"\n Question {question_number}: "
            f"What is the translation for '{word}'?\n"
            )
        for idx, option in enumerate(options):
            print(f"  {chr(97 + idx)}) {option}\n")
        while True:
            user_answer = input("Please enter your answer (a, b, c): ").lower()

            if validate_answer(user_answer):
                break
        answer_index = ord(user_answer) - 97
        selected_option = options[answer_index]
        if selected_option == correct_answer:
            print(f"{Fore.GREEN}It's correct!")
            user_score += 20
            number_correct_answers += 1
        else:
            print(
                f"{Fore.RED}Oops! That is not correct. "
                "The right answer is '{correct_answer}'."
                )
        print("The next question will be displayed in 3 seconds...")
        time.sleep(2)
        clear()
    end_quiz(user_score, number_correct_answers, language)
    score_data = [user_score, language]
    return score_data


def validate_answer(answer):
    """
    Validates the user's answer to the quiz question.
    Args:
        answer (str): The user's answer to validate.
    Returns:
        bool: True if the answer is valid, False otherwise.
    """
    try:
        if answer not in ["a", "b", "c"]:
            raise ValueError(
                f"Sorry, but the option {answer} doesn't exist."
            )
    except ValueError as e:
        print(f"{Fore.RED}Invalid data: {e}, please enter a, b, or c.")
        return False
    return True


def end_quiz(score, correct_answers, language):
    """
    Displays the user's quiz results.
    Args:
        score (int): The user's total score.
        correct_answers (int): The number of correct answers given by the user.
        language (str): The language of the quiz.
    """
    print(f"\nThe result of the {language.capitalize()} Quiz\n")
    print(f"The number of correct answers: {correct_answers} \n")
    print(f"Your score is {score}% \n")
    clear()


def add_score_to_score_sheet(data):
    """
    Adds the user's score to the Google Sheets score table.
    Args:
        data (list): A list containing the username, score, and language.
    """
    username = data[0]
    print(f"Adding {username}'s score to the score table... \n")
    score_sheet = SHEET.worksheet("scores")
    score_sheet.append_row(data)
    print(
        f"{username}'s score has been added successfully to the score table.\n"
        )
    while True:
        score_answer = input(
            "Would you like to see the whole score table? Enter y or n: \n"
            )
        score_answer = score_answer.lower()

        if validate_answer_yes_no(score_answer):
            break

    if score_answer == "y":
        show_score()
    else:
        print("Returning to the menu... \n")
        clear()
        main()


def validate_answer_yes_no(data):
    """
    Validates the user's input for viewing the score table.
    Args:
        data (str): The user's input (either 'y' or 'n').
    Returns:
        bool: True if the input is valid, False otherwise.
    """
    try:
        if data not in ["y", "n"]:
            raise ValueError(
                f"The answer can only be 'y' or 'n'. Your input: {data}"
            )
    except ValueError as e:
        print(f"{Fore.RED}Invalid data: {e}, please try again.")
        return False
    return True


def show_score():
    """
    Displays the entire score table with borders.
    """
    print("The score table:")
    score_sheet = SHEET.worksheet("scores")
    data = score_sheet.get_all_values()
    headers = data[0]
    scores_data = data[1:]
    scores_data.sort(key=lambda row: int(row[1]), reverse=True)
    col_widths = [max(len(str(item)) for item in col) for col in zip(*([headers] + scores_data))]  # noqa
    border_line = "+" + "+".join("-" * (width + 2) for width in col_widths) + "+"  # noqa
    print(border_line)
    print("| " + " | ".join(f"{header:{col_widths[i]}}" for i, header in enumerate(headers)) + " |")  # noqa
    print(border_line)
    for row in scores_data:
        print("| " + " | ".join(f"{item:{col_widths[i]}}" for i, item in enumerate(row)) + " |")  # noqa
        print(border_line)
    back_to_menu = input("\n Would you like to return to the menu?(y/n): \n")
    while True:
        back_to_menu = back_to_menu.lower()
        if validate_answer_yes_no(back_to_menu):
            break
    if back_to_menu == "y":
        print("Returning to the menu...")
        main()
    else:
        exit_program(USERNAME)


def exit_program(username):
    """
    Exits the program with a goodbye message.
    Args:
        username (str): The username to include in the goodbye message.
    """
    clear()
    print("The program is closing...")
    print(f"Bye-bye, {username}!")


def main():
    """
    Runs the main program loop, displaying the menu and handling user input.
    """
    username = get_username()
    print(f"\nHi, {username}! Here is the menu of the game:\n")
    print("\n (1) Start Language Quiz!")
    print("\n (2) Show the scores")
    print("\n (3) Exit\n")
    number_action = user_action()
    if number_action == 1:
        result = start_quiz()
        result.insert(0, username)
        add_score_to_score_sheet(result)
    elif number_action == 2:
        show_score()
    else:
        exit_program(username)


main()