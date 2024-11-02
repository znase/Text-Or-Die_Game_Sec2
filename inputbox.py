import pygame as pg

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class inputBox:
    def __init__(self, game_instance):
        self.game_instance = game_instance  # รับอินสแตนซ์ Game จาก main.py
        self.window = self.game_instance.window  # ใช้ window จากอินสแตนซ์ Game

        # Set font and input box dimensions
        self.font = pg.font.Font(None, 36)
        self.input_box_width = 300
        self.input_box_height = 40
        self.input_box = pg.Rect(
            (self.game_instance.width - self.input_box_width) // 2 - 100,
            (self.game_instance.height // 3  * 2+ 50),
            self.input_box_width,
            self.input_box_height
        )
        self.color_inactive = pg.Color(30,144,255)
        self.color_active = pg.Color(0,191,255)
        self.color = self.color_inactive
        self.text = ''
        self.active = False
        self.cursor_visible = True
        self.cursor_timer = pg.time.get_ticks()
        self.input_box_visible = True

    def draw_input_box(self):
        txt_surface = self.font.render(self.text, True, self.color)
        width = max(500, txt_surface.get_width() + 10)
        self.input_box.w = width
        self.window.fill(WHITE, self.input_box)
        self.window.blit(txt_surface, (self.input_box.x + 5, self.input_box.y + 5))
        pg.draw.rect(self.window, self.color, self.input_box, 2)

    def draw_cursor(self):
        cursor_x = self.input_box.x + 5 + self.font.size(self.text)[0]
        cursor_height = self.input_box.height - 10
        pg.draw.rect(self.window, self.color, (cursor_x, self.input_box.y + 5, 2, cursor_height))
