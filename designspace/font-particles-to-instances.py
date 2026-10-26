#MenuTitle: Expand name particles to instances
__doc__ = """
	Expand each particle instance (instance.type == 4) into static instances
	(instance.type == 0).

	The new instances are the cross product of the GSNameParticles stored on
	that particle instance, one list per font axis. Style names are joined in
	font axis order. Regular, Normal, and Roman are left out of a name when
	another particle already names the style, so "Normal Thin" becomes "Thin"
	and "Compressed Regular" becomes "Compressed".

	A particle with active turned off is left out of the product. If every
	particle is inactive, the whole set is used — Glyphs omits the flag when
	it is simply on.

	Existing static instances with the same style name are left in place.
"""

from itertools import product

from GlyphsApp import GSInstance, Glyphs, INSTANCETYPESINGLE

# GSInstanceTypeParticle. Not exported by GlyphsApp.py yet.
INSTANCETYPEPARTICLE = 4
NAME_PARTICLES_KEY = "com.glyphsapp.NameParticles"
ELIDABLE_NAMES = {"normal", "roman"}
MAX_INSTANCES = 5000


class ParticleRecord:
	def __init__(self, name, internal, external=None, active=None, names=None):
		self.name = "" if name is None else str(name).strip()
		self.internal = float(internal)
		self.external = None if external is None else float(external)
		self.active = active
		self.names = names or {}


def style_name_from_parts(parts):
	"""Join name particles, dropping elidable words when other words remain."""
	cleaned = ["" if part is None else str(part).strip() for part in parts]
	kept = [part for part in cleaned if part and part.casefold() not in ELIDABLE_NAMES]
	if kept:
		return " ".join(kept)
	for part in cleaned:
		if part.casefold() == "regular":
			return part
	for part in cleaned:
		if part:
			return part
	return "Regular"


def localized_style_names(records):
	languages = []
	seen = set()
	for record in records:
		for language in record.names:
			if language not in seen:
				seen.add(language)
				languages.append(language)
	if not languages:
		return {}

	localized = {}
	for language in languages:
		parts = []
		for record in records:
			if language in record.names:
				parts.append(record.names[language])
			else:
				parts.append(record.name)
		localized[language] = style_name_from_parts(parts)
	return localized


def _mapping_get(mapping, key):
	if mapping is None:
		return None
	try:
		if key in mapping:
			return mapping[key]
	except Exception:
		pass
	try:
		return mapping.objectForKey_(key)
	except Exception:
		return None


def _names_from_entries(entries):
	names = {}
	for entry in entries or []:
		language = getattr(entry, "languageTag", None) or _mapping_get(entry, "language")
		value = getattr(entry, "value", None)
		if value is None:
			value = _mapping_get(entry, "value")
		if language and value is not None and str(value).strip():
			names[str(language)] = str(value).strip()
	return names


def _is_particle_object(particle):
	return hasattr(particle, "setInternal_") or (
		hasattr(particle, "internal") and hasattr(particle, "active") and not hasattr(particle, "objectForKey_")
	)


def particle_record(particle):
	"""Read a GSNameParticle or a plist dict into one record."""
	if isinstance(particle, ParticleRecord):
		return particle

	if _is_particle_object(particle):
		return ParticleRecord(
			name=particle.name,
			internal=particle.internal,
			external=particle.external,
			active=bool(particle.active),
			names=_names_from_entries(getattr(particle, "names", None)),
		)

	internal = _mapping_get(particle, "internal")
	if internal is None:
		return None
	active = _mapping_get(particle, "active")
	if active is not None:
		active = bool(active)
	return ParticleRecord(
		name=_mapping_get(particle, "name"),
		internal=internal,
		external=_mapping_get(particle, "external"),
		active=active,
		names=_names_from_entries(_mapping_get(particle, "names")),
	)


def participating_particles(records):
	"""Active particles win. A set that is entirely inactive is kept whole."""
	if any(record.active is not False for record in records):
		return [record for record in records if record.active is not False]
	return list(records)


def _stored_map(stored):
	if not stored:
		return {}
	mapped = {}
	try:
		keys = list(stored.keys())
	except Exception:
		keys = list(stored)
	for key in keys:
		value = _mapping_get(stored, key)
		if value is None:
			try:
				value = stored[key]
			except Exception:
				continue
		mapped[str(key)] = value
	return mapped


def raw_particle_map(instance):
	"""Particles keyed by axis id or axis tag."""
	getter = getattr(instance, "pyobjc_instanceMethods", None)
	if getter is not None:
		try:
			mapped = _stored_map(getter.nameParticles())
		except Exception:
			mapped = {}
		if any(list(value) for value in mapped.values()):
			return mapped

	user_data = getattr(instance, "userData", None)
	return _stored_map(_mapping_get(user_data, NAME_PARTICLES_KEY))


def _axis_keys(axis):
	keys = []
	for key in (getattr(axis, "axisId", None), getattr(axis, "axisTag", None), getattr(axis, "name", None)):
		if key:
			keys.append(str(key))
	return keys


