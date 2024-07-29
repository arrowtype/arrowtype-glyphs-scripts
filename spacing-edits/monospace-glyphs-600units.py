#MenuTitle: Monospace selected glyphs (600 unit width)
__doc__="""
	Sets selected glyphs to 600 units wide, then matches the left & right sidebearings.
"""

myLayers = Glyphs.font.selectedLayers

width = 600

for layer in myLayers:
	layer.width = width
	totalMargin = layer.LSB + layer.RSB
	layer.LSB = totalMargin/2
	layer.width = width
