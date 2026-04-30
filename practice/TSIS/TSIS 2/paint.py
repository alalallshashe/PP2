import pygame
from datetime import datetime
from tools import draw_shape, flood_fill

pygame.init()
pygame.display.init()
info = pygame.display.Info()
W, H, TH = info.current_w, info.current_h, 70
screen = pygame.display.set_mode((W, H), pygame.FULLSCREEN)
canvas = pygame.Surface((W, H - TH))
canvas.fill((255, 255, 255))
clock = pygame.time.Clock()

fu = pygame.font.SysFont("Arial", 14, bold=True)
fs = pygame.font.SysFont("Arial", 16)
ft = pygame.font.SysFont("Arial", 24, bold=True)

TOOLS = ["pencil", "line", "rect", "circle", "square", "rtriangle", "etriangle", "rhombus", "eraser", "fill", "text"]
LABELS = ["Pen", "Line", "Rect", "Circ", "Sq", "RTri", "ETri", "Rhom", "Era", "Fill", "Txt"]
COLORS = [
    (0, 0, 0),
    (255, 255, 255),
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255),
    (255, 255, 0),
    (255, 165, 0),
    (128, 0, 128),
    (0, 255, 255),
    (165, 42, 42),
]
BSIZES = [2, 5, 10]

tool, color, bi = "pencil", (0, 0, 0), 1
drawing, sp, lp, pbuf = False, None, None, None
ta, tp, tb = False, None, ""

BUTTON_W, BUTTON_H = 58, 42
SIZE_W, SIZE_H = 34, 24
COLOR_W, COLOR_H = 24, 44


def cp(pos):
    return pos[0], pos[1] - TH


def on_cv(pos):
    return pos[1] >= TH


