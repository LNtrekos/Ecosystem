'''
This file contains the helper functions for User Input:
- Integer Input
- Float Input
- Character Input

Throughout this project, input from the user is frequently required.  
These helper functions ensure a smooth workflow with consistent error handling,  
value checks, and confirmation prompts.
'''


def user_input_int(input_prompt, check_prompt, error_prompt,
                   lower_limit=-float('inf'), upper_limit=float('inf')):
    '''
    Handles integer input from the user with:
    - Type validation
    - Lower/upper bound checks
    - Custom prompts for incorrect entries

    Parameters:
        input_prompt  : Main message shown to the user.
        check_prompt  : Message shown when the value is outside limits.
        error_prompt  : Message shown when the input is not an integer.
        lower_limit   : Minimum acceptable value (default: -inf).
        upper_limit   : Maximum acceptable value (default: +inf).

    Returns:
        Validated integer input from the user.
    '''
    while True:
        try:
            # Attempt to convert user input to integer
            user_input = int(input(input_prompt))

            # Check if value lies outside user-defined limits
            if user_input < lower_limit or user_input > upper_limit:
                print(check_prompt)
                continue

            return user_input

        except ValueError:
            # Triggered when int conversion fails
            print(error_prompt)


def user_input_float(input_prompt, check_prompt, error_prompt,
                     lower_limit=-float('inf'), upper_limit=float('inf')):
    '''
    Handles floating-point input with:
    - Type validation
    - Lower/upper bound checks
    - Custom prompts for invalid numerical entries

    Parameters mirror those of user_input_int() but for float inputs.
    '''
    while True:
        try:
            # Attempt to convert user input to float
            user_input = float(input(input_prompt))

            # Range check
            if user_input < lower_limit or user_input > upper_limit:
                print(check_prompt)
                continue

            return user_input

        except ValueError:
            # For invalid float entries
            print(error_prompt)


def user_input_character(input_prompt):
    '''
    Handles string input where:
    - Blank inputs are rejected
    - User must confirm the entered value
    - Ensures non-empty, user-approved text input

    Returns:
        A validated, confirmed string.
    '''
    while True:
        # Remove surrounding spaces; ensure non-blank
        user_input = input(input_prompt).strip()

        if user_input == "":
            print("Wrong Input. Blank space is not allowed.")
            continue

        # Confirmation loop
        while True:
            confirm = input(f"You entered '{user_input}'. Proceed? [Y]/n: ").strip().lower()

            # Accept input on Enter or 'y'
            if confirm == "" or confirm == "y":
                print("\n")
                return user_input

            # Restart input if 'n'
            elif confirm == "n":
                print("Okay, let's try again.\n")
                break

            # Handle invalid confirmation inputs
            else:
                print("Invalid choice. Please type 'Y' or 'n'.")

