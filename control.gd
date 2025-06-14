extends Control

@onready var fps_label = $FpsLabel
@onready var fps_toggle_button = $FPSToggleButton

var visible_fps := true

func _ready():
	fps_toggle_button.pressed.connect(_on_toggle_button_pressed)
	
func _process(_delta):
	if visible_fps:
		fps_label.text = "FPS: " + str(Engine.get_frames_per_second())
		
func _on_toggle_button_pressed():
	visible_fps = !visible_fps
	fps_label.visible = visible_fps
