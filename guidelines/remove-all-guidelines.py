#MenuTitle: Set cap-height-centered guide (horizontal)
__doc__="""
	Remove all (non-global) guidlines from the current or selected glyphs.
"""

myLayers = Glyphs.font.selectedLayers

for layer in myLayers:
    layer.guides = ()