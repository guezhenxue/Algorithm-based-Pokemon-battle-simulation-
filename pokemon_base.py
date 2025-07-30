"""
This module contains PokeType, TypeEffectiveness and an abstract version of the Pokemon Class
"""
from abc import ABC
from enum import Enum
from data_structures.referential_array import ArrayR
import math

__author__ = "Gue Zhen Xue"

class PokeType(Enum):
    """
    This class contains all the different types that a Pokemon could belong to
    """
    FIRE = 0
    WATER = 1
    GRASS = 2
    BUG = 3
    DRAGON = 4
    ELECTRIC = 5
    FIGHTING = 6
    FLYING = 7
    GHOST = 8
    GROUND = 9
    ICE = 10
    NORMAL = 11
    POISON = 12
    PSYCHIC = 13
    ROCK = 14

class TypeEffectiveness:
    """
    Represents the type effectiveness of one Pokemon type against another.
    """
    def __init__(self):
        """
        Initializes a TypeEffectiveness instance by populating the type effectiveness table from a CSV file.
        """
        self.table = self.populate_data("type_effectiveness.csv")

    def populate_data(self, filename) -> list:
        """
        Populates the type effectiveness table from a CSV file.

        Param args:
            filename (str): The name of the CSV file containing the type effectiveness data.

        Returns:
            list: A list representing the type effectiveness table.
        
        Preconditions:
            There must be lines in the CSV file.
        
        Postconditions:
            The list should not be modified
            
        Complexity:
            Bestcase: O(1) - when there is only 1 line in the file (with only the heading of the file).
            Worstcase: O(n^2(m+p)), where:
                        - n is the number of lines in the file.
                        - m and p are the number of characters in each line
        """
        temp_table = []
        with open(filename,"r") as file:
            for line in file:
                data = line.strip().split(",")
                try:
                    temp_table.append([float(value) for value in data])
                except ValueError:
                    pass
        return temp_table

    @classmethod
    def get_effectiveness(cls, attack_type: PokeType, defend_type: PokeType) -> float:
        """
        Returns the effectiveness of one Pokemon type against another, as a float.

        Parameters:
            attack_type (PokeType): The type of the attacking Pokemon.
            defend_type (PokeType): The type of the defending Pokemon.

        Returns:
            float: The effectiveness of the attack, as a float value between 0 and 4.
        
        Preconditions:
            There must be lines in the CSV file.

        Postconditions:
            The list should not be modified

        Complexity: 
            Best and worst case: O(1) - when the effectiveness is found in the table.
        """

        return float(TypeEffectiveness().table[attack_type.value][defend_type.value])

        

    def __len__(self) -> int:
        """
        Returns the number of types of Pokemon

        Complexity: 
            Best and worst case: O(1) - when the length of poketype returned.
        """
        return len(PokeType)


