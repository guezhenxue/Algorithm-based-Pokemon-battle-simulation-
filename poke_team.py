from pokemon import *
import random
from typing import List
from battle_mode import BattleMode
from data_structures.queue_adt import CircularQueue
from data_structures.bset import BSet
from data_structures.stack_adt import ArrayStack
from data_structures.stack_adt import ArrayR
from data_structures.array_sorted_list import ArraySortedList, ListItem

__author__ = "Gue Zhen Xue"

class PokeTeam:
    """
    Represents a team of Pokemon with methods for managing the team.

    Attributes:
    - POKE_LIST: List of all Pokemon types.
    - TEAM_LIMIT: Maximum number of Pokemon in a team.
    """

    POKE_LIST = get_all_pokemon_types()
    TEAM_LIMIT = 6

    def __init__(self): 
        """
        Initializes a new instance of the PokeTeam class.
        """
        self.size = 1
        self.team = ArrayR(self.size)
        self.memory_team = None
        self.special_condition = False
    
    def __len__(self) -> int:
        """
        Returns the number of Pokemon in the team.
        
        Returns:
            int: The number of Pokemon in the team.

        Complexity:
            Best & Worst case: O(1) - accessing the length of the team.
        """
        return len(self.team) 

    def choose_manually(self) -> None:
        """
        Allows the user to manually choose Pokemon for their team.

        If the team size is less than the limit, the user can choose a Pokemon
        from a list of available Pokemon types. The process continues until
        the team size reaches the limit.

        Complexity analysis:
            Best Case: O(1) - when the user selects to quit immediately.
            Worst Case: O(2^n) - when the user repetitively select the choice other than "1" and "2"

        """
        print("==================================\nEnter your choice:\n1. Choose Pokemon\n2. Quit.\n==================================")
        choice = input()
        if choice == "1":
            self.choose_pokemon()
        elif choice == "2":
            pass
        else:
            self.choose_manually()
        self.copy_team()
        
                
    def choose_pokemon(self) -> None:   
        """
        Allows the user to choose a Pokemon to add to the team.

        If the team size is less than the limit, the user can choose a Pokemon
        from a list of available Pokemon types. The process continues until
        the team size reaches the limit.
        
        Preconditions:
            The team size must be less than the limit.
        
        Postconditions:
            Allows the user to choose a Pokemon to add to the team.
        
        Complexity analysis:
            Best Case: O(1) - when the team is full.
            Worst Case: O(2^n) - when the user repetitively select the choice other than "1" and "2" (in choose_manually)
        
        """       
        if self.size < self.TEAM_LIMIT:
            print(f"Choose a Pokemon for your team (up to {self.TEAM_LIMIT})")
            chosen_pokemon = input("Your Pokemon: ")
            self.check_database(chosen_pokemon)
        else:
            print("The team is full.")
        self.choose_manually()
        
    def check_database(self, chosen_pokemon: str) -> None:
        """
        Adds the chosen Pokemon to the team if it is valid.

        Args:
            chosen_pokemon (str): The name of the chosen Pokemon.

        Preconditions:
            chosen_pokemon must be a valid Pokemon type.

        Postconditions:
            Adds the chosen Pokemon to the team if it is valid.

        Complexity:
            Best case: O(1) - when the chosen Pokemon is the first one in the list.
            Worst case: O(n) - when the chosen Pokemon is not found in the list.
        """
        for pokemon in self.POKE_LIST:
            if chosen_pokemon.lower() == pokemon().get_name().lower():
                self.add_size()
                self.team[self.size - 1] = pokemon
                print(f"{pokemon().get_name()} is added into your team!")
                return
        print("The given name is invalid.")
        
    def add_size(self) -> None:
        """
        Increases the size of the team array if needed.

        Postconditions:
            Increases the size of the team array if needed.
        Complexity:
            Best Case: O(1) - when the team array is not full.
            Worst Case: O(n) - when the team array is full and needs to be resized.

        """
        if self.team[0] != None:
            self.size +=1
            temp_table = ArrayR(self.size)
            temp_table[:-1] = self.team
            self.team = temp_table
        
    def choose_randomly(self) -> None:
        """
        Randomly chooses Pokemon to add to the team until the team limit is reached.

        Postconditions:
            Length of the team must be the same of the size limit

        Complexity:
            Best case: O(1) - when the team is already full.
            Worst case: O(n) - when the team is empty.
        """
        all_pokemon = get_all_pokemon_types()
        while self.size < self.TEAM_LIMIT:
            rand_int = random.randint(0, len(all_pokemon)-1)
            targeted_pokemon = all_pokemon[rand_int]()
            self.add_size()
            self.team[self.size - 1] = targeted_pokemon
        self.copy_team()
        

    def copy_team(self) -> None:
        """
        Copies the current team to a memory team.

        Preconditions:
            A current team must be created.

        Postconditions:
            Copies the current team to a memory team.

        Complexity:
            Best case: O(1) - when the team has only 1 Pokemon.
            Worst case: O(n) - when the team has Pokemons.
        """
        self.memory_team = ArrayR(self.size)
        for i in range(self.size):
            self.memory_team[i] = self[i]
            

    def regenerate_team(self, battle_mode, criterion = None) -> None:
        """
        Regenerates the team based on the provided battle mode and criterion.

        Preconditions:
            None

        Postconditions:
            Regenerates the team based on the provided battle mode and criterion.

        Complexity:
            Best case: O(n) - when regenerating the team without any specific criteria. (When Set or Rotate mode is called)
            Worst case: O(n^2) - when regenerating the team with specific criteria that require sorting. (When Optimise mode is called)
        """
        for pokemon in self.memory_team:
            pokemon.health = (type(pokemon)().get_health())

        self.team = self.memory_team
        self.team = self.assemble_team(battle_mode, criterion)

        if self.special_condition:
            self.special(battle_mode, criterion)
        

    def assemble_team(self, battle_mode, criterion = "health") -> None:
        """
        Assembles the team based on the provided battle mode and criterion.

        Preconditions:
            None

        Postconditions:
            Assembles the team based on the provided battle mode and criterion.

        Complexity:
            Best case: O(1) - when the team is not in ArrayR format.
            Worst case: O(n^2) - when assign team method is called.
        """
        
        if type(self.team) == ArrayR:
            if battle_mode.value == 0:
                temp = ArrayStack(len(self.team))
                
                for pokemon in self.team:
                    temp.push(pokemon)
            
            elif battle_mode.value == 1:
                temp = CircularQueue(len(self.team))
                
                for pokemon in self.team:
                    temp.append(pokemon)  
            
            elif battle_mode.value == 2:
                temp =  self.assign_team(criterion)

            return temp

    def assign_team(self, attribute) -> ArraySortedList:
        """
        Assigns the team based on the provided attribute.

        Preconditions:
            A team must be created.

        Postconditions:
            Assigns the team based on the provided attribute.
        
        Complexity:
            Best case: O(1) - When there is only 1 pokemon in the team.
            Worst case: O(n^2) - when changing the whole team (ArrayR) to ArraySortedList format.
        """
        team = ArraySortedList(len(self.team))
        
        for pokemon in self.team:
            number = self.attribute(pokemon, attribute)
            team.add(ListItem(value = pokemon, key = number))
        return team
    
    def attribute(self, pokemon, attribute):
        """
        Returns the specified attribute of the Pokemon.

        Preconditions:
            None

        Postconditions:
            Returns the specified attribute of the Pokemon.
        
        Returns:
            functions: attribute required.

        Complexity:
            Best & Worst case: O(1) - accessing the attribute of the Pokemon.
        """
        if attribute == "health":
            return  pokemon.health
        elif attribute == "level":
            return pokemon.level
        elif attribute == "speed":
            return pokemon.speed
        elif attribute == "battle_power":
            return pokemon.battle_power
        elif attribute == "defence":
            return pokemon.defence

    def special(self, battle_mode, criterion = "health") -> None: 
        """
        Performs a special operation on the team based on the provided battle mode.

        Preconditions:
            None

        Postconditions:
            Performs a special operation on the team based on the provided battle mode.

        Complexity:
            Best case: O(n) - when performing the special_set or special_rotate.
            Worst case: O(n^2) - when performing the special_optimise.
        """
        self.special_condition = True
        if battle_mode.value == 0:
            self.special_set()
        
        if battle_mode.value == 1:
            self.special_rotate()
        
        if battle_mode.value == 2:
            self.special_optimise(criterion)

    def special_set(self) -> None:
        """
        Rearranges the team by splitting it into two halves and reversing the order of the first half.

        Complexity: 
            Best Case: O(1) - when the team has team of length 1.
            Worst Case: O(n) - when the team has n Pokemons.
        """
        team  = self.team
        temp_1 = ArrayStack(len(self.team))
        temp_2 = ArrayStack(len(self.team))

        for i in range(len(self.team) // 2):
            temp_1.push(team.pop())

        while len(temp_1) > 0:
            temp_2.push(temp_1.pop())

        while len(temp_2) > 0:
            team.push(temp_2.pop())

    def special_rotate(self) -> None: 
        """
        Rearranges the team by splitting it into two halves and interleaving the elements of the two halves.

        Complexity
            Best Case: O(1) - when the team has team of length 1.
            Worst Case: O(n) - when the team has n Pokemons.
        """
        team = self.team
        temp_1 = ArrayStack(len(self.team))
        temp_2 = CircularQueue(len(self.team))

        for i in range(len(self.team) // 2):
            temp_2.append(team.serve())

        while len(team) > 0:
            temp_1.push(team.serve())

        while len(temp_1) > 0:
            temp_2.append(temp_1.pop())

        while len(temp_2) > 0:
            team.append(temp_2.serve())

    def special_optimise(self, criterion) -> None:
        """
        Reverses the sorting order of the team based on the provided criterion.

        Postconditions:
            Reverses the sorting order of the team based on the provided criterion.

        Complexity:
            Best case: O(1) - when len(self.team) = 1
            Worst case: O(n^2) - when n is the length of the team
        """
        for i in range(len(self.team)):
            update_pokemon = self.team.delete_at_index(i)
            update_pokemon.key *= -1
            self.team.add(update_pokemon)

    def __getitem__(self, index: int) -> Pokemon: 
        """
        Returns the Pokemon at the specified index in the team.

        Args:
            index (int): The index of the Pokemon in the team.

        Returns:
            Pokemon: The Pokemon at the specified index in the team.

        Preconditions:
            self.team must be either in format of one of the ArrayR, ArraySortedList, ArrayStack and CircularQueue

        Complexity:
            Best & Worst case: O(1) - accessing the Pokemon at the specified index in the team.
        """
        if type(self.team) == ArraySortedList:
            return self.team[index].value
        elif type(self.team) == ArrayStack:
            return self.team.array[len(self.team) - index - 1]
        elif type(self.team) == CircularQueue:
            return self.team.array[index]
        else:
            return self.team[index]

    
    def __str__(self) -> str:
        """
        Returns a string representation of the team.

        Returns:
            str: A string representation of the team.
        
        Complexity:
            Best & Worst case: O(n) - returning the required string (where n is the number of pokemons).
        """
        x=""
        for i in range(self.team_count):
            x+=str(self.team[i])+"\n"
        return x

class Trainer:
    """
    Represents a trainer that has methods managing the team.
    """
    def __init__(self, name) -> None:
        """
        Initializes a new instance of the Trainer class.
        """
        self.name = name
        self.team_status = PokeTeam()
        self.pokedex = BSet()

    def register_pokedex(self) -> None:
        """
        Registers the Pokemon in the team status to the Pokedex.

        Preconditions:
            Team (in ArrayR) is formed with (at least 1) pokemon

        Postconditions:
            Registers the Pokemon in the team status to the Pokedex.

        Complexity:
            Best case: O(n^2) - when all Pokemon in the team status are new to the Pokedex.
            Worst case: O(n^2) - when all Pokemon in the team status are already registered in the Pokedex.
        """
        for pokemon in self.team_status:
            try:
                self.pokedex.add(pokemon().get_poketype().value + 1) 
            except TypeError:
                if pokemon.get_health() > 0:
                    self.pokedex.add(pokemon.get_poketype().value + 1)


    def pick_team(self, method: str) -> None:
        """
        Allows the trainer to pick a team either randomly or manually.

        Args:
            method (str): The method to pick the team, either 'Random' or 'Manual'.

        Complexity:
            Best case: O(1) - when the trainer picks a team (with team size limit of 1) randomly or manually.
            Worst case: O(n) - when the trainer picks a team manually and selects 1 Pokemon 
                                or picks a team randomly with size up to size limit.
        """
        method = method.lower()
        if method == "random":
            self.team_status.choose_randomly()
            self.register_pokedex()
        elif method == "manual":
            self.team_status.choose_manually()
            self.register_pokedex()
        
    def get_team(self) -> PokeTeam:
        """
        Returns the team status of the trainer.

        Preconditions:
            Team must be formed.

        Returns:
            self.team_status (PokeTeam): return the team of the poketeam

        Complexity:
            Best & Worst case: O(1) - when accessing the team status.
        """
        return self.team_status

    def get_name(self) -> str:
        """"
        Returns the name of the trainer.

        Returns:
            str.name (str): Trainer's name

        Complexity:
            Best & Worst case: O(1) - when accessing the name.
        """
        return self.name

    def register_pokemon(self, pokemon: Pokemon) -> None:
        """
        Registers a Pokemon to the trainer's Pokedex.

        Args:
            pokemon (Pokemon): The Pokemon to register to the Pokedex.

        Preconditions:
            The pokemon type must be able to be enumerated to a value from Poketype class.

        Postconditions:
            Registers a Pokemon to the trainer's Pokedex.

        Complexity:
            Best & Worst case: O(n) - when registering a new Pokemon type to the Pokedex.
        """
        self.pokedex.add(pokemon.get_poketype().value + 1)


    def get_pokedex_completion(self) -> float:
        """
        Returns the completion percentage of the trainer's Pokedex.

        Preconditions:
            The pokedex must be registered correctly for each pokemon that the trainer seen.

        Postconditions:
            Returns the completion percentage of the trainer's Pokedex.

        Returns:
            pokedex_completion (float): pokedex completion rounded to 2 decimal places.

        Complexity:
            Best & Worst case: O(1) - when the Pokedex is empty or full.
        """
        return round((len(self.pokedex)/ len(PokeType)), 2) 
    
    def __str__(self) -> str:
        """
        Returns a string representation of the trainer.

        Preconditions:
            The pokedex completion must be calculated (with pokedex generated correctly.)

        Returns:
            str: required format of string reflecting the name of trainer and the pokedex completion (in %).

        Complexity Analysis:
            Best & Worst case: O(1) - when string is returned
        """    
        return f"Trainer {self.name} Pokedex Completion: {int(self.get_pokedex_completion() * 100)}%"

