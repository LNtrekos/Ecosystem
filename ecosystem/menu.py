"""
This file contains the functions that connect user input with the
Ecosystem and Species classes.

It provides:
- Main menu interface
- Input-driven creation and modification of ecosystems and species
- Simulation controls (automated and interactive)
- Utility functions for listing and displaying ecosystem status
"""


from .utils import user_input_int, user_input_float, user_input_character
from .classes import Species, Ecosystem, AVAILABLE_SPECIES
import copy

def menu():
    """
    Display the main menu and return the user's selection.
    Valid options: 1–10
    """
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

# ==============================================================
#                     CREATE NEW ECOSYSTEM
# ==============================================================

def create_new_ecosystem():
    """
    Prompt the user for resources and growth rate,
    create a new ecosystem, and return it.
    """
    # Resources input
    user_input_resources = user_input_int(
        input_prompt="\nPlease enter starting resources for the ecosystem: ", 
        check_prompt="Resources have to be at least 1.",
        error_prompt="Wrong input. Please enter an integer greater or equal to 1.", 
        lower_limit=1
    ) # Resources have to be interger and at least 1.

    # Growth rate input
    user_input_growth_rate = user_input_float(
            input_prompt=f"Please Enter Ecosystem's Growth rate: ",
            check_prompt="Growth must be at least one!",
            error_prompt="Invalid input. Please enter a real number greater than 0.",
            lower_limit=1e-16
        )

    # Create ecosystem instance
    eco = Ecosystem(resources=user_input_resources, growth_rate=user_input_growth_rate)
    print("\n               --- POOF ----      \n")
    print("       ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("               NEW ECOSYSTEM         ")
    print("       ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print(f"\nNew ecosystem with starting resources {eco.resources} and {eco.growth_rate} growth rate created!\n")
    return eco

# ==============================================================
#                     PRINT ECOSYSTEM INFO
# ==============================================================

def print_ecosystem_info(ecosytem):
    """
    Print a readable summary of the ecosystem.
    Handles cases where the ecosystem doesn't exist or has no species.
    """
    print("\n")
    if ecosytem == None:
        print("No ecosystem exists yet! Create one first.")
        return
    
    if ecosytem.species_list == []:
        print(f"Ecosystem has {ecosytem.resources} resources and {ecosytem.growth_rate} growth rate but no Species exist yet!")
        return
    
    print(ecosytem)

# ==============================================================
#                     ADD NEW SPECIES
# ==============================================================

def add_new_species(ecosystem):
    """
    Allow the user to create a new Species object and add it to the ecosystem.
    Ensures:
    - Valid name
    - Name not already in ecosystem
    - Valid population, growth rate, mutation rate
    """
    if ecosystem == None:
        print("No ecosystem exists yet! Create one first.")
        return

    while True:

        # Ask user for species name
        user_input_name = user_input_character("\nPlease enter genus' name (first letter capital is preffered) or type 'exit' to return: ")

        # Check for exit
        if user_input_name == "" or user_input_name.lower() == "exit":
            print("Returning to main menu")
            return
        
        # Check if name already exists
        existing_names = [genus.name.lower() for genus in ecosystem.species_list]
        if user_input_name.lower() in existing_names:
            print(f"{user_input_name} already exists in the ecosystem. Please choose a different name.\n")
            continue

        # Ask for species attributes
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

        # Create species and add to ecosystem
        genus = Species(user_input_name, user_input_population, user_input_growth_rate, user_input_mutation_rate)
        ecosystem.add_species(genus)
        
# ==============================================================
#                     SEARCH SPECIES
# ==============================================================

def search_species(ecosystem):
    """
    Search for a species by name within the ecosystem and display info.
    """
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

# ==============================================================
#                     UPDATE SPECIES ATTRIBUTES
# ==============================================================

def update_species(ecosystem):
    """
    Allow the user to select a species and update its attributes:
    - Population
    - Growth rate
    - Mutation rate
    """
    if ecosystem == None:
        print("No ecosystem exists yet! Create one first.")
        return
    
    list_len = len(ecosystem.species_list)
    
    while True:

        print("\n-----------------------------")
        print("        Species List         ")
        print("-----------------------------\n")

        # Display species list
        counter = 1
        for genus in ecosystem.species_list:
            print(f"{counter}. {genus.name}")
            counter += 1
        print(f"{counter}. Exit\n")
        
        # User selects species to update
        user_input = user_input_int(
        input_prompt = f"Please enter the number (from 1 to {list_len}) of the genus you wish to update: (or {list_len + 1 } to exit): ",
        check_prompt = f"Please choose an integer from 1 to {list_len + 1}",
        error_prompt = f"Wrong Input. Please choose an integer from 1 to {list_len + 1}",
        lower_limit = 1, upper_limit = list_len + 1
        )

        # Handle exit
        if user_input == (list_len + 1):
            print("Returning to main menu.")
            return

        # Convert to index
        user_input = user_input - 1 # python's indexing
        chosen_genus = ecosystem.species_list[user_input]

        # Update attributes
        new_population = user_input_int(
            input_prompt=f"Please Enter {chosen_genus}'s new Population: ",
            check_prompt="Population cannot be negative!",
            error_prompt="Invalid input. Please enter an integer greater than 0.",
            lower_limit=1
        )
        chosen_genus.population = new_population

        new_growth = user_input_float(
            input_prompt=f"Please Enter {chosen_genus}'s new Growth rate: ",
            check_prompt="Growth rate cannot be negative!",
            error_prompt="Invalid input. Please enter a real number greater than 0.",
            lower_limit=1e-16
        )
        chosen_genus.growth_rate = new_growth

        new_mutation = user_input_float(
            input_prompt=f"Please Enter {chosen_genus}'s new mutation rate (0-1): ",
            check_prompt="Mutation rate must be between 0 and 1!",
            error_prompt="Invalid input. Please enter a number between 0 and 1.",
            lower_limit=0, upper_limit=1
        )
        chosen_genus.mutation_rate = new_mutation

        print("\nUpdated species information:\n")
        print(chosen_genus.display_info() + "\n")
        
# ==============================================================
#                     REMOVE SPECIES
# ==============================================================

def remove_species(ecosystem):
    """
    Allow the user to remove a species from the ecosystem by selecting it
    from a numbered list.
    """
    if ecosystem == None:
        print("No ecosystem exists yet! Create one first.")
        return
    
    while True:

        list_len = len(ecosystem.species_list)

        print("\n-----------------------------")
        print("        Species List         ")
        print("-----------------------------\n")

        # Display species
        for i, genus in enumerate(ecosystem.species_list, start=1):
            print(f"{i}. {genus.name}")
        print(f"{list_len + 1}. Exit\n")

        # Select species to remove
        user_input = user_input_int(
            input_prompt = f"Please enter the number (from 1 to {list_len}) of the genus you wish to remove (or {list_len + 1} to exit): ",
            check_prompt = f"Please choose an integer from 1 to {list_len + 1}",
            error_prompt = f"Wrong Input. Please choose an integer from 1 to {list_len + 1}",
            lower_limit = 1, upper_limit = list_len + 1
        )

        if user_input == (list_len + 1):
            print("Returning to main menu:")
            return

        species_to_remove = ecosystem.species_list[user_input - 1]
        ecosystem.remove_species(species_to_remove)


# ==============================================================
#                     DISPLAY ALL SPECIES
# ==============================================================

def show_all_species(ecosystem):
    """
    Display detailed information for all species in the ecosystem.
    """
    if ecosystem == None:
        print("\nNo ecosystem exists yet! Create one first.")
        return
    
    print("\nCurrent State for each Genus that leaves in the Ecosystem: ")
    ecosystem.display()

# ==============================================================
#                     UPDATE RESOURCES
# ==============================================================

def update_resources(ecosystem):
    """
    Allow the user to add or remove resources from the ecosystem.
    """ 
    print("\n")
    if ecosystem == None:
        print("No ecosystem exists yet! Create one first.")
        return
    
    print("1. Add resourses")
    print("2. Remove resourses")
    print("3. Update Ecosystem's growth rate ")
    print("\n")
    
    # Choose add or remove
    user_input_choice = user_input_int(
        input_prompt="Please choose one of the above (Enter 1, 2 or 3): ",
        check_prompt="Out of range. Please enter one of the options above.",
        error_prompt="Wrong Input. Please enter one of the options above.",
        lower_limit=1, upper_limit=3
    )

    if user_input_choice == 3:

        new_growth_rate = user_input_float(
            input_prompt="Enter new growth rate: ",
            check_prompt="Growth Rate must be positive.",
            error_prompt="Invalid input. Please enter a positive real number.",
            lower_limit=0
        )

        ecosystem.update_growth_rate(new_growth_rate)
        return
    
    # Ask for amount
    amount = user_input_int(
        input_prompt="Enter the amount: ",
        check_prompt="Resources must be positive or 0.",
        error_prompt="Invalid input. Please enter a positive integer or 0.",
        lower_limit=0
    )

    # Convert to positive/negative
    if user_input_choice == 2:
        amount = -amount

    ecosystem.update_resources(amount)
    print(f"\nEcosystem's resources successfully updated to {ecosystem.resources}!")


# ==============================================================
#                     SIMULATE GENERATIONS
# ==============================================================

def simulate_generations(ecosystem, generations = 10, count = 1):
    """
    Automatically simulate a fixed number of generations without
    user interaction. Uses recursion to track generation count.
    """
    ecosystem.run_generation()

    # Stop if ecosystem collapses
    if ecosystem.resources <= 0:
        print(f"\nEcosystem run out of Resources after {count} Generations with Current State: ")
        show_all_species(ecosystem)
        return ecosystem
    
    # Last generation → print summary
    elif generations <= 1:
        print(f"\nAfter {count} Generations :")
        print_ecosystem_info(ecosystem)
        print("\nMore detailed: ")
        show_all_species(ecosystem)
        return ecosystem
    
    # Recursive call
    else:
        simulate_generations(ecosystem, generations - 1, count = count + 1)

# ==============================================================
#                     SIMULATE WITH USER INTERACTION
# ==============================================================

def simulate_generations_with_interaction(ecosystem, generations = 10, count = 1):
    """
    Interactive simulation where the user confirms each generation.
    """
    # Ask user whether to proceed
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
            simulate_generations_with_interaction(ecosystem, generations - 1, count + 1)
           

    elif user_input == "n":

        print(f"\nStopped at {count} Generations: ")
        print_ecosystem_info(ecosystem)
        print("\nMore detailed: ")
        show_all_species(ecosystem)
        return ecosystem
    
    else:
        print("Invalid choice. Please type 'Y' or 'n'.")
        return simulate_generations_with_interaction(ecosystem, generations, count)

# ==============================================================
#                 SIMULATION MODE WRAPPER
# ==============================================================

def simulate_generations_wrapper(ecosystem):
    """
    Wrapper function providing:
    - Permanent or safe simulation mode
    - Automated or interactive simulation options
    - Returns the simulated ecosystem (copy or original)
    """
    if ecosystem is None:
        print("\nNo ecosystem exists yet! Create one first.")
        return None
    
    print("\nSimulation Mode:")
    print("1. Permanent simulation (affects real ecosystem)")
    print("2. Safe test simulation (works on a copy)")
    
    mode = user_input_int(
        input_prompt="Choose mode (1 or 2): ",
        check_prompt="Please enter 1 or 2.",
        error_prompt="Invalid input.",
        lower_limit=1, upper_limit=2
    )

    # Determine ecosystem to simulate
    if mode == 1:
        sim_ecosystem = ecosystem
        print("\n→ Running simulation on the REAL ecosystem.\n")

    else:
        sim_ecosystem = copy.deepcopy(ecosystem)
        print("\n→ Running simulation on a COPY (original stays unchanged).\n")

    # Simulation loop
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
            return sim_ecosystem   # ← return what was simulated

        print("\n")
        generations = user_input_int(
            input_prompt="How many generations would you like to simulate? ",
            check_prompt="Number of generations must be at least 1.",
            error_prompt="Invalid Input. Please enter an integer ≥ 1.", 
            lower_limit=1
        )

        # Run selected simulation type
        if user_choice == 1:
            sim_ecosystem = simulate_generations(sim_ecosystem, generations)

        elif user_choice == 2:
            sim_ecosystem = simulate_generations_with_interaction(sim_ecosystem, generations)

    


    