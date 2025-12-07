from ecosystem.menu import (
    menu, create_new_ecosystem, print_ecosystem_info,
    add_new_species, search_species, update_species, remove_species, show_all_species,
    update_resources, simulate_generations_wrapper
)
from ecosystem.classes import Ecosystem, AVAILABLE_SPECIES

print("\nWelcome to Ecosystem: \n")
eco = Ecosystem(10**3, 0.2)
for genus in AVAILABLE_SPECIES:
    eco.add_species(genus)

while True:
    choice = menu()

    if choice == 1:
        eco = create_new_ecosystem()
    
    elif choice == 2:
        print_ecosystem_info(eco)

    elif choice == 3:
        add_new_species(eco)
    
    elif choice == 4:
        search_species(eco)
            
    elif choice == 5:
        update_species(eco)

    elif choice == 6:
        remove_species(eco)
        
    elif choice == 7:
        show_all_species(eco)

    elif choice == 8:
        update_resources(eco)

    elif choice == 9:
        simulate_generations_wrapper(eco)
        
    elif choice == 10:
        print("Exiting...")
        break