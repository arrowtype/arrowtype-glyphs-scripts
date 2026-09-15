# MenuTitle: Center All Anchors in Selected Glyphs
# -*- coding: utf-8 -*-

# Fetch the current font context
Font = Glyphs.font

# Ensure a font file is open and layers are selected
if Font and Font.selectedLayers:
	# Begin an undo grouping so you can easily revert if needed
	Font.disableUpdateInterface()
	try:
		for selectedLayer in Font.selectedLayers:
			# Get the parent glyph to access ALL of its layers (masters, backups, etc.)
			glyph = selectedLayer.parent
			
			print("Centering anchors for glyph: %s" % glyph.name)
			
			for layer in glyph.layers:
				# Calculate the horizontal center of this specific layer
				layer_center = layer.width / 2.0
				
				# Move each anchor to the calculated center
				if layer.anchors:
					for anchor in layer.anchors:
						anchor.x = layer_center
						
	finally:
		# Refresh the UI and wrap up the macro execution
		Font.enableUpdateInterface()
		print("Done!")
else:
	print("Please open a font and select at least one glyph.")
