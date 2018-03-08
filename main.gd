extends MarginContainer

onready var COUNT = 0 # This should go up to 5, but no further.
onready var py_code = get_node("python_code")
onready var name_label = get_node("background/Layout/Info/HBoxContainer/VBoxContainer/Name")
onready var personality_label = get_node("background/Layout/Info/HBoxContainer/VBoxContainer/Personality")
onready var job_label = get_node("background/Layout/Info/HBoxContainer/VBoxContainer/Job")
var npcs = []

func add_or_subtract(modifier):
    if modifier == "-1":
        COUNT -= 1
    else:
        COUNT += 1
    COUNT = clamp(COUNT, 0, 4)

func _ready():
    randomize()
    # All of the "jobs" an NPC can have.
    var jobs = ['peasent','aristocrat','farmer','shopkeeper','warrior']
    # Fill up an array with the data for NPCs.
    for i in range(0, jobs.size() ):
        var job = jobs[ randi() % ( jobs.size() ) ]
        var gender ='male' if randf() > 0.5 else 'female'
        var npc = py_code.create_npc(gender, job)
        npcs.append(npc)

func _process(change_in_frame):
    # Assign the names and stuff to the labels in the GUI.
    name_label.text = "Name: " + npcs[COUNT]['name']
    personality_label.text = "Personality: " + npcs[COUNT]['personality']
    job_label.text = "Job: " + npcs[COUNT]['profession']

func _on_Left_Arrow_pressed():
    add_or_subtract("-1")

func _on_Right_Arrow_pressed():
    add_or_subtract("+1")
