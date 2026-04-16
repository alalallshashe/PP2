import pygame
import random
# Импортируем наши функции из файла ball.py
from ball import draw_pencil, draw_eraser, draw_rectangle, draw_circle, draw_line, fill_area

def save_canvas_state(canvas, history, max_history):
    """Save current canvas state for undo functionality"""
    history.append(canvas.copy())
    if len(history) > max_history:
        history.pop(0)

def undo_canvas(canvas, history):
    """Undo last action"""
    if history:
        canvas.blit(history.pop(), (0, 0))

def draw_text(surface, text, pos, color, font_size=24):
    """Draw text on surface"""
    font = pygame.font.SysFont(None, font_size)
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, pos)

def main():
    pygame.init()
    info = pygame.display.Info()
    screen_width, screen_height = info.current_w, info.current_h
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
    pygame.display.set_caption("Microsoft Paint Clone with Moving Ball")

    # UI Layout
    toolbar_height = 80
    palette_height = 140
    canvas_margin = 40
    canvas_x, canvas_y = canvas_margin, toolbar_height + 10
    canvas_width = screen_width - canvas_margin * 2
    canvas_height = screen_height - toolbar_height - palette_height - 20

    # Создаем холст (белый слой), на котором будем рисовать
    canvas = pygame.Surface((canvas_width, canvas_height))
    canvas.fill((255, 255, 255))

    # Переменные состояния
    running = True
    drawing = False
    start_pos = (0, 0)
    last_pos = (0, 0)
    
    # Настройки по умолчанию
    current_color = (0, 0, 0) # Черный
    tool = "pencil"           # Режим: pencil, eraser, rect, circle, line, fill, text
    brush_size = 3
    ball_mode = False
    
    # Moving ball variables
    ball_pos = [400, 300]  # Center of canvas
    ball_vel = [random.randint(-5, 5), random.randint(-5, 5)]
    ball_radius = 10
    ball_color = (255, 0, 0)  # Red ball
    ball_trail = []  # List of positions for trail

    # Color palette
    colors = [
        (0, 0, 0), (255, 255, 255), (255, 0, 0), (0, 255, 0), (0, 0, 255),
        (255, 255, 0), (255, 0, 255), (0, 255, 255), (128, 128, 128),
        (255, 128, 0), (128, 255, 0), (0, 128, 255), (255, 0, 128),
        (128, 0, 255), (0, 255, 128), (255, 128, 128)
    ]

    # Tool buttons
    tools = ["pencil", "eraser", "line", "rect", "circle", "fill", "text"]
    tool_buttons = []
    button_width = 60
    button_height = 40
    for i, tool_name in enumerate(tools):
        x = 60 + i * (button_width + 10)
        y = 10
        tool_buttons.append((tool_name, pygame.Rect(x, y, button_width, button_height)))

    # Undo/Redo system
    canvas_history = []
    max_history = 20
    
    # Text input
    text_input = ""
    text_mode = False
    text_pos = (0, 0)
    
    # Track if state was saved for current drawing action
    state_saved = False

    clock = pygame.time.Clock()

    while running:
        # Заливаем основной экран серым цветом (фон для меню)
        screen.fill((220, 220, 220))
        
        # Draw toolbar background
        pygame.draw.rect(screen, (180, 180, 180), (0, 0, screen_width, toolbar_height))
        
        # Draw tool buttons
        font = pygame.font.SysFont(None, 24)
        for tool_name, rect in tool_buttons:
            color = (100, 150, 255) if tool == tool_name else (150, 150, 150)
            pygame.draw.rect(screen, color, rect, border_radius=8)
            pygame.draw.rect(screen, (0, 0, 0), rect, 2, border_radius=8)
            text = font.render(tool_name[:4].title(), True, (0, 0, 0))
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)
        
        # Draw ball mode button
        ball_button = pygame.Rect(tool_buttons[-1][1].right + 20, 10, 80, 40)
        ball_color_btn = (255, 100, 100) if ball_mode else (150, 150, 150)
        pygame.draw.rect(screen, ball_color_btn, ball_button, border_radius=8)
        pygame.draw.rect(screen, (0, 0, 0), ball_button, 2, border_radius=8)
        ball_text = font.render("Ball", True, (0, 0, 0))
        screen.blit(ball_text, (ball_button.x + 10, ball_button.y + 10))
        
        # Draw save and clear buttons
        right_x = screen_width - 10
        redo_button = pygame.Rect(right_x - 60, 10, 60, 40)
        undo_button = pygame.Rect(redo_button.x - 70, 10, 60, 40)
        clear_button = pygame.Rect(undo_button.x - 70, 10, 60, 40)
        save_button = pygame.Rect(clear_button.x - 70, 10, 60, 40)
        pygame.draw.rect(screen, (100, 200, 100), save_button, border_radius=8)
        pygame.draw.rect(screen, (200, 100, 100), clear_button, border_radius=8)
        pygame.draw.rect(screen, (150, 150, 200), undo_button, border_radius=8)
        pygame.draw.rect(screen, (150, 150, 200), redo_button, border_radius=8)
        pygame.draw.rect(screen, (0, 0, 0), save_button, 2, border_radius=8)
        pygame.draw.rect(screen, (0, 0, 0), clear_button, 2, border_radius=8)
        pygame.draw.rect(screen, (0, 0, 0), undo_button, 2, border_radius=8)
        pygame.draw.rect(screen, (0, 0, 0), redo_button, 2, border_radius=8)
        save_text = font.render("Save", True, (0, 0, 0))
        clear_text = font.render("Clear", True, (0, 0, 0))
        undo_text = font.render("Undo", True, (0, 0, 0))
        redo_text = font.render("Redo", True, (0, 0, 0))
        screen.blit(save_text, (save_button.x + 5, save_button.y + 10))
        screen.blit(clear_text, (clear_button.x + 5, clear_button.y + 10))
        screen.blit(undo_text, (undo_button.x + 5, undo_button.y + 10))
        screen.blit(redo_text, (redo_button.x + 5, redo_button.y + 10))
        
        # Draw brush size controls
        size_minus = pygame.Rect(ball_button.right + 20, 10, 30, 40)
        size_plus = pygame.Rect(size_minus.right + 10, 10, 30, 40)
        pygame.draw.rect(screen, (150, 150, 150), size_minus, border_radius=8)
        pygame.draw.rect(screen, (150, 150, 150), size_plus, border_radius=8)
        pygame.draw.rect(screen, (0, 0, 0), size_minus, 2, border_radius=8)
        pygame.draw.rect(screen, (0, 0, 0), size_plus, 2, border_radius=8)
        screen.blit(font.render("-", True, (0, 0, 0)), (size_minus.x + 10, size_minus.y + 8))
        screen.blit(font.render("+", True, (0, 0, 0)), (size_plus.x + 10, size_plus.y + 8))
        size_text = font.render(f"Size: {brush_size}", True, (0, 0, 0))
        screen.blit(size_text, (size_plus.right + 10, 20))
        
        # Draw color palette
        palette_y = screen_height - palette_height + 10
        color_size = 36
        for i, color in enumerate(colors):
            x = 60 + i * (color_size + 8)
            rect = pygame.Rect(x, palette_y, color_size, color_size)
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, (0, 0, 0), rect, 2)
            if current_color == color:
                pygame.draw.rect(screen, (255, 255, 255), rect, 4)
        
        # Draw current color indicator
        pygame.draw.rect(screen, current_color, (10, palette_y, 40, 40))
        pygame.draw.rect(screen, (0, 0, 0), (10, palette_y, 40, 40), 2)
        
        # Draw RGB sliders
        slider_y = palette_y + 50
        slider_width = max(200, (screen_width - 260) // 3)
        slider_height = 20
        
        # Red slider
        red_slider_x = 60
        pygame.draw.rect(screen, (100, 100, 100), (red_slider_x, slider_y, slider_width, slider_height))
        red_pos = red_slider_x + (current_color[0] / 255) * slider_width
        pygame.draw.rect(screen, (255, 0, 0), (red_pos - 5, slider_y - 5, 10, slider_height + 10))
        screen.blit(font.render("R", True, (0, 0, 0)), (red_slider_x - 20, slider_y))
        
        # Green slider
        green_slider_x = red_slider_x + slider_width + 40
        pygame.draw.rect(screen, (100, 100, 100), (green_slider_x, slider_y, slider_width, slider_height))
        green_pos = green_slider_x + (current_color[1] / 255) * slider_width
        pygame.draw.rect(screen, (0, 255, 0), (green_pos - 5, slider_y - 5, 10, slider_height + 10))
        screen.blit(font.render("G", True, (0, 0, 0)), (green_slider_x - 20, slider_y))
        
        # Blue slider
        blue_slider_x = green_slider_x + slider_width + 40
        pygame.draw.rect(screen, (100, 100, 100), (blue_slider_x, slider_y, slider_width, slider_height))
        blue_pos = blue_slider_x + (current_color[2] / 255) * slider_width
        pygame.draw.rect(screen, (0, 0, 255), (blue_pos - 5, slider_y - 5, 10, slider_height + 10))
        screen.blit(font.render("B", True, (0, 0, 0)), (blue_slider_x - 20, slider_y))
        
        # Отображаем наш белый холст для рисования
        screen.blit(canvas, (canvas_x, canvas_y))
        
        # Draw text input cursor when in text mode
        if text_mode:
            cursor_x = canvas_x + text_pos[0]
            cursor_y = canvas_y + text_pos[1]
            pygame.draw.line(screen, (0, 0, 0), (cursor_x, cursor_y), (cursor_x, cursor_y + brush_size * 6), 2)
            if text_input:
                draw_text(screen, text_input, (cursor_x, cursor_y), current_color, brush_size * 6)

        # Update moving ball
        if ball_mode:
            # Update ball position
            ball_pos[0] += ball_vel[0]
            ball_pos[1] += ball_vel[1]
            
            # Bounce off walls
            if ball_pos[0] - ball_radius <= 0 or ball_pos[0] + ball_radius >= canvas_width:
                ball_vel[0] = -ball_vel[0]
                ball_pos[0] = max(ball_radius, min(canvas_width - ball_radius, ball_pos[0]))
            if ball_pos[1] - ball_radius <= 0 or ball_pos[1] + ball_radius >= canvas_height:
                ball_vel[1] = -ball_vel[1]
                ball_pos[1] = max(ball_radius, min(canvas_height - ball_radius, ball_pos[1]))
            
            # Draw ball trail
            ball_trail.append(tuple(ball_pos))
            if len(ball_trail) > 1:
                draw_pencil(canvas, ball_color, ball_trail[-2], ball_trail[-1], brush_size)
            
            # Draw ball on screen
            pygame.draw.circle(screen, ball_color, (int(ball_pos[0] + canvas_x), int(ball_pos[1] + canvas_y)), ball_radius)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Handle mouse clicks
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
                mouse_pos = event.pos
                
                # Check tool buttons
                for tool_name, rect in tool_buttons:
                    if rect.collidepoint(mouse_pos):
                        tool = tool_name
                
                # Check ball mode button
                if ball_button.collidepoint(mouse_pos):
                    ball_mode = not ball_mode
                    if ball_mode:
                        ball_trail = []  # Reset trail when starting ball mode
                
                # Check save and clear buttons
                if save_button.collidepoint(mouse_pos):
                    pygame.image.save(canvas, "drawing.png")
                    print("Drawing saved as drawing.png")
                elif clear_button.collidepoint(mouse_pos):
                    save_canvas_state(canvas, canvas_history, max_history)
                    canvas.fill((255, 255, 255))
                    ball_trail = []
                elif undo_button.collidepoint(mouse_pos):
                    undo_canvas(canvas, canvas_history)
                elif redo_button.collidepoint(mouse_pos):
                    pass  # Redo not implemented yet
                
                # Check RGB sliders
                if slider_y <= mouse_pos[1] <= slider_y + slider_height:
                    if red_slider_x <= mouse_pos[0] <= red_slider_x + slider_width:
                        r = int(((mouse_pos[0] - red_slider_x) / slider_width) * 255)
                        current_color = (r, current_color[1], current_color[2])
                    elif green_slider_x <= mouse_pos[0] <= green_slider_x + slider_width:
                        g = int(((mouse_pos[0] - green_slider_x) / slider_width) * 255)
                        current_color = (current_color[0], g, current_color[2])
                    elif blue_slider_x <= mouse_pos[0] <= blue_slider_x + slider_width:
                        b = int(((mouse_pos[0] - blue_slider_x) / slider_width) * 255)
                        current_color = (current_color[0], current_color[1], b)
                
                # Check brush size buttons
                if size_minus.collidepoint(mouse_pos):
                    brush_size = max(brush_size - 1, 1)
                elif size_plus.collidepoint(mouse_pos):
                    brush_size = min(brush_size + 1, 20)
                
                # Check color palette
                for i, color in enumerate(colors):
                    x = 60 + i * (color_size + 5)
                    rect = pygame.Rect(x, palette_y, color_size, color_size)
                    if rect.collidepoint(mouse_pos):
                        current_color = color
                
                # Check if click is on canvas
                canvas_rect = pygame.Rect(canvas_x, canvas_y, canvas_width, canvas_height)
                if canvas_rect.collidepoint(mouse_pos) and not ball_mode:
                    drawing = True
                    start_pos = (mouse_pos[0] - canvas_x, mouse_pos[1] - canvas_y)
                    last_pos = start_pos
                    if tool in ["pencil", "eraser"]:
                        state_saved = False  # Will save on first motion
            
            # Keyboard shortcuts (still available)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r: current_color = (255, 0, 0)   # Red
                if event.key == pygame.K_g: current_color = (0, 255, 0)   # Green
                if event.key == pygame.K_b: current_color = (0, 0, 255)   # Blue
                if event.key == pygame.K_k: current_color = (0, 0, 0)     # Black
                if event.key == pygame.K_y: current_color = (255, 255, 0) # Yellow
                if event.key == pygame.K_w: current_color = (255, 255, 255) # White
                
                if event.key == pygame.K_p: tool = "pencil"
                if event.key == pygame.K_e: tool = "eraser"
                if event.key == pygame.K_m: tool = "rect"    # Прямоугольник
                if event.key == pygame.K_c: tool = "circle"  # Круг
                if event.key == pygame.K_l: tool = "line"    # Line
                if event.key == pygame.K_f: tool = "fill"    # Fill
                
                if event.key == pygame.K_EQUALS or event.key == pygame.K_PLUS: brush_size = min(brush_size + 1, 20)
                if event.key == pygame.K_MINUS: brush_size = max(brush_size - 1, 1)
                
                if event.key == pygame.K_SPACE: 
                    ball_mode = not ball_mode
                    if ball_mode:
                        ball_trail = []  # Reset trail when starting ball mode
                
                if event.key == pygame.K_s:  # Save canvas
                    pygame.image.save(canvas, "drawing.png")
                    print("Drawing saved as drawing.png")
                
                if event.key == pygame.K_x:  # Clear canvas
                    save_canvas_state(canvas, canvas_history, max_history)
                    canvas.fill((255, 255, 255))
                    ball_trail = []
                
                if event.key == pygame.K_z and (pygame.key.get_mods() & pygame.KMOD_CTRL):  # Ctrl+Z Undo
                    undo_canvas(canvas, canvas_history)
                
                # Text input handling
                if text_mode:
                    if event.key == pygame.K_RETURN:
                        save_canvas_state(canvas, canvas_history, max_history)
                        draw_text(canvas, text_input, text_pos, current_color, brush_size * 6)
                        text_mode = False
                        text_input = ""
                    elif event.key == pygame.K_BACKSPACE:
                        text_input = text_input[:-1]
                    elif event.key == pygame.K_ESCAPE:
                        text_mode = False
                        text_input = ""
                    else:
                        if len(event.unicode) > 0 and event.unicode.isprintable():
                            text_input += event.unicode

            # 3. Логика отпускания мышки (для фигур)
            if not ball_mode and event.type == pygame.MOUSEBUTTONUP and drawing:
                save_canvas_state(canvas, canvas_history, max_history)
                end_pos = (event.pos[0] - canvas_x, event.pos[1] - canvas_y)
                if tool == "rect":
                    draw_rectangle(canvas, current_color, start_pos, end_pos, brush_size)
                elif tool == "circle":
                    draw_circle(canvas, current_color, start_pos, end_pos, brush_size)
                elif tool == "line":
                    draw_line(canvas, current_color, start_pos, end_pos, brush_size)
                elif tool == "fill":
                    fill_area(canvas, current_color, start_pos)
                elif tool == "text":
                    text_pos = start_pos
                    text_mode = True
                    text_input = ""
                drawing = False
                state_saved = False  # Reset for next drawing action

            # 4. Логика движения мышки (для карандаша и ластика)
            if not ball_mode and event.type == pygame.MOUSEMOTION and drawing:
                current_pos = (event.pos[0] - canvas_x, event.pos[1] - canvas_y)
                if tool == "pencil":
                    if not state_saved:
                        save_canvas_state(canvas, canvas_history, max_history)
                        state_saved = True
                    draw_pencil(canvas, current_color, last_pos, current_pos, brush_size)
                    last_pos = current_pos
                elif tool == "eraser":
                    if not state_saved:
                        save_canvas_state(canvas, canvas_history, max_history)
                        state_saved = True
                    draw_eraser(canvas, current_pos, brush_size * 2)

        pygame.display.flip()
        clock.tick(60)  # 60 FPS

    pygame.quit()

if __name__ == "__main__":
    main()