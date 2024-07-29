# MenuTitle: Prep "faux bold" template in background
__doc__ = """
    For all selected glyphs, copy the foreground to background, then copy again and translate it, 
    to give a suggested starting point for bold outline adjustments.
	
	Adapts function from
	https://github.com/mekkablue/Glyphs-Scripts/blob/1933522ae026c311ac6e5ef62527357ef227d18a/Interpolation/Copy%20Layer%20to%20Layer.py#L13

    This seems to work, but is probably more complicated than it has to be.

    Open in a code editor to adjust X/Y layer shift!
"""

from GlyphsApp import Glyphs, GSPath, GSComponent
from AppKit import NSAffineTransform

# Starting point for Kyrios: over 100 units, up 50 units
shiftX, shiftY = 200, 100


def copyPathsFromLayerToLayer(sourceLayer, targetLayer, keepOriginal=False):
    """Copies all paths from sourceLayer to targetLayer"""
    numberOfPathsInSource = len(sourceLayer.paths)
    numberOfPathsInTarget = len(targetLayer.paths)
    
    print(f"target layer {targetLayer}")

    if numberOfPathsInTarget != 0 and not keepOriginal:
        print("- Deleting %i paths in target layer" % numberOfPathsInTarget)
        try:
            # GLYPHS 3
            for i in reversed(range(len(targetLayer.shapes))):
                if isinstance(targetLayer.shapes[i], GSPath):
                    del targetLayer.shapes[i]
        except:
            # GLYPHS 2
            targetLayer.paths = None

    if numberOfPathsInSource > 0:
        print("- Copying paths")
        
    for thisPath in sourceLayer.paths:
        newPath = thisPath.copy()
        try:
            # GLYPHS 3
            targetLayer.shapes.append(newPath)
        except:
            # GLYPHS 2
            targetLayer.paths.append(newPath)


# This should be the active selection, not necessarily the selection on the inputted fonts
Font = Glyphs.font
selectedGlyphs = [
    layer for layer in Font.selectedLayers if layer.parent.name is not None
]


for thisGlyphLayer in selectedGlyphs:
    try:
        print("🔠 %s" % thisGlyph.name)
        

        sourcelayer = thisGlyphLayer
        targetlayer = sourcelayer.background
        
        print(f"sourcelayer {sourcelayer}")
        print(f"targetlayer {targetlayer}")

        copyPathsFromLayerToLayer(sourcelayer, targetlayer, keepOriginal=False)

        ## translate copy by shiftX, shiftY

        # set up a transformation object, and add a transformation
        transform = NSAffineTransform.new()
        transform.translateXBy_yBy_(shiftX, shiftY)

        # apply the transformation to all background path nodes
        for path in targetlayer.paths:
            for node in path.nodes:
                node.position = transform.transformPoint_(node.position)

        copyPathsFromLayerToLayer(sourcelayer, targetlayer, keepOriginal=True)

    except Exception as e:
        Glyphs.showMacroWindow()
        print("\n⚠️ Script Error:\n")
        import traceback

        print(traceback.format_exc())
