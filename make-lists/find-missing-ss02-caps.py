#MenuTitle: Make list of caps without ss02 alts
__doc__="""
	Check which uppercase glyphs don’t yet have ss02 alts, and report list.
"""

Glyphs.showMacroWindow()
Glyphs.clearLog()

font = Glyphs.font

basicUppercase = [c for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"]
defaultUppercase = []
basicsWithSs02 = []
needsSs02 = []
hasSs02 = []

for glyph in font.glyphs:
    if ".ss02" in glyph.name and glyph.name.split(".")[0] in basicUppercase and glyph.export == True:
        basicsWithSs02.append(glyph.name.replace(".ss02",""))

for glyph in font.glyphs:
    if glyph.case == 1 and "." not in glyph.name:
        defaultUppercase.append(glyph.name)

for glyph in font.glyphs:
    if glyph.case == 1 and "." not in glyph.name and glyph.name[0] in basicsWithSs02:
        needsSs02.append(glyph.name.replace(".ss02",""))
    
    if ".ss02" in glyph.name and glyph.name.replace(".ss02","") in defaultUppercase:
        hasSs02.append(glyph.name.replace(".ss02",""))

print("Still needs to be created for ss02:")

for glyphName in needsSs02:
    if glyphName not in hasSs02:
        print(glyphName + ".ss02")