class Pokemon(ABC): 
    """
    Represents a base Pokemon class with properties and methods common to all Pokemon.
    """
    def __init__(self):
        """
        Initializes a new instance of the Pokemon class.
        """
        self.health = None
        self.level = None
        self.poketype = None
        self.battle_power = None
        self.evolution_line = None
        self.name = None
        self.experience = None
        self.defence = None
        self.speed = None
        self.boost_value = 1.5


    def get_name(self) -> str:
        """
        Returns the name of the Pokemon.

        Returns:
            str: The name of the Pokemon.
        
        Complexity: 
            Best and worst case: O(1) - when the name be returned
        """
        return self.name

    def get_health(self) -> int:
        """
        Returns the current health of the Pokemon.

        Returns:
            int: The current health of the Pokemon.
        
        Complexity: 
            Best and worst case: O(1) - when the health value be returned
        """
        return int(self.health)

    def get_level(self) -> int:
        """
        Returns the current level of the Pokemon.

        Returns:
            int: The current level of the Pokemon.
        
        Complexity: 
            Best and worst case: O(1) - when the level be returned
        """
        return int(self.level)

    def get_speed(self) -> int:
        """
        Returns the current speed of the Pokemon.

        Returns:
            int: The current speed of the Pokemon.
            
        Complexity: 
            Best and worst case: O(1) - when the speed be returned
        """
        return int(self.speed)

    def get_experience(self) -> int:
        """
        Returns the current experience of the Pokemon.

        Returns:
            int: The current experience of the Pokemon.
            
        Complexity: 
            Best and worst case: O(1) - when the experience be returned
        """
        return int(self.experience)

    def get_poketype(self) -> PokeType:
        """
        Returns the element type of the Pokemon.

        Returns:
            PokeType: The element type of the Pokemon.
            
        Complexity: 
            Best and worst case: O(1) - when the poketype be returned
        """
        return self.poketype

    def get_defence(self) -> int:
        """
        Returns the defence of the Pokemon.

        Returns:
            int: The defence of the Pokemon.
            
        Complexity: 
            Best and worst case: O(1) - when the defense be returned
        """
        return int(self.defence)

    def get_evolution(self) -> list:
        """
        Returns the evolution line of the Pokemon.

        Returns:
            list: The evolution of the Pokemon.
            
        Complexity: 
            Best and worst case: O(1) - when the evolution line be returned
        """
        return self.evolution_line

    def get_battle_power(self) -> int:
        """
        Returns the battle power of the Pokemon.

        Returns:
            int: The battle power of the Pokemon.
            
        Complexity: 
            Best and worst case: O(1) - when the battle power be returned
        """
        return int(self.battle_power)

    def attack(self, other_pokemon) -> int:
        """
        Calculates and returns the damage that this Pokemon inflicts on the
        other Pokemon during an attack.

        Args:
            other_pokemon (Pokemon): The Pokemon that this Pokemon is attacking.

        Returns:
            int: The damage that this Pokemon inflicts on the other Pokemon during an attack.
        
        Complexity: 
            Best and worst case: O(1) - when the damage be returned
        """
        if other_pokemon.get_defence() < self.get_battle_power() / 2:
            
            damage = self.get_battle_power() - other_pokemon.get_defence()

        elif other_pokemon.get_defence() < self.get_battle_power():
            
            damage = math.ceil(self.get_battle_power() * 5/8 - other_pokemon.get_defence() / 4)
        
        else:
            
            damage = math.ceil(self.get_battle_power() / 4)

        effective_multiplier = (TypeEffectiveness.get_effectiveness(self.get_poketype(), other_pokemon.get_poketype()))

        effective_damage = damage * effective_multiplier

        return effective_damage

    def defend(self, damage: int) -> None:
        """
        Reduces the health of the Pokemon by the given amount of damage, after taking
        the Pokemon's defence into account.

        Args:
            damage (int): The amount of damage to be inflicted on the Pokemon.
        
        Complexity: 
            Best and worst case: O(1) - when the health-after-damage be reflected
        """
        effective_damage = damage/2 if damage < self.get_defence() else damage
        self.health = self.health - effective_damage

    def level_up(self) -> None:
        """
        Increases the level of the Pokemon by 1, and evolves the Pokemon if it has
          reached the level required for evolution.
        
        Complexity: 
            Best case: O(1) - when the level increased and (must) evolved, and the name is \
                                at the first index of the evolution line.
            Worst case: O(n) - when the level increased and (not) evolved evolved, and the name is\
                                at the last index of the evolution line
        """
        
        self.level += 1
        if len(self.evolution_line) > 0 and self.evolution_line.index\
            (self.name) != len(self.evolution_line)-1:
            self._evolve()

    def _evolve(self) -> None:
        """
        Evolves the Pokemon to the next stage in its evolution line, and updates
          its attributes accordingly.
          
        Complexity: 
            Best and worst case: O(1) - when the pokemon evolved and stats being boosted
        """
        self.name = self.evolution_line[self.level - 1]
        self.boost_stats()

    def boost_stats(self) -> None:
        """
        Boosts the stats of the Pokemon by a fixed multiplier.

        The method multiplies the Pokemon's battle power, health, speed, and defence
        by the boost value specified in the class.

        Preconditions:
            The Pokemon's boost value must be set.

        Postconditions:
            The Pokemon's stats are multiplied by the boost value.

        Complexity: 
            Best and worst case: O(1) - when the boosted stats being reflected
        """
        self.battle_power *= self.boost_value
        self.health *= self.boost_value
        self.speed *= self.boost_value
        self.defence *= self.boost_value

    def is_alive(self) -> bool:
        """
        Checks if the Pokemon is still alive (i.e. has positive health).

        Returns:
            bool: True if the Pokemon is still alive, False otherwise.
        
        Complexity: O(1), when bool value of Pokemon is still alive is returned
        """
        return self.health > 0

    def __str__(self) -> str:
        """
        Return a string representation of the Pokemon instance in the format:
        <name> (Level <level>) with <health> health and <experience> experience
        
        Complexity: 
            Best and worst case: O(1) - when string is returned
        """
        return f"{self.name} (Level {self.level}) with {self.health} health and {self.get_experience()} experience"



