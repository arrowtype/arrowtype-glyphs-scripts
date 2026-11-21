#MenuTitle: Set overshoot guidelines (global, all masters)
__doc__="""
	For each master, add global guidelines at the boundary and middle of each alignment zone.

	For example, at an x-height of 524 with a 16-unit zone, guidelines go at 540 and 532.

	Guidelines are named with an "Overshoot" prefix. Rerunning the script replaces them,
	leaving all other global guidelines untouched.
"""

from GlyphsApp import Glyphs, GSGuide, Message

GUIDE_PREFIX = "Overshoot"


def formatValue(value):
	if value == int(value):
		return str(int(value))
	return str(round(value, 2))


def overshootGuides(master):
	guides = []
	seen = set()
	for zone in master.alignmentZones:
		if not zone.size:
			continue
		edge = zone.position + zone.size
		middle = zone.position + zone.size / 2
		for y, label in ((edge, "edge"), (middle, "middle")):
			if y in seen:
				continue
			seen.add(y)
			guide = GSGuide()
			guide.position = (0, y)
			guide.name = "%s %s %s" % (GUIDE_PREFIX, label, formatValue(y))
			guides.append(guide)
	return guides


def setOvershootGuides(font):
	for master in font.masters:
		kept = [guide for guide in master.guides if not (guide.name or "").startswith(GUIDE_PREFIX)]
		master.guides = kept + overshootGuides(master)


font = Glyphs.font
if font is None:
	Message("Open a font first.", title="No Font Open")
else:
	setOvershootGuides(font)
