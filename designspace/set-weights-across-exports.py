#MenuTitle: Set weight values across exports
__doc__ = """
	Opens a window listing each distinct weight in the current font’s static
	exports (instances), with its internal (design) and external (user) value.

	Exports that share the same weight values are grouped into one row, so in
	a grid of styles (e.g. Bold, Bold Italic, Bold Condensed) one edit updates
	every export at that weight.

	Double-click a value to edit it, then click Set Values. Only the weight
	values that changed are written. Names, custom parameters, and other axis
	values are left alone.

	Requires Glyphs 3.2 or later for external values.
"""

from vanilla import FloatingWindow, List, Button, TextBox
from GlyphsApp import Glyphs, Message, INSTANCETYPESINGLE

# Keep window controllers alive after the script finishes running.
_windows = []


def weightAxis(font):
	for axis in font.axes:
		if (axis.axisTag or "").casefold() == "wght" or (axis.name or "").casefold() == "weight":
			return axis
	return None


def isStaticInstance(instance):
	try:
		return int(instance.type) == INSTANCETYPESINGLE
	except Exception:
		return True


def formatValue(value):
	if value is None:
		return ""
	number = float(value)
	if number.is_integer():
		return str(int(number))
	return str(round(number, 3))


def parseValue(text):
	text = ("" if text is None else str(text)).strip().replace(",", ".")
	if not text:
		return None
	return float(text)


def readValues(instance, axisId):
	internal = instance.internalAxesValues[axisId]
	try:
		external = instance.externalAxesValues[axisId]
	except Exception:
		external = None
	return internal, external


def sameValue(a, b):
	if a is None or b is None:
		return a is b
	return abs(float(a) - float(b)) < 1e-6


def groupKey(internal, external):
	return (
		None if internal is None else round(float(internal), 3),
		None if external is None else round(float(external), 3),
	)


def sharedName(names):
	"""Words found in every name, in the order of the first name. "Bold", "Bold Italic" -> "Bold"."""
	wordLists = [(name or "").split() for name in names]
	if not wordLists or not wordLists[0]:
		return ""
	common = [word for word in wordLists[0] if all(word in words for words in wordLists[1:])]
	if common:
		return " ".join(common)
	return wordLists[0][0] if len(names) == 1 else "%s, …" % names[0]


class SetWeightsWindow(object):

	def __init__(self, font, axis):
		self.font = font
		self.axis = axis
		self.groups = []

		self.w = FloatingWindow((440, 420), "Set Weight Values", minSize=(340, 240))
		self.w.note = TextBox(
			(16, 12, -16, 17),
			"Axis: %s (%s). Double-click a value to edit." % (axis.name, axis.axisTag),
			sizeStyle="small",
		)
		self.w.list = List(
			(16, 36, -16, -54),
			[],
			columnDescriptions=[
				{"title": "Weight", "key": "name", "editable": False},
				{"title": "Exports", "key": "count", "editable": False, "width": 56},
				{"title": "Internal", "key": "internal", "editable": True, "width": 72},
				{"title": "External", "key": "external", "editable": True, "width": 72},
			],
			allowsMultipleSelection=False,
			drawFocusRing=False,
		)
		self.w.setButton = Button((16, -38, -16, 22), "Set Values", callback=self.setCallback)
		self.w.setDefaultButton(self.w.setButton)

		self.populate()
		self.w.bind("close", self.windowClosed)
		self.w.open()
		self.w.makeKey()

	def collectGroups(self):
		"""Return [(internal, external, [instances])], sorted by internal value."""
		byKey = {}
		for instance in self.font.instances:
			if not isStaticInstance(instance):
				continue
			internal, external = readValues(instance, self.axis.axisId)
			key = groupKey(internal, external)
			if key not in byKey:
				byKey[key] = (internal, external, [])
			byKey[key][2].append(instance)
		return sorted(
			byKey.values(),
			key=lambda group: (group[0] is None, group[0] or 0, group[1] is None, group[1] or 0),
		)

	def populate(self):
		self.groups = self.collectGroups()
		rows = []
		for internal, external, instances in self.groups:
			rows.append({
				"name": sharedName([instance.name for instance in instances]),
				"count": str(len(instances)),
				"internal": formatValue(internal),
				"external": formatValue(external),
			})
		self.w.list.set(rows)

	def windowClosed(self, sender):
		if self in _windows:
			_windows.remove(self)

	def setCallback(self, sender):
		rows = self.w.list.get()
		if len(rows) != len(self.groups):
			Message("The list of exports changed. Close and reopen the window.", title="Exports Changed")
			return

		planned = []
		for group, row in zip(self.groups, rows):
			try:
				internal = parseValue(row["internal"])
				external = parseValue(row["external"])
			except ValueError:
				Message("“%s” has a value that isn’t a number." % row["name"], title="Invalid Value")
				return
			planned.append((group, internal, external))

		axisId = self.axis.axisId
		changes = []
		self.font.disableUpdateInterface()
		try:
			for (oldInternal, oldExternal, instances), internal, external in planned:
				setInternal = internal is not None and not sameValue(internal, oldInternal)
				setExternal = external is not None and not sameValue(external, oldExternal)
				if not (setInternal or setExternal):
					continue
				for instance in instances:
					if setInternal:
						instance.internalAxesValues[axisId] = internal
					if setExternal:
						instance.externalAxesValues[axisId] = external
				changed = []
				if setInternal:
					changed.append("internal %s → %s" % (formatValue(oldInternal), formatValue(internal)))
				if setExternal:
					changed.append("external %s → %s" % (formatValue(oldExternal), formatValue(external)))
				changes.append((instances, changed))
		finally:
			self.font.enableUpdateInterface()

		self.populate()
		updated = sum(len(instances) for instances, _changed in changes)
		print("Set weight values across exports")
		if not changes:
			print("  No values changed.")
		for instances, changed in changes:
			print("  %s" % ", ".join(changed))
			for instance in instances:
				print("    %s" % instance.name)
		Glyphs.showNotification(
			"Weight values",
			"Updated %d export%s." % (updated, "" if updated == 1 else "s"),
		)


font = Glyphs.font
if font is None:
	Message("Open a font first.", title="No Font Open")
else:
	axis = weightAxis(font)
	if axis is None:
		Message("This font has no weight axis.", title="No Weight Axis")
	elif not any(isStaticInstance(instance) for instance in font.instances):
		Message("This font has no static exports.", title="No Exports")
	else:
		_windows.append(SetWeightsWindow(font, axis))
