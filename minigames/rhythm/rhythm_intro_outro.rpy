## default intro label

transform tf_mg_rhythm_starting_splash:
  align (0.5,0.5)
  alpha 0.0
  zoom 0.01
  easein 0.5 alpha 1.0 zoom 1.0
  1.0
  easeout 0.25 alpha 0.0

style mg_rhythm_starting_splash_text is default:
  size 192
  color "#FFF"
  outlines [(4,"#000")]

image mg_rhythm_starting_splash=Text("Prepare!",style="mg_rhythm_starting_splash_text")
## Text stating splash used for testing purposes, can replace it with actual image
#image mg_rhythm_starting_splash="minigames/rhythm/starting_splash.png"

label mg_rhythm_default_intro:
  show mg_rhythm_starting_splash at tf_mg_rhythm_starting_splash
  $renpy.pause(1.5,hard=True)
  return

## default outro label

transform tf_mg_rhythm_ending_flash:
  alpha 0.0
  0.25
  easein 0.1 alpha 1.0
  easeout 0.5 alpha 0.0
  easein 0.1 alpha 1.0
  easeout 0.5 alpha 0.0
  easein 0.25 alpha 1.0

image mg_rhythm_ending_flash=Solid("#FFF")

label mg_rhythm_default_outro:
  show mg_rhythm_ending_flash at tf_mg_rhythm_ending_flash
  $renpy.pause(3.0,hard=True)
  return
