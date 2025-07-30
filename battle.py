from poke_team import Trainer, PokeTeam
from typing import Tuple
from battle_mode import BattleMode
from pokemon import *
from data_structures.queue_adt import CircularQueue
from data_structures.bset import BSet
from data_structures.stack_adt import ArrayStack
from data_structures.stack_adt import ArrayR
from data_structures.array_sorted_list import ArraySortedList, ListItem
from abc import ABC, abstractmethod
import math
import random

__author__ = "Gue Zhen Xue"

class BattleMechanism(ABC):
    """
    Abstract base class for battle mechanisms.

    Methods:
    - update_team_status(trainer, team, pokemon, attribute): Abstract method to update the team status based on the battle mechanism.
    - get_front_poke(team): Abstract method to get the front Pokemon in the team based on the battle mechanism.
    """

    @staticmethod
    def _select_battle_mechanism(battlemode_value):
        """
        Selects a battle mechanism based on the battle mode value.

        Args:
            battlemode_value (int): The value of the battle mode.

        Returns:
            BattleMechanism (function): The selected battle mechanism.

        Complexity:
            Best & Worst case: O(1) - when selecting the battle mechanism.
        """
        if battlemode_value == 0:
            return SetBattle()
        
        elif battlemode_value == 1:
            return RotateBattle()
        
        elif battlemode_value == 2:
            return OptimiseBattle()

    @abstractmethod
    def update_team_status(self, trainer, team, pokemon, attribute):
        """
        Abstract method to update the team status based on the battle mechanism.

        Args:
            trainer (Trainer): The trainer object.
            team (PokeTeam): The team object.
            pokemon (Pokemon): The Pokemon object.
            attribute (str): The attribute based on which the team is updated.

        Postconditions:
            Updates the team status based on the battle mechanism.
        """
        pass

    @abstractmethod
    def get_front_poke(self, team):
        """
        Abstract method to get the front Pokemon in the team based on the battle mechanism.

        Args:
            team (PokeTeam): The team object.

        Returns:
            Pokemon: The front Pokemon in the team.

        Postconditions:
            Returns the front Pokemon in the team based on the battle mechanism.
        """
        pass

class SetBattle(BattleMechanism):
    """
    Class implementing the Set Battle mechanism.

    Methods:
    - update_team_status(trainer, team, pokemon, attribute): Updates the team status based on the Set Battle mechanism.
    - get_front_poke(team): Returns the front Pokemon in the team based on the Set Battle mechanism.
    """
    
    def update_team_status(self, trainer, team, pokemon, attribute):
        """
        Updates the team status based on the Set battle mechanism.

        Args:
            trainer (Trainer): The trainer object.
            team (PokeTeam): The team object.
            pokemon (Pokemon): The Pokemon object.
            attribute (str): The attribute based on which the team is updated.

        Complexity:
            Best & Worst case: O(1) - when updating the team status.
        """
        if pokemon.is_alive():
            team.push(pokemon)

    def get_front_poke(self, team):
        """
        Returns the front Pokemon in the team based on the Set battle mechanism.

        Args:
            team (PokeTeam): The team object.

        Returns:
            Pokemon: The front Pokemon in the team.

        Complexity:
            Best & Worst case: O(1) - when accessing the front Pokemon.
        """
        return team.pop()

class RotateBattle(BattleMechanism):
    """
    Class implementing the Rotate Battle mechanism.

    Methods:
    - update_team_status(trainer, team, pokemon, attribute): Updates the team status based on the Rotate Battle mechanism.
    - get_front_poke(team): Returns the front Pokemon in the team based on the Rotate Battle mechanism.
    """ 

    def update_team_status(self, trainer, team, pokemon, attribute):
        """
        Updates the team status based on the Rotate battle mechanism.

        Args:
            trainer (Trainer): The trainer object.
            team (PokeTeam): The team object.
            pokemon (Pokemon): The Pokemon object.
            attribute (str): The attribute based on which the team is updated.

        Complexity:
            Best & Worst case: O(1) - when updating the team status.
        """
        if pokemon.is_alive():
            team.append(pokemon)


    def get_front_poke(self, team):
        """
        Returns the front Pokemon in the team based on the Rotate battle mechanism.

        Args:
            team (PokeTeam): The team object.

        Returns:
            Pokemon: The front Pokemon in the team.

        Complexity:
            Best & Worst case: O(1) - when accessing the front Pokemon.
        """
        return team.serve()


