init python:
  ## this dict list all possible attacks
  ## attack is defined by unique id and settings
  ## settings:
  ##   img: image used to represent attack
  ##   player_damage: damage done to player if attack reach ending point/surrender button
  ##   enemy_damage_good: damage done to enemy if attack is blocked while in "good" zone
  ##   enemy_damage_perfect: damage done to enemy if attack is blocked while in "perfect" zone
  mg_rhythm_attack_info={
    "default": {
      "img": "minigames/rhythm/attack_default.png",
      "player_damage": 1,
      "enemy_damage_good": 1,
      "enemy_damage_perfect": 2,
      },
    "super": {
      "img": "minigames/rhythm/attack_super.png",
      "player_damage": 3,
      "enemy_damage_good": 1,
      "enemy_damage_perfect": 5,
      },
    "super-heavy": {
      "img": "minigames/rhythm/attack_super.png",
      "player_damage": 5,
      "enemy_damage_good": 1,
      "enemy_damage_perfect": 10,
      },
    "dummy": {
      "img": "minigames/rhythm/attack_default.png",
      "player_damage": 1,
      "enemy_damage_good": 1,
      "enemy_damage_perfect": 3,
      },
    "mosquitto": {
      "img": "minigames/rhythm/attack_default.png",
      "player_damage": 1,
      "enemy_damage_good": 1,
      "enemy_damage_perfect": 3,
      },
    "mosquitto_no_damage": {
      "img": "minigames/rhythm/attack_default.png",
      "player_damage": 0,
      "enemy_damage_good": 1,
      "enemy_damage_perfect": 3,
      },
    }
