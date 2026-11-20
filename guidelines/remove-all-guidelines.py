#MenuTitle: Remove all guidelines from selected glyphs
__doc__="""
	Remove all (non-global) guidelines from the current or selected glyphs.
"""

from GlyphsApp import Glyphs

myLayers = Glyphs.font.selectedLayers

for layer in myLayers:
    layer.guides = ()
