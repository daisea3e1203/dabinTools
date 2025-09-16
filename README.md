# Dabin Tools

Houdini package with some shelf tools and nodes

## Installation

- Copy dabinTools.json to the package folder (ex: C:/Users/username/Documents/houdini18.5/packages in Windows)
- Open dabinTools.json in your favorite code editor or notepad and edit the path to wherever you cloned this repository

## What's in here ?

### Tools
Add shelf tab "dabin_tools" to your Shelf. In it you will find the tools below and more.
Some are pretty usable, while others are minimal examples from the houdini document and random demos.
- Copy node as Object Merge
- Place Box (while initializing its dimensions to the selected node's bounding box)
  - Partially deprecated in favor of the Shape Spawner node.
- Align Nodes (Tailored to the way I like to organize my nodes.)
  - When there is a single node selected, this will try and layout the selected node's parent nodes recursively.
  - If there are multiple selections, it will layout the selected nodes using the youngest node as the pivot.
  - Try experimenting what it does to some random tree of nodes. Or look into the script.
- Create PBR Shader
  - Select one texture file, and create a Redshift shader with all related textures pluged in the right place.
  - Demands a certain kind of filename, look into script for details.
  - Usable, but might behave unexpectedly in some cases. Its not going to delete your file or do anything destructive so
    it should be fine to play around with.
- etc...

### Nodes
- Mirror and Weld: Mirror and weld input using the origin or 2nd input's center as the pivot
- Extend Shape: Cut input along plane and extend.
- Shape Spawner: Spawn different kinds of shape initialized to the size of the second input's bounding box. Intelligently adds and lays out spawned shapes to the first input's merge node.
- Array: Array mesh. Copy and transform where you can set the endpoint instead of the spacing. Can also use second input's bounding box to calculate spacing.
