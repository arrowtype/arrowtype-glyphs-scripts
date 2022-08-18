#MenuTitle: Set centered guide (vertical)
__doc__="""
	Add a vertical guideline in the horizontal center of the current or selected glyphs.

    Useful for arranging anchors, accents, and more.
"""

myLayers = Glyphs.font.selectedLayers

for layer in myLayers:
	newGuide = GSGuide()
	newGuide.position = (layer.width/2, layer.master.xHeight/2)
	newGuide.angle = 90 - layer.master.italicAngle
	layer.guides.append(newGuide)