# MenuTitle: Set side refs for ALL suffixed glyphs in font
__doc__ = """
	Apply metrics keys to all glyphs with suffixes, except for some ignored (see script).

	Can be useful as a shortcut in e.g. a "handwriting" font for comics.
	
	Assumes glyphs with one suffix after a period are alts, unless the suffixes match a list of feature suffixes.
"""

# add to this list if you have opentype feature suffixes in your glyphs font
ignoreSuffixes = "tnum case dnom supr sinf ss01 ss02 ss03 ".split(" ")

font = Glyphs.fonts[0]

for glyph in font.glyphs:
    print(glyph.name)
    if "." in glyph.name:
        baseGlyphName = glyph.name.split(".")[0]
        print("\t", baseGlyphName)
        glyph.leftMetricsKey = baseGlyphName
        glyph.rightMetricsKey = baseGlyphName
