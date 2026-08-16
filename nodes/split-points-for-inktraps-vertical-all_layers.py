#MenuTitle: Split Selected Nodes Vertically (All Layers)
# -*- coding: utf-8 -*-
__doc__ = """
Splits nodes into two and separates them by 2 units at vertical angle.
Great for making doubles of side extemes, as a possible part of making a condensed font.

Applies change to all layers (layers must be compatible.)

Credit to @danielgamage:
https://github.com/danielgamage/Glyphs-Scripts/blob/17685b4e04cd194ce05683859df78bb3a068833d/Nodes/Split%20Selected%20Nodes.py
"""

import Cocoa
import math
import copy

def translateNode(node, distance):
    path = node.parent
    angleFloat = path.tangentAngleAtNode_direction_(node, path.direction) * path.direction
    print(angleFloat)
    print(path.direction)
    angleSnapped = round(angleFloat / 90) * 90
    # always make corners LESS acute and separate away from vertex
    direction = -1 if angleFloat < angleSnapped else 1
    # convert to radians for translation
    angleSnappedRadians = angleSnapped * (math.pi/180)

    x = node.x + distance * direction * math.cos(angleSnappedRadians)
    y = node.y + distance * direction * math.sin(angleSnappedRadians)
    newPoint = Cocoa.NSMakePoint(x, y)
    return newPoint

def splitNode(node, path):

    print(node.parent.parent)
    cloneNode = node.copy()
    # make sure nodes don't go in the same direction
    originPosition = translateNode(node, 1)
    clonePosition = translateNode(node, -1)

    path.insertNode_atIndex_(cloneNode, node.index)

    # make joining path segment a line
    if node.type == "curve":
        node.type = "line"

    # separate nodes from origin
    node.setPosition_(originPosition)
    cloneNode.setPosition_(clonePosition)


font = Glyphs.font

current_layer = Glyphs.font.selectedLayers[0]

compatible = current_layer.parent.mastersCompatible


for node in current_layer.selection:
    path = node.parent

    path_index = current_layer.indexOfPath_(path)
    node_index = node.index

    print("path_index", path_index)

    # if layers not compatible, just run on node of current layer
    if not compatible:
        splitNode(node)
        continue

    # if layers are compatible
    # get node index, and run script on that node of each layer
    for layer in current_layer.parent.layers:

        # skip non-master layers? (Would this skip special layers, too?)
        if layer.name not in [master.name for master in font.masters]:
            continue

        layer_path = layer.paths[path_index]
        layer_node = layer_path.nodes[node_index]
        splitNode(layer_node, layer_path)


