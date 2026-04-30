import pygame
import math
from collections import deque
def draw_shape(surface, tool, sp, ep, color, bsize):
    if tool == "rect":
        r = pygame.Rect(sp, (ep[0]-sp[0], ep[1]-sp[1]))
        pygame.draw.rect(surface, color, r, bsize)
    elif tool == "circle":
        dx, dy = ep[0]-sp[0], ep[1]-sp[1]
        rad = int((dx**2+dy**2)**0.5)
        pygame.draw.circle(surface, color, sp, rad, bsize)
    elif tool == "square":
        size = max(abs(ep[0]-sp[0]), abs(ep[1]-sp[1]))
        pygame.draw.rect(surface, color, pygame.Rect(sp, (size, size)), bsize)
    elif tool == "rtriangle":
        pts = [sp, (ep[0], sp[1]), ep]
        pygame.draw.polygon(surface, color, pts, bsize)
    elif tool == "etriangle":
        side = abs(ep[0]-sp[0])
        h = int((math.sqrt(3)/2)*side)
        p1, p2, p3 = sp, (sp[0]+side, sp[1]), (sp[0]+side//2, sp[1]-h)
        pygame.draw.polygon(surface, color, [p1, p2, p3], bsize)
    elif tool == "rhombus":
        cx = (sp[0]+ep[0])//2
        cy = (sp[1]+ep[1])//2
        dx = abs(ep[0]-sp[0])//2
        dy = abs(ep[1]-sp[1])//2
        pts = [(cx, cy-dy), (cx+dx, cy), (cx, cy+dy), (cx-dx, cy)]
        pygame.draw.polygon(surface, color, pts, bsize)
    elif tool == "line":
        pygame.draw.line(surface, color, sp, ep, bsize)
def flood_fill(surface, pos, fill_color):
    x, y = pos
    w, h = surface.get_size()
    if not (0 <= x < w and 0 <= y < h):
        return
    target = surface.get_at((x, y))[:3]
    fill_c = fill_color[:3]
    if target == fill_c:
        return
    queue = deque([(x, y)])
    visited = {(x, y)}
    while queue:
        cx, cy = queue.popleft()
        surface.set_at((cx, cy), fill_color)
        for nx, ny in ((cx+1,cy),(cx-1,cy),(cx,cy+1),(cx,cy-1)):
            if (nx, ny) not in visited and 0 <= nx < w and 0 <= ny < h:
                if surface.get_at((nx, ny))[:3] == target:
                    visited.add((nx, ny))
                    queue.append((nx, ny))