init python:
  import pygame

  ## this dict contains all minigame ui elements and targets
  mg_rhythm_elements_info={
    ## hp bars
    ##   place: ((posx,posy),(anchorx,anchory),(offsetx,offsety))
    ##   size: (w,h)
    ##   empty_img: background image
    ##   full_img: foregound image, cropped based on max_hp/hp
    "player_hp_bar": {
      "place": ((0.5,850),(0.5,1.0),(0,-5)),
      "size": (400,30),
      "empty_img": "minigames/rhythm/hp_bar_empty.png",
      "full_img": "minigames/rhythm/hp_bar_full.png",
      },
    "enemy_hp_bar": {
      "place": ((0.5,850),(0.5,0.0),(0,5)),
      "size": (600,40),
      "empty_img": "minigames/rhythm/hp_bar_empty.png",
      "full_img": "minigames/rhythm/hp_bar_full.png",
      },

    ## surrender buttons
    ## more than one surrender button can be defined if different minigame layout needed
    ##   btn_place: ((posx,posy),(anchorx,anchory),(offsetx,offsety))
    ##   btn_bg: image
    ##   surrender_button: should be True if element is surrender button, False or not present otherwise
    ##   surrender_default_sound: played when player click "Surrender" button
    ##   surrender_flavor_sounds: list of optional flavor sounds, make little sense for surrender button
    "surrender": {
      "btn_place": ((0.5,0.5),(0.5,0.5),(0,0-125)),
      "btn_bg": "minigames/rhythm/el_surrender.png",
      "surrender_button": True,
      "surrender_default_sound": "minigames/rhythm/landed_default.mp3",
#      "surrender_flavor_sounds": [
#        "minigames/rhythm/blocked_1_1.mp3",
#        "minigames/rhythm/blocked_1_2.mp3",
#        "minigames/rhythm/blocked_1_3.mp3",
#        ],
      },

    ## target buttons
    ## target button position and attack paths is independent, be sure to update path if changed position
    ## attack moves from attack_start position to attack_end position
    ## once attack is at attack_end attack considered "landed"
    ## bad/good/perfect is defined by distant from attack position to perfect_center
    ## if player activate target when attack within good/perfect distance attack considered "blocked"
    ##   keys: list of keycodes to activate target, see https://www.pygame.org/docs/ref/key.html for values
    ##   btn_place: ((posx,posy),(anchorx,anchory),(offsetx,offsety))
    ##   btn_bg: image
    ##   attack_start: (x,y) of attack position when progress is 0%
    ##   attack_end: (x,y) of attack position when progress is 100%
    ##   perfect_center: (x,y) center of hit circle, distance is calculatd from here to each attack
    ##   perfect_radius: int, if target activated and distance is less than that attack is "perfect blocked"
    ##   good_radius: int, if target activated and distance is less than that attack is "good blocked", if more then not blocked
    ##   good_img: None/color/image, shown if target can "good block" attack, None - show nothing, color - show color rect
    ##   perfect_img: None/color/image, shown if target can "perfect block" attack, None - show nothing, color - show color rect
    ##   out_img: None/color/image, shown if no attacks in good_radius, None - show nothing, color - show color rect
    ##   blocked_default_sound: None/sound, played when flavor sound not defined or can't be played yet
    ##   blocked_flavor_sounds: None/list of sounds, optional flavor sounds
    ##   landed_default_sound: None/sound, played when flavor sound not defined or can't be played yet
    ##   landed_flavor_sounds: None/list of sounds, optional flavor sounds
    "top-left": {
      "keys": [pygame.K_1,pygame.K_a],
      "btn_place": ((0.5,0.5),(1.0,1.0),(-10,-10-125)),
      "btn_bg": "minigames/rhythm/el_quad_top_left.png",
      "attack_start": (-200,390-125),
      "attack_end": (960-160,390-125),
      "perfect_center": (960-390,390-125),
      "perfect_radius": 50,
      "good_radius": 125,
      "perfect_img": "#0F04",
      "good_img": "#FF04",
      "out_img": None,
      "blocked_flavor_sounds": [
        "minigames/rhythm/blocked_1_1.mp3",
        "minigames/rhythm/blocked_1_2.mp3",
        "minigames/rhythm/blocked_1_3.mp3",
        ],
      },
    "top-right": {
      "keys": [pygame.K_3,pygame.K_d],
      "btn_place": ((0.5,0.5),(0.0,1.0),(10,-10-125)),
      "btn_bg": "minigames/rhythm/el_quad_top_right.png",
      "attack_start": (1920+200,390-125),
      "attack_end": (960+160,390-125),
      "perfect_center": (960+390,390-125),
      "perfect_radius": 50,
      "good_radius": 125,
      "perfect_img": "#0F04",
      "good_img": "#FF04",
      "out_img": None,
      "blocked_flavor_sounds": [
        "minigames/rhythm/blocked_2_1.mp3",
        "minigames/rhythm/blocked_2_2.mp3",
        "minigames/rhythm/blocked_2_3.mp3",
        ],
      },
    "bottom-left": {
      "keys": [pygame.K_2,pygame.K_s],
      "btn_place": ((0.5,0.5),(1.0,0.0),(-10,10-125)),
      "btn_bg": "minigames/rhythm/el_quad_bottom_left.png",
      "attack_start": (-200,1080-390-125),
      "attack_end": (960-160,1080-390-125),
      "perfect_center": (960-390,1080-390-125),
      "perfect_radius": 50,
      "good_radius": 125,
      "perfect_img": "#0F04",
      "good_img": "#FF04",
      "out_img": None,
      "blocked_flavor_sounds": [
        "minigames/rhythm/blocked_3_1.mp3",
        "minigames/rhythm/blocked_3_2.mp3",
        "minigames/rhythm/blocked_3_3.mp3",
        ],
      },
    "bottom-right": {
      "keys": [pygame.K_4,pygame.K_f],
      "btn_place": ((0.5,0.5),(0.0,0.0),(10,10-125)),
      "btn_bg": "minigames/rhythm/el_quad_bottom_right.png",
      "attack_start": (1920+200,1080-390-125),
      "attack_end": (960+160,1080-390-125),
      "perfect_center": (960+390,1080-390-125),
      "perfect_radius": 50,
      "good_radius": 125,
      "perfect_img": "#0F04",
      "good_img": "#FF04",
      "out_img": None,
      ## can add target-specific default sounds, along with flavor sounds
      ## all sound entries are optional and minigame defaults will be used if not provided by element
#      "blocked_default_sound": "minigames/rhythm/blocked_default.mp3",
      "blocked_flavor_sounds": [
        "minigames/rhythm/blocked_4_1.mp3",
        "minigames/rhythm/blocked_4_2.mp3",
        "minigames/rhythm/blocked_4_3.mp3",
        ],
#      "landed_default_sound": "minigames/rhythm/landed_default.mp3",
#      "landed_flavor_sounds": [],
      },
    }
