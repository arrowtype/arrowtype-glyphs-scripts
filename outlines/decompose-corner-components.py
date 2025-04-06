# MenuTitle: Decompose all corner components in current font
__doc__ = """
    Decompose all corner omponents in the current font.
	
	Useful if you want to build a font with FontMake, etc.
	
	See:
	https://forum.glyphsapp.com/t/decompose-corner-cap-components/10758
"""


font = Glyphs.font

for glyph in font.glyphs:
	for layer in glyph.layers:
		layer.decomposeCorners()
		