init python:
  import pygame
  import time
  import math

  class RhythmMinigameDisplayable(renpy.Displayable):
    def __init__(self,*args,**kwargs):
      super(RhythmMinigameDisplayable,self).__init__(*args,**kwargs)
      ## size will be updated during first render
      self.width=config.screen_width
      self.height=config.screen_height
      self.last_frame_time=0.0
      ## internal render cache
      self.img_cache={}
      ## place to store some input events to catch them all
      self.queued_input_events=[]
    @property
    def paused(self):
      ## internally set pause
      rv=mg_rhythm["paused"]
      ## player can pause, overriding internal settings
      if mg_rhythm["player_paused"]:
        rv="full"
      ## if there is any system renpy screens then stop all animations
      if renpy.get_screen("confirm") or _menu:
        rv="full"
      return rv
    def end_minigame(self,rv):
      ## clean up internal stuff
      self.img_cache={}
      self.queued_input_events=[]
      ## save minigame result to external variable
      mg_rhythm["result"]=rv
    def img(self,img_name,mode=None):
      ## internal render cache, improve performance a bit
      img=self.img_cache.get((img_name,mode))
      if img is None:
        img=renpy.displayable(img_name)
        img=img.render(self.width,self.height,mg_rhythm["time"],mg_rhythm["time"])
        self.img_cache[(img_name,mode)]=img
      return img
    def play_flavor_sound(self,sound_type,target):
      target_info=mg_rhythm_elements_info[target]
      sfx=None
      ## if it was long enough then try to use target flavor sound
      if mg_rhythm["flavor_timer"]>mg_rhythm["flavor_time"]:
        flavor_sounds=target_info.get(sound_type+"_flavor_sounds")
        if flavor_sounds:
          sfx=renpy.random.choice(flavor_sounds)
          mg_rhythm["flavor_timer"]=0.0
      ## if no flavor sound used then try use target default sound
      if not sfx:
        sfx=target_info.get(sound_type+"_default_sound")
      ## if no appropriate target sound found then try to use minigame default sound
      if not sfx:
        sfx=mg_rhythm.get(sound_type+"_default_sound")
      ## play sound if found any appropriate
      if sfx:
        mg_rhythm_play_sfx(sfx)
    def block_attack(self,attack,target):
      ## try to block attack, marking attack as "blocked" and hurting enemy if successfuly
      ## moved to separate method to allow more complex code without copy-paste
      if attack["target"]==target:
        target_info=mg_rhythm_elements_info[target]
        if attack["dist"]<target_info["good_radius"]:
          attack["mode"]="blocked"
          attack["stage_start"]=mg_rhythm["time"]
          attack_info=mg_rhythm_attack_info[attack["id"]]
          if attack["dist"]<target_info["perfect_radius"]:
            mg_rhythm["enemy_hp"]-=attack_info["enemy_damage_perfect"]
          else:
            mg_rhythm["enemy_hp"]-=attack_info["enemy_damage_good"]
          self.play_flavor_sound("blocked",target)
    def land_attack(self,attack):
      ## mark attack as "landed" and hurt player
      ## moved to separate method to allow more complex code without copy-paste
      attack_info=mg_rhythm_attack_info[attack["id"]]
      mg_rhythm["hp"]-=attack_info["player_damage"]
      attack["mode"]="landed"
      attack["stage_start"]=mg_rhythm["time"]
      self.play_flavor_sound("landed",attack["target"])
    def generate_attacks(self):
      ## we don't check if source is valid, as we want code fail early so we can detect errors
      source,source_args=mg_rhythm["source"]
      source=getattr(store,source,None)
      source(source_args)
    def render(self,width,height,st,at):
      ## update sizes and prepare actual render
      self.width=width
      self.height=height
      rv=renpy.Render(width,height)
      ## update input devices states
      mx,my=renpy.get_mouse_pos()
      ## update time, calc deltas
      current_time=time.time()
      if self.last_frame_time>current_time:
        self.last_frame_time=current_time
      time_delta=min(0.05,current_time-self.last_frame_time)
      if self.paused!="full":
        mg_rhythm["time"]+=time_delta
      if not self.paused:
        mg_rhythm["flavor_timer"]+=time_delta
      self.last_frame_time=current_time
      attack_progress_delta=0.0 if self.paused else time_delta/mg_rhythm["attack_time"]
      ## generate attacks
      if not self.paused:
        self.generate_attacks()
      ## update active attacks positions/states, target dists
      target_dists={}
      for attack in mg_rhythm["attacks"]:
        if attack["mode"]=="launched":
          target=attack["target"]
          target_info=mg_rhythm_elements_info[target]
          attack_info=mg_rhythm_attack_info[attack["id"]]
          attack["progress"]=progress=min(1.0,attack["progress"]+attack_progress_delta)
          x0,y0=target_info["attack_start"]
          x1,y1=target_info["attack_end"]
          x=int(x0+(x1-x0)*progress)
          y=int(y0+(y1-y0)*progress)
          attack["pos"]=(x,y)
          if progress>=1.0:
            self.land_attack(attack)
          else:
            cx,cy=target_info["perfect_center"]
            attack["dist"]=dist=math.sqrt((cx-x)*(cx-x)+(cy-y)*(cy-y))
            if dist<target_dists.get(target,9999):
              target_dists[target]=dist
      ## render buttons and update hovered status
      clickables=[]
      hovered=None
      for target in list(mg_rhythm["targets"])+[mg_rhythm["surrender_id"]]:
        if target:
          target_info=mg_rhythm_elements_info[target]
          img=self.img(target_info["btn_bg"])
          placement=[v for l in target_info["btn_place"] for v in l]+[False]
          x,y=renpy.display.core.place(width,height,img.width,img.height,placement)
          rv.blit(img,(x,y))
          clickables.append([target,img,x,y])
          if hovered is None and img.is_pixel_opaque(mx-x,my-y):
            hovered=target
      ## render target states
      for target in mg_rhythm["targets"]:
        target_info=mg_rhythm_elements_info[target]
        dist=target_dists.get(target,9999)
        if dist<target_info["perfect_radius"]:
          img=target_info["perfect_img"]
          img_radius=target_info["perfect_radius"]
        elif dist<target_info["good_radius"]:
          img=target_info["good_img"]
          img_radius=target_info["good_radius"]
        else:
          img=target_info["out_img"]
          img_radius=target_info["good_radius"]
        if img:
          img=renpy.easy.displayable(img)
          if isinstance(img,Solid):
            img=img.render(img_radius*2,img_radius*2,mg_rhythm["time"],mg_rhythm["time"])
          else:
            img=img.render(width,height,mg_rhythm["time"],mg_rhythm["time"])
          rv.blit(img,(target_info["perfect_center"][0]-img.width//2,target_info["perfect_center"][1]-img.height//2))
      ## process queued events
      for event in self.queued_input_events:
        ## process clickable elements
        if event[0] in ["mouse_down","mouse_up"]:
          if not self.paused:
            emx,emy=event[1],event[2]
            for target,img,x,y in clickables:
              if img.is_pixel_opaque(emx-x,emy-y):
                target_info=mg_rhythm_elements_info[target]
                if target_info.get("surrender_button"):
                  if event[0]=="mouse_up":
                    self.end_minigame("surrender")
                    self.play_flavor_sound("surrender",target)
                else:
                  if event[0]=="mouse_down":
                    for attack in mg_rhythm["attacks"]:
                      if attack["mode"]=="launched":
                        self.block_attack(attack,target)
                break
        ## process target keys
        elif event[0]=="keyup":
          if not self.paused:
            target=mg_rhythm["keymap"].get(event[1])
            if target:
              for attack in mg_rhythm["attacks"]:
                if attack["mode"]=="launched":
                  self.block_attack(attack,target)
              break
      self.queued_input_events=[]
      ## render attacks
      for attack in mg_rhythm["attacks"]:
        target_info=mg_rhythm_elements_info[attack["target"]]
        attack_img=mg_rhythm_attack_info[attack["id"]]["img"]
        if attack["mode"]=="launched":
          img=self.img(attack_img)
          x,y=attack["pos"]
          rv.blit(img,(x-img.width//2,y-img.height//2))
        elif attack["mode"]=="landed":
          t=mg_rhythm["time"]-attack["stage_start"]
          img=tf_mg_rhythm_landed(attack["tag"])(attack_img).render(width,height,t,t)
          x,y=attack["pos"]
          rv.blit(img,(x-img.width//2,y-img.height//2))
        elif attack["mode"]=="blocked":
          t=mg_rhythm["time"]-attack["stage_start"]
          img=tf_mg_rhythm_blocked(attack["tag"])(attack_img).render(width,height,t,t)
          x,y=attack["pos"]
          rv.blit(img,(x-img.width//2,y-img.height//2))
      ## render hp bars
      t=mg_rhythm["time"]
      for hp_bar_id,max_hp_id,hp_id,invert_hp_bar in (("player_hp_bar","max_hp","hp",False),("enemy_hp_bar","enemy_max_hp","enemy_hp",True)):
        hp_bar_id=mg_rhythm[hp_bar_id]
        if hp_bar_id:
          hp_bar_info=mg_rhythm_elements_info[hp_bar_id]
          hp_empty=Transform(renpy.easy.displayable(hp_bar_info["empty_img"]),size=hp_bar_info["size"])
          hp_emptyr=hp_empty.render(width,height,t,t)
          hp_full=Transform(renpy.easy.displayable(hp_bar_info["full_img"]),size=hp_bar_info["size"])
          hp_fullr=hp_full.render(width,height,t,t)
          placement=[v for l in hp_bar_info["place"] for v in l]+[False]
          x,y=renpy.display.core.place(width,height,hp_emptyr.width,hp_emptyr.height,placement)
          rv.blit(hp_emptyr,(x,y))
          hp_bar_range=mg_rhythm[max_hp_id]
          hp_bar_value=(mg_rhythm[max_hp_id]-mg_rhythm[hp_id]) if invert_hp_bar else mg_rhythm[hp_id]
          rv.blit(Crop((0,0,int(hp_fullr.width*hp_bar_value/hp_bar_range),hp_fullr.height),hp_full).render(width,height,t,t),(x,y))
      ## remove finished attacks
      mg_rhythm["attacks"]=[attack for attack in mg_rhythm["attacks"] if attack["mode"]!="finished"]
      ## check end game conditions
      ## exhausted notes ending
      if mg_rhythm["notes_left"] is not None:
        if mg_rhythm["notes_left"]<=0 and len(mg_rhythm["attacks"])==0:
          self.end_minigame("exhausted")
      ## player lost ending
      if mg_rhythm["hp"]<=0:
        for attack in mg_rhythm["attacks"]:
          if attack["mode"]=="launched":
            attack["mode"]="landed"
            attack["stage_start"]=mg_rhythm["time"]
        self.end_minigame("lose")
      ## player win ending
      if mg_rhythm["enemy_hp"]<=0:
        for attack in mg_rhythm["attacks"]:
          if attack["mode"]=="launched":
            attack["mode"]="blocked"
            attack["stage_start"]=mg_rhythm["time"]
        self.end_minigame("win")
      ## tell renpy we want minigame redrawn every frame
      renpy.redraw(self,0)
      ## clean up cached renders so they wouldn't mess with save system
      self.img_cache={}
      return rv
    def event(self,ev,x,y,st):
      ## make sure event method called every frame
      renpy.game.interface.timeout(0)
      if mg_rhythm["result"] and renpy.get_screen("mg_rhythm_controller"):
        mg_rhythm["paused"]="attacks"
        return mg_rhythm["result"]
      ## process mouse events, saving them into queue
      if self.paused!="full":
        if ev.type==pygame.MOUSEBUTTONDOWN and ev.button==1:
          self.queued_input_events.append(["mouse_down",x,y])
          raise renpy.IgnoreEvent()
        if ev.type==pygame.MOUSEBUTTONUP and ev.button==1:
          self.queued_input_events.append(["mouse_up",x,y])
          raise renpy.IgnoreEvent()
      if self.paused!="full":
        if ev.type==pygame.KEYDOWN:
          key=(ev.key,ev.mod)
          if key in mg_rhythm["keymap"]:
            self.queued_input_events.append(["keydown",key])
            raise renpy.IgnoreEvent()
        if ev.type==pygame.KEYUP:
          key=(ev.key,ev.mod)
          if key in mg_rhythm["keymap"]:
            self.queued_input_events.append(["keyup",key])
            raise renpy.IgnoreEvent()

  ## this is used by transforms to mark attack as "finished" after animation is done
  class mg_rhythm_remove_attack(object):
    def __init__(self,tag):
      self.tag=tag
    def __call__(self,tf,st,at):
      for n,attack in enumerate(mg_rhythm["attacks"]):
        if attack["tag"]==self.tag:
          attack["mode"]="finished"
          break

## main minigame screen, shown while minigame is not completely ended
screen mg_rhythm_main():
  layer "master"
  add RhythmMinigameDisplayable()

## minigame controller screen, once controller hidden minigame start ending process
screen mg_rhythm_controller():
  imagebutton:
    xalign 0.5
    yalign 0.97
    if mg_rhythm["player_paused"]:
      idle "minigames/rhythm/btn_unpause.png"
    else:
      idle "minigames/rhythm/btn_pause.png"
    action ToggleDict(mg_rhythm,"player_paused")

init python:
  ## setting sane default parameters if not supplied by caller
  import inspect

  def mg_rhythm_init_arg_from_settings(arg_name,default_value=None):
    scope=inspect.currentframe().f_back.f_locals
    mg_rhythm=scope["rv"]
    kwargs=scope["kwargs"]
    mg_rhythm[arg_name]=kwargs.get(arg_name,mg_rhythm_default_args.get(arg_name,default_value))

  def mg_rhythm_init(**kwargs):
    init=mg_rhythm_init_arg_from_settings
    rv={}
    rv["result"]=None
    ## time related
    rv["time"]=0.0
    init("attack_time",3.0)
    init("flavor_time",5.0)
    rv["flavor_timer"]=0.0
    rv["paused"]=False
    rv["player_paused"]=False
    ## intro/outro
    init("intro","mg_rhythm_default_intro")
    init("outro","mg_rhythm_default_outro")
    ## ui settings
    init("player_hp_bar",None)
    init("enemy_hp_bar","enemy_hp_bar")
    init("surrender_id","surrender")
    ## audio related
    init("landed_default_sound",None)
    init("blocked_default_sound",None)
    init("surrender_default_sound",None)
    ## hp values
    init("max_hp",5)
    init("hp","max")
    if rv["hp"]=="max":
      rv["hp"]=rv["max_hp"]
    init("enemy_max_hp",10)
    init("enemy_hp","max")
    if rv["enemy_hp"]=="max":
      rv["enemy_hp"]=rv["enemy_max_hp"]
    ## possible targets
    init("targets",["top-left","top-right","bottom-left","bottom-right"])
    ## attacks/notes source
    init("default_attack","default")
    init("source",None)
    rv["source"]=mg_rhythm_prepare_source(rv,rv["source"])
    init("max_random_attacks",5)
    init("time_between_same_target_random_attacks",1.0)
    ## build targets keymap
    rv["keymap"]={}
    for target in rv["targets"]:
      target_info=mg_rhythm_elements_info[target]
      keys=target_info.get("keys")
      if keys:
        for key in keys:
          if key:
            if not isinstance(key,tuple):
              key=(key,pygame.KMOD_NONE)
            rv["keymap"][key]=target
    ## attacks bookkeeping
    rv["attack_counter"]=0
    rv["attacks"]=[]
    return rv

## this label called to play minigame, named arguments used to initialize minigame
label start_rhythm_minigame(**kwargs):
  ## init minigame variables, show main minigame screen
  $mg_rhythm=mg_rhythm_init(**kwargs)
  $mg_rhythm["paused"]="full"
  show screen mg_rhythm_main
  ## show intro/"prepare!"/tutorial if any
  if mg_rhythm["intro"]:
    call expression mg_rhythm["intro"]
  ## enter minigame main mode
  $mg_rhythm["paused"]=False
  call screen mg_rhythm_controller
  ## show outro/combat stage note/flashing if any
  if mg_rhythm["outro"]:
    call expression mg_rhythm["outro"]
  ## report minigame result back to caller
  return mg_rhythm["result"]
