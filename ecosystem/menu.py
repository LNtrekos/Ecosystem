"""
This files contains the functions that connect the user's Input with 
the Ecosystem/Species Classes.
"""


from .utils import user_input_int, user_input_float, user_input_character
from .classes import Species, Ecosystem, AVAILABLE_SPECIES
import copy

def menu():
    print("""
=========================
           MENU
=========================
1. Create new Ecosystem
2. Print Ecosystem Information
3. Add New Genus
4. Search Genus
5. Update Genus
6. Remove Genus
7. Show All Species
8. Update Resources
9. Simulate Generations
10. Exit
""")

    user_input = user_input_int(
                input_prompt="Please choose an option (1–10): ",
                check_prompt="Choice out of range. Please choose a number between 1 and 10.",
                error_prompt="Invalid input. Please enter a number between 1 and 10.",
                lower_limit=1, upper_limit=10    
            )
    
    return user_input

# New ecosystem function: 
def create_new_ecosystem():

    user_input_resources = user_input_int(
        input_prompt="\nPlease enter starting resources for the ecosystem: ", 
        check_prompt="Resources have to be at least 1.",
        error_prompt="Wrong input. Please enter an integer greater or equal to 1.", 
        lower_limit=1
    ) # Resources have to be interger and at least 1.

    user_input_growth_rate = user_input_float(
            input_prompt=f"Please Enter Ecosystem's Growth rate: ",
            check_prompt="Growth must be at least one!",
            error_prompt="Invalid input. Please enter a real number greater than 0.",
            lower_limit=1e-16
        )

    print("\n")
    eco = Ecosystem(resources=user_input_resources, growth_rate=user_input_growth_rate)
    print("\n               --- POOF ----      \n")
    print("       ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("               NEW ECOSYSTEM         ")
    print("       ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print(f"\nNew ecosystem with starting resources {eco.resources} and {eco.growth_rate} growth rate created!\n")
    return eco

# Print some basic info 
def print_ecosystem_info(ecosytem):

    print("\n")
    if ecosytem == None:
        print("No ecosystem exists yet! Create one first.")
        return
    
    if ecosytem.species_list == []:
        print(f"Ecosystem has {ecosytem.resources} resources and {ecosytem.growth_rate} growth rate but no Species exist yet!")
        return
    
    print(ecosytem)

# Function to add new Species (that the user creates) to the ecosystem:
def add_new_species(ecosystem):

    if ecosystem == None:
        print("No ecosystem exists yet! Create one first.")
        return

    while True:

        # The sequence of inputs, basically creates instance of class Species:
        user_input_name = user_input_character("\nPlease enter genus' name (first letter capital is preffered) or type 'exit' to return: ")

        # Check if name already exists
        existing_names = [genus.name.lower() for genus in ecosystem.species_list]

        if user_input_name.lower() in existing_names:
            print(f"{user_input_name} already exists in the ecosystem. Please choose a different name.\n")
            continue

        if user_input_name == "" or user_input_name.lower() == "exit":
            print("Returning to main menu")
            return

        user_input_population = user_input_int(
            input_prompt=f"Please Enter {user_input_name}'s Population: ",
            check_prompt="Population must be at least 1!",
            error_prompt="Invalid input. Please enter an integer greater than 0.",
            lower_limit=1
            )

        user_input_growth_rate = user_input_float(
            input_prompt=f"Please Enter {user_input_name}'s Growth rate: ",
            check_prompt="Growth must be at least one!",
            error_prompt="Invalid input. Please enter a real number greater than 0.",
            lower_limit=1e-16
        )

        user_input_mutation_rate = user_input_float(
            input_prompt=f"Please Enter {user_input_name}'s mutation rate (0-1): ",
            check_prompt="Mutation rate must be between 0 and 1!",
            error_prompt="Invalid input. Please enter a number between 0 and 1.",
            lower_limit=0, upper_limit=1
        )

        genus = Species(user_input_name, user_input_population, user_input_growth_rate, user_input_mutation_rate)
        ecosystem.add_species(genus)
        

# Search Species function:
def search_species(ecosystem):

    if ecosystem == None:
        print("No ecosystem exists yet! Create one first.")
        return

    while True:
        print("\n")
        user_input = user_input_character("Please enter genus' name you wish to search (or type 'exit' to stop): ")

        if user_input.lower() == "exit":
            print("Returning to main menu.")
            return
        
        ecosystem.search_species(user_input)



# Function for Updating the Selected Species:
def update_species(ecosystem):
    
    if ecosystem == None:
        print("No ecosystem exists yet! Create one first.")
        return
    
    list_len = len(ecosystem.species_list)
    
    while True:

        print("\n-----------------------------")
        print("        Species List         ")
        print("-----------------------------\n")

        counter = 1
        for genus in ecosystem.species_list:
            print(f"{counter}. {genus.name}")
            counter += 1
        print(f"{counter}. Exit\n")
        

        user_input = user_input_int(
        input_prompt = f"Please enter the number (from 1 to {list_len}) of the genus you wish to remove: (or {list_len + 1 } to exit): ",
        check_prompt = f"Please choose an integer from 1 to {list_len + 1}",
        error_prompt = f"Wrong Input. Please choose an integer from 1 to {list_len + 1}",
        lower_limit = 1, upper_limit = list_len + 1
        )
        print("\n")

        if user_input == (list_len + 1):
            print("Returning to main menu.")
            return

        user_input = user_input - 1 # python's indexing
        chosen_genus = ecosystem.species_list[user_input]

        user_input_population = user_input_int(
            input_prompt=f"Please Enter {chosen_genus}'s Population: ",
            check_prompt="Population cannot be negative!",
            error_prompt="Invalid input. Please enter an integer greater than 0.",
            lower_limit=1
        )
        ecosystem.species_list[user_input].population = user_input_population

        user_input_growth_rate = user_input_float(
            input_prompt=f"Please Enter {chosen_genus}'s Growth rate: ",
            check_prompt="Growth rate cannot be negative!",
            error_prompt="Invalid input. Please enter a real number greater than 0.",
            lower_limit=1e-16
        )
        ecosystem.species_list[user_input].growth_rate = user_input_growth_rate

        user_input_mutation_rate = user_input_float(
            input_prompt=f"Please Enter {chosen_genus}'s mutation rate (0-1): ",
            check_prompt="Mutation rate must be between 0 and 1!",
            error_prompt="Invalid input. Please enter a number between 0 and 1.",
            lower_limit=0,
            upper_limit=1
        )
        ecosystem.species_list[user_input].mutation_rate = user_input_mutation_rate

        print("\n" + f"{chosen_genus}'s new features are:\n")
        print(ecosystem.species_list[user_input].display_info() + "\n")
        
    

# Function to remove Selected Species:
def remove_species(ecosystem):

    if ecosystem == None:
        print("No ecosystem exists yet! Create one first.")
        return
    
    while True:

        list_len = len(ecosystem.species_list)

        print("\n-----------------------------")
        print("        Species List         ")
        print("-----------------------------\n")

        counter = 1
        for genus in ecosystem.species_list:
            print(f"{counter}. {genus.name}")
            counter += 1
        print(f"{counter}. Exit\n")

        user_input = user_input_int(
            input_prompt = f"Please enter the number (from 1 to {list_len}) of the genus you wish to remove (or {list_len + 1} to exit): ",
            check_prompt = f"Please choose an integer from 1 to {list_len + 1}",
            error_prompt = f"Wrong Input. Please choose an integer from 1 to {list_len + 1}",
            lower_limit = 1, upper_limit = list_len + 1
        )

        if user_input == (list_len + 1):
            print("Returning to main menu:")
            return

        user_input = user_input - 1 # python's indexing

        print("\n")
        ecosystem.remove_species(ecosystem.species_list[user_input])


# Function to display all details about the
def show_all_species(ecosystem):

    if ecosystem == None:
        print("\nNo ecosystem exists yet! Create one first.")
        return
    
    print("\nCurrent State for each Genus that leaves in the Ecosystem: ")
    ecosystem.display()


# Function to update resources:
def update_resourses(ecosystem):

    print("\n")
    if ecosystem == None:
        print("No ecosystem exists yet! Create one first.")
        return
    
    print("1. Add recources")
    print("2. Remove recourses")
    print("\n")
    
    user_input_choice = user_input_int(
        input_prompt="Please choose one of the above (Enter 1 or 2): ",
        check_prompt="Out of range. Please enter 1(Add) or 2(Remove)",
        error_prompt="Wrong Input. Please enter an integer (1 or 2)",
        lower_limit=1, upper_limit=2
    ) 
    
    # 1 for addtition, 2 for subtraction 
    if user_input_choice == 1:

        user_input = user_input_int(
        input_prompt="Please enter the resources to ADD for the ecosystem: ", 
        check_prompt="Resources cannot be less than 0 !",
        error_prompt="Wrong input. Please enter an integer greate than 0.", 
        lower_limit=1
        )
    else:
        user_input = user_input_int(
        input_prompt="Please enter the resources to REMOVE from the ecosystem: ", 
        check_prompt="Resources cannot be less than 0 !",
        error_prompt="Wrong input. Please enter an integer greate than 0.", 
        lower_limit=1
        )

        user_input = - user_input

    
    ecosystem.update_resources(user_input)
    print("\n")
    print(f"Ecosystem's resourses successfully updated to {ecosystem.resources}!")

def simulate_generations(ecosystem, generations = 10, count = 1):
    
    ecosystem.run_generation()

    if ecosystem.resources <= 0:
        print(f"\nEcosystem run out of Resources after {count} Generations with Current State: ")
        show_all_species(ecosystem)
        return ecosystem
    
    elif generations <= 1:
        print(f"\nAfter {count} Generations :")
        print_ecosystem_info(ecosystem)
        print("\nMore detailed: ")
        show_all_species(ecosystem)
        return ecosystem
    
    else:
        simulate_generations(ecosystem, generations - 1, count = count + 1)

def simulate_generations_with_interaction(ecosystem, generations = 10, count = 1):
    
    user_input = input(f"\nCurrent Generation: {count}. Proceed? [Y]/n: ").strip().lower()
    
    if user_input == "" or user_input == "y":
        
        ecosystem.run_generation()

        if ecosystem.resources <= 0:
            print(f"\nEcosystem run out of Resources after {count} Generations with Current State: ")
            return ecosystem
    
        elif generations <= 1:
            print(f"\nAfter {count} Generations:")
            print_ecosystem_info(ecosystem)
            print("\nMore detailed: ")
            show_all_species(ecosystem)
            return ecosystem

        else:
            simulate_generations_with_interaction(ecosystem, generations - 1, count)
           

    elif user_input == "n":

        print(f"\nStopped at {count} Generations: ")
        print_ecosystem_info(ecosystem)
        print("\nMore detailed: ")
        show_all_species(ecosystem)
        return ecosystem
    
    else:
        print("Invalid choice. Please type 'Y' or 'n'.")
        return simulate_generations_with_interaction(ecosystem, generations, count)


def simulate_generations_wrapper(ecosystem):

    if ecosystem == None:
        print("\nNo ecosystem exists yet! Create one first.")
        return
    
    copy_ecosytem = copy.deepcopy(ecosystem)

    while True:
        print("\n---- Simulation ----")
        print("1. Simulate")
        print("2. Simulate with Interactions")
        print("3. Exit\n")

        user_choice = user_input_int(
            input_prompt="Please enter one of the options above: ",
            check_prompt="Choice out of range. Please choose 1, 2 or 3.",
            error_prompt="Invalid Input. Please choose 1, 2 or 3.", 
            lower_limit=1, upper_limit=3
        )

        if user_choice == 3:
            print("Returning to main menu")
            return

        print("\n")
        user_input = user_input_int(
            input_prompt="Please choose how many generations would you like to simulate: ",
            check_prompt="Choice out of range. Number of generation must be at least 1.",
            error_prompt="Invalid Input. Please enter an integer greater or equal to 1.", 
            lower_limit=1
        )

        if user_choice == 1:
            simulate_generations(copy_ecosytem, user_input)

        elif user_choice == 2:
            simulate_generations_with_interaction(copy_ecosytem, user_input)


    


    