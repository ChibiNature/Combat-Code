init python:
  ## this dict values used if start_rhythm_minigame called without providing specific value
  mg_rhythm_default_args={
    ## how long it takes for attack to reach surrender button and land attack
    "attack_time": 3.0,
    ## used only by random source
    "max_random_attacks": 5,
    ## used only by random source
    "time_between_same_target_random_attacks": 1.0,
    ## how much time should pass before we try to play flavor sound
    "flavor_time": 5.0,
    ## optional intro label to call before minigame starts, default show "Prepare" for few seconds
    "intro": "mg_rhythm_default_intro",
    ## optional outro label to call after minigame is finished, but still visible, default show white flash
    "outro": "mg_rhythm_default_outro",
    ## element id to use when showing hp bars, or None if should be invisible
    "player_hp_bar": None,
    "enemy_hp_bar": "enemy_hp_bar",
    ## element id to use when showing surrender button
    "surrender_id": "surrender",
    ## default sounds played if flavor sound is not played and element have no custom default sound
    "landed_default_sound": "minigames/rhythm/landed_default.mp3",
    "blocked_default_sound": "minigames/rhythm/blocked_default.mp3",
    "surrender_default_sound": None,
    ## player/enemy hp settings, if "hp" set to "max" then "max_hp" value used
    "max_hp": 5,
    "hp": "max",
    "enemy_max_hp": 10,
    "enemy_hp": "max",
    ## visible targets id
    "targets": ["top-left","bottom-left","top-right","bottom-right"],
    ## default attack used if there is no special attacks to be launched
    "default_attack": "default",
    ## attacks source:
    ## None: unlimited random notes, always use default attack
    ## integer: limited random notes, always use default attack, can result in "exhaused" ending
    ## list of [count,[attack,attack,...]]: limited by count notes, selected randomly from attacks list
    ## string: hardcoded notes, single string with multiple lines, empty lines are ignored
    ##   line format: attack->target,attack->target,attack->target@timestamp
    ##   there can be one or multiple attack->target parts, separated by comma
    ##   attack-> part is optional, if not provided then default attack will be used
    ##   target part can be either target id or number in targets list, 1 - first, 2 - second etc
    ## string starting with "$": name of callable, callable will be used as source function
    ## list/tuple of [[[[attack,target],...],timestamp],...]: hardcoded and already converted notes
    "source": None,
    }
