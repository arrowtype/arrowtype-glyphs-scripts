# MenuTitle: Make tab with string showing selected accents plus glyphs that use them
__doc__ = """
    A simple way to make string to edit accents and their use in selected glyphs.
"""

font = Glyphs.font
myLayers = Glyphs.font.selectedLayers

selectedAccents = set([layer.parent.name for layer in myLayers])

print(selectedAccents)

accentGlyphsDict = {}

for name in selectedAccents:

    accentGlyphsDict[name] = []

    for glyph in font.glyphs:

        gname = glyph.name

        layerGlyph = font.glyphs[gname].layers[0]
        
        if len(layerGlyph.components) > 0:
            for component in layerGlyph.components:
                if component.name == name:
                    print(f"{name} {glyph.name}")

                    accentGlyphsDict[name].append(gname)
                    break

print(accentGlyphsDict)

# convert accentGlyphsDict to text
text = ""
for accent in accentGlyphsDict.keys():
    text += f"/{accent} {''.join(['/'+gname for gname in accentGlyphsDict[accent]])}\n"

print(text)

font.newTab(text)