from poke_team import Trainer
from data_structures.queue_adt import CircularQueue
from battle import *
import random

__author__ = "Gue Zhen Xue"

class BattleTower:
    """
    Represents a Battle Tower where a player battles against multiple enemy trainers.

    Attributes:
    - MIN_LIVES: Minimum number of lives a trainer can have.
    - MAX_LIVES: Maximum number of lives a trainer can have.
    - battle_mode: The battle mode used in the tower (default is ROTATE).
    - my_trainer: The player's trainer object.
    - enemy_trainers: CircularQueue containing enemy trainer objects.
    - enemies_lives_remaining: CircularQueue containing the remaining lives of enemy trainers.
    - my_lives: The number of lives the player has.
    - enemy_lives_taken: The total number of enemy lives taken by the player.
    - battle_number: The number of battles that have occurred in the tower.
    """
    MIN_LIVES = 1
    MAX_LIVES = 3

    def __init__(self) -> None:
        """
        Initializes a new instance of the BattleTower class.
        """
        self.battle_mode = BattleMode.ROTATE
        self.my_trainer = None
        self.enemy_trainers = None
        self.enemies_lives_remaining = None

        self.my_lives = 0
        self.enemy_lives_taken = 0
        self.battle_number = 0

    def set_my_trainer(self, player_team: Trainer) -> None:
        """
        Sets the player's trainer and randomly assigns lives.

        Preconditions:
            A trainer instance must be called before.

        Args:
            player_team: A valid player (Trainer object).

        Postconditions:
        - The player's trainer is set.
        - The player's lives are set to a random value between MIN_LIVES and MAX_LIVES.

        Complexity:
        - Best & Worst Case: O(1) - setting the trainer and lives.

        Args:
            player_team (Trainer): The player's team (PokeTeam object).
        """
        self.my_trainer = player_team
        self.my_lives = random.randint(self.MIN_LIVES, self.MAX_LIVES)

    def generate_enemy_trainers(self, n) -> None:
        """
        Generates and adds enemy trainers to the tower.

        Args:
            n: A positive integer representing the number of enemy trainers to generate.

        Postconditions:
        - Enemy trainers are generated and added to the tower.

        Complexity:
            Best Case: O(1) - when only one enemy trainer is generated.
            Worst Case: O(n) - generating and adding enemy trainers.

        Args:
            n (int): The number of enemy trainers to generate.
        """
        self.enemy_trainers = CircularQueue(n)
        self.enemies_lives_remaining = CircularQueue(n)
        for i in range(n):
            trainer = Trainer(f"Trainer {str(i + 1)}")
            trainer.pick_team("Random")
            self.enemy_trainers.append(trainer)
            random_number = random.randint(self.MIN_LIVES, self.MAX_LIVES)
            self.enemies_lives_remaining.append(random_number)

    def battles_remaining(self) -> bool:
        """
        Checks if there are battles remaining in the tower.

        Returns:
        - bool: True if there are battles remaining, False otherwise.

        Complexity:
        - Best & Worst Case: O(1) - checking if battles are remaining.
        """
        return (self.my_lives > 0 and self.enemy_trainers)

    def next_battle(self) -> Tuple[Trainer, Trainer, Trainer, int, int]:
        """
        Conducts the next battle in the tower.

        Returns:
        - tuple: A tuple containing the winner trainer, player trainer, enemy trainer, remaining player lives, and remaining enemy lives.

        Complexity:
            Best Case: O(1) - when one of the team have no team member.
            Worst Case: O(N) - conducting the next battle.
        """
        self.battle_number += 1
        enemy, enemy_lives, battle = self.initialise_battle()
        winner = battle.commence_battle() 
        if winner == enemy:
            self.my_lives -= 1
            self.determine_enemy_team(enemy, enemy_lives)
        elif winner == self.my_trainer:
            enemy_lives -= 1
            self.enemy_lives_taken += 1
            self.determine_enemy_team(enemy, enemy_lives)
        else:
            self.my_lives -= 1
            enemy_lives -= 1
            self.enemy_lives_taken += 1
            self.determine_enemy_team(enemy, enemy_lives)

        return winner, self.my_trainer, enemy, self.my_lives, enemy_lives

    def initialise_battle(self) -> Tuple[Trainer, int, Battle]:
        """
        Initializes a battle between the player and an enemy trainer.

        Returns:
        - tuple: A tuple containing the enemy trainer, remaining enemy lives, and the battle object.

        Complexity:
            Best case: O(n) - when regenerating the team without any specific criteria. (When Set or Rotate mode is called)
            Worst case: O(n^2) - when regenerating the team with specific criteria that require sorting. (When Optimise mode is called)
        """
        enemy, enemy_lives = self.enemy_trainers.serve(), self.enemies_lives_remaining.serve()
        battle = Battle(self.my_trainer, enemy, self.battle_mode)
        self.my_trainer.team_status.regenerate_team(self.battle_mode)
        enemy.team_status.regenerate_team(self.battle_mode)
        return enemy, enemy_lives, battle

    def determine_enemy_team(self, enemy, enemy_lives) -> None:
        """
        Determines if the enemy trainer should continue in the tower based on remaining lives.

        Args:
        - enemy: The enemy trainer.
        - enemy_lives: The remaining lives of the enemy trainer.

        Complexity:
        - Best & Worst Case: O(1) - determining the enemy team.
        """
        if enemy_lives > 0:
            self.enemy_trainers.append(enemy)    
            self.enemies_lives_remaining.append(enemy_lives) 

    def enemies_defeated(self) -> int:
        """
        Returns the total number of enemy lives taken by the player.

        Returns:
        - int: The total number of enemy lives taken.

        Complexity:
        - Best & Worst Case: O(1) - calculating the total enemy lives taken.
        """
        return self.enemy_lives_taken

