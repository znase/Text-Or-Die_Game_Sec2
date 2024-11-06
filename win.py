import pygame as pg

class Win:
    def __init__(self, game_instance):
        self.game_instance = game_instance
        original_win_img = pg.image.load(r"assets/win.png")
        
        # Scale win.png with padding (20 pixels on each side)
        self.win_img = pg.transform.scale(
            original_win_img, 
            (100, 100)
        )

        # Set initial position: middle of screen (X-axis) and starting Y position
        self.win_x = (self.game_instance.width - self.win_img.get_width()) // 2
        self.win_y = -1600  # Starting just above the visible screen
        self.target_y = self.win_y

    def move_up(self, char_count):
        """Set a new target position based on the number of correct characters."""
        move_distance = char_count * 20
        self.target_y += move_distance

    def update(self, character_rect):
        """Gradually move win.png down in sync with the background."""
        
        # Move win.png downwards as the background moves up
        if self.win_y < self.target_y:
            self.win_y += 1.5

        # Create a rect for the win image to check for collision with the character
        win_rect = pg.Rect(self.win_x, self.win_y-10, self.win_img.get_width(), self.win_img.get_height())

        # Check if win.png collides with the character
        if win_rect.colliderect(character_rect):
            return True  # Signal that win.png has collided with the character

        return False

    def draw(self):
        """Draw win.png at the current position (top layer of the screen)."""
        self.game_instance.window.blit(self.win_img, (self.win_x, self.win_y))
