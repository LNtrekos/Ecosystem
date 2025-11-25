"""
This File contains the classes used for the project.
"""

import random
import pandas as pd 

class Species:
    def __init__(self, name, population, growth_rate, mutation_rate):
        
        if not isinstance(name, str) or name.strip() == "":
            raise ValueError("Species name must be a non-empty string.")

        if population <= 0:
            raise ValueError("Population must be > 0.")

        if growth_rate <= 0:
            raise ValueError("Growth rate must be > 0.")

        if not (0 <= mutation_rate <= 1):
            raise ValueError("Mutation rate must be between 0 and 1.")

        self.name = name
        self.population = population
        self.growth_rate = growth_rate
        self.mutation_rate = mutation_rate
    
    def reproduce(self, food_availability):
        current_growth_rate = (
            self.growth_rate if food_availability == 1 else 0.5 * self.growth_rate
        )

        self.population += int(current_growth_rate * self.population)
        return self.population

    def mutate(self):
        if random.random() <= self.mutation_rate:
            multiplier = random.choice([1.1, 0.7])
            self.growth_rate *= multiplier
            print(f"{self.name} mutated! New growth rate: {self.growth_rate:.2f}")
        else:
            print(f"{self.name} did not mutate.")

        return self.growth_rate

    def __str__(self):
        return self.name

    def display_info(self):
        return (
            f"Species Name: {self.name}\n"
            f"Population: {self.population}\n"
            f"Growth rate: {self.growth_rate}\n"
            f"Mutation rate: {self.mutation_rate}"
        )
    
    
class Ecosystem:

    def __init__(self, resources, growth_rate, species_list=None):
        
        if resources < 0:
            raise ValueError("Resources must be >= 0")
        
        if growth_rate < 0:
            raise ValueError("Growth Rate must be >= 0")

        self.resources = resources
        self.growth_rate = growth_rate
        self.species_list = species_list if species_list is not None else []


    def __str__(self):
        
        existing_names = [s.name for s in self.species_list]
        return f"Resources: {self.resources}\n Growth_rate : {self.growth_rate} \nSpecies: {existing_names}"

    # Function to add new species to the ecosystem:
    def add_species(self, species: Species):

        for genus in self.species_list:
            if genus.name == species.name:
                print(f"{species.name} already exists in the ecosystem.\n")
                return
            
        self.species_list.append(species)
        print(f"{species.name} added to the Ecosystem")

    # Function to Search inside the ecosystem for species:
    def search_species(self, genus_name):
        
        for species in self.species_list:
            if species.name == genus_name:
                print(f"{species.name} exists in the Ecosystem:\n")
                print(species.display_info())
                return 
            
        print(f"Sorry but {genus_name} doesn't currently live in the Ecosystem.")
    
    # Display all Information:
    def display(self):

        if not self.species_list:
            print("No Species currently live in the Ecosystem")
        
        population_list = [] ; growth_list = [] ; mutation_list = []
        for genus in self.species_list:
            population_list.append(genus.population)
            growth_list.append(genus.growth_rate)
            mutation_list.append(genus.mutation_rate)

        info_df = pd.DataFrame({
            "Species Name": self.species_list,
            "Population" : population_list, 
            "Growth Rate": growth_list, 
            "Mutation Rate" : mutation_list
        })

        print(info_df)
        return(info_df)

        

    # Update Ecosystem's resources
    def update_resources(self, num_recourses):

        new_resources = self.resources + num_recourses
        
        if new_resources < 0:
            raise ValueError("Resources cannot become negative!")

        self.resources = new_resources
        print(f"Resources updated to {self.resources}")


    def remove_species(self, genus):
        for species in self.species_list:
            if species.name == genus.name:
                self.species_list.remove(species)
                print(f"{genus.name} successfully removed from the Ecosystem!")
                return
        
        print(f"Sorry but {genus.name} doesn't currently live in the Ecosystem")


    def run_generation(self):

        if not self.species_list:
            print("No species currently in the ecosystem. Nothing to simulate.")
            return
        
        print("\n--- Running Generation ---")

        total_population_current = sum(genus.population for genus in self.species_list)

        # food availability accounts for the half amount 
        food_availability = 1 if (self.resources/2) >= total_population_current else 0 

        for species in self.species_list:
            species.reproduce(food_availability)
            species.mutate()

        total_population = sum(genus.population for genus in self.species_list)

        # The idea is to have self.growth_rate depend on number of species and the actual resources:
        resources_add = int(self.resources * (self.growth_rate * len(self.species_list)))
        
        self.resources -= total_population
        self.resources += resources_add

        if self.resources < 0:
            self.resources = 0

        print(f"\nFood availability = {food_availability}")
        print(f"Total population before = {total_population_current}")
        print(f"Total population after reproduction = {total_population}")
        print(f"Resources added = {resources_add}")
        print(f"Remaining resources = {self.resources}")
        

AVAILABLE_SPECIES = [
    Species("Lion", 30, 1.2, 0.3),
    Species("Zebra", 50, 1.5, 0.1),
    Species("Elephant", 15, 0.8, 0.2),
    Species("Wolf", 25, 1.4, 0.4),
    Species("Giraffe", 20, 1.0, 0.1)
]

