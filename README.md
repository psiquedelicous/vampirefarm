# vampirefarm
Puzzle game in pygame for LOWREZJAM 2019

<img src="https://img.itch.zone/aW1nLzI3MzkyNzMuZ2lm/347x500/fLoeGs.gif" width="300" height="300" align="center">

You are a vampire lord conquering the world. Humans are your only enemy, but also your food. 
Subjugate all the humans without starving, maintaining all humans in farms for your underlings to feast.

## Objectives
Transform every human unit in a level-farm unit.

## Rules
Each turn the player can move each vampire unit one time.

Vampires and humans are affected by the combined level of the enemies that surround them.

### Humans raise their level:

+Left alone;

+Near vampires of combined lower level.

### Humans lower their level:

+Near vampires of combined higher level.

### Vampires raise their level:

+Near humans of combined lower level.

### Vampires lower their level or die:

+Near vampires of combined higher level

A level-farm unit is created lowering the level of a level 1 human. The unit can die if it's surrounded by too many vampires for a certain period of time.

## Controls
Left Mouse Click - select tile

Right Mouse Click - deselect tile

Space - new turn

## About the development
The base of the game was made entirely in pygame in one week (11/8 - 17/8). 

Code by Catarina Pereira, some help by Pedro Caetano.

Art by Pedro Caetano.

### December update:

Animations (by Pedro Caetano);

Sounds (by Pedro Caetano);

Background music (by Catarina Pereira on BeepBox);

Changes to the splash screen, win and game over screens;

Retro font (8-bit pusab by Seba Perez);

Retro mouse cursor (by Pedro Caetano);

Change of selection highlights.

### Future updates?

Maybe I'll add a level creator in the future, but the Python code is easy to change to create a new level.

## Play without Python
File available on [itch.io](https://psiquedelicous.itch.io/vampire-farm)
