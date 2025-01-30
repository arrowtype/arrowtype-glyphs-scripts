# MenuTitle: Copy foreground to replace background
__doc__ = """
	Replace the background with the foreground layer content.

 	Note: this is very similar to "Path > Selection to Background",
  	but doesn’t require (or consider) selection.
"""

import math

font = Glyphs.font

selectedLayer = font.selectedLayers[0]

selectedLayer.background = selectedLayer.copy()
