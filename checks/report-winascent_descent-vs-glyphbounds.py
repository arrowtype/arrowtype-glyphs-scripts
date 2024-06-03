#MenuTitle: Report winAscent and winDescent vs glyph bounds
__doc__="""
    Get winAscent and winDescent for the font.
    Report which glyphs (if any) exceed those, and by how much.
"""

font = Glyphs.font

lowGlyphs = []
tallGlyphs = []

if font.customParameters['winAscent'] != None:
    winAscent = font.customParameters['winAscent']
    winDescent = font.customParameters['winDescent']

    # make global guide for winAscent
    # make global guide for winDescent

    for master in font.masters:
        print()
        for glyph in font.glyphs:
            layerGlyph = glyph.layers[master.id]
            if layerGlyph.bounds.origin.y < -winDescent:
                # print(master.name, glyph.name, layerGlyph.bounds.origin.y)
                lowGlyphs.append(glyph.name)
                newGuide = GSGuide()
                newGuide.name = "winDescent"
                newGuide.position = (0, -winDescent)
                layerGlyph.guides.append(newGuide)
            if layerGlyph.bounds.origin.y + layerGlyph.bounds.size.height > winAscent:
                # print(master.name, glyph.name, layerGlyph.bounds.origin.y)
                tallGlyphs.append(glyph.name)
                newGuide = GSGuide()
                newGuide.name = "winAscent"
                newGuide.position = (0, winAscent)
                layerGlyph.guides.append(newGuide)

text = "".join([f"/{n}" for n in set(tallGlyphs)]) + "".join([f"/{n}" for n in set(lowGlyphs)])

print(len(text))

if len(text) > 0:
    font.newTab(text)
else:
    font.newTab("All glyphs within winDescent and winAscent")

