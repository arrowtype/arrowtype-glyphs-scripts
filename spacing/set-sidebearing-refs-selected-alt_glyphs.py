# MenuTitle: Set side refs for selected suffixed glyphs
__doc__ = """
	Apply metrics keys to all glyphs with suffixes, except for some ignored (see script).

	Can be useful as a shortcut in e.g. a "handwriting" font for comics.
	
	Assumes glyphs with one suffix after a period are alts, unless the suffixes match a list of feature suffixes.
"""

myLayers = Glyphs.font.selectedLayers

# # The code part. This goes through selected glyphs and outputs a proofing list.
for layer in myLayers:
    glyph = layer.parent
    name = glyph.name

    if "." in name:
        baseGlyphName = name.split(".")[0]
        print("\t", baseGlyphName)
        glyph.leftMetricsKey = baseGlyphName
        glyph.rightMetricsKey = baseGlyphName
