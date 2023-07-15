#MenuTitle: Monospace selected glyphs (equal to width of /n)
__doc__="""
	Sets selected glyphs to the same width as n, then matches the left & right sidebearings.
"""


myLayers = Glyphs.font.selectedLayers

width = document.font["n"].layers[0].width

for layer in myLayers:
	layer.width = width
	totalMargin = layer.LSB + layer.RSB
	layer.LSB = totalMargin/2
	layer.width = width
	layer.parent.widthMetricsKey="n"