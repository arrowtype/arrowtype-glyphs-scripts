# MenuTitle: Remove Unicode values from selected glyphs
__doc__ = """
	Removes Unicode values from selected glyphs
"""


font = Glyphs.font
myLayers = Glyphs.font.selectedLayers

# The code part. This goes through selected glyphs and outputs a proofing list.
for layer in myLayers:
    g = layer.parent
    g.unicode = None