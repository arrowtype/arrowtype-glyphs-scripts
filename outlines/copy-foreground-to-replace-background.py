# MenuTitle: Copy foreground to replace background
__doc__ = """
	Replace the background with the foreground layer content.
"""

import math

font = Glyphs.font

selectedLayer = font.selectedLayers[0]

selectedLayer.background = selectedLayer.copy()
