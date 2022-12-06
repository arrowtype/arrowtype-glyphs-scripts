#MenuTitle: Make list of alphas without Text alts
__doc__="""
	Check which uppercase glyphs don’t yet have Text alts, and report list.
"""

Glyphs.showMacroWindow()
Glyphs.clearLog()

font = Glyphs.font

basicAlpha = [c for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"]
defaultAlphas = []
basicsWithText = []
needsText = []
hasText = []

for glyph in font.glyphs:
    if ".text" in glyph.name and glyph.name.split(".")[0] in basicAlpha and glyph.export == True:
        basicsWithText.append(glyph.name.replace(".text",""))

for glyph in font.glyphs:
    if glyph.category == "Letter" and "." not in glyph.name:
        defaultAlphas.append(glyph.name)

for glyph in font.glyphs:
    if glyph.category == "Letter" and "." not in glyph.name and glyph.name[0] in basicsWithText:
        # remove some false positives
        if glyph.name not in "Thorn Eth eth germandbls".split():
            needsText.append(glyph.name.replace(".text",""))
    
    if ".text" in glyph.name and glyph.name.replace(".text","") in defaultAlphas:
        hasText.append(glyph.name.replace(".text",""))

print("Still needs to be created for ss02:")

for glyphName in needsText:
    if glyphName not in hasText:
        print(glyphName + ".text")
