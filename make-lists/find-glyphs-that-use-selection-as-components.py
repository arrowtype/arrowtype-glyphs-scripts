#MenuTitle: List glyphs the use selection as components
__doc__="""
    Make a list of glyphnames that use currently-selected glyphs as components.

    Useful for making alt glyphs for diacritics and for writing features.
"""

Glyphs.showMacroWindow()
Glyphs.clearLog()

font = Glyphs.font

myLayers = Glyphs.font.selectedLayers

listOfChildGlyphs = []

# go through all selected layers (e.g. selected glyphs, current glyph, or glyphs in tab)
for layer in myLayers:
    # get glyph name
    glyphName = layer.parent.name
    id = font.selectedLayers[0].layerId

    # go through font
    for glyph in font.glyphs:

        if glyphName in [comp.name for comp in glyph.layers[id].components]:
            listOfChildGlyphs.append(glyph.name)

print(" ".join(sorted(set(listOfChildGlyphs))))