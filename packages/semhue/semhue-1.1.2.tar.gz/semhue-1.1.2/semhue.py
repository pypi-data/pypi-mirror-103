from phue import Bridge
import random
import time

def rgb_to_xy(red, green, blue):
    """ 
    Conversion of RGB colors to CIE1931 XY colors
    Formulas implemented from: https://gist.github.com/popcorn245/30afa0f98eea1c2fd34d
    """

    # gamma correction
    red = pow((red + 0.055) / (1.0 + 0.055), 2.4) if red > 0.04045 else (red / 12.92)
    green = pow((green + 0.055) / (1.0 + 0.055), 2.4) if green > 0.04045 else (green / 12.92)
    blue =  pow((blue + 0.055) / (1.0 + 0.055), 2.4) if blue > 0.04045 else (blue / 12.92)

    # convert rgb to xyz
    x = red * 0.649926 + green * 0.103455 + blue * 0.197109
    y = red * 0.234327 + green * 0.743075 + blue * 0.022598
    z = green * 0.053077 + blue * 1.035763

    # convert xyz to xy
    x = x / (x + y + z)
    y = y / (x + y + z)
     
    return [x, y]

def turn_lights_on(room_name: str, IP_ADDRESS: str) -> bool:
    """
    Function for turning on the lights of a 
    room

    Params
    :room_name:     =>  name of the room in which light
                        color has to be turned on
    :IP_ADDRESS:    =>  IP address of the bridge
    """

    try:
        b = Bridge(IP_ADDRESS)
        b.set_group(b.get_group_id_by_name(room_name), "on", True)
        return True
    
    except:
        return False

def turn_lights_off(room_name: str, IP_ADDRESS: str) -> bool:
    """
    Function for turning off the lights of a 
    room

    Params
    :room_name:     =>  name of the room in which light
                        color has to be turned off
    :IP_ADDRESS:    =>  IP address of the bridge
    """

    try:
        b = Bridge(IP_ADDRESS)
        b.set_group(b.get_group_id_by_name(room_name), "on", False)
        return True

    except:
        return False

def random_color(room_name: str, IP_ADDRESS: str) -> bool:
    """
    Function for turning the lights of a 
    room to a random color

    Params
    :room_name:     =>  name of the room in which light
                        color has to be changed
    :IP_ADDRESS:    =>  IP address of the bridge
    """

    try:
        b = Bridge(IP_ADDRESS)
        lights = b.get_light_objects("name")

        b.set_group(b.get_group_id_by_name(room_name), "on", True)
        lights[room_name].brightness = 254
        lights[room_name].xy = [random.random(), random.random()]

        return True

    except:
        return False

def change_color(room_name: str, color: str, IP_ADDRESS: str) -> bool:
    """
    Function for turning the lights of a 
    room to a specified color

    Params
    :room_name:     =>  name of the room in which light
                        color has to be changed
    :color:         =>  name of the color (should be present in
                        color_list dictionary)
    :IP_ADDRESS:    =>  IP address of the bridge
    """

    try:
        color_list = {
            "red": [0.73, 0.24],
            "green": [0.11, 0.93],
            "blue": [0.16, 0.02],
            "orange ": [0.57, 0.39],
            "yellow": [0.42, 0.61],
            "purple": [0.28, 0.09],
            "pink": [0.41, 0.22],
            "normal": [0.40, 0.55] 
        }

        if color in list(color_list.keys()):
            b = Bridge(IP_ADDRESS)
            b.set_group(b.get_group_id_by_name(room_name), "on", True)

            xy = color_list[color]

            lights = b.get_light_objects("name")
            lights[room_name].brightness = 254
            lights[room_name].xy = xy

            return True
        
        else:
            return False

    except:
        return False

def loop_all_colors(room_name: str, IP_ADDRESS: str) -> bool:
    """
    Function for turning the lights of a 
    room to a random color

    Params
    :room_name:     =>  name of the room in which light
                        color has to be changed
    :IP_ADDRESS:    =>  IP address of the bridge
    """

    try:

    	while True:
	        color_list = {
	            "red": [0.73, 0.24],
	            "green": [0.11, 0.93],
	            "blue": [0.16, 0.02],
	            "orange ": [0.57, 0.39],
	            "yellow": [0.42, 0.61],
	            "purple": [0.28, 0.09],
	            "pink": [0.41, 0.22],
	            "normal": [0.40, 0.55] 
	        }

	        b = Bridge(IP_ADDRESS)

	        for color in color_list:
	            b.set_group(b.get_group_id_by_name(room_name), "on", True)
	            xy = color_list[color]

	            lights = b.get_light_objects("name")
	            lights[room_name].brightness = 254
	            lights[room_name].xy = xy
	            lights[room_name].transitiontime = 3

	        return True

    except:
        return False

def available_colors():
    """
    Prints the colors available for lights
    """
    color_list = [
        "red",
        "green",
        "blue",
        "orange ",
        "yellow",
        "purple",
        "pink",
        "normal"
    ]

    for color in color_list:
        print(color, end = ", ")

def set_brightness(room_name: str, brightness: int, IP_ADDRESS: str) -> bool:
    """
    Set custom brightness for a room

    Params
    :room_name:     =>  name of the room in which light
                        color has to be changed
    :brightness:    =>  brightness that has to be set
    :IP_ADDRESS:    =>  IP address of the bridge
    """
    try:
        b = Bridge(IP_ADDRESS)
        lights = b.get_light_objects("name")
        b.set_group(b.get_group_id_by_name(room_name), "on", True)
        lights[room_name].brightness = brightness

        return True

    except:
        return False

def get_rooms(IP_ADDRESS: str):
	"""
	Prints all the room names available

	Params
	:IP_ADDRESS:	=>	IP address of the bridge
	"""
	try:
		b = Bridge(IP_ADDRESS)
		lights = b.get_light_objects("name")

		for light in lights:
			print(light, end = ", ")

	except:
		return False

# color_list = {
#     "red": (255, 0, 0),
#     "green": (0, 255, 0),
#     "blue": (0, 0, 255),
#     "orange ": (225, 145, 0),
#     "yellow": (225, 225, 0),
#     "purple": (171, 0, 255),
#     "pink": (225, 0, 213),
#     "normal": (255, 200, 188) 
# }
