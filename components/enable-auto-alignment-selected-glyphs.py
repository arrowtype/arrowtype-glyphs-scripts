#MenuTitle: Enable auto alignment for components of all selected glyphs
__doc__="""
	Turn on automatic alignment for all components of selected glyphs.
"""


font = Glyphs.font

for layer in font.selectedLayers:
	glyph = layer.parent
	
	for layer in glyph.layers:
		for comp in layer.components:
			comp.automaticAlignment = True