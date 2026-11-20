# MenuTitle: Make guideline between selected points
__doc__ = """
	Add an angled guideline in the center of two currently selected nodes.
"""

import math

from GlyphsApp import Glyphs, GSGuide, Message

font = Glyphs.font
selectedLayers = font.selectedLayers

if not selectedLayers:
	Message("Select a glyph layer first.", title="Make guideline between selected points")
else:
	selectedLayer = selectedLayers[0]
	selection = selectedLayer.selection

	if len(selection) < 2:
		Message("Select at least two nodes.", title="Make guideline between selected points")
	else:
		firstNode = selection[0]
		lastNode = selection[-1]

		def calculate_angle(point1, point2):
			x1, y1 = point1.x, point1.y
			x2, y2 = point2.x, point2.y
			delta_x = x2 - x1
			delta_y = y2 - y1
			return math.degrees(math.atan2(delta_y, delta_x))

		guideLine = GSGuide()
		guideLine.position = ((firstNode.x + lastNode.x) / 2, (firstNode.y + lastNode.y) / 2)
		guideLine.angle = calculate_angle(firstNode, lastNode)
		selectedLayer.guides.append(guideLine)
