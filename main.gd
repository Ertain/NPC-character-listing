extends MarginContainer

func _ready():
    randomize()
    var py_code = get_node("python_code")
    var npcs = []
    var jobs = ['peasent','aristocrat','farmer','soldier','warrior']
    for i in range(0,4):
        var job = jobs[ randi() % 4 ]
        var gender =' male' if randf() > 0.5 else 'female'
        var npc = py_code.create_npc(gender, job)
        npcs.append(npc)
