import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

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

def get_username():
    """
    Prompts the user to create a username.
    Ensures the username is at least 4 characters long.
    Returns:
        username (str): The validated username entered by the user.
    """
    print("Welcome to the Language Quiz!\n")
    while True:
        print("Before the game starts - you need to create a username. Username should be more than 4 letters.\n")
        username = input("Enter a username: \n")

        if validate_username(username):
            break
        
    return username

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
                f'The username should contain at least 4 letters. Your username contains just {len(username)} letters.'
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
        number_action = input("Please enter the number of the action you want to do: \n")

        if validate_user_action(number_action):
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
        print(f"Invalid data: {e}. Please choose a number of action from 1 to 3.")
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
    while True:
        number_language = int(input("Enter the number of the selected language:\n"))

        if validate_user_action(number_language):
            break

    if number_language == 1:
        result = show_questions("russian")
    elif number_language == 2:
        result = show_questions("spanish")
    else:
        result = show_questions("french")

    return result

def show_questions(language):
    """
    Displays all questions in the selected language, collects user answers, and calculates the score.
    Args:
        language (str): The selected language for the quiz.
    Returns:
        score_data (list): A list containing the user's score and the language.
    """
    print(f"You chose {language.capitalize()} language.")
    lan_sheet = SHEET.worksheet(language)
    all_data = lan_sheet.get_all_values()
    questions = all_data[1:]
    user_score = 0
    number_correct_answers = 0
    for row in questions:
        question_number = row[0]
        word = row[1]
        first_option = row[2]
        second_option = row[3]
        third_option = row[4]
        correct_answer = row[5]
        
        print(f"\n Question {question_number}: What is the translation for '{word}'?\n")
        print(f"  a) {first_option}\n")
        print(f"  b) {second_option}\n")
        print(f"  c) {third_option}\n")
        while True:
            user_answer = input("Please enter your answer (a, b, c): ")
            user_answer = user_answer.lower()

            if validate_answer(user_answer):
                break
        if user_answer == correct_answer:
            print(f"It's correct!")
            user_score += 20
            number_correct_answers += 1
        else:
            print(f"Oops! That is not correct. The right answer is {correct_answer}.")
    
    end_quiz(user_score, number_correct_answers, language)
    score_data = [user_score, language]
    return score_data


