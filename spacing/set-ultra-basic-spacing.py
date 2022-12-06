#MenuTitle: Set super-basic spacing (60 units each side) for selected glyphs
__doc__="""
	Set super-basic spacing (60 units each side) for selected glyphs

    Useful as an early step in making a handwriting font, and copy-pasting glyph shapes.
"""

myLayers = Glyphs.font.selectedLayers

for layer in myLayers:
    layer.LSB = 60
    layer.RSB = 60

# repeating this to maybe correct for accents that start as zero-width glyphs
for layer in myLayers:
    layer.LSB = 60
    layer.RSB = 60