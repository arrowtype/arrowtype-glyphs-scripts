#MenuTitle: Variable feature conditions to Rename Glyphs parameters
__doc__ = """
	Finds `#ifdef VARIABLE` blocks in active features, and turns their
	`condition …; sub A by B;` rules into "Rename Glyphs" custom parameters on
	the static exports (instances) that fall inside each condition.

	Conditions are matched against each export’s axis values, by axis tag,
	with inclusive bounds, as in the variable font. When several rules rename
	the same glyph for one export, the first one wins, as in the variable font.

	Rerunning is safe: rename lines for glyphs that the variable rules
	substitute are replaced in the first active "Rename Glyphs" parameter.
	Renames for other glyphs are kept. A report is printed to the Macro window.
"""

import re

from GlyphsApp import Glyphs, GSCustomParameter, INSTANCETYPESINGLE, Message

PARAMETER_NAME = "Rename Glyphs"
TOLERANCE = 0.001

VARIABLE_BLOCK = re.compile(r"#ifdef\s+VARIABLE\b(.*?)(?:#else\b.*?)?#endif\b", re.DOTALL)
COMPARISON = re.compile(r"(<=|>=|<|>)")


def stripComments(code):
	lines = []
	for line in code.splitlines():
		if line.lstrip().startswith(("#ifdef", "#ifndef", "#else", "#endif")):
			lines.append(line)
		else:
			lines.append(line.split("#", 1)[0])
	return "\n".join(lines)


def parseClause(clause, warnings):
	"""
	Parses "wght < 850", "50 < wdth < 70" or "400 <= wght" into (tag, minimum, maximum).
	Missing bounds are None.
	"""
	parts = [part.strip() for part in COMPARISON.split(clause) if part.strip()]
	tag = None
	minimum = maximum = None
	for i in range(1, len(parts) - 1, 2):
		left, operator, right = parts[i - 1], parts[i], parts[i + 1]
		try:
			value = float(right)
			subject = left
			flipped = False
		except ValueError:
			try:
				value = float(left)
			except ValueError:
				warnings.append("Couldn’t read condition “%s”" % clause.strip())
				return None
			subject = right
			flipped = True
		if tag is not None and subject != tag:
			warnings.append("Couldn’t read condition “%s”" % clause.strip())
			return None
		tag = subject
		# "tag < value" is an upper bound; "value < tag" is a lower bound.
		isUpper = (operator in ("<", "<=")) != flipped
		if isUpper:
			maximum = value
		else:
			minimum = value
	if tag is None:
		warnings.append("Couldn’t read condition “%s”" % clause.strip())
		return None
	return tag, minimum, maximum


def parseCondition(statement, warnings):
	body = statement[len("condition"):]
	clauses = []
	for clause in body.split(","):
		if not clause.strip():
			continue
		parsed = parseClause(clause, warnings)
		if parsed is None:
			return None
		clauses.append(parsed)
	return clauses


def expandGlyphs(font, token):
	token = token.strip()
	if token.startswith("[") and token.endswith("]"):
		names = []
		for part in token[1:-1].split():
			names.extend(expandGlyphs(font, part))
		return names
	if token.startswith("@"):
		glyphClass = font.classes[token[1:]]
		if glyphClass is None:
			return []
		return glyphClass.code.split()
	return [token]


def parseSubstitution(font, statement, warnings):
	match = re.match(r"(?:sub|substitute)\s+(.+?)\s+by\s+(.+)$", statement, re.DOTALL)
	if not match:
		warnings.append("Skipped “%s”: only “sub A by B” rules can become renames" % statement)
		return []
	sources = expandGlyphs(font, match.group(1))
	targets = expandGlyphs(font, match.group(2))
	if len(targets) == 1 and sources:
		targets = targets * len(sources)
	if not sources or len(sources) != len(targets):
		warnings.append("Skipped “%s”: source and replacement glyphs don’t line up" % statement)
		return []
	return list(zip(sources, targets))


