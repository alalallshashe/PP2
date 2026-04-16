import pygame
import datetime
import os

class MickeyClock:
    def __init__(self, screen_width, screen_height):
        self.width = screen_width
        self.height = screen_height
        self.center = (screen_width // 2, screen_height // 2)
        
        # Путь к папке с картинками
        assets_path = os.path.join(os.path.dirname(__file__), "images")
        
        # Загрузка твоих файлов
        self.bg = pygame.image.load(os.path.join(assets_path, "mickey.png"))
        self.bg = pygame.transform.scale(self.bg, (self.width, self.height))
        
        # Загружаем руки (минуты - правая, секунды - левая)
        self.hand_min_img = pygame.image.load(os.path.join(assets_path, "right_hand.png"))
        self.hand_sec_img = pygame.image.load(os.path.join(assets_path, "left_hand.png"))

    def get_angles(self):
        now = datetime.datetime.now()
        # В Pygame 0 градусов — это 3 часа (направо). 
        # Чтобы 0 был на 12 часах, нужно вычесть угол из текущего положения.
        # Также инвертируем, чтобы шло по часовой стрелке.
        sec_angle = -now.second * 6
        min_angle = -now.minute * 6
        return sec_angle, min_angle

    def draw(self, surface):
        # 1. Рисуем циферблат (mickey.png)
        surface.blit(self.bg, (0, 0))
        
        sec_angle, min_angle = self.get_angles()
        
        # 2. Отрисовка минутной стрелки (Right hand)
        self._blit_rotate(surface, self.hand_min_img, min_angle)
        
        # 3. Отрисовка секундной стрелки (Left hand)
        self._blit_rotate(surface, self.hand_sec_img, sec_angle)

    def _blit_rotate(self, surface, image, angle):
        """Центрированное вращение"""
        # Вращаем картинку. По умолчанию вращение идет вокруг центра Rect
        rotated_image = pygame.transform.rotate(image, angle)
        new_rect = rotated_image.get_rect(center=self.center)
        surface.blit(rotated_image, new_rect)