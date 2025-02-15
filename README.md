# Flappy Bird AI using NEAT

This project implements an AI that learns to play Flappy Bird using the NEAT (NeuroEvolution of Augmented Topologies) algorithm. The AI starts with no knowledge of the game and progressively learns to navigate through the pipes by evolving neural networks over multiple generations.

## Demo

![2025-02-15 14-46-22-VEED](https://github.com/user-attachments/assets/31a00787-70fe-46f3-8c72-a9c1e1125c91)

## Features

- Implementation of Flappy Bird game mechanics using Pygame
- NEAT algorithm integration for evolutionary learning
- Neural network visualization for the best performing birds
- Real-time display of game statistics and fitness scores
- Configurable NEAT parameters for experimentation

## Requirements

- Python 3.x
- pygame
- neat-python
- os
- random

## Installation

1. Clone the repository
```bash
git clone https://github.com/[your-username]/flappy-bird-neat.git
cd flappy-bird-neat
```

2. Install required packages
```bash
pip install -r /requirments.txt
```

3. Run the game
```bash
python main.py
```

## Project Structure

```
flappy-bird-neat/
│
├── main.py           # Main game and NEAT implementation
├── config.txt        # NEAT configuration file
│
├── imgs/
│   ├── bird1.png    # Bird animation frames
│   ├── bird2.png
│   ├── bird3.png
│   ├── pipe.png     # Pipe obstacle
│   ├── base.png     # Ground texture
│   └── bg.png       # Background image
│
└── README.md
```

## How It Works

### Game Mechanics
- The bird can flap upward using the neural network's output
- Pipes spawn at regular intervals with random heights
- Score increases as the bird successfully passes through pipes
- Collision with pipes or going out of bounds ends the run

### NEAT Implementation
- Input Layer (3 neurons):
  - Bird's Y position
  - Distance to top pipe
  - Distance to bottom pipe
- Output Layer (1 neuron):
  - Jump probability (>0.5 triggers a jump)
- Fitness Function:
  - +0.1 points for each frame survived
  - +5 points for each pipe passed
  - -1 point for collision

### Neural Network Evolution
1. Initial population of random neural networks
2. Each network controls a bird
3. Birds that perform better have higher chance to pass their genes
4. Networks evolve through mutation and crossover
5. Process repeats until satisfactory performance is achieved

## Configuration

The `config.txt` file contains all NEAT algorithm parameters. Key parameters include:

- Population size: 100
- Fitness threshold: 100
- Number of generations: 50
- Network architecture parameters
- Species and reproduction settings

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- NEAT-Python library developers
- Original Flappy Bird game creators

## Author

Ayushman Rathi
- GitHub: @AMRzip
- Email: ayushmanrathi0@gmail.com

## Future Improvements

- [ ] Add checkpointing to save training progress
- [ ] Implement adjustable game speed for faster training
- [ ] Add visualization of neural network architecture
- [ ] Create a mode to showcase the best performing AI
- [ ] Implement parallel training for faster evolution
