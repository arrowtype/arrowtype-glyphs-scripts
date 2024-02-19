# MenuTitle: Update side refs for ".sc" glyphs
__doc__ = """
    Assumes smallcaps have ".sc" suffix.

    Updates sidebearing references by adding this suffix if not already present.

    So, e.g., in "Q.sc" a reference to "O" becomes "O.sc"
"""

font = Glyphs.fonts[0]

for glyph in font.glyphs:
    if ".sc" in glyph.name:
        if (
            glyph.leftMetricsKey
            and ".sc" not in glyph.leftMetricsKey
            and "=|" not in glyph.leftMetricsKey
        ):
            glyph.leftMetricsKey += ".sc"
            print(f"updated {glyph.name} LSB")
        if (
            glyph.rightMetricsKey
            and ".sc" not in glyph.rightMetricsKey
            and "=|" not in glyph.rightMetricsKey
        ):
            glyph.rightMetricsKey += ".sc"
            print(f"updated {glyph.name} RSB")
