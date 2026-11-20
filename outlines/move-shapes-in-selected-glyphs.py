#MenuTitle: [!WIP!] Move shapes in selected glyphs
__doc__ = """
	Move every shape in the selected layers.

	X and Y are the total offset since this window opened. Changing either
	field moves the shapes immediately. With a field focused, Up and Down
	nudge it by 1, Shift by 10, and Command by 100. Auto-aligned components
	are unlocked so the shift can stick.
"""

import objc
from AppKit import NSNumberFormatter
from Foundation import NSObject
from vanilla import FloatingWindow, TextBox, EditText, Stepper
from GlyphsApp import Glyphs, GSComponent, GSPath, Message

MIN_OFFSET = -100000
MAX_OFFSET = 100000

# Keep window controllers alive after the script finishes running.
_windows = []


def integerFormatter():
	formatter = NSNumberFormatter.alloc().init()
	formatter.setAllowsFloats_(False)
	formatter.setMinimum_(MIN_OFFSET)
	formatter.setMaximum_(MAX_OFFSET)
	return formatter


def _fieldDelegateClass():
	# Defined once. Methods only forward to the window, so rerunning the script
	# still picks up new window code.
	try:
		return objc.lookUpClass("ATMoveShapesFieldDelegate")
	except Exception:
		pass

	class ATMoveShapesFieldDelegate(NSObject):
		def initWithOwner_(self, owner):
			self = objc.super(ATMoveShapesFieldDelegate, self).init()
			if self is None:
				return None
			self.owner = owner
			return self

		def controlTextDidChange_(self, notification):
			owner = self.owner
			if owner is not None:
				owner._textChanged(notification.object())

		def control_textView_doCommandBySelector_(self, control, textView, selector):
			owner = self.owner
			if owner is None:
				return False
			return owner._handleFieldCommand(control, textView, selector)

	return ATMoveShapesFieldDelegate


# Up/Down with modifiers are delivered as different field-editor commands.
_NUDGE_UP = (
	"moveUp:",
	"moveUpAndModifySelection:",
	"moveToBeginningOfParagraph:",
	"moveToBeginningOfParagraphAndModifySelection:",
	"moveParagraphBackward:",
	"moveToBeginningOfDocument:",
	"moveToBeginningOfDocumentAndModifySelection:",
)
_NUDGE_DOWN = (
	"moveDown:",
	"moveDownAndModifySelection:",
	"moveToEndOfParagraph:",
	"moveToEndOfParagraphAndModifySelection:",
	"moveParagraphForward:",
	"moveToEndOfDocument:",
	"moveToEndOfDocumentAndModifySelection:",
)


def _selectorName(selector):
	if isinstance(selector, str):
		return selector
	if isinstance(selector, bytes):
		return selector.decode("utf-8")
	try:
		return selector.name()
	except Exception:
		text = str(selector)
	if text.startswith("<SEL ") and text.endswith(">"):
		return text[5:-1]
	return text


def _modifierStep():
	try:
		from AppKit import NSEvent
		flags = int(NSEvent.modifierFlags())
	except Exception:
		return 1
	if flags & (1 << 20):  # command
		return 100
	if flags & (1 << 17):  # shift
		return 10
	return 1


