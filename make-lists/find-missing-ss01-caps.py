#MenuTitle: Make list of caps without ss01 alts
__doc__="""
	Check which uppercase glyphs don’t yet have ss01 alts, and report list.
"""

Glyphs.showMacroWindow()
Glyphs.clearLog()

font = Glyphs.font

defaultUppercase = []
hasSs01 = []

for glyph in font.glyphs:
    if glyph.case == 1 and "." not in glyph.name:
        defaultUppercase.append(glyph.name)
    
    if ".ss01" in glyph.name:
        hasSs01.append(glyph.name.replace(".ss01",""))

print("Still needs to be created for ss01:")

for glyphName in defaultUppercase:
    if glyphName not in hasSs01:
        print(glyphName + ".ss01")
