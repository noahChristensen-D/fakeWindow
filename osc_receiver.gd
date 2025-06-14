extends Node

@onready var camera = $"../WindowCamera"

var osc := UDPServer.new()
var port := 8000

var head_pos := Vector3.ZERO

func _ready():
	print("✅ OscReceiver is loaded")
	osc.listen(port)
	print("🔌 Listening on port", port, "status:", osc.is_connection_available())
	
func _process(_delta):
	while osc.is_connection_available():
		var packet = osc.take_packet()
		var path = packet.path
		var args = packet.arguments

		print("Received:", path, args)
		
		match path:
			"/head/x":
				head_pos.x = args[0]
			"/head/y":
				head_pos.y = args[0]
			"/head/z":
				head_pos.z = args[0]

		# Apply with some light scaling to make movement realistic
		camera.position = Vector3(
			head_pos.x * 0.5,     # shift camera left/right
			head_pos.y * 0.3,     # vertical tilt (optional)
			-2.0 + head_pos.z * 0.5  # adjust camera Z distance
		)
func _input(event):
	if event.is_action_pressed("quit"):
		get_tree().quit()
