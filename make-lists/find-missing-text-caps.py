#MenuTitle: Make list of caps without Text alts
__doc__="""
	Check which uppercase glyphs don’t yet have Text alts, and report list.
"""

Glyphs.showMacroWindow()
Glyphs.clearLog()

font = Glyphs.font

basicUppercase = [c for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"]
defaultUppercase = []
basicsWithText = []
needsText = []
hasText = []

for glyph in font.glyphs:
    if ".text" in glyph.name and glyph.name.split(".")[0] in basicUppercase and glyph.export == True:
        basicsWithText.append(glyph.name.replace(".text",""))

for glyph in font.glyphs:
    if glyph.case == 1 and "." not in glyph.name:
        defaultUppercase.append(glyph.name)

for glyph in font.glyphs:
    if glyph.case == 1 and "." not in glyph.name and glyph.name[0] in basicsWithText:
        needsText.append(glyph.name.replace(".text",""))
    
    if ".text" in glyph.name and glyph.name.replace(".text","") in defaultUppercase:
        hasText.append(glyph.name.replace(".text",""))

print("Still needs to be created for ss02:")

for glyphName in needsText:
    if glyphName not in hasText:
        print(glyphName + ".text")
