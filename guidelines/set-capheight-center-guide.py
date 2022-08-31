#MenuTitle: Set cap-height-centered guide (horizontal)
__doc__="""
	Add a vertical guideline in the horizontal center of the current or selected glyphs.

    Useful for arranging anchors, accents, and more.
"""

myLayers = Glyphs.font.selectedLayers

for layer in myLayers:
	newGuide = GSGuide()
	newGuide.position = (0, layer.master.capHeight/2)
	layer.guides.append(newGuide)