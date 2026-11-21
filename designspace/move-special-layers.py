#MenuTitle: Move special layers between masters
__doc__ = """
	Pick a "From" and a "To" master, then click Move Special Layers.

	Every special layer (brace, bracket, color, and other non-master layers)
	associated with the From master is reassigned to the To master. Backup
	layers are left where they are.

	A report of which glyphs had which layers moved is printed to the
	Macro window.
"""

from vanilla import FloatingWindow, TextBox, PopUpButton, Button
from GlyphsApp import Glyphs, Message

# Keep window controllers alive after the script finishes running.
_windows = []


def isSpecialLayer(layer):
	if layer.layerId == layer.associatedMasterId:
		return False
	try:
		return bool(layer.isSpecialLayer)
	except AttributeError:
		return bool(layer.attributes)


def moveSpecialLayers(font, fromMaster, toMaster):
	moved = []
	font.disableUpdateInterface()
	try:
		for glyph in font.glyphs:
			layers = [
				layer for layer in glyph.layers
				if layer.associatedMasterId == fromMaster.id and isSpecialLayer(layer)
			]
			if not layers:
				continue
			glyph.beginUndo()
			try:
				for layer in layers:
					layer.associatedMasterId = toMaster.id
			finally:
				glyph.endUndo()
			moved.append((glyph.name, [layer.name for layer in layers]))
	finally:
		font.enableUpdateInterface()
	return moved


def printReport(fromMaster, toMaster, moved):
	Glyphs.clearLog()
	print("Moved special layers from “%s” to “%s”" % (fromMaster.name, toMaster.name))
	print()
	if not moved:
		print("No special layers found on “%s”." % fromMaster.name)
		return
	layerCount = 0
	for glyphName, layerNames in moved:
		layerCount += len(layerNames)
		print("%s:" % glyphName)
		for layerName in layerNames:
			print("\t%s" % layerName)
	print()
	print("%d layers in %d glyphs." % (layerCount, len(moved)))


class MoveSpecialLayersWindow(object):

	def __init__(self, font):
		self.font = font
		masterNames = [master.name for master in font.masters]

		self.w = FloatingWindow((300, 132), "Move Special Layers")

		self.w.fromLabel = TextBox((16, 18, 40, 17), "From")
		self.w.fromPopUp = PopUpButton((60, 15, -16, 22), masterNames)

		self.w.toLabel = TextBox((16, 50, 40, 17), "To")
		self.w.toPopUp = PopUpButton((60, 47, -16, 22), masterNames)
		if len(masterNames) > 1:
			self.w.toPopUp.set(1)

		self.w.moveButton = Button((16, -38, -16, 22), "Move Special Layers", callback=self.moveCallback)
		self.w.setDefaultButton(self.w.moveButton)

		self.w.bind("close", self.windowClosed)
		self.w.open()
		self.w.makeKey()

	def windowClosed(self, sender):
		if self in _windows:
			_windows.remove(self)

	def moveCallback(self, sender):
		masters = self.font.masters
		fromMaster = masters[self.w.fromPopUp.get()]
		toMaster = masters[self.w.toPopUp.get()]
		if fromMaster.id == toMaster.id:
			Message("Choose two different masters.", title="Same Master")
			return

		moved = moveSpecialLayers(self.font, fromMaster, toMaster)
		printReport(fromMaster, toMaster, moved)
		Glyphs.showMacroWindow()


font = Glyphs.font
if font is None:
	Message("Open a font first.", title="No Font Open")
elif len(font.masters) < 2:
	Message("This font needs at least two masters.", title="Not Enough Masters")
else:
	_windows.append(MoveSpecialLayersWindow(font))
