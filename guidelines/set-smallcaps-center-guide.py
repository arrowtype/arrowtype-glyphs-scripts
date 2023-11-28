# MenuTitle: Set smallcap-height-centered guide (horizontal)
__doc__ = """
	Add a horizontal guideline in the height center of the current or selected glyphs.

	Assumes "Small Cap" is the title of the metric.

    Useful for arranging anchors, accents, and more.
"""

myLayers = Glyphs.font.selectedLayers

for layer in myLayers:
    for metric in layer.master.metrics:
        if "Small Cap" in metric.name or ".sc" in metric.name:
            newGuide = GSGuide()
            newGuide.position = (0, metric.position / 2)
            layer.guides.append(newGuide)
