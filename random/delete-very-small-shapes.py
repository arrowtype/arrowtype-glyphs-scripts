# MenuTitle: Delete very small shapes (clean up traced paths)
__doc__ = """
    Remove shapes with small surface areas, to clean up detritus after auto-traced and/or offset curves.
"""


font = Glyphs.font

layer = font.selectedLayers[0]

Glyphs.showMacroWindow()
Glyphs.clearLog()


for i in range(len(layer.shapes) - 1, -1, -1):
	if layer.shapes[i].shapeType == 2:
		print(layer.shapes[i].area())
		if layer.shapes[i].area() <= 200:
			print("Removing ", layer.shapes[i], layer.shapes[i].area())
			del layer.shapes[i]

# for i in range(len(layer.shapes) - 1, -1, -1):
# 	for n in range(len(layer.shapes[i].nodes) - 1, -1, -1):
# 		this_xy = 
# 		if 