def variableRules(font, warnings):
	"""Returns [(featureName, clauses, source, target)] in feature order."""
	rules = []
	for feature in font.features:
		if not feature.active:
			continue
		code = stripComments(feature.code or "")
		for block in VARIABLE_BLOCK.findall(code):
			clauses = None
			for statement in block.split(";"):
				statement = " ".join(statement.split())
				if not statement:
					continue
				if statement.startswith("condition"):
					clauses = parseCondition(statement, warnings)
				elif statement.startswith(("sub ", "substitute ")):
					if clauses is None:
						warnings.append("Skipped “%s” in %s: no readable condition before it" % (statement, feature.name))
						continue
					for source, target in parseSubstitution(font, statement, warnings):
						rules.append((feature.name, clauses, source, target))
	return rules


def instanceLocation(font, instance):
	try:
		values = instance.internalAxesValues
	except AttributeError:
		values = instance.axes
	return {axis.axisTag: float(values[i]) for i, axis in enumerate(font.axes)}


def matches(clauses, location):
	for tag, minimum, maximum in clauses:
		value = location.get(tag)
		if value is None:
			return False
		if minimum is not None and value < minimum - TOLERANCE:
			return False
		if maximum is not None and value > maximum + TOLERANCE:
			return False
	return True


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


def renameSource(line):
	return line.partition("=")[0].strip()


def updateInstance(instance, renames, managedSources):
	"""
	Replaces rename lines for managedSources with renames, in the first active
	Rename Glyphs parameter. Returns (added, removed) line lists.
	"""
	parameters = list(instance.customParameters.values())
	indexes = [
		i for i, parameter in enumerate(parameters)
		if parameter.name == PARAMETER_NAME and parameter.active
	]
	if not indexes and not renames:
		return [], []

	newLines = ["%s=%s" % pair for pair in renames]
	if not indexes:
		instance.customParameters.append(GSCustomParameter(PARAMETER_NAME, newLines))
		return newLines, []

	parameter = parameters[indexes[0]]
	existing = renameLines(parameter.value)
	kept = [line for line in existing if renameSource(line) not in managedSources]
	combined = kept + newLines
	added = [line for line in newLines if line not in existing]
	removed = [line for line in existing if line not in combined]
	if not added and not removed:
		return [], []

	if not combined:
		instance.removeObjectFromCustomParametersAtIndex_(indexes[0])
	elif isinstance(parameter.value, str):
		parameter.value = "\n".join(combined)
	else:
		parameter.value = combined
	return added, removed


def applyRules(font):
	Glyphs.clearLog()
	print("Variable feature conditions → “%s” in %s" % (PARAMETER_NAME, font.familyName))
	print()

	warnings = []
	rules = variableRules(font, warnings)
	for warning in warnings:
		print("Warning: %s" % warning)
	if warnings:
		print()

	if not rules:
		print("No `sub A by B` rules found in `#ifdef VARIABLE` blocks of active features.")
		Glyphs.showMacroWindow()
		return

	axisTags = {axis.axisTag for axis in font.axes}
	unknownTags = sorted({tag for _, clauses, _, _ in rules for tag, _, _ in clauses} - axisTags)
	if unknownTags:
		print("Warning: conditions use axes not in this font, so those rules never match: %s" % ", ".join(unknownTags))
		print()

	managedSources = {source for _, _, source, _ in rules}
	changedCount = 0
	for instance in font.instances:
		if instance.type != INSTANCETYPESINGLE:
			continue
		location = instanceLocation(font, instance)

		renames = []
		renamed = {}
		conflicts = []
		for featureName, clauses, source, target in rules:
			if not matches(clauses, location):
				continue
			if source in renamed:
				if renamed[source] != target:
					conflicts.append("%s (kept %s, skipped %s)" % (source, renamed[source], target))
				continue
			renamed[source] = target
			renames.append((source, target))

		added, removed = updateInstance(instance, renames, managedSources)
		if not added and not removed and not conflicts:
			continue
		changedCount += 1
		print("%s:" % instance.name)
		for line in added:
			print("\t+ %s" % line)
		for line in removed:
			print("\t- %s" % line)
		for conflict in conflicts:
			print("\tWarning: renamed more than once: %s" % conflict)
		print()

	if changedCount:
		print("Updated %d exports." % changedCount)
	else:
		print("All exports were already up to date.")
	Glyphs.showMacroWindow()


font = Glyphs.font
if font is None:
	Message("Open a font first.", title="No Font Open")
else:
	applyRules(font)