def draw_tool_icon(surface, name, rect, icon_color):
    x, y, w, h = rect
    cx, cy = x + w // 2, y + h // 2
    if name == "pencil":
        pygame.draw.line(surface, icon_color, (x + 10, y + h - 10), (x + w - 10, y + 10), 3)
        pygame.draw.circle(surface, icon_color, (x + 12, y + h - 12), 4)
    elif name == "line":
        pygame.draw.line(surface, icon_color, (x + 10, y + h - 10), (x + w - 10, y + 10), 3)
    elif name == "rect":
        pygame.draw.rect(surface, icon_color, (x + 12, y + 12, w - 24, h - 24), 3)
    elif name == "circle":
        pygame.draw.circle(surface, icon_color, (cx, cy), min(w, h) // 3, 3)
    elif name == "square":
        pygame.draw.rect(surface, icon_color, (x + 12, y + 12, w - 24, h - 24), 3)
    elif name == "rtriangle":
        pygame.draw.polygon(surface, icon_color, [(x + 10, y + h - 12), (x + w - 10, y + h - 12), (x + w - 14, y + 12)], 3)
    elif name == "etriangle":
        pygame.draw.polygon(surface, icon_color, [(x + 10, y + h - 10), (x + w - 10, y + h - 10), (cx, y + 12)], 3)
    elif name == "rhombus":
        pygame.draw.polygon(surface, icon_color, [(cx, y + 10), (x + w - 10, cy), (cx, y + h - 10), (x + 10, cy)], 3)
    elif name == "eraser":
        pygame.draw.rect(surface, icon_color, (x + 12, y + 14, w - 24, h - 18), 0)
        pygame.draw.line(surface, (255, 255, 255), (x + 14, y + h - 14), (x + w - 14, y + 14), 3)
    elif name == "fill":
        pygame.draw.rect(surface, icon_color, (x + 14, y + 18, w - 28, h - 18), 0)
        pygame.draw.polygon(surface, icon_color, [(x + 12, y + 16), (cx, y + 10), (x + w - 12, y + 16)])
    elif name == "text":
        pygame.draw.line(surface, icon_color, (x + 14, y + h - 14), (x + w - 14, y + h - 14), 3)
        pygame.draw.line(surface, icon_color, (x + 18, y + 14), (x + 18, y + h - 14), 3)
        pygame.draw.line(surface, icon_color, (x + w - 18, y + 14), (x + w - 18, y + h - 14), 3)


def get_toolbar_layout():
    tool_rects = []
    for i in range(len(TOOLS)):
        tool_rects.append(pygame.Rect(10 + i * (BUTTON_W + 8), 12, BUTTON_W, BUTTON_H))

    size_rects = []
    base_x = 10
    for i in range(len(BSIZES)):
        size_rects.append(pygame.Rect(base_x + i * (SIZE_W + 8), TH - SIZE_H - 10, SIZE_W, SIZE_H))

    color_rects = []
    for i in range(len(COLORS)):
        color_rects.append(pygame.Rect(W - 10 - COLOR_W - i * (COLOR_W + 8), 12, COLOR_W, COLOR_H))

    return {
        "tool_rects": tool_rects,
        "size_rects": size_rects,
        "color_rects": color_rects,
    }


def toolbar():
    pygame.draw.rect(screen, (28, 34, 52), (0, 0, W, TH))
    pygame.draw.rect(screen, (35, 45, 70), (8, 8, W - 16, TH - 16), border_radius=18)

    screen.blit(ft.render("TSIS Paint", True, (240, 240, 240)), (14, 14))
    info_text = "Ctrl+S: Save   Esc: Quit   P/L/R/C/E/F/T: shortcuts"
    screen.blit(fs.render(info_text, True, (175, 180, 210)), (14, 42))

    layout = get_toolbar_layout()
    for i, rect in enumerate(layout["tool_rects"]):
        selected = tool == TOOLS[i]
        color_bg = (98, 118, 170) if selected else (65, 75, 105)
        pygame.draw.rect(screen, color_bg, rect, border_radius=12)
        draw_tool_icon(screen, TOOLS[i], rect.inflate(-16, -16), (245, 245, 245))
        label = fu.render(LABELS[i], True, (230, 230, 230))
        screen.blit(label, (rect.x + (rect.w - label.get_width()) // 2, rect.y + rect.h - 18))
        if selected:
            pygame.draw.rect(screen, (255, 195, 0), rect, 3, border_radius=12)

    for i, rect in enumerate(layout["size_rects"]):
        selected = bi == i
        btn_color = (40, 52, 78) if selected else (45, 55, 80)
        pygame.draw.rect(screen, btn_color, rect, border_radius=10)
        pygame.draw.rect(screen, (255, 255, 255) if selected else (100, 110, 140), rect, 2, border_radius=10)
        size_label = fu.render(str(BSIZES[i]), True, (255, 255, 255))
        screen.blit(size_label, (rect.x + (rect.w - size_label.get_width()) // 2, rect.y + (rect.h - size_label.get_height()) // 2))

    for i, rect in enumerate(layout["color_rects"]):
        pygame.draw.rect(screen, COLORS[i], rect, border_radius=10)
        if COLORS[i] == color:
            pygame.draw.rect(screen, (255, 255, 255), rect, 3, border_radius=10)

    pygame.draw.rect(screen, (255, 255, 255), (W - 260, 16, 220, 42), border_radius=12)
    pygame.draw.rect(screen, color, (W - 256, 20, 40, 34), border_radius=10)
    pygame.draw.rect(screen, (130, 140, 170), (W - 210, 20, 160, 34), border_radius=10)
    screen.blit(fs.render("Current color", True, (40, 45, 55)), (W - 204, 24))

    status = f"Tool: {tool.title()}   Size: {BSIZES[bi]}   Color: {color}"
    screen.blit(fs.render(status, True, (200, 210, 230)), (W // 2 - 120, TH - 34))


running = True
while running:
    bs = BSIZES[bi]
    layout = get_toolbar_layout()

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        elif e.type == pygame.KEYDOWN:
            if ta:
                if e.key == pygame.K_RETURN:
                    canvas.blit(ft.render(tb, True, color), tp)
                    ta = False
                    tb = ""
                elif e.key == pygame.K_ESCAPE:
                    ta = False
                    tb = ""
                elif e.key == pygame.K_BACKSPACE:
                    tb = tb[:-1]
                elif e.unicode:
                    tb += e.unicode
                continue
            if e.key == pygame.K_ESCAPE:
                running = False
            if e.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                fname = "canvas_" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".png"
                pygame.image.save(canvas, fname)
            for k, t in [
                (pygame.K_p, "pencil"),
                (pygame.K_l, "line"),
                (pygame.K_r, "rect"),
                (pygame.K_c, "circle"),
                (pygame.K_e, "eraser"),
                (pygame.K_f, "fill"),
                (pygame.K_t, "text"),
            ]:
                if e.key == k:
                    tool = t
            if e.key == pygame.K_q:
                bi = 0
            if e.key == pygame.K_w:
                bi = 1
            if e.key == pygame.K_F1:
                bi = 2
        elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
            mx, my = e.pos
            if my < TH:
                for i, rect in enumerate(layout["tool_rects"]):
                    if rect.collidepoint(mx, my):
                        tool = TOOLS[i]
                for i, rect in enumerate(layout["size_rects"]):
                    if rect.collidepoint(mx, my):
                        bi = i
                for i, rect in enumerate(layout["color_rects"]):
                    if rect.collidepoint(mx, my):
                        color = COLORS[i]
                continue
            if not on_cv(e.pos):
                continue
            p = cp(e.pos)
            if tool == "fill":
                flood_fill(canvas, p, color)
            elif tool == "text":
                ta = True
                tp = p
                tb = ""
            else:
                drawing = True
                sp = p
                lp = p
                if tool not in ("pencil", "eraser"):
                    pbuf = canvas.copy()
        elif e.type == pygame.MOUSEBUTTONUP and e.button == 1:
            if drawing and on_cv(e.pos) and tool not in ("pencil", "eraser"):
                draw_shape(canvas, tool, sp, cp(e.pos), color, bs)
            drawing = False
            pbuf = None
        elif e.type == pygame.MOUSEMOTION and drawing and on_cv(e.pos):
            p = cp(e.pos)
            if tool == "pencil":
                pygame.draw.line(canvas, color, lp, p, bs)
                lp = p
            elif tool == "eraser":
                pygame.draw.line(canvas, (255, 255, 255), lp, p, bs * 3)
                lp = p
            elif pbuf:
                canvas.blit(pbuf, (0, 0))
                draw_shape(canvas, tool, sp, p, color, bs)

    screen.fill((20, 24, 34))
    pygame.draw.rect(screen, (210, 210, 210), (0, TH, W, H - TH))
    screen.blit(canvas, (0, TH))
    pygame.draw.rect(screen, (80, 90, 110), (2, TH + 2, W - 4, H - TH - 4), 3, border_radius=12)

    if ta and tp:
        screen.blit(ft.render(tb + "|", True, color), (tp[0], tp[1] + TH))
    toolbar()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
