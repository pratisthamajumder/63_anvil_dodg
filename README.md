# Anvil Dodge Repair Lab

This project is a modular survival dodger game using **Pygame**. It introduces students to falling hazard mechanics, boundary management, collision detection, and survival time tracking within a clean, object-oriented codebase.

---

## What's Provided

A working Anvil Dodge game with:

- A player character that can move left and right across the ground line using keyboard inputs
- Heavy anvils spawned continuously from random horizontal positions falling toward the ground
- Collision detection when an anvil hits the player, triggering game over
- Real-time survival time tracking and a Game Over overlay with restart functionality

It has **one deliberate bug** and **three optional features** left as tasks to implement. You are expected to **analyze**, **interact with an AI assistant**, and **complete/fix** the game to make it fully functional and more interesting.

### **Use an LLM (e.g. ChatGPT or Claude) as your debugging and pair-programming partner for this lab.**
---

## Getting Started

### Setup

1. Make sure you have Python 3.10+ installed.
2. Install dependencies:

```bash
pip install pygame
```

3. Run the game:

```bash
python main.py
```

**Controls:** Left / A to move left, Right / D to move right, R to reset after Game Over.   


## Tasks to Complete

Each task must be completed using an iterative process involving LLM suggestions and your critical code review.

### Task 1: Fix the player off-screen boundary bug

The player character can walk past the left and right screen edges into hidden space where falling anvils cannot hit them, exploiting an infinite survival time. Constrain the player so movement is strictly clamped within the visible boundaries of the display window.

### Task 2: Implement dynamic difficulty scaling

The player character can walk past the left and right screen edges into hidden space where falling anvils cannot hit them, exploiting an infinite survival time. Constrain the player so movement is strictly clamped within the visible boundaries of the display window.

### Task 3: Implement speed-based anvil warning tints

All falling hazards currently share the same grey appearance regardless of velocity. Apply visual hazard tiers to falling anvils by tinting higher-velocity anvils with distinct hot warning colors to signal urgent threats to the player.

### Task 4: Implement ground impact FX & screen shake

Anvils reaching the floor vanish silently without physical presence. Add kinetic feedback on impact—such as localized dust cloud particles or a subtle camera shake whenever an anvil smashes into the ground line.

---

## Expected Behavior

- The player cannot move beyond the visible left and right edges of the screen
- Anvils fall continuously from randomized X coordinates and clean up after passing below the screen
- Touching any falling anvil immediately triggers the Game Over screen and stops time tracking
- Pressing R after losing resets the player, clears all falling anvils, and restarts the survival timer

---

## Folder Structure

```
anvil_dodge/
├── game/
│   ├── anvil.py
│   ├── game_engine.py
│   └── player.py
├── main.py
└── README.md
```

---

## Submission Checklist

Submission is only the following three things:

- [] A 10-second video of gameplay **before** your changes, showing the bug/broken behavior
- [] A 10-second video of gameplay **after** your changes, showing the bug fixed and the new features working
- [] The Chat/LLM used page link, with the complete chat history
