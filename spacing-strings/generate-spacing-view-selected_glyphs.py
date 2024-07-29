# MenuTitle: Make tab with spacing string for selected glyphs
__doc__ = """
    A simple way to make an arbitrary spacing string.

    Open in a code editor to adjust!
"""

# Update to make different lists. copy these from your font editor as space-seperated glyph names

# Configurable pattern. By default, this will put glyphs between nn and oo
# Remove leading slashes and trailing spaces if you instead want to proof characters (not just glyph names), especially for InDesign, etc.
# Add "\\n" at the end of your pattern if you want your output to include newlines, e.g. for the RoboFont space center
# pattern = "HH /$1  HOHO /$1  OO" # for zero-width combining accents
# pattern = "nn/$1 nono/$1 oo" # lowercase only
pattern = "HH/$1 HOHO/$1 OO\nnn/$1 nono/$1 oo"

# If you want to change the way each pattern is separated, change this. It adds a basic newline (`\n`) by default.
# Change to a space (`" "`) if you want to only use spaces, e.g. as one option for an easy InDesign proof (newlines & columns might be better, though).
# Change to "\\n" at the end of your pattern if you want your output to include newlines in the RoboFont space center.
separator = "\n"

text = "HHHOHOHOOO\nnnnononooo\n"

font = Glyphs.font
myLayers = Glyphs.font.selectedLayers

# The code part. This goes through selected glyphs and outputs a proofing list.
for layer in myLayers:
    name = layer.parent.name

    if ".sc" in name:
        smallCapPattern = (
            "HH/$1 HOHO/$1 OO\n/H.sc /H.sc /$1 /H.sc /O.sc /H.sc /O.sc /$1 /O.sc /O.sc"
        )
        text += smallCapPattern.replace("$1", name) + separator

    else:
        text += pattern.replace("$1", name) + separator


font.newTab(text)
