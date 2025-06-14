extends Node3D

@onready var cam = $WindowCamera

var speed := 1.0

func _process(delta):
	var move := Vector3.ZERO
	
	if Input.is_key_label_pressed(KEY_W):
		move.z -= 1
	if Input.is_key_label_pressed(KEY_S):
		move.z += 1
	if Input.is_key_label_pressed(KEY_A):
		move.x -= 1
	if Input.is_key_label_pressed(KEY_D):
		move.x += 1
		
	cam.position += move * speed * delta

func _input(event):
	if event.is_action_pressed("quit"):
		get_tree().quit()
