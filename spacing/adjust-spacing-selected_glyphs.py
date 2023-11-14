# MenuTitle: Adjust overall spacing for all selected glyphs
__doc__ = """
    A simple way to adjust spacing across all selected glyphs, similar to tracking.
"""

from robofab.interface.all.dialogs import AskString
import math

adjustmentUnits = int(AskString("Units of tracking to adjust by (e.g. -20):"))

print(adjustmentUnits)

font = Glyphs.font
myLayers = Glyphs.font.selectedLayers

# # The code part. This goes through selected glyphs and outputs a proofing list.
for layer in myLayers:
    layer.RSB += math.floor(adjustmentUnits / 2)
    layer.LSB += math.floor(adjustmentUnits / 2)

# font.newTab(text)
