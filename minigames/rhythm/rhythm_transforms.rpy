transform tf_mg_rhythm_landed(tag):
  rotate 0
  zoom 1.0
  alpha 1.0
  easein 0.1 zoom 1.35
  easeout 0.25 zoom 0.25 alpha 0.0
  ## next line should be last line of transform
  function mg_rhythm_remove_attack(tag)

transform tf_mg_rhythm_blocked(tag):
  rotate 0
  zoom 1.0
  alpha 1.0
  easein 0.35 rotate 360 zoom 0.25 alpha 0.0
  ## next line should be last line of transform
  function mg_rhythm_remove_attack(tag)
