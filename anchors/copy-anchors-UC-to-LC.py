# MenuTitle: Copy anchors from Uppercase to Lowercase
__doc__ = """
    For all-caps fonts where the lowercase use components of uppercase,
    propogate anchors from uppercase to lowercase. Assumes LC glyphs
    have lowercased names matching UC glyphs, which is usually true (but not always)
"""

import copy

font = Glyphs.font

for glyph in font.glyphs:
    if glyph.case == 1:
        # assumes lowercase glyph name is just UC glyph name, lowercased, which is usually true
        try:
            lc_glyph = font.glyphs[glyph.name.lower()]
            for layer in glyph.layers:
                lc_glyph.layers[layer.layerId].anchors = copy.copy(layer.anchors)
        except AttributeError:
            continue

        # TODO? match via Unicodes, rather than glyph names?