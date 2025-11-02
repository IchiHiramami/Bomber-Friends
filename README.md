# 💣 Bomber Friends the CLI Game
===========================

CLI game taking advantage of Python's OOP capabilities.

---

# 💥 Ultimate Bomber Friends

Welcome to **Ultimate Bomber Friends**, a fast-paced, grid-based multiplayer game where players battle it out using bombs, skills, and strategy. This project is built in Python and runs in the terminal, featuring real-time movement, skill activation, and dynamic board updates.

---

## 🎮 Gameplay Overview

- Two players compete on a grid-based board.
- Players can move, place bombs, and activate special skills.
- The board updates in real time, with visual feedback for bombs, skills, and warnings.
- Skills like **Speed Boost**, **Quick Hand**, and **Raygun** add tactical depth.

---

## 🧠 Features

- **Real-time movement** using keyboard input (`WASD` for Player 1, Arrow Keys for Player 2).
- **Bomb placement** with optional skill modifiers.
- **Raygun skill** highlights danger zones without blocking movement.
- **Speed Boost** allows double-step movement if path is clear.
- **Quick Hand** places bombs in adjacent cells.
- **Skill pickups** scattered across the board.
- **ASCII-based rendering** for visual clarity in terminal.

---

## 🕹️ Controls

### Player 1
- Move: `W`, `A`, `S`, `D`
- Bomb: `E`
- Special Bomb: `Q`

### Player 2
- Move: Arrow Keys
- Bomb: `P`
- Special Bomb: `O`

---

## 🧱 Cell Types

| Symbol | Meaning                  |
|--------|--------------------------|
| `[☺]`  | Player 1                 |
| `[☻]`  | Player 2                 |
| `[◎]`  | Bomb                     |
| `[★]`  | Skill pickup             |
| `[☒]`  | Breakable wall           |
| `[▣]`  | Unbreakable wall         |
| `[#]`  | Raygun warning zone      |
| `[ ]`  | Empty/passable cell      |
---

## 🛠 Development Log

### BASIC BUILD UP SESSION
- **Session 1:** October 28 19:27–20:13 → Basic Class Definition, Interobject actionability  
- **Session 2:** October 28 21:58–23:59 → Experimentation with Threading  
- **Session 3:** October 29 00:27–02:01 → Random Spawnpoint, Assignment of Properties, Grid Reflection  
- **Session 4:** October 29 02:50–03:41 → Refactoring and Debugging  
- **Session 5:** October 29 09:31–11:13 → Player and Enemy Movement, 2-Player Gamemode  
- **Session 6:** October 29 11:47–12:52 → Asynchronization of Functions  
- **Session 7:** October 29 13:36–14:30 → Removal of Threading, Replaced with Asyncio  
  > TODO: Critical Bug in Board Creation (Player vs People)  
- **Session 8:** October 29 16:03–17:37 → SuperSkills Implementation  
  > TODO: Critical Bug disallowing player movement after bomb placement  
- **Session 9:** October 30 09:42–11:30 → Gave up, initiated refactoring due to non-modular design

### REFACTORING SESSION
- **Session 1:** October 31 16:20–16:50 → Started Refactoring, emotional damage  
- **Session 2:** November 1 11:00–12:30 → Regret intensifies  
- **Session 3:** November 1 14:32–18:47 → FIXED: Movement bug, restored original functionality  
- **Session 4:** November 1 19:54–22:24 → ALL GAME FUNCTIONS IMPLEMENTED  
  > TODO: Fix bug in raygun function

---

## 🧪 Known Issues

- Players standing on raygun-highlighted cells may get stuck if `isPassable` isn't properly reset.
- Movement logic assumes grid is square; rectangular grids may need adjustments.
- Terminal compatibility may vary depending on font and encoding.

---

## 📁 Project Structure

```
├── main.py
├── Refactored_Bomb_Friend_Game.py
├── README.md
```

---