class OptimiseBattle(BattleMechanism):
    """
    Class implementing the Optimise Battle mechanism.

    Methods:
    - update_team_status(trainer, team, pokemon, attribute): Updates the team status based on the Optimise Battle mechanism.
    - get_front_poke(team): Returns the front Pokemon in the team based on the Optimise Battle mechanism.
    """

    def update_team_status(self, trainer, team, pokemon, attribute):
        """
        Updates the team status based on the Optimise battle mechanism.

        Args:
            trainer (Trainer): The trainer object.
            team (PokeTeam): The team object.
            pokemon (Pokemon): The Pokemon object.
            attribute (str): The attribute based on which the team is updated.

        Complexity:
            Best & Worst case: O(n) - when updating the team status.
        """
        if pokemon.is_alive():
           team.add(ListItem(pokemon, trainer.team_status.attribute(pokemon, attribute)))

    def get_front_poke(self, team):
        """
        Returns the front Pokemon in the team based on the Optimise battle mechanism.

        Args:
            team (PokeTeam): The team object.

        Returns:
            Pokemon: The front Pokemon in the team.

        Complexity:
            Best & Worst case: O(1) - when accessing the front Pokemon.
        """
        return team.delete_at_index(0).value
    
class Battle:

    def __init__(self, trainer_1: Trainer, trainer_2: Trainer, battle_mode: BattleMode, criterion="health") -> None:
        """
        Initializes a new instance of the Battle class.

        Args:
            trainer_1 (Trainer): The first trainer.
            trainer_2 (Trainer): The second trainer.
            battle_mode (BattleMode): The battle mode.
            criterion (str): The criterion for battle.
        """
        self.trainer_1, self.trainer_2 = trainer_1, trainer_2
        self.battle_mode = battle_mode
        self.criterion = criterion
        self.trainer_1.team_status, self.trainer_2.team_status = self._create_teams()
        self.trainer_1.team_status.team, self.trainer_2.team_status.team = self.trainer_1.team_status.assemble_team(
            self.battle_mode, self.criterion), self.trainer_2.team_status.assemble_team(self.battle_mode, self.criterion)
        self.battle_mechanism = BattleMechanism._select_battle_mechanism(self.battle_mode.value)

    def commence_battle(self) -> Trainer | None:
        """
        Commences the battle between the trainers.

        Returns:
            Trainer | None: The winning trainer, or None if it's a tie.

        Complexity:
            Best case: O(1) - when one of the team have no team member.
            Worst case: O(N) - when n is the number of rounds that the battle goes.
        """
        round_num = 0

        while self.trainer_1.team_status.team and self.trainer_2.team_status.team:
            
            self.round(round_num, self.trainer_1, self.trainer_2, self.trainer_1.team_status.team, self.trainer_2.team_status.team)
            round_num += 1

        if self.trainer_1.team_status.team:
            return self.trainer_1 
        
        elif self.trainer_2.team_status.team:
            return self.trainer_2
        else:
            return None
        
    def round(self, round_num, trainer_1, trainer_2, team_1, team_2) -> None:
        """
        Executes a round of the battle.

        Args:
            round_num (int): The round number.
            trainer_1 (Trainer): The first trainer.
            trainer_2 (Trainer): The second trainer.
            team_1 (PokeTeam): The team of the first trainer.
            team_2 (PokeTeam): The team of the second trainer.

        Returns:
            None

        Preconditions:
            None

        Postconditions:
            Executes a round of the battle.

        Complexity:
            Best & Worst case: O(n) - when accessing and updating team and Pokemon attributes for each round.
        """
        poke_1, poke_2 = self.get_front_poke(team_1), self.get_front_poke(team_2)
        self.trainer_1.register_pokemon(poke_2)
        self.trainer_2.register_pokemon(poke_1)

        self.commence_attack(team_1, poke_1, team_2, poke_2)

        self.update_team_status(trainer_1, team_1, poke_1, self.criterion)
        self.update_team_status(trainer_2, team_2, poke_2, self.criterion)

    def commence_attack(self, team_1, poke_1, team_2, poke_2) -> None:
        """
        Executes the attack phase of the battle.

        Args:
            team_1 (PokeTeam): The team of the first trainer.
            poke_1 (Pokemon): The Pokemon of the first trainer.
            team_2 (PokeTeam): The team of the second trainer.
            poke_2 (Pokemon): The Pokemon of the second trainer.

        Preconditions:
            Both pokemon are alive.

        Postconditions:
            Affect the HP of both pokemon

        Complexity:
            Best case: O(1) - when determining the damage inflicted by each Pokemon (both pokemon not evolve).
            Worst case: O(n) - when determining the damage inflicted by each Pokemon (both pokemon evolve).
        """
        pokedex_1,  pokedex_2 = self.trainer_1.get_pokedex_completion(), self.trainer_2.get_pokedex_completion()

        speed_1, speed_2 = poke_1.get_speed(), poke_2.get_speed()
        damage_1, damage_2 = self.determine_damage(poke_1, pokedex_1, poke_2, pokedex_2), self.determine_damage(poke_2, pokedex_2, poke_1, pokedex_1)

        if speed_1 > speed_2:
            self.attack_with_priority(poke_1, poke_2, damage_1, damage_2)
        elif speed_2 > speed_1:
            self.attack_with_priority(poke_2, poke_1, damage_2, damage_1)
        else:
            self.attack_without_priority(poke_1, poke_2, damage_1, damage_2)

    def attack_with_priority(self, first_poke: Pokemon, second_poke: Pokemon, first_damage, second_damage) -> None:
        """
        Executes an attack with priority.

        Args:
            first_poke (Pokemon): The attacking Pokemon with priority.
            second_poke (Pokemon): The defending Pokemon.
            first_damage (float): The damage inflicted by the first Pokemon.
            second_damage (float): The damage inflicted by the second Pokemon.

        Returns:
            None

        Preconditions:
            None

        Postconditions:
            Executes an attack with priority.

        Complexity:
            Best case: O(1) - when determining the damage, updating their health, and both pokemon is alive.
            Worst case: O(n) - when determining the damage, updating their health, and both pokemon is alive, with both pokemon have range of evolution.
        """
        second_poke.defend(first_damage)
        if second_poke.is_alive(): 
            first_poke.defend(second_damage)
            if first_poke.is_alive():
                self.health_reduction(first_poke, second_poke, 1)
            else:
                second_poke.level_up()
        else:
            first_poke.level_up()
    
    def attack_without_priority(self, first_poke: Pokemon, second_poke: Pokemon, first_damage, second_damage) -> None:
        """
        Executes an attack without priority.

        Args:
            first_poke (Pokemon): The first attacking Pokemon.
            second_poke (Pokemon): The second attacking Pokemon.
            first_damage (float): The damage inflicted by the first Pokemon.
            second_damage (float): The damage inflicted by the second Pokemon.

        Returns:
            None

        Preconditions:
            None

        Postconditions:
            Executes an attack without priority.

        Complexity:
            Best case: O(1) - when determining the damage, updating their health, and both pokemon is alive.
            Worst case: O(n) - when determining the damage, updating their health, and both pokemon is alive, with both pokemon have range of evolution.
        """
        second_poke.defend(first_damage)
        first_poke.defend(second_damage)

        if first_poke.is_alive() and second_poke.is_alive():
            self.health_reduction(first_poke, second_poke, 1)
        elif not first_poke.is_alive():
            second_poke.level_up()
        elif not second_poke.is_alive():
            first_poke.level_up()
    
    def health_reduction(self, first_poke, second_poke, health_to_reduce) -> None:
        """
        Reduces the health of the Pokemon.

        Args:
            first_poke (Pokemon): The first Pokemon.
            second_poke (Pokemon): The second Pokemon.
            health_to_reduce (int): The amount of health to reduce.

        Preconditions:
            Both pokemon are alive.

        Postconditions:
            Reduces the health of the Pokemon.

        Complexity:
            Best & Worst case: O(1) - when updating the health of the Pokemon, there is no range of evolution for pokemon.
            Best & Worst case: O(n) - when updating the health of the Pokemon, there is range of evolution for pokemo.
        """
        second_poke.health -= health_to_reduce
        first_poke.health -= health_to_reduce
        if not second_poke.is_alive() and first_poke.is_alive():
            first_poke.level_up()
        if not first_poke.is_alive() and second_poke.is_alive():
            second_poke.level_up()

    def determine_damage(self,attacking_pokemon, attacking_pokedex_completion, defending_pokemon, defending_pokedex_completion) -> float:
        """
        Determines the damage inflicted by a Pokemon.

        Args:
            attacking_pokemon (Pokemon): The attacking Pokemon.
            attacking_pokedex_completion (float): The Pokedex completion of the attacking trainer.
            defending_pokemon (Pokemon): The defending Pokemon.
            defending_pokedex_completion (float): The Pokedex completion of the defending trainer.

        Returns:
            float: The damage inflicted by the attacking Pokemon.

        Complexity:
            Best & Worst case: O(1) - when calculating the damage based on the Pokemon's attack and the Pokedex completion.
        """
        return math.ceil(attacking_pokemon.attack(defending_pokemon) * (attacking_pokedex_completion / defending_pokedex_completion))

    def get_front_poke(self, team) -> Pokemon:
        """
        Gets the front Pokemon in the team by calling the required method from the abstract class.

        Args:
            team (PokeTeam): The team object.

        Returns:
            Pokemon: The front Pokemon in the team.

        Postconditions:
            Gets the front Pokemon in the team.

        Complexity:
            Best & Worst case: O(1) - when accessing the front Pokemon in the team.
        """
        return self.battle_mechanism.get_front_poke(team)
    
    def update_team_status(self, trainer, team, pokemon, attribute) -> None:
        """
        Updates the team status based on the battle mechanism.

        Args:
            trainer (Trainer): The trainer object.
            team (PokeTeam): The team object.
            pokemon (Pokemon): The Pokemon object.
            attribute (str): The attribute based on which the team is updated.

        Returns:
            None

        Preconditions:
            None

        Postconditions:
            Updates the team status based on the battle mechanism.

        Complexity:
            Best case: O(1) - when updating the team status (Set/ Rotate).
            Best case: O(n) - when updating the team status (Optimise).
        """
        return self.battle_mechanism.update_team_status(trainer, team, pokemon, attribute)

    def _create_teams(self) -> Tuple[PokeTeam, PokeTeam]:
        """
        Creates teams for the battle.

        Returns:
            Tuple[PokeTeam, PokeTeam]: A tuple containing the team objects of both trainers.

        Preconditions:
            None

        Postconditions:
            Creates teams for the battle.

        Complexity:
            Best case: O(1) - when the trainer picks a team (with team size limit of 1) randomly.
            Worst case: O(n) - when the trainer picks a team randomly with size up to size limit.
        """
        if len(self.trainer_1.get_team()) == 1:
            self.trainer_1.pick_team("Random")
        if len(self.trainer_2.get_team()) == 1:
            self.trainer_2.pick_team("Random")
        
        return [self.trainer_1.get_team(), self.trainer_2.get_team()]

