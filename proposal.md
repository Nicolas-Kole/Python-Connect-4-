# Python Connect 4

#Repository
<https://github.com/Nicolas-Kole/Python-Connect-4-.git>

## Description
A simplified version of Connect 4 built using Python and Pygame. 
The project focuses on interactive game design and visual feedback, allowing users to play either against another player or a CPU opponent.

## Features
- 7x6 Board
  - Use a 2D list to store the board values
  - Use pygame to draw the chip slots

- Player VS Player
  - Track turns using a variable that switches between Player 1 and Player 2 after each move
  - Assign red chips to Player 1 and yellow chips to Player 2

- Player VS CPU
  - A game mode where the CPU automatically selects a column
  - Use random column selection while checking for valid spaces in columns

- Mouse Click Inputs
  - Detect mouse clicks using `pygame.MOUSEBUTTONDOWN`
  - Use `event.pos` to get the mouse position and determine which column was clicked

- Keyboard Inputs
  - Use `pygame.KEYDOWN` to detect left and right arrow keys
  - Move left or right to select a column 
  - Press ENTER to drop a chip in that column

- Chip Stacking System
  - When a column is selected, place the chip in the lowest available row
  - Loop from the bottom row upward to find the first empty space

- Win Detection
  - Check for 4 matching values in horizontal, vertical, or diagonal directions
  - Use loops to compare 4 positions in a row

- Win Display
  - Display text on the screen to show who won the game

- Full Column Detection
  - Check the top row of the column before placing a chip
    - If full, block the move and ignore the click

- Turn Indicator
  - Use text rendering to to display whose turn it is
  - Update the text every time the turn changes

- Main Menu Screen
  - Create a separate screen before the game loop starts
  - Use rectangles as buttons and detect clicks on them to choose between VS Player and VS CPU

- Play Again
  - After a win, show options on screen to either play again or go to the main menu screen
  - Reset variables when restarting the game

- Tutorial Pop-Up
  - Display a short instruction screen at the start explaining how to play Connect 4 and 
  - Also explains how to use the left arrow, right arrow and enter keys or the mouse to drop chips or select a column
  - Player can press the space key to skip the tutorial

- Exit Game
  - Allow the player to quit the game from the menu or during gameplay by pressing the ESC key

## Challenges
-The program being able to detect all possible win conditions using loops
- Being able to properly detect both mouse and keyboard input in the same program
- Making sure chips stack correctly from the bottom without skipping spaces 
- Preventing players from placing chips in full columns
- Keeping track of turns and making sure they switch correctly every time
- Making sure the CPU choose valid moves and not pick full columns

## Outcomes
Ideal Outcome: 
- A fully functional Connect 4 game with Player vs Player and Player vs CPU modes with win detection and point and click or keyboard controls.

Minimal Viable Outcome:
- A working Connect 4 game where two players can take turns placing their chips onto the board with working win detection.

## Milestones
-Week 1
  1. Create the Pygame window and main game loop
  2. Draw the board grid and empty slots visually on screen
  3. Add chip dropping logic

-Week 2
  1. Implement switching between Player 1 and Player 2 turns
  2. Add full column detection to prevent invalid moves
  3. Implement mouse click input and keyboard controls to select columns 

-Week 3
  1. Implement win detection
  2. Display win message when a player wins
  3. Add logic to stop further moves from being made when a game is finished

-Final Week
  1. Add Player vs CPU mode
  2. Ensure CPU avoids full columns
  3. Add play again feature to restart the game or return to the main menu
