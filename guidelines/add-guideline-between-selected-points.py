# MenuTitle: Make guideline between selected points
__doc__ = """
	Add an angled guideline in the center of two currently selected nodes.
"""

import math

font = Glyphs.font
selectedLayer = font.selectedLayers[0]

firstNode = selectedLayer.selection[0]
lastNode = selectedLayer.selection[-1]


def calculate_angle(point1, point2):
    # Unpack the tuples
    x1, y1 = point1.x, point1.y
    x2, y2 = point2.x, point2.y

    # Calculate the differences in x and y coordinates
    delta_x = x2 - x1
    delta_y = y2 - y1

    # Calculate the angle in radians
    angle_radians = math.atan2(delta_y, delta_x)

    # Convert the angle to degrees
    angle_degrees = math.degrees(angle_radians)

    return angle_degrees


guideLine = GSGuide()

posX, posY = (firstNode.x + lastNode.x) / 2, (firstNode.y + lastNode.y) / 2

guideLine.position = (posX, posY)

guideLine.angle = calculate_angle(firstNode, lastNode)

selectedLayer.guides.append(guideLine)
