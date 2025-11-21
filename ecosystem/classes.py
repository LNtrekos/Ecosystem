import random

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

    def __init__(self, resources, species_list=None):
        if resources < 0:
            raise ValueError("Resources must be >= 0")

        self.resources = resources
        self.species_list = species_list if species_list is not None else []

    def __str__(self):
        existing_names = [s.name for s in self.species_list]
        return f"Resources: {self.resources}\nSpecies: {existing_names}"

    def add_species(self, species: Species):
        for genus in self.species_list:
            if genus.name == species.name:
                print(f"{species.name} already exists.")
                return
            
        self.species_list.append(species)
        print(f"{species.name} added to the Ecosystem")

    def search_species(self, species: Species):
        for genus in self.species_list:
            if species.name == genus.name:
                print(f"{species.name} exists in the Ecosystem:\n")
                print(genus.display_info())
                return 
        print(f"Sorry but {species} doesn't currently live in the Ecosystem")
        return None

    def remove_species(self, genus):
        if genus in self.species_list:
            self.species_list.remove(genus)
            print(f"{genus.name} successfully removed from the Ecosystem!")
            return 
        
        print(f"Sorry but {genus.name} doesn't currently live in the Ecosystem")
        return None

    def display(self):

        if not self.species_list:
            print("No Species currently live in the Ecosystem")
        for genus in self.species_list:
            print(f"{genus.name} lives in the Ecosystem with population {genus.population}")

        print(f"and the resources is: {self.resources}")

    #def update_resources(self, num_resources):



AVAILABLE_SPECIES = [
    Species("Lion", 30, 1.2, 0.05),
    Species("Zebra", 120, 1.5, 0.02),
    Species("Elephant", 15, 0.8, 0.01),
    Species("Wolf", 25, 1.4, 0.03),
    Species("Giraffe", 20, 1.0, 0.01)
]

