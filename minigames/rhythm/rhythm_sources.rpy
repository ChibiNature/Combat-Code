init python:
  ## random notes, optionally limited by notes_left count
  def mg_rhythm_source_random(attacks):
    time=mg_rhythm["time"]
    if len(mg_rhythm["attacks"])<mg_rhythm["max_random_attacks"]:
      if len(mg_rhythm["attacks"])==0 or (time-mg_rhythm["attacks"][-1]["stage_start"])>mg_rhythm["time_between_same_target_random_attacks"]:
        notes_left=mg_rhythm["notes_left"]
        if notes_left is None or notes_left>0:
          attack_id=renpy.random.choice(attacks)
          if not isinstance(attack_id,basestring):
            attack_id=renpy.random.choice(attack_id)
          target=renpy.random.choice(mg_rhythm["targets"])
          mg_rhythm_add_attack(attack_id,target)

  ## hardcoded notes
  def mg_rhythm_parse_notes(mg_rhythm,source):
    targets=mg_rhythm["targets"]
    rev_targets={target:n for n,target in enumerate(mg_rhythm["targets"])}
    rv=[]
    prev_timestamp=0.0
    for line in source.splitlines():
      line=line.strip()
      if line:
        notes,timestamp=line.split("@",1)
        notes=notes.split(",") if "," in notes else [notes]
        for n,note in enumerate(notes):
          attack,sep,target=note.strip().rpartition("->")
          if not attack:
            attack=mg_rhythm["default_attack"]
            if not isinstance(attack,basestring):
              attack=renpy.random.choice(attack)
          if target not in rev_targets:
            target=targets[int(target)-1]
          notes[n]=(attack,target)
        timestamp=timestamp.strip()
        if timestamp.startswith("+"):
          timestamp=float(timestamp[1:])+prev_timestamp
        else:
          timestamp=float(timestamp)
        prev_timestamp=timestamp
        rv.append((notes,timestamp))
    return rv

  def mg_rhythm_source_hardcoded(source):
    time=mg_rhythm["time"]
    while len(source)>0 and source[0][1]<time:
      notes,timestamp=source.pop(0)
      for attack_id,target in notes:
        mg_rhythm_add_attack(attack_id,target)

  ## internal source-related functions
  def mg_rhythm_prepare_source(mg_rhythm,source):
    mg_rhythm["notes_left"]=None
    if isinstance(source,basestring):
      ## custom note generator callable
      if source.startswith("$"):
        return (source[1:],None)
      ## else parse hardcoded notes into tuple
      source=mg_rhythm_parse_notes(mg_rhythm,source)
    if isinstance(source,(list,tuple)):
      if source[0] is None or isinstance(source[0],int):
        mg_rhythm["notes_left"]=source[0]
        return ("mg_rhythm_source_random",source[1])
      else:
        notes_left=0
        for notes,timestamp in source:
          notes_left+=len(notes)
        mg_rhythm["notes_left"]=notes_left
        return ("mg_rhythm_source_hardcoded",source[:])
    elif isinstance(source,int):
      mg_rhythm["notes_left"]=source
      return ("mg_rhythm_source_random",[mg_rhythm["default_attack"]])
    return ("mg_rhythm_source_random",[mg_rhythm["default_attack"]])

  def mg_rhythm_add_attack(attack_id,target):
    target_info=mg_rhythm_elements_info[target]
    attack={
      "id": attack_id,
      "target": target,
      "stage_start": mg_rhythm["time"],
      "progress": 0.0,
      "pos": target_info["attack_start"],
      "mode": "launched",
      "tag": mg_rhythm["attack_counter"],
      }
    mg_rhythm["attack_counter"]+=1
    mg_rhythm["attacks"].append(attack)
    if isinstance(mg_rhythm["notes_left"],int):
      mg_rhythm["notes_left"]-=1
    return attack
