# Import required libraries
import neat.population
import pygame
import neat
import os 
import random
pygame.font.init()

# Define window dimensions
WIN_WiDTH = 500
WIN_HEIGHT = 800

# Load and scale bird images for animation (3 different poses)
BIRD_IMAGE = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png"))), 
              pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird2.png"))), 
              pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png")))]

# Load and scale other game assets
PIPE_IMAGE = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png")))
BASE_IMAGE = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")))
BG_IMAGE = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))

# Font for score display
STAT_FONT = pygame.font.SysFont("comicsans", 30)

class Bird:
    """
    Bird class representing the flappy bird
    Controls bird animation, movement, and physics
    """
    IMGS = BIRD_IMAGE
    MAX_ROTATION = 25  # Maximum rotation angle
    ROT_VEL = 20      # Rotation velocity
    ANIMATION_TIME = 5 # Time between animation frames

    def __init__(self, x, y):
        """Initialize bird position and properties"""
        self.x = x
        self.y = y
        self.tilt = 0          # Bird's tilt angle
        self.tick_count = 0    # Physics timer
        self.vel = 0           # Vertical velocity
        self.height = self.y   # Starting height
        self.img_count = 0     # Animation frame counter
        self.img = self.IMGS[0]# Current image

    def jump(self):
        """Make the bird jump by setting upward velocity"""
        self.vel = -10.5       # Negative velocity means upward movement
        self.tick_count = 0    # Reset physics timer
        self.height = self.y   # Store height at jump

    def move(self):
        """Update bird position based on physics"""
        self.tick_count += 1
        
        # Calculate displacement using physics equation: d = vt + (1/2)at^2
        d = self.vel * self.tick_count + 1.5 * self.tick_count ** 2
        
        # Terminal velocity checks
        if d >= 16:  # Maximum downward speed
            d = 16
        if d < 0:    # Upward movement boost
            d -= 2

        self.y = self.y + d
        
        # Tilt the bird based on movement
        if d < 0:  # Moving upward
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:      # Moving downward
            if self.tilt > -90:
                self.tilt -= self.ROT_VEL

    def draw(self, win):
        """Draw the bird with animation"""
        self.img_count += 1

        # Animation cycle through bird images
        if self.img_count < self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_count < self.ANIMATION_TIME*2:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME*3:
            self.img = self.IMGS[2]
        elif self.img_count < self.ANIMATION_TIME*4:
            self.img = self.IMGS[1]
        elif self.img_count == self.ANIMATION_TIME*4 + 1:
            self.img = self.IMGS[0]
            self.img_count = 0
        
        # No flapping animation when nose-diving
        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME*2
        
        # Rotate image around center for animation
        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        new_rect = rotated_image.get_rect(center=self.img.get_rect(topleft=(self.x, self.y)).center)
        win.blit(rotated_image, new_rect.topleft)
    
    def get_mask(self):
        """Get mask for pixel-perfect collision detection"""
        return pygame.mask.from_surface(self.img)

class Pipe:
    """
    Pipe class representing obstacles
    Controls pipe generation, movement, and collision
    """
    GAP = 200  # Gap between pipes
    VEL = 5    # Pipe movement speed

    def __init__(self, x):
        """Initialize pipe position and properties"""
        self.x = x
        self.height = 0
        self.top = 0           # Top pipe y position
        self.bottom = 0        # Bottom pipe y position
        self.PIPE_TOP = pygame.transform.flip(PIPE_IMAGE, False, True)  # Flipped pipe for top
        self.PIPE_BOTTOM = PIPE_IMAGE
        self.passed = False    # Flag if bird passed this pipe
        self.set_height()

    def set_height(self):
        """Randomly set the height of the pipe"""
        self.height = random.randrange(50, 400)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP

    def move(self):
        """Move pipe towards the left"""
        self.x -= self.VEL
    
    def draw(self, win):
        """Draw both top and bottom pipes"""
        win.blit(self.PIPE_TOP, (self.x, self.top))
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

    def collision(self, bird):
        """Check for collision with bird using mask collision"""
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)
        
        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        t_point = bird_mask.overlap(top_mask, top_offset)
        
        return bool(t_point or b_point)

