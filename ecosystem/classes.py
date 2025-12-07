"""
classes.py

This file contains the classes used for the Ecosystem project:

- Species class:
    Represents a living genus with population dynamics,
    mutation behavior, and growth characteristics.

- Ecosystem class:
    Manages resources and a collection of species, simulates
    generations, reproduction, mutation, and ecosystem-level updates.

The classes provide the core structure and logic used throughout the project.
"""

import random
import pandas as pd 

class Species:

    """
    Represents an individual species in the ecosystem.

    Parameters:
        name          : Species name (non-empty string).
        population    : Initial population (> 0).
        growth_rate   : Growth rate (> 0).
        mutation_rate : Probability of mutation (0 <= rate <= 1).

    Methods:
        reproduce(food_availability)
        mutate()
        display_info()
        __str__()
    """
    
    def __init__(self, name, population, growth_rate, mutation_rate):

        # Basic validation
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
        """
        Reproduce the species based on food availability.
        If food is limited, reproduction growth rate is halved.

        Parameters:
            food_availability : 1 for enough food, 0 for shortage.

        Returns:
            Updated population.
        """
        current_growth_rate = (
            self.growth_rate if food_availability == 1 else 0.5 * self.growth_rate
        )

        self.population += int(current_growth_rate * self.population)
        return self.population

    def mutate(self):
        """
        Stochastic mutation:
        - With probability 'mutation_rate', growth rate is multiplied by 1.1 or 0.7.
        - Otherwise, no mutation occurs.

        Returns:
            Updated growth rate.
        """
        if random.random() <= self.mutation_rate:
            multiplier = random.choice([1.1, 0.7])
            self.growth_rate *= multiplier
            print(f"{self.name} mutated! New growth rate: {self.growth_rate:.2f}")
        else:
            print(f"{self.name} did not mutate.")

        return self.growth_rate

    def __str__(self):
        """String representation: returns species name."""
        return self.name

    def display_info(self):
        """Return formatted information string for the species."""
        return (
            f"Species Name: {self.name}\n"
            f"Population: {self.population}\n"
            f"Growth rate: {self.growth_rate}\n"
            f"Mutation rate: {self.mutation_rate}"
        )
    
    
class Ecosystem:
    """
    Represents the ecosystem environment containing multiple species.

    Parameters:
        resources     : Initial total resources (>= 0).
        growth_rate   : Resource regeneration factor (>= 0).
        species_list  : Optional initial list of Species objects.

    Methods:
        add_species(species)
        search_species(name)
        display()
        update_resources(amount)
        remove_species(species)
        run_generation()
        __str__()
    """

    def __init__(self, resources, growth_rate, species_list=None):
        
        # Validation
        if resources < 0:
            raise ValueError("Resources must be >= 0")
        
        if growth_rate < 0:
            raise ValueError("Growth Rate must be >= 0")

        self.resources = resources
        self.growth_rate = growth_rate
        self.species_list = species_list if species_list is not None else []


    def __str__(self):
        """String representation of the ecosystem."""
        existing_names = [s.name for s in self.species_list]
        return (
            f"Resources: {self.resources}\n"
            f"Growth_rate : {self.growth_rate}\n"
            f"Species: {existing_names}"
        )
    
    # ---------------------------
    # Species Management Methods
    # ---------------------------

    def add_species(self, species: Species):
        """
        Add a new species to the ecosystem if not already present.
        """
        for genus in self.species_list:
            if genus.name == species.name:
                print(f"{species.name} already exists in the ecosystem.\n")
                return
            
        self.species_list.append(species)
        print(f"{species.name} added to the Ecosystem")

    def search_species(self, genus_name):
        """
        Search for a species by name and display its information.
        """
        for species in self.species_list:
            if species.name == genus_name:
                print(f"{species.name} exists in the Ecosystem:\n")
                print(species.display_info())
                return 
            
        print(f"Sorry but {genus_name} doesn't currently live in the Ecosystem.")
    
    def display(self):
        """
        Display detailed information of all species in the ecosystem.

        Returns:
            A pandas DataFrame summary of populations and rates.
        """
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

    # ---------------------------
    # Resource Management
    # ---------------------------

    # Update Ecosystem's resources
    def update_resources(self, num_recourses):
        """
        Update the ecosystem's resources by the specified amount.
        Negative values decrease resources but cannot reduce below zero.
        """
        new_resources = self.resources + num_recourses
        
        if new_resources < 0:
            raise ValueError("Resources cannot become negative!")

        self.resources = new_resources
        print(f"Resources updated to {self.resources}")

    def update_growth_rate(self, new_growth_rate):
        """
        Update the ecosystem's growth rate by the specified amount.
        Updated growth rate can be 0 but not negative
        """
        if new_growth_rate < 0:
            raise ValueError("Growth rate cannot be negative!")
        
        self.growth_rate = new_growth_rate
        print(f"Resources updated to {self.growth_rate}")


    def remove_species(self, genus):
        """
        Remove a species instance from the ecosystem by name.
        """
        for species in self.species_list:
            if species.name == genus.name:
                self.species_list.remove(species)
                print(f"{genus.name} successfully removed from the Ecosystem!")
                return
        
        print(f"Sorry but {genus.name} doesn't currently live in the Ecosystem")

    # ---------------------------
    # Simulation
    # ---------------------------

    def run_generation(self):
        """
        Run one full generation of the ecosystem:
        - Calculate food availability
        - Reproduce each species
        - Apply mutations
        - Update resources based on growth_rate and population consumption
        """
        if not self.species_list:
            print("No species currently in the ecosystem. Nothing to simulate.")
            return
        
        print("\n--- Running Generation ---")

        total_population_current = sum(genus.population for genus in self.species_list)

        # Food availability indicator (1 = enough food, 0 = limited)
        food_availability = 1 if (self.resources/2) >= total_population_current else 0 

        # Reproduction & mutation for each species
        for species in self.species_list:
            species.reproduce(food_availability)
            species.mutate()

        total_population_after = sum(genus.population for genus in self.species_list)

        # Resource regeneration depends on growth_rate and number of species    
        resources_add = int(self.resources * (self.growth_rate * len(self.species_list)))
        
        # Update resources after consumption and regeneration
        self.resources -= total_population_after
        self.resources += resources_add
        self.resources = max(self.resources, 0)

        print(f"\nFood availability = {food_availability}")
        print(f"Total population before = {total_population_current}")
        print(f"Total population after reproduction = {total_population_after}")
        print(f"Resources added = {resources_add}")
        print(f"Remaining resources = {self.resources}")
        

# ----------------------------------------------------------
# Predefined Species Instances
# ----------------------------------------------------------

AVAILABLE_SPECIES = [
    Species("Lion", 30, 1.2, 0.3),
    Species("Zebra", 50, 1.5, 0.1),
    Species("Elephant", 15, 0.8, 0.2),
    Species("Wolf", 25, 1.4, 0.4),
    Species("Giraffe", 20, 1.0, 0.1)
]

