'''
This files contains the helper functions for Input:
- Integer Input
- Float Input
- Charachter Input
Throughout this project, almost constanty was needed input from the user. The functions help maintain a nice flow
with proper error handling. 
'''

def user_input_int(input_prompt, check_prompt , error_prompt, lower_limit=-float('inf'), upper_limit=float('inf')):
    while True:
        try:
            user_input = int(input(input_prompt))

            if user_input < lower_limit or user_input > upper_limit:
                print(check_prompt)
                continue

            return user_input

        except ValueError:
            print(error_prompt)


def user_input_float(input_prompt, check_prompt , error_prompt, lower_limit=-float('inf'), upper_limit=float('inf')):
    while True:
        try:
            user_input = float(input(input_prompt))

            if user_input < lower_limit or user_input > upper_limit :
                print(check_prompt)
                continue

            return user_input

        except ValueError:
            print(error_prompt)


def user_input_character(input_prompt):

    while True:
        user_input = input(input_prompt).strip()

        if user_input == "":
            print("Wrong Input. Blank space is not allowed.")
            continue

        while True:
            confirm = input(f"You entered '{user_input}'. Proceed? [Y]/n: ").strip().lower()

            if confirm == "" or confirm == "y":
                print("\n")
                return user_input
            

            elif confirm == "n":
                print("Okay, let's try again.\n")
                break  

            else:
                print("Invalid choice. Please type 'Y' or 'n'.")
        