class MoveShapesWindow(object):

	def __init__(self, font, layers):
		self.font = font
		self.appliedX = 0
		self.appliedY = 0
		self._syncing = False
		self._records = self._snapshot(layers)

		size = (168, 80)
		self.w = FloatingWindow(size, "Move Shapes", minSize=size, maxSize=size)

		self.w.xLabel = TextBox((16, 18, 18, 17), "X")
		self.w.xField = EditText((36, 14, 80, 22), 0, continuous=True, formatter=integerFormatter())
		self.w.xStepper = Stepper((116, 14, 19, 22), value=0, minValue=MIN_OFFSET, maxValue=MAX_OFFSET, increment=1, callback=self.valueChanged)

		self.w.yLabel = TextBox((16, 48, 18, 17), "Y")
		self.w.yField = EditText((36, 44, 80, 22), 0, continuous=True, formatter=integerFormatter())
		self.w.yStepper = Stepper((116, 44, 19, 22), value=0, minValue=MIN_OFFSET, maxValue=MAX_OFFSET, increment=1, callback=self.valueChanged)

		self._fieldDelegate = _fieldDelegateClass().alloc().initWithOwner_(self)
		for field in (self.w.xField, self.w.yField):
			field.getNSTextField().setDelegate_(self._fieldDelegate)

		self.w.bind("close", self.windowClosed)
		self.w.open()
		self.w.makeKey()
		xField = self.w.xField.getNSTextField()
		self.w.getNSWindow().makeFirstResponder_(xField)
		xField.selectText_(None)

	def windowClosed(self, sender):
		if self._fieldDelegate is not None:
			self._fieldDelegate.owner = None
		if self in _windows:
			_windows.remove(self)

	def _textChanged(self, nsField):
		if self._syncing:
			return
		field = self._vanillaField(nsField)
		if field is not None:
			self.valueChanged(field)

	def _handleFieldCommand(self, control, textView, selector):
		if self._vanillaField(control) is None:
			return False
		name = _selectorName(selector)
		if name in _NUDGE_UP:
			self._nudge(control, textView, _modifierStep())
			return True
		if name in _NUDGE_DOWN:
			self._nudge(control, textView, -_modifierStep())
			return True
		return False

	def _nudge(self, nsField, textView, delta):
		field = self._vanillaField(nsField)
		if field is None or delta == 0:
			return
		current = self._asInt(textView.string())
		if current is None:
			current = 0
		updated = min(MAX_OFFSET, max(MIN_OFFSET, current + delta))
		text = str(updated)
		textView.setString_(text)
		textView.setSelectedRange_((0, len(text)))
		self._syncing = True
		try:
			field.set(updated)
			nsField.setStringValue_(text)
		finally:
			self._syncing = False
		editor = nsField.currentEditor()
		if editor is not None:
			editor.setString_(text)
			editor.setSelectedRange_((0, len(text)))
		self.valueChanged(field)

	def _vanillaField(self, nsField):
		if nsField == self.w.xField.getNSTextField():
			return self.w.xField
		if nsField == self.w.yField.getNSTextField():
			return self.w.yField
		return None

	def valueChanged(self, sender):
		if self._syncing:
			return

		pairs = (
			(self.w.xField, self.w.xStepper),
			(self.w.yField, self.w.yStepper),
		)
		self._syncing = True
		for field, stepper in pairs:
			if sender is field:
				value = self._fieldInt(field)
				if value is None:
					self._syncing = False
					return
				stepper.set(value)
			elif sender is stepper:
				value = self._asInt(stepper.get())
				field.set(value)
				self._writeEditor(field, value)
		self._syncing = False
		self._apply()

	def _writeEditor(self, field, value):
		if value is None:
			return
		nsField = field.getNSTextField()
		try:
			editor = nsField.currentEditor()
		except Exception:
			editor = None
		if editor is None:
			return
		text = str(value)
		editor.setString_(text)
		editor.setSelectedRange_((0, len(text)))

	def _fieldInt(self, field):
		# While editing, the field editor has the text. stringValue() can lag behind it.
		nsField = field.getNSTextField()
		try:
			editor = nsField.currentEditor()
		except Exception:
			editor = None
		if editor is not None:
			return self._asInt(editor.string())
		return self._asInt(nsField.stringValue())

	def _asInt(self, value):
		if value is None or value == "":
			return None
		try:
			return int(round(float(value)))
		except (TypeError, ValueError):
			return None

	def _snapshot(self, layers):
		records = []
		for layer in layers:
			for shape in layer.shapes:
				if isinstance(shape, GSPath):
					points = [(node.position.x, node.position.y) for node in shape.nodes]
					records.append((shape, points))
				elif isinstance(shape, GSComponent):
					position = shape.position
					records.append((shape, (position.x, position.y)))
		return records

	def _apply(self):
		x = self._fieldInt(self.w.xField)
		y = self._fieldInt(self.w.yField)
		if x is None or y is None:
			return
		if x == self.appliedX and y == self.appliedY:
			return

		undo = self.font.undoManager()
		undo.beginUndoGrouping()
		try:
			for shape, origin in self._records:
				if isinstance(shape, GSPath):
					for node, (originX, originY) in zip(shape.nodes, origin):
						node.position = (originX + x, originY + y)
				else:
					if shape.automaticAlignment:
						shape.automaticAlignment = False
					originX, originY = origin
					shape.position = (originX + x, originY + y)
		finally:
			undo.endUndoGrouping()

		self.appliedX = x
		self.appliedY = y


font = Glyphs.font
if font is None:
	Message("Open a font and select some glyphs first.", title="No Font Open")
else:
	layers = []
	seen = set()
	for layer in font.selectedLayers:
		if layer is None or layer.parent is None:
			continue
		key = (id(layer.parent), layer.layerId)
		if key in seen:
			continue
		seen.add(key)
		layers.append(layer)

	if not layers:
		Message("Select one or more glyphs, then run the script again.", title="Nothing Selected")
	else:
		_windows.append(MoveShapesWindow(font, layers))
