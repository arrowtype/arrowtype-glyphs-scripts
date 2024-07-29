# MenuTitle: Make tab with bigger fraction spacing string
__doc__ = """
    A simple way to make a fraction spacing string.

    Assumes name /fraction and /one.numr /two.dnom, etc, exist.

    Open in a code editor to adjust!
"""

# Update to make different lists. copy these from your font editor as space-seperated glyph names

# Configurable pattern. By default, this will put glyphs between nn and oo
# Remove leading slashes and trailing spaces if you instead want to proof characters (not just glyph names), especially for InDesign, etc.
# Add "\\n" at the end of your pattern if you want your output to include newlines, e.g. for the RoboFont space center
# pattern = "HH /$1  HOHO /$1  OO" # for zero-width combining accents
# pattern = "nn/$1 nono/$1 oo" # lowercase only
pattern = "H$1 H"

# If you want to change the way each pattern is separated, change this. It adds a basic newline (`\n`) by default.
# Change to a space (`" "`) if you want to only use spaces, e.g. as one option for an easy InDesign proof (newlines & columns might be better, though).
# Change to "\\n" at the end of your pattern if you want your output to include newlines in the RoboFont space center.
separator = "\n"

numerals = "zero one two three four five six seven eight nine".split(" ")

text = ""

font = Glyphs.font

for numr in numerals:
    text += "H"

    for dnom in numerals:

        fraction = f"/{numr}.numr/fraction/{dnom}.dnom"

        text += pattern.replace("$1", fraction)

    text += "H" + separator

font.newTab(text)
