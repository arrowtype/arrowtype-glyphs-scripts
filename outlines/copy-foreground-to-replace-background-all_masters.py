# MenuTitle: Copy foreground to replace background, all masters
__doc__ = """
	Replace the background with the foreground layer content.

 	Note: this is very similar to "Path > Selection to Background",
  	but doesn’t require (or consider) selection.
"""

import math

font = Glyphs.font

for currentLayer in font.selectedLayers:

	parentGlyph = currentLayer.parent

	for layer in parentGlyph.layers:

		layer.background = layer.copy()
