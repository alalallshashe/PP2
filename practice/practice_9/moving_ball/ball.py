import pygame

class Ball:
    def __init__(self, x, y, radius, color, width, height):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.screen_width = width
        self.screen_height = height
        self.step = 20

    def move(self, dx, dy):
        # Рассчитываем новые координаты
        new_x = self.x + dx * self.step
        new_y = self.y + dy * self.step

        # Проверка границ (центр +/- радиус)
        if self.radius <= new_x <= self.screen_width - self.radius:
            self.x = new_x
        
        if self.radius <= new_y <= self.screen_height - self.radius:
            self.y = new_y

    def draw(self, screen):
        # Рисуем тень для презентабельности
        shadow_color = (100, 100, 100)
        pygame.draw.circle(screen, shadow_color, (self.x + 3, self.y + 3), self.radius)
        # Рисуем мяч
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)