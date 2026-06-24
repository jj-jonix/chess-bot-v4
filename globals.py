import pygame
pygame.font.init()
PADDING = 40
BOARD_WIDTH = 800-80
BOARD_HEIGHT = 800-80
DIMENTION = 8
WIN_WIDTH = BOARD_WIDTH + PADDING*2
WIN_HEIGHT = BOARD_HEIGHT +  PADDING*2
SQUARE_SIZE = BOARD_WIDTH//DIMENTION

BLACK = (0,0,0)
WHITE = (255,255,255)
GRAY = (100,100,100)
LIGHT_GRAY = (200,200,200)
CHESSDOTCOM_GREEN = (78,120,55)
BLUE = (53, 204, 240)
IMAGES = {}



def handle_text_input(event, text, active, x, y, width, height):
    if event.type == pygame.MOUSEBUTTONDOWN:
        pos = event.pos
        input_rect = pygame.Rect(x, y, width, height)
        active = input_rect.collidepoint(pos)
    
    if event.type == pygame.KEYDOWN and active:
        if event.key == pygame.K_BACKSPACE:
            text = text[:-1]
        elif event.key == pygame.K_RETURN:
            active = False
        else:
            text += event.unicode
    
    return text, active

def draw_text_input_box(win, font, text, x, y, width, height, prompt='', active=False):
    input_rect = pygame.Rect(x, y, width, height)
    border_color = WHITE if active else GRAY
    
    pygame.draw.rect(win, border_color, input_rect, 2)
    
    display_text = text if text else prompt
    text_color = WHITE if text else LIGHT_GRAY
    rendered_text = font.render(display_text, 1, text_color)
    
    text_rect = rendered_text.get_rect(topleft=(x + 5, y + 5))
    win.blit(rendered_text, text_rect)
    
    if active:
        cursor_x = text_rect.right + 2
        pygame.draw.line(win, WHITE, (cursor_x, y + 5), (cursor_x, y + height - 5), 2)
    
