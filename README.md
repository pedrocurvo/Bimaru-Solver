# Bimaru-Solver
by Pedro Curvo (@pedrocurvo)

This project is a solver for the Bimaru Puzzle and was developed as a project for the course of Artificial Intelligence at Instituto Superior Técnico.

## 1. What is Bimaru?
A **Bimaru puzzle**, also known as **Battleship Solitaire** or **Battleships**, is a logic-based puzzle that involves filling a grid with ships while satisfying certain clues or hints provided. It is played on a rectangular grid, typically square in shape.
The objective of a Bimaru puzzle is to place a fleet of battleships (or ships) within the grid, following specific rules. The grid is divided into cells, and each cell can either contain a ship segment or be empty. The ships in the puzzle are represented by connected segments, either horizontally or vertically, without touching each other.

The puzzle begins with some clues provided outside the grid, often represented by numbers. These clues indicate the number of ship segments in each row and column. The clues may be placed at the beginning of each row and column or at the end, and they indicate the length of the ship segments and their arrangement within the corresponding row or column.

To solve the puzzle, you must use deductive reasoning and logical thinking to determine the placement of ships based on the given clues.
The rules for placing ships are as follows:
- Ships cannot touch each other, not even diagonally.
- Ships cannot occupy cells filled by Water.
- Each row and column must have the exact number of ship segments as indicated by the clues.
- The ships should be arranged in a straight line, either horizontally or vertically.

Using the provided clues and following these rules, you gradually fill in the grid, marking ship segments and empty cells until the entire puzzle is solved. The challenge lies in deducing the correct placement of ships by considering the constraints imposed by the clues and the already filled cells.

Bimaru puzzles can come in various sizes and difficulty levels, ranging from small grids with a few ships to larger grids with numerous ships. They provide an engaging and enjoyable exercise for logical thinking and problem-solving skills.

This Project is a solver for the Bimaru Puzzle on a **10x10 grid** with the following ships: 
- **4** ships with size **one**
- **3** ships with size **two**
- **2** ships with size **three**
- **1** ship with size **four**

## 2. Input Format
## 3. Output Format

## 4. Constraints
### 4.1 Zero Rows and Zero Columns
<img align="center" src="gifs/zero_rows_cols.gif" alt="Zeros" title="Zero Rows and Columns" width="300" height="300" align="center"/> 

### 4.2 Around Ships 
|     One Piece   |      Top Piece     |  Right Piece |
|:-----------------:|:---------------------:|:------:|
| <img align="center" src="gifs/one_ship.gif" alt="One" title="Around One Piece" width="200" height="200" align="center"/>  |  <img align="center" src="gifs/left.gif" alt="Top" title="Around Top Piece" width="200" height="200" align="center" style="transform:rotate(90deg);"/>  | <img align="center" src="gifs/left.gif" alt="Right" title="Around Right Piece" width="200" height="200" align="center" style="transform:rotate(180deg);"/>  |
| Middle Piece   |      Bottom Piece      |  Left Piece |
| <img align="center" src="gifs/middle.gif" alt="Middle" title="Around Middle Piece" width="200" height="200" align="center"/>  | <img align="center" src="gifs/left.gif" alt="Bottom" title="Around Bottom Piece" width="200" height="200" align="center" style="transform:rotate(270deg);"/> | <img align="center" src="gifs/left.gif" alt="Left" title="Around Left Piece" width="200" height="200" align="center"/>  | 


  
- Terminal Pieces 
- Terminal Rows 
- Terminal Columns 
- Fill Rows and Columns With Right Number of Pieces 
- Empty Spaces 
- Waters per Column and Row

### Heuristic 
- Probabilistic Grid