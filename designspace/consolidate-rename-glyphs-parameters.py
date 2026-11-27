#MenuTitle: Consolidate Rename Glyphs parameters
__doc__ = """
	For every export (instance), combine all active "Rename Glyphs" custom
	parameters into the first one, one rename per line, in their original
	order. The other active "Rename Glyphs" parameters are then removed.

	Exact duplicate lines are only kept once. Disabled parameters are left
	alone. A report is printed to the Macro window.
"""

from GlyphsApp import Glyphs, Message

PARAMETER_NAME = "Rename Glyphs"


def renameLines(value):
	if value is None:
		return []
	items = [value] if isinstance(value, str) else list(value)
	lines = []
	for item in items:
		for line in str(item).splitlines():
			line = line.strip()
			if line:
				lines.append(line)
	return lines


def conflictingSources(lines):
	targets = {}
	for line in lines:
		source, _, target = line.partition("=")
		targets.setdefault(source.strip(), set()).add(target.strip())
	return sorted(source for source, found in targets.items() if len(found) > 1)


def consolidateInstance(instance):
	"""Returns (number of parameters merged, combined lines, conflicting sources), or None if nothing changed."""
	parameters = list(instance.customParameters.values())
	indexes = [
		i for i, parameter in enumerate(parameters)
		if parameter.name == PARAMETER_NAME and parameter.active
	]
	if len(indexes) < 2:
		return None

	combined = []
	for i in indexes:
		for line in renameLines(parameters[i].value):
			if line not in combined:
				combined.append(line)

	first = parameters[indexes[0]]
	if isinstance(first.value, str):
		first.value = "\n".join(combined)
	else:
		first.value = combined

	for i in reversed(indexes[1:]):
		instance.removeObjectFromCustomParametersAtIndex_(i)

	return len(indexes), combined, conflictingSources(combined)


def consolidateFont(font):
	Glyphs.clearLog()
	print("Consolidate “%s” parameters in %s" % (PARAMETER_NAME, font.familyName))
	print()

	changedCount = 0
	for instance in font.instances:
		result = consolidateInstance(instance)
		if result is None:
			continue
		changedCount += 1
		mergedCount, combined, conflicts = result
		print("%s: merged %d parameters into one with %d renames" % (instance.name, mergedCount, len(combined)))
		for line in combined:
			print("\t%s" % line)
		if conflicts:
			print("\tWarning: renamed more than once: %s" % ", ".join(conflicts))
		print()

	if changedCount:
		print("Consolidated %d exports." % changedCount)
	else:
		print("No exports had more than one active “%s” parameter." % PARAMETER_NAME)
	Glyphs.showMacroWindow()


font = Glyphs.font
if font is None:
	Message("Open a font first.", title="No Font Open")
else:
	consolidateFont(font)