def records_for_axis(raw, axis):
	wanted = {key.casefold() for key in _axis_keys(axis)}
	values = None
	for key, stored in raw.items():
		if str(key).casefold() in wanted:
			values = stored
			break
	if values is None:
		return []
	records = []
	for particle in values:
		record = particle_record(particle)
		if record is not None:
			records.append(record)
	return participating_particles(records)


def axis_groups(font, instance):
	raw = raw_particle_map(instance)
	if not raw:
		return []
	groups = []
	for axis in font.axes:
		records = records_for_axis(raw, axis)
		if records:
			groups.append((axis, records))
	return groups


def expanded_instances(groups):
	"""Yield (style name, [(axis, record), ...], localized names) for the cross product."""
	if not groups:
		return
	axes = [axis for axis, _records in groups]
	lists = [records for _axis, records in groups]
	count = 1
	for records in lists:
		count *= len(records)
	if count > MAX_INSTANCES:
		raise ValueError("cross product has %d instances (limit %d)" % (count, MAX_INSTANCES))

	for combo in product(*lists):
		name = style_name_from_parts(record.name for record in combo)
		yield name, list(zip(axes, combo)), localized_style_names(combo)


def _is_particle_instance(instance):
	try:
		return int(instance.type) == INSTANCETYPEPARTICLE
	except Exception:
		return False


def _existing_single_names(font):
	names = set()
	for instance in font.instances:
		try:
			is_single = int(instance.type) == INSTANCETYPESINGLE
		except Exception:
			is_single = False
		if is_single and instance.name:
			names.add(instance.name)
	return names


def _apply_location(instance, pairs):
	for axis, record in pairs:
		axis_id = getattr(axis, "axisId", None)
		if axis_id:
			instance.internalAxesValues[axis_id] = record.internal
			if record.external is not None:
				instance.externalAxesValues[axis_id] = record.external
			continue
		axis_index = list(instance.font.axes).index(axis)
		instance.internalAxesValues[axis_index] = record.internal
		if record.external is not None:
			instance.externalAxesValues[axis_index] = record.external


def _apply_localized_names(instance, localized):
	for language, name in localized.items():
		instance.setProperty_value_languageTag_("styleNames", name, language)


def expand_font(font):
	created = []
	skipped = []
	notes = []
	existing_names = _existing_single_names(font)
	particle_instances = [instance for instance in font.instances if _is_particle_instance(instance)]

	if not particle_instances:
		return created, skipped, ["No particle instances (type 4) were found."]

	for particle_instance in particle_instances:
		groups = axis_groups(font, particle_instance)
		if not groups:
			notes.append("Particle instance “%s” has no name particles." % (particle_instance.name or "particles"))
			continue
		try:
			specs = list(expanded_instances(groups))
		except ValueError as error:
			notes.append("Skipped particle instance “%s”: %s." % (particle_instance.name or "particles", error))
			continue

		for style_name, pairs, localized in specs:
			if style_name in existing_names:
				skipped.append(style_name)
				continue
			new_instance = GSInstance()
			try:
				new_instance.setType_(INSTANCETYPESINGLE)
			except Exception:
				pass
			new_instance.name = style_name
			new_instance.active = True
			font.instances.append(new_instance)
			_apply_location(new_instance, pairs)
			if localized:
				_apply_localized_names(new_instance, localized)
			existing_names.add(style_name)
			created.append((style_name, pairs))

	if not created and not skipped and not notes:
		notes.append("No name particles were found on the particle instances.")
	return created, skipped, notes


def _location_label(pairs):
	bits = []
	for axis, record in pairs:
		label = getattr(axis, "axisTag", None) or getattr(axis, "name", None) or "axis"
		if record.external is None:
			bits.append("%s=%s" % (label, _format_number(record.internal)))
		else:
			bits.append("%s=%s/%s" % (label, _format_number(record.internal), _format_number(record.external)))
	return ", ".join(bits)


def _format_number(value):
	number = float(value)
	if number.is_integer():
		return str(int(number))
	return str(number)


def _report(created, skipped, notes):
	print("Expand name particles to instances")
	for note in notes:
		print("  %s" % note)
	print("  Added %d static instance%s." % (len(created), "" if len(created) == 1 else "s"))
	for style_name, pairs in created:
		print("    %s  (%s)" % (style_name, _location_label(pairs)))
	if skipped:
		unique_skipped = []
		seen = set()
		for style_name in skipped:
			if style_name not in seen:
				seen.add(style_name)
				unique_skipped.append(style_name)
		print("  Left %d existing static instance%s in place:" % (len(unique_skipped), "" if len(unique_skipped) == 1 else "s"))
		for style_name in unique_skipped:
			print("    %s" % style_name)


def main():
	font = Glyphs.font if Glyphs else None
	if font is None:
		print("Open a font first.")
		return

	font.disableUpdateInterface()
	undo = None
	try:
		undo = font.undoManager()
	except Exception:
		undo = None
	if undo is not None:
		undo.beginUndoGrouping()
	try:
		created, skipped, notes = expand_font(font)
	finally:
		if undo is not None:
			undo.endUndoGrouping()
		font.enableUpdateInterface()

	_report(created, skipped, notes)
	if created:
		Glyphs.showNotification(
			"Name particles",
			"Added %d static instance%s." % (len(created), "" if len(created) == 1 else "s"),
		)


main()
