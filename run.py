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


