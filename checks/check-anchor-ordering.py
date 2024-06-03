# MenuTitle: Check for mismatching anchor orders
__doc__ = """
	Check for mismatching anchor orders in all glyphs.
"""

import math

font = Glyphs.font

layerAnchors = {}

for glyph in font.glyphs:
    for layer in glyph.layers:
        if len(layer.anchors) > 0:

            if glyph.name not in layerAnchors:
                layerAnchors[glyph.name] = {}

            anchorNames = tuple(a.name for a in layer.anchors)

            layerAnchors[glyph.name][layer.name] = anchorNames

            # check if there are any duplicates in the anchor names
            if len([a.name for a in layer.anchors]) != len(
                set([a.name for a in layer.anchors])
            ):
                print(f"☣️ Duplicate anchor name in /{glyph.name}")

ordersMatch = True

for glyphName, layerAnchors in layerAnchors.items():
    if len(set(layerAnchors.values())) != 1:
        print(f"Anchor order mismatch between layers in /{glyphName}")
        print(layerAnchors)
        print()
        ordersMatch = False

if ordersMatch:
    print("It looks like all anchor orders match! Nice.")
