extends MarginContainer

func _ready():
    randomize()
    var py_code = get_node("python_code")
    var name_label = get_node("background/Layout/Info/HBoxContainer/VBoxContainer/Name")
    var personality_label = get_node("background/Layout/Info/HBoxContainer/VBoxContainer/Personality")
    var job_label = get_node("background/Layout/Info/HBoxContainer/VBoxContainer/Job")
    var npcs = []
    var COUNT = 0 # This should go up to 5, but no further.
    # All of the "jobs" an NPC can have.
    var jobs = ['peasent','aristocrat','farmer','soldier','warrior']
    # Fill up an array with the data for NPCs.
    for i in range(0,4):
        var job = jobs[ randi() % 5 ]
        var gender =' male' if randf() > 0.5 else 'female'
        var npc = py_code.create_npc(gender, job)
        npcs.append(npc)
    if npcs.size() == 0:
        print("'npcs' array is empty. Looks like we couldn't generate some NPCS.")
        get_tree().quit()
    elif typeof(npcs[COUNT]) == TYPE_NIL:
        print("Some NPC names were not generated!")
        get_tree().quit()
    # Assign the names and stuff to the labels in the GUI.
    name_label.text = "Name: " + npcs[COUNT]['name']
    personality_label.text = "Personality: " + npcs[COUNT]['personality']
    job_label.text = "Job: " + npcs[COUNT]['profession']
