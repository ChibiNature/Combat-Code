default hero=Character("Hero")
default trainer=Character("Combat Trainer")
default orc=Character("Orc")
default boss=Character("Evil Boss")

## first fight sample
## we show tutorial, launch 10 random attacks, after game is done we tell how good player was

label first_fight_intro:
  ## can call tutorial screen instead
  trainer "You need to survive 10 attacks. When attack over defence button click on it."
  ## now show normal "Prepare" intro
  jump mg_rhythm_default_intro

label first_fight:
  trainer "You need to learn how to fight if you plan to go beyond Great Wall."
label first_fight_combat:
  call start_rhythm_minigame(
    ## show player hp
    player_hp_bar="player_hp_bar",
    enemy_max_hp=10,
    ## 10 random attacks
    source=10,
    ## custom intro label
    intro="first_fight_intro",
    ## we select only two targets
    targets=["top-left","bottom-right"],
    )
  scene bg with dissolve
  if _return=="win":
    if mg_rhythm["hp"]==mg_rhythm["max_hp"]:
      trainer "Flawless victory!"
    else:
      trainer "Good!"
  elif _return=="exhausted":
    trainer "Endurance victory! Well, at least you can survive long enough."
  elif _return=="surrender":
    menu:
      trainer "Hey, where are you going?! You need to learn how to fight if you want survive this cruel world!"
      "Right, i will try again":
        jump first_fight_combat
      "Nah, i have high charisma stat, will talk thru any problem":
        pass
  else:
    trainer "This will not do... Again!"
    jump first_fight_combat
  return

## mosquitto swarm, lots of tiny attacks, even when landed some do zero damage, generally you need to survive long enough
label mosquitto_fight_intro:
  hero "*Slap* *Slap* uuuggh *SLAP* *SLAP* *SLAP* AAAAAAARRGGHHH!!!111"
  jump mg_rhythm_default_intro

label mosquitto_fight:
  call start_rhythm_minigame(
    ## we set high hp values to make sure fight is long enough, yet there is possibility for every outcome
    max_hp=75,
    enemy_max_hp=99,
    ## we list same attack to "load dice", as result mosquitto_no_damage attack will be launched in 66%
    source=[250,["mosquitto","mosquitto_no_damage","mosquitto_no_damage"]],
    ## set random source settings for more and often attacks
    attack_time=1.5,
    max_random_attacks=25,
    time_between_same_target_random_attacks=0.25,
    )
  scene bg with dissolve
  if _return=="win":
    hero "*SLAP*SLAP*SLAP*SLAP* *SLAP* ... *slap* ... Anyone else?!"
    "Not only you got artifact, but also you have liberated this swamp from mosquittos! Well, at least for next 15 minutes..."
  elif _return=="exhausted":
    hero "Gaaah... Are you all well fed now?!! Little suckers! One day i will return and dry this whole swamp! You hear me?!!"
    "At least you got artifact."
  elif _return=="surrender":
    menu:
      "[[Botch the mission] Gah, i'm not going to feed whole swamp!":
        pass
      "[[Try again] THERE. IS. NO. PASSION!":
        jump mosquitto_fight
  else:
    "BAD ENDING: eaten by mosquittos\nAnd so hero died not a very noble or beautiful death..."
    jump game_over
  return

## orc, mix of normal and super attacks, fight till death, no "exhausted" option
label orc_fight:
  call start_rhythm_minigame(
    max_hp=10,
    enemy_max_hp=25,
    ## endless attacks, 33% is super attack to represent orc special skill
    source=[None,["default","default","super"]],
    )
  scene bg with dissolve
  if _return=="win":
    "Orc - slain, village - saved, you - paid."
  elif _return=="surrender":
    orc "Ahaha, you will become part of my harem, little squirmy thing! Will see how long you will last."
    "BED ENDING: harem ending\nDifferent kind of Harem Ending"
    jump game_over
  else:
    "BAD ENDING: died in battle\nLocal villagers will remember you for some time..."
    jump game_over
  return

## boss figth, hardcoded attacks, enemy is tough and hit hard, need to block most of attacks to win, no surrender option

init python:
  boss_fight_notes="""
    1,2,3,4@0.0
    super->1,super->top-right@1.0
    2,3@1.5
    super-heavy->bottom-left@3
    1,2,3,4@4
    super->1@+0.5
    2@+0.5
    super-heavy->3@+0.5
    4@+0.5
    super->1@+0.5
    2@+0.5
    super-heavy->3@+0.5
    4@+0.5
    super->1@+0.5
    2@+0.5
    super-heavy->3@+0.5
    4@+0.5
    super->1@+0.5
    2@+0.5
    super-heavy->3@+0.5
    4@+0.5
    super->1@+0.5
    2@+0.5
    super-heavy->3@+0.5
    4@+0.5
    super->1@+0.5
    2@+0.5
    super-heavy->3@+0.5
    4@+0.5
    super->1@+0.5
    2@+0.5
    super-heavy->3@+0.5
    4@+0.5
    """

label boss_fight:
  boss "Another fool came looking for death. I will oblige!"
  call start_rhythm_minigame(
    max_hp=25,
    enemy_max_hp=99,
    surrender_id=None,
    source=boss_fight_notes,
    )
  if _return=="win":
    scene bg with dissolve
    "And so the Great Evil is slain by hand of Great Hero!"
  elif _return=="exhausted":
    scene bg with dissolve
    "You fought for hours and both are exhausted. Gathering all you have you thrust one last time and by great skill or pure luck managed to strike very heart of Great Adversary! With deafening roar abomination falls dead."
  else:
    scene black with dissolve
    boss "Yet another skull for my Throne!"
    "BAD ENDING: died in battle\nYet another soul lost in struggle against forces of evil"
    jump game_over
  return

###########

image bg=Solid("#48F")

label game_over:
  ## forced exit to main menu
  $MainMenu(confirm=False)()
  return

label start:
  $quick_menu=False
  play music "audio/boss_fight/boss_fight_music.mp3"
  scene bg with dissolve
  "Winter, 521AH - Capital City, Adventurers Guild\nYou decided to become an adventurer, after you filled all papers guild master sent you to combat trainer."
  call first_fight
  "Summer, 523AH - Eastern Swamps\nAfter some easy missions you accepted mission in swamps to recover long lost artifact, there surprisingly little monsters, but mosquittos really got you..."
  call mosquitto_fight
  "Spring, 529AH - Draynor Village\nRich (but not {i}that{/i} Draynor) village is terrorized by orcs band, you decided to take this lucrative contract."
  call orc_fight
  "Winter, 543AH - Dark Castle\nAs most experienced and resourceful adventurer it was up to you to finally end Dominion of Horrorspawn."
  call boss_fight
  "Spring, 544AH - Capital City, Royal District\nAfter your great victory you decided to settle down, with money earned and noble title earned you bought grand estate next to royal palace. Legends of your adventures are written in books and told in taverns."
  "GOOD ENDING: rich and famous\nBecause hard work does not pays as good as killing things for money."
  return
