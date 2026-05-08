# MenuTitle: Report area of selected paths
__doc__ = """
    Report the area of selected paths in the current layer.
"""


font = Glyphs.font

layer = font.selectedLayers[0]

Glyphs.showMacroWindow()
Glyphs.clearLog()

areas = []

for path in layer.paths:
	if path.selected:
		areas.append(path.area())
		print(path.area())
		
print()

if len(areas) == 2:
	print(f"Balance: {areas[1]/areas[0]}")
	print(f"Total:   {int((areas[0]+areas[1])/72)} sq in")	
else:
	print(len(areas))
	
print()
	
print(round(layer.bounds.size.width / 72, 2), "in wide")