class Base:
    """
    Base class representing the moving ground
    Creates infinite scrolling effect
    """
    VEL = -5   # Scroll speed
    WIDTH = BASE_IMAGE.get_width()
    img = BASE_IMAGE

    def __init__(self, y):
        """Initialize two bases for infinite scroll"""
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH
    
    def move(self):
        """Move bases to create scrolling effect"""
        self.x1 += self.VEL
        self.x2 += self.VEL

        # Reset positions when off screen
        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH
        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self, win):
        """Draw both bases"""
        win.blit(self.img, (self.x1, self.y))
        win.blit(self.img, (self.x2, self.y))

def draw_windows(win, birds, pipes, base, score):
    """Draw all game elements to the window"""
    win.blit(BG_IMAGE, (0,0))
    for pipe in pipes:
        pipe.draw(win)
    
    # Draw score
    text = STAT_FONT.render("Score: " + str(score), 1, (255,255,255))
    win.blit(text, (WIN_WiDTH - 10 - text.get_width(), 10))

    base.draw(win)
    for bird in birds:
        bird.draw(win)
    pygame.display.update()

def main(genomes, config):
    """
    Main game loop and NEAT algorithm implementation
    Handles:
    - Neural network creation and management
    - Game physics and collision
    - Fitness evaluation
    - Population management
    """
    nets = []    # Neural networks
    ge = []      # Genomes
    birds = []   # Birds

    # Create neural network for each genome
    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        birds.append(Bird(230, 350))
        g.fitness = 0
        ge.append(g)

    base = Base(730)
    pipes = [Pipe(500)]
    score = 0
    win = pygame.display.set_mode((WIN_WiDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()

    running = True
    while running:
        clock.tick(30)  # 30 FPS
        # Handle quit event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()

        # Determine which pipe to focus on
        pipe_ind = 0
        if len(birds) > 0:
            if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].PIPE_BOTTOM.get_width():
                pipe_ind = 1
        else:
            running = False
            break

        # Move birds and get neural network decisions
        for x, bird in enumerate(birds):
            bird.move()
            ge[x].fitness += 0.1  # Reward for staying alive

            # Neural network input and output
            output = nets[x].activate((
                bird.y,
                abs(bird.y - pipes[pipe_ind].height),
                abs(bird.y - pipes[pipe_ind].bottom)
            ))
            
            if output[0] > 0.0:  # Threshold for jump decision
                bird.jump()

        # Handle pipe movement and collision
        rem = []
        add_pipe = False
        for pipe in pipes:
            for x, bird in enumerate(birds):
                # Check collisions
                if pipe.collision(bird):
                    ge[x].fitness -= 1  # Penalty for collision
                    birds.pop(x)
                    nets.pop(x)
                    ge.pop(x)

                # Check if pipe was passed
                if not pipe.passed and pipe.x < bird.x:
                    pipe.passed = True
                    add_pipe = True

            # Remove pipes that are off screen
            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)

            pipe.move()
        
        # Add new pipe and increase score
        if add_pipe:
            score += 1
            for g in ge:
                g.fitness += 5  # Reward for passing pipe
            pipes.append(Pipe(600))

        # Remove old pipes
        for r in rem:
            pipes.remove(r)

        # Check for birds hitting ground or ceiling
        for x, bird in enumerate(birds):
            if bird.y + bird.img.get_height() >= 730 or bird.y < 0:
                birds.pop(x)
                nets.pop(x)
                ge.pop(x)

        base.move()
        draw_windows(win, birds, pipes, base, score)

def run(config_path):
    """
    Load NEAT config and run the evolution process
    """
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path
    )
    
    # Create population and add reporters
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    p.add_reporter(neat.StatisticsReporter())

    # Run for 50 generations
    winner = p.run(main, 50)

# Entry point
if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward.txt")
    run(config_path)