#MenuTitle: Set centered guides (centered & middle)
__doc__="""
	For current or selected glyphs:
	- Clear guidelines
	- Add a vertical guideline in the horizontal center
	- Add a horizontal guideline in the cap-height middle
	- Add a horizontal guideline in the x-height middle

    Useful for arranging anchors, accents, and more.
"""

myLayers = Glyphs.font.selectedLayers

for layer in myLayers:
	# clear existing guides
	layer.guides = ()

	# add new guide at width center
	centerGuide = GSGuide()
	centerGuide.position = (layer.width/2, layer.master.xHeight/2)
	centerGuide.angle = 90 - layer.master.italicAngle
	centerGuide.name = "Vertical Center"
	layer.guides.append(centerGuide)

	# add new guide at cap height middle
	capHeightMidGuide = GSGuide()
	capHeightMidGuide.position = (0, layer.master.capHeight/2)
	capHeightMidGuide.name = "Cap Height Middle"
	layer.guides.append(capHeightMidGuide)

	# add new guide at x height middle
	xHeightMidGuide = GSGuide()
	xHeightMidGuide.position = (0, layer.master.xHeight/2)
	xHeightMidGuide.name = "x-Height Middle"
	layer.guides.append(xHeightMidGuide)
