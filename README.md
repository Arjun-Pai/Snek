# Snek

A simple endless obstacle-course game built with Python and Pygame.

Run through a procedurally generated level, jump over spikes, avoid lava, and try to achieve the highest score possible.

## Features

- Endless side-scrolling gameplay
- Randomly generated obstacles
- Spike and lava hazards
- Running and jumping animations
- Score tracking based on distance traveled
- Background music and death sound effects
- Restart functionality after game over
- Optional speed boost while holding Shift

## Requirements

- Python 3.8 or newer
- Pygame

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Arjun-Pai/Snek.git
   cd Snek
   ```

2. Install Pygame:

   ```bash
   pip install pygame
   ```

## Running the Game

Start the game with:

```bash
python Snek_game.py
```

## Controls

| Key | Action |
|---|---|
| `Space` | Jump |
| `W` | Jump |
| `Up Arrow` | Jump |
| `Left Shift` / `Right Shift` | Move faster |
| `R` | Restart after game over |
| `Esc` | Quit the game |

## Gameplay

Your character automatically moves forward through an endless level.

- Jump over spikes.
- Jump across lava.
- Avoid colliding with obstacles.
- Travel as far as possible to increase your score.
- Press `R` after losing to start a new run.

## Project Structure

```text
Snek/
├── Snek_game.py       # Main game script
├── music.mp3          # Background music
├── death.mp3          # Death sound effect
└── imgs/
    ├── Idle.png       # Idle animation
    ├── walking.png    # Walking animation
    ├── Jumping 1.png  # Jump animation frame
    └── Jumping 2.png  # Jump animation frame
```

## Notes

The game expects the image and audio assets to remain in their current locations relative to `Snek_game.py`.

If the audio files cannot be loaded, the game will continue running without music or sound effects.

## License

No license has been specified for this project yet.
