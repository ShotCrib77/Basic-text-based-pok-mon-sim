import random

pokemon_strengths = {
  "normal": [],
  "fire": ["grass", "ice", "bug", "steel"],
  "water": ["fire", "ground", "rock"],
  "electric": ["water", "flying"],
  "grass": ["water", "ground", "rock"],
  "ice": ["grass", "ground", "flying", "dragon"],
  "fighting": ["normal", "ice", "rock", "dark", "steel"],
  "poison": ["grass", "fairy"],
  "ground": ["fire", "electric", "poison", "rock", "steel"],
  "flying": ["grass", "fighting", "bug"],
  "psychic": ["fighting", "poison"],
  "bug": ["grass", "psychic", "dark"],
  "rock": ["fire", "ice", "flying", "bug"],
  "ghost": ["psychic", "ghost"],
  "dragon": ["dragon"],
  "dark": ["psychic", "ghost"],
  "steel": ["ice", "rock", "fairy"],
  "fairy": ["fighting", "dragon", "dark"]
}


class Pokemon:
  def __init__(self, name: str, level:int, base_stats: dict, type_1:str, type_2=None) -> None:
    self.name = name
    self.level = level
    self.type_1 = type_1
    self.type_2 = type_2
    
    # Stats
    self.health = base_stats["HP"]
    self.max_health = base_stats["HP"]
    self.attack = base_stats["Atk"]
    self.defense = base_stats["Def"]
    self.special_attack = base_stats["Sp.Atk"]
    self.special_defense = base_stats["Sp.Def"]
    self.speed = base_stats["Speed"]
    
  def description(self) -> None:
    print(f"\n{self.name} is a {self.type_1}{f'/{self.type_2}' if self.type_2 else ''}-type and is level {self.level}.")
    print(f"{self.name}'s stats: HP: {self.health}/{self.max_health}, Atk: {self.attack}, Def: {self.defense}, Sp.Atk: {self.special_attack}, Sp.Def: {self.special_defense}, Speed: {self.speed}")
    #print(f"{self.name} is a {self.type_1}{f'/{self.type_2}' if self.type_2 else ''}-type and is level {self.level} with {self.health} HP.")
    
  def train(self, levels=1) -> None:
    self.level += levels
    print(f"Pokemonen has leveled up to level {self.level}")
  
  def evolve(self, new_name) -> None:
    old_name = self.name
    self.name = new_name
    print(f"{old_name} has evolved to a {self.name}")
  
  def attack_pokemon(self, enemy:"Pokemon") -> None:
    effectiveness = self.calc_effectiveness(enemy)
    damage = self.level * 10 * effectiveness
    enemy.health -= damage
    
    print(f"{self.name} has attacked {enemy.name} and dealt {damage} damage!")
    
    if effectiveness > 1.0:
      print("It's super effective!")
    elif effectiveness < 1.0:
      print("It's not very effective...")
    
    if not enemy.is_alive():
      print(f"{enemy.name} fainted...")
      
  
  def calc_effectiveness(self, enemy:"Pokemon") -> int:
    effectiveness = 1.0
    # Check effectiveness of self.type_1 against both of the enemy's types
    if enemy.type_1.lower() in pokemon_strengths[self.type_1.lower()]:
      effectiveness *= 2.0
      
    if self.type_1.lower() in pokemon_strengths[enemy.type_1.lower()]:
      effectiveness *= 0.5
    
    if enemy.type_2:
      if enemy.type_2.lower() in pokemon_strengths[self.type_1.lower()]:
        effectiveness *= 2.0
      if self.type_1.lower() in pokemon_strengths[enemy.type_2.lower()]:
        effectiveness *= 0.5

    
    # Check effectiveness of self.type_2 against both of the enemy's types (if the Pokemon has a second type)
    if self.type_2:
      if enemy.type_1.lower() in pokemon_strengths[self.type_2.lower()]:
        effectiveness *= 2.0
      if self.type_2.lower() in pokemon_strengths[enemy.type_1.lower()]:
        effectiveness *= 0.5
        
      if enemy.type_2: # (If the enemy has a second type)
        if enemy.type_2.lower() in pokemon_strengths[self.type_2.lower()]:
          effectiveness *= 2.0
        if self.type_2.lower() in pokemon_strengths[enemy.type_2.lower()]:
          effectiveness *= 0.5
      
    return effectiveness

  
  def heal(self) -> None:
    self.health = self.max_health
    print(f"{self.name} has been heald to {self.max_health} HP!")
  
  def is_alive(self) -> bool:
    return self.health > 0

class BattleManager:
  def __init__(self) -> None:
    pass
  
  def generate_pokemon(self) -> Pokemon:
    with open("pokemon.txt", "r") as pokemon_file:
      pokemon_list = [[row.strip()] for row in pokemon_file.readlines()] # Creates sublists for every pokemon

      pokemon_num = random.randint(0, 150)
      generated_pokemon = pokemon_list[pokemon_num][0].split(" - ")
      pokemon_name = generated_pokemon[0].split(". ", 1)[1]
      pokemon_details = [pokemon_name] + generated_pokemon[1:]

      if "/" in pokemon_details[1]:
        type_1, type_2 = pokemon_details[1].split("/")
      else:
        type_1 = pokemon_details[1]
        type_2 = None

      pokemon_stats = pokemon_details[2].split(",")
      stats_dict = {}
      for stat in pokemon_stats:
        key, value = stat.split(": ")
        stats_dict[key.strip()] = int(value.strip())

      return Pokemon(pokemon_details[0], 5, stats_dict, type_1, type_2)
  
  def get_pokemon(self) -> None:
    pokemon_1 = self.generate_pokemon()
    pokemon_2 = self.generate_pokemon()
    
    pokemon_1.description()
    pokemon_2.description()
    