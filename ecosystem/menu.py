from .utils import user_input_int, user_input_float, user_input_character
from .classes import Species, Ecosystem, AVAILABLE_SPECIES

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


def create_new_ecosystem():

    user_input = user_input_int(
        input_prompt="Please enter starting resources for the ecosystem: ", 
        check_prompt="Resources cannot be less than 0 !",
        error_prompt="Wrong input. Please enter an integer greate than 0.", 
        lower_limit=1
    )
    eco = Ecosystem(user_input)
    print(f"New ecosystem with starting resources {eco.resources} created!")
    return eco


def print_ecosystem_info(ecosytem):

    if ecosytem == None:
        print("No ecosystem exists yet! Create one first.")
        return
    
    if ecosytem.species_list == []:
        print(f"Ecosystem has {ecosytem.resources} but no Species live here yet !")
        return
    
    print(ecosytem)


def add_new_species(ecosystem):

    if ecosystem == None:
        print("No ecosystem exists yet! Create one first.")
        return

    user_input_name = user_input_character("Please Enter genus Name: ")

    user_input_population = user_input_int(
        input_prompt=f"Please Enter {user_input_name}'s Population: ",
        check_prompt="Population cannot be negative!",
        error_prompt="Invalid input. Please enter an integer greater than 0.",
        lower_limit=1
    )

    user_input_growth_rate = user_input_float(
        input_prompt=f"Please Enter {user_input_name}'s Growth rate: ",
        check_prompt="Growth rate cannot be negative!",
        error_prompt="Invalid input. Please enter a real number greater than 0.",
        lower_limit=1e-16
    )

    user_input_mutation_rate = user_input_float(
        input_prompt=f"Please Enter {user_input_name}'s mutation rate (0-1): ",
        check_prompt="Mutation rate must be between 0 and 1!",
        error_prompt="Invalid input. Please enter a number between 0 and 1.",
        lower_limit=0,
        upper_limit=1
    )

    genus = Species(user_input_name, user_input_population, user_input_growth_rate, user_input_mutation_rate)
    ecosystem.add_species(genus)


def search_species(ecosystem):

    if ecosystem == None:
        print("No ecosystem exists yet! Create one first.")
        return

    user_input = user_input_character("Please enter genus' name you wish to search: ").strip()

    for genus in ecosystem.species_list:
        if user_input.lower() == genus.name.lower():
            ecosystem.search_species(genus)
            return
        

    print(f"{user_input} does not live in the ecosystem")


def update_species(ecosystem):

    if ecosystem == None:
        print("No ecosystem exists yet! Create one first.")
        return
    
    list_len = len(ecosystem.species_list)
    
    counter = 1
    for genus in ecosystem.species_list:
        print(f"{counter}. {genus.name}")
        counter += 1
    
    user_input = user_input_int(
        input_prompt = f"Please enter the number (from 1 to {list_len}) of the genus you wish to remove: ",
        check_prompt = f"Please choose an integer from 1 to {list_len}",
        error_prompt = f"Wrong Input. Please choose an integer from 1 to {list_len}",
        lower_limit = 1,
        upper_limit = list_len
    )

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

    print(f"{chosen_genus} new features are: \n")
    print(ecosystem.species_list[user_input].display_info())
    


def remove_species(ecosystem):

    if ecosystem == None:
        print("No ecosystem exists yet! Create one first.")
        return

    list_len = len(ecosystem.species_list)
    
    counter = 1
    for genus in ecosystem.species_list:
        print(f"{counter}. {genus.name}")
        counter += 1

    user_input = user_input_int(
        input_prompt = f"Please enter the number (from 1 to {list_len}) of the genus you wish to remove: ",
        check_prompt = f"Please choose an integer from 1 to {list_len}",
        error_prompt = f"Wrong Input. Please choose an integer from 1 to {list_len}",
        lower_limit = 1,
        upper_limit = list_len
    )

    user_input = user_input - 1 # python's indexing

    ecosystem.remove_species(ecosystem.species_list[user_input])


def show_all_species(ecosystem):

    if ecosystem == None:
        print("No ecosystem exists yet! Create one first.")
        return
    
    for genus in ecosystem.species_list:
        print("----------------------")
        print("----------------------")
        print(genus.display_info())
        print("----------------------")
        print("----------------------")


def update_resourses(ecosystem):
    
    if ecosystem == None:
        print("No ecosystem exists yet! Create one first.")
        return
    
    user_input = user_input_int(
        input_prompt="Please enter the UPDATING resources for the ecosystem: ", 
        check_prompt="Resources cannot be less than 0 !",
        error_prompt="Wrong input. Please enter an integer greate than 0.", 
        lower_limit=1
    )
    
    ecosystem.resourses = user_input
    print(f"Ecosystem's resourses successfully updated to {user_input}")

