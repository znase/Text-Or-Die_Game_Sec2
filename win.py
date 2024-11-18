import pygame as pg

class Win:
    def __init__(self, game_instance):
        """
        สร้างคลาส Win สำหรับการแสดงภาพ 'win.png' 
        และจัดการตำแหน่งและการเคลื่อนไหว
        """
        self.game_instance = game_instance  # อ้างอิงถึงอินสแตนซ์ของเกมหลัก
        
        # โหลดภาพ 'win.png' และปรับขนาดให้เป็น 100x100 พิกเซล
        original_win_img = pg.image.load(r"assets/win.png")
        self.win_img = pg.transform.scale(original_win_img, (100, 100))

        # กำหนดตำแหน่งเริ่มต้นให้ตรงกลางของหน้าจอ (แกน X) 
        # และแกน Y เริ่มต้นอยู่เหนือจอภาพ
        self.win_x = (self.game_instance.width - self.win_img.get_width()) // 2
        self.win_y = -1600  # เริ่มต้นอยู่นอกจอด้านบน
        self.target_y = self.win_y  # ตำแหน่งเป้าหมายของแกน Y

    def move_up(self, char_count):
        """
        กำหนดตำแหน่งเป้าหมายใหม่ของภาพ win.png ตามจำนวนตัวอักษรถูกต้อง
        """
        move_distance = char_count * 40  # คำนวณระยะที่ต้องเลื่อนขึ้น
        self.target_y += move_distance  # เพิ่มตำแหน่งเป้าหมาย

    def update(self, character_rect):
        """
        อัปเดตตำแหน่งของภาพ win.png ให้ค่อย ๆ เคลื่อนลง
        และตรวจสอบว่ามีการชนกับตัวละครหรือไม่
        """
        # เลื่อนภาพ win.png ลงเมื่อยังไม่ถึงตำแหน่งเป้าหมาย
        if self.win_y < self.target_y:
            self.win_y += 1.5  # ความเร็วในการเลื่อนภาพ win.png

        # สร้างเรคแทงเกิลของภาพ win.png สำหรับตรวจสอบการชน
        win_rect = pg.Rect(self.win_x, self.win_y - 10, self.win_img.get_width(), self.win_img.get_height())

        # ตรวจสอบการชนระหว่าง win.png และตัวละคร
        if win_rect.colliderect(character_rect):
            return True  # ส่งสัญญาณว่ามีการชนเกิดขึ้น
        return False  # หากไม่มีการชน ให้คืนค่า False

    def draw(self):
        """
        วาดภาพ win.png ในตำแหน่งปัจจุบันที่ด้านบนสุดของหน้าจอ
        """
        self.game_instance.window.blit(self.win_img, (self.win_x, self.win_y))  # วาดภาพ win.png บนหน้าจอ
