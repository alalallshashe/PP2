import pygame
import math

def draw_pencil(surface, color, start_pos, end_pos, thickness=3):
    """
    Рисует линию между двумя точками. 
    Использование линий вместо точек делает рисование плавным.
    """
    if start_pos and end_pos:
        pygame.draw.line(surface, color, start_pos, end_pos, thickness)

def draw_eraser(surface, pos, size=20):
    """
    Рисует круг цветом фона (белым), имитируя ластик.
    """
    pygame.draw.circle(surface, (255, 255, 255), pos, size)

def draw_rectangle(surface, color, start_pos, end_pos, thickness=2):
    """
    Рисует прямоугольник. 
    Используем min/abs, чтобы можно было тянуть рамку в любую сторону.
    """
    if start_pos and end_pos:
        x = min(start_pos[0], end_pos[0])
        y = min(start_pos[1], end_pos[1])
        width = abs(start_pos[0] - end_pos[0])
        height = abs(start_pos[1] - end_pos[1])
        pygame.draw.rect(surface, color, (x, y, width, height), thickness)

def draw_line(surface, color, start_pos, end_pos, thickness=2):
    """
    Рисует прямую линию между двумя точками.
    """
    if start_pos and end_pos:
        pygame.draw.line(surface, color, start_pos, end_pos, thickness)

def fill_area(surface, color, pos):
    """
    Заполняет область цветом, начиная с заданной позиции.
    Использует flood fill алгоритм.
    """
    if not (0 <= pos[0] < surface.get_width() and 0 <= pos[1] < surface.get_height()):
        return
    
    # Получаем цвет в начальной позиции
    start_color = surface.get_at(pos)
    if start_color == color:
        return
    
    # Создаем стек для flood fill
    stack = [pos]
    while stack:
        x, y = stack.pop()
        if not (0 <= x < surface.get_width() and 0 <= y < surface.get_height()):
            continue
        if surface.get_at((x, y)) != start_color:
            continue
        
        # Заполняем пиксель
        surface.set_at((x, y), color)
        
        # Добавляем соседей
        stack.extend([(x+1, y), (x-1, y), (x, y+1), (x, y-1)])

def draw_circle(surface, color, start_pos, end_pos, thickness=2):
    """
    Рисует круг, где start_pos — центр, а расстояние до end_pos — радиус.
    """
    if start_pos and end_pos:
        # math.hypot вычисляет расстояние между двумя точками (гипотенузу)
        radius = int(math.hypot(end_pos[0] - start_pos[0], end_pos[1] - start_pos[1]))
        if radius > 0:
            pygame.draw.circle(surface, color, start_pos, radius, thickness)