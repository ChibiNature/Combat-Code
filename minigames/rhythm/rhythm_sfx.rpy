init 999 python:
  ## when game is launched we preload all sounds used/referenced by rhythm data structures
  ## this should avoid any disk access during minigame, hopefully reducing any sfx lags
  ## we preload any dict element ending with _sound or _sounds, like blocked_default_sound etc
  ## we preload only direct file names with "." in it

  mg_rhythm_sfx_root="audio/"

  mg_rhythm_sfx_cache={}

  def mg_rhythm_preload_sfx():
    for el in list(mg_rhythm_elements_info.values())+[mg_rhythm_default_args]:
      for k,v in el.items():
        if k.endswith("sound"):
          v=[v]
        elif not k.endswith("sounds"):
          continue
        for sfx in v:
          if isinstance(sfx,basestring) and "." in sfx:
            sfx_path=mg_rhythm_sfx_root+sfx
            data=renpy.loader.load(sfx_path).read()
            mg_rhythm_sfx_cache[sfx]=AudioData(data,sfx_path)

  def mg_rhythm_play_sfx(sfx):
    sfx=mg_rhythm_sfx_cache.get(sfx,sfx)
    if sfx:
      renpy.play(sfx,channel="audio")

  mg_rhythm_preload_sfx()
