# MenuTitle: Scale selected points to zero height
__doc__ = """
    Scale currently selected points to zero height. E.g. Scale a diagonal line to horizontal, in the middle.

    Useful for flattening angled terminals, etc.
"""

# based on https://forum.glyphsapp.com/t/tranformations-on-selected-nodes-paths-via-scripting/19690/6

from AppKit import NSAffineTransform

middleY = Layer.selectionBounds.origin.y + Layer.selectionBounds.size.height / 2

transform = NSAffineTransform.new()
transform.translateXBy_yBy_(0, middleY)
transform.scaleXBy_yBy_(1, 0)
transform.translateXBy_yBy_(0, -middleY)

for node in Layer.selection:
    node.position = transform.transformPoint_(node.position)
