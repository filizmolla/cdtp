def generate_gcode(rectangle_positions):
    gcode = ""

    for i in range(len(rectangle_positions)):
        x, y = rectangle_positions[i]

        # Move to the starting point of the rectangle
        gcode += f"G0 X{x} Y{y} ; Move to starting point\n"

        # Cut the rectangle
        gcode += f"G1 X{x} Y{y} ; Start cutting\n"
        gcode += f"G1 X{x + width} Y{y} ; Cut top side\n"
        gcode += f"G1 X{x + width} Y{y - height} ; Cut right side\n"
        gcode += f"G1 X{x} Y{y - height} ; Cut bottom side\n"
        gcode += f"G1 X{x} Y{y} ; Cut left side\n"

    return gcode

# Example coordinates for rectangles
rectangle_positions = [(0, 0), (5, 5), (10, 10)]
width = 2
height = 3

# Generate G-code
gcode_output = generate_gcode(rectangle_positions)

# Save the G-code to a file
with open("output.gcode", "w") as file:
    file.write(gcode_output)
