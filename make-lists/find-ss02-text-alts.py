#MenuTitle: Make list of alphas with both .ss02 and .text alts
__doc__="""
	Check which uppercase glyphs have *both* .ss02 and .text alts, and report list.
"""

Glyphs.showMacroWindow()
Glyphs.clearLog()

font = Glyphs.font

hasSS02Alts = [glyph.name.split(".")[0] for glyph in font.glyphs if ".ss02" in glyph.name]
hasTextAlts = [glyph.name.split(".")[0] for glyph in font.glyphs if ".text" in glyph.name]

commonAlts = set(hasSS02Alts).intersection(hasTextAlts)

print("\n".join(sorted(commonAlts)))
