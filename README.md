# FIT1008_S1_2024 - Pokemon

#### Basic Premise
Pokemon
The titular Pokemon are the backbone of the Pokemon Battles. There are different types of pokemon each with their own names and stats, and one type of pokemon can evolve into another type of pokemon when they level up.

Pokemon have the following information:

- Health
- Level
- Defence
- Type
- Battle Power (attack points)
- Name
- Evolution Line
- Experience
- Speed

These stats will be covered over the future tasks but here is a short overview of each of them:


1. Health - This is the stat that lets you know how many health points a Pokemon has before it faints. Once the Pokemon gets attacked, it loses some health and once the health drops to 0, the Pokemon faints

2. Level - This stat refers to the level that the Pokemon is on. Once a Pokemon battles another and makes it faint, the level of the Pokemon goes up by 1, boosting most of its other stats. 

3. Defence - This stat refers to the resistance that is offered by the Pokemon when it gets attacked. You will learn more about the use of this stat when we discuss battling.

4. Type - A Pokemon's type affects the amount of damage it can do to another Pokemon. You will learn more about this in Task 1.

5. Battle Power - This stat refers to the amount of base damage a Pokemon does to another during the course of a battle. 

6. Name - This refers to the name of the Pokemon

7. Evolution Line - This is a list of the Evolution names for this line of Pokemon. The length of this list can vary as many Pokemon don't evolve, evolve once or even twice in some cases! 

8. Experience - This stat refers to the experience that a Pokemon has. A pokemon gains experience from battling another pokemon.

9. Speed - This stat refers to the speed of the Pokemon. Speed determines how fast the Pokemon is and the faster Pokemon attacks first.


#### What is PokemonBase?
Because there are over 70 Pokemon to define, and we don't want to write out all the classes individually.  In particular, because almost all of the logic for all Pokemon are the same, all we have to do is define this shared logic in PokemonBase. Then Pokemon.py creates different classes, which all inherit from PokemonBase, and implements all of the abstract class methods at the bottom of pokemon_base.py.

For example, you can do the following without touching the assignment and it works just fine:


from pokemon import Charmander, Gastly

charmander = Charmander()
gastly = Gastly()

print(charmander.get_name())        # Charmander
print(charmander.get_poketype())    # PokeType.FIRE
print(gastly.get_evolution())       # ['Gastly', 'Haunter', 'Gengar']

#### Teams
Pokemon are combined to form teams, which are used in battle. There are multiple options for teams, such as the team mode, and selection mode.


#### Battling
Battling is done between two teams in a turn-based manner, where every "turn" includes an action from both teams. In a battle, each team selects one Pokemon to be currently out on the field, while the rest of each team waits to help out.

#### Battle anatomy

In a battle, turns continue to occur until one or both teams have no more pokemon left (in the team and on the field). If a pokemon on the field is killed (HP <= 0), then a new pokemon from the team is sent out at the end of the turn.

#### Turn anatomy

In a Battle turn, each team selects an action, either ATTACK  or SPECIAL. If SPECIAL is chosen, the pokemon is returned to the team, the method .special() is called on the team object, and a pokemon is retrieved from the team (possibly the same pokemon). If ATTACK is chosen, then the currently out-on-the-field pokemon attacks the currently out-on-the-field pokemon for the other team.

When determining the order and impact of Pokémon actions in a battle, there are specific rules and calculations to follow:

Action Order: SPECIAL actions are always resolved before ATTACK actions.

ATTACK Action Logic: If both Pokémon are set to attack in the same round, the Pokémon with the higher Speed stat will execute its attack first. If the slower Pokémon still has HP remaining after the first Pokémon’s attack, it will then have the opportunity to retaliate. If both Pokémon have equal Speed stats, they will both attack simultaneously. In this simultaneous attack scenario, the outcome of the attacks is not influenced by whether the defending Pokémon would still be alive after taking the damage.

Damage Calculation Process:

Step 1: Compute Base Damage:

The base damage is calculated by comparing the attacking Pokémon's Attack stat with the defending Pokémon's Defence stat.
If the Defence stat is less than half of the Attack stat, the damage is computed as the difference between the Attack and Defence stats.
If the Defence stat is less than the Attack stat but not less than half of it, the damage is calculated using the formula: ceil(Attack * 5/8 - Defence / 4).
If the Defence stat is equal to or greater than the Attack stat, the damage is computed as ceil(Attack / 4).
Step 2: Apply Damage Multipliers:

The initial damage value is then modified based on type effectiveness. Pokémon types interact with each other in specific ways; for example, Water-type Pokémon have an effectiveness coefficient of 2 against Fire-type Pokémon. This means the base damage is multiplied by 2 in such cases.
Additionally, the trainer's Pokedex completion is taken into account. This is done by calculating a multiplier based on the ratio of the attacking trainer's Pokedex completion to that of the defending trainer. This multiplier is then applied to the effective damage.
