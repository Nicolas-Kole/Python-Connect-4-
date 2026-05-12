# CONNECT 4

## Demo

Demo Video: https://youtu.be/Rn4RS07Gge4

## GitHub Repository

https://github.com/Nicolas-Kole/Python-Connect-4-.git

## Description

Connect 4 is a Python game project created using the Pygame library. The game recreates the classic Connect 4 experience while adding additional features such as multiple game modes, CPU difficulties, fullscreen support, keyboard controls, and visual effects.

The program includes two game modes: Classic Mode and Timed Mode. Classic Mode follows the standard Connect 4 rules, while Timed Mode gives players only five seconds to make a move before a chip is automatically dropped into the selected column. Players can also choose between Player vs Player and Player vs CPU gameplay.

The CPU includes three difficulty levels. Easy Mode selects random valid moves, Intermediate Mode can block the player, and Advanced Mode analyzes the board and scores moves strategically to create smarter gameplay.

The project was built using object-oriented programming. The `Button` class handles menu buttons and click detection, the `Board` class manages the grid and win detection, and the `Game` class controls gameplay, CPU behavior, timers, menus, and visual effects like confetti animations and win highlights.

One of the biggest challenges during development was implementing reliable win detection for horizontal, vertical, and diagonal connections. Another challenge was creating CPU logic that became progressively smarter across the different difficulty levels.

Future improvements for the project could include sound effects, animated chip drops, custom themes, and additional visual polish.

Overall, this project demonstrates Python programming concepts such as game loops, event handling, object-oriented design, AI logic, timers, and interactive user interface systems within a fully playable Connect 4 game.


