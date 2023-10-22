#MenuTitle: Scale selected points to zero width
__doc__="""
    Scale currently selected points to zero width. E.g. Scale a diagonal line to vertical, in the middle.

    Useful for flattening angled terminals.
"""

# based on https://forum.glyphsapp.com/t/tranformations-on-selected-nodes-paths-via-scripting/19690/6

from AppKit import NSAffineTransform

middleX = Layer.selectionBounds.origin.x + Layer.selectionBounds.size.width/2

transform = NSAffineTransform.new()
transform.translateXBy_yBy_(middleX, 0)
transform.scaleXBy_yBy_(0, 1)
transform.translateXBy_yBy_(-middleX, 0)

for node in Layer.selection:
    node.position = transform.transformPoint_(node.position)