import pygame
import sys
import time

pygame.init()

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

BLOCK_SIZE = 40

# Carregar imagens para os símbolos
ground_image = pygame.transform.scale(pygame.image.load('grass.jpg'), (BLOCK_SIZE, BLOCK_SIZE))
wall_image = pygame.transform.scale(pygame.image.load('wall.png'), (BLOCK_SIZE, BLOCK_SIZE))
dog_image = pygame.transform.scale(pygame.image.load('dog.webp'), (BLOCK_SIZE, BLOCK_SIZE))
exit_image = pygame.transform.scale(pygame.image.load('bone.png'), (BLOCK_SIZE, BLOCK_SIZE))
pygame.mixer.init()
bark_sound = pygame.mixer.Sound('bark.mp3')

# Leitura do arquivo mapa.txt
def read_map(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        return [list(line.strip()) for line in lines]

def draw_map_with_images(map_array):
    rows = len(map_array)
    cols = len(map_array[0])
    screen_size = (cols * BLOCK_SIZE, rows * BLOCK_SIZE)
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption('Toby')

    symbols = {
        '0': ground_image,
        '1': wall_image,
        'm': dog_image,
        'e': exit_image
    }

    for row in range(rows):
        for col in range(cols):
            x = col * BLOCK_SIZE
            y = row * BLOCK_SIZE
            symbol_image = symbols.get(map_array[row][col], None)
            if symbol_image:
                if map_array[row][col] == 'e':
                    screen.blit(symbols['0'], (x, y))  # Desenha o chão ('0') primeiro
                    screen.blit(symbol_image, (x, y))  # Depois desenha o osso por cima
                if map_array[row][col] == 'm':
                    screen.blit(symbols['0'], (x, y))  # Desenha o chão ('0') primeiro
                    screen.blit(symbol_image, (x, y))  # Depois desenha o cachorro por cima
                else:
                    screen.blit(symbol_image, (x, y))
    
    pygame.display.flip()
    return screen

def find_path_backtracking(current_pos, exit_pos, game_map, visited, screen):
    if current_pos == exit_pos:
        return True

    moves = [(0, -1), (0, 1), (-1, 0), (1, 0)]

    for move in moves:
        new_row = current_pos[0] + move[0]
        new_col = current_pos[1] + move[1]

        if 0 <= new_row < len(game_map) and 0 <= new_col < len(game_map[0]) and game_map[new_row][new_col] != '1' and (new_row, new_col) not in visited:
            visited.add((new_row, new_col))
            game_map[current_pos[0]][current_pos[1]] = '0'  # atualiza piso quando cachorro passar
            game_map[new_row][new_col] = 'm'  # dog recebe nova posição
            draw_map_with_images(game_map)  # redesenha o mapa
            pygame.display.flip()
            time.sleep(0.2) 
            updated_pos = (new_row, new_col)
            
            if find_path_backtracking(updated_pos, exit_pos, game_map, visited, screen):
                return True

    return False

def find_path_dfs(start_pos, exit_pos, game_map, screen):
    visited = set()
    visited.add(start_pos)
    
    return find_path_backtracking(start_pos, exit_pos, game_map, visited, screen)

def main():
    MAP_FILE = 'mapa.txt'
    game_map = read_map(MAP_FILE)
    screen = draw_map_with_images(game_map)
    pygame.mixer.music.load('dogsound.mp3')
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

    start_pos = None
    exit_pos = None
    rows = len(game_map)
    cols = len(game_map[0])
    
    # Encontrar posição inicial do dog e da saída
    for row in range(rows):
        for col in range(cols):
            if game_map[row][col] == 'm':
                start_pos = (row, col)
            elif game_map[row][col] == 'e':
                exit_pos = (row, col)

    # Verifique se a posição inicial e a saída foram encontradas
    if start_pos is None or exit_pos is None:
        print("Erro: Posição inicial ou saída não encontrada no mapa.")
        pygame.quit()
        sys.exit()

    path_to_exit = find_path_dfs(start_pos, exit_pos, game_map, screen)

    # Dog achou o osso
    if path_to_exit:
        pygame.mixer.music.stop()
        bark_sound.play()
        font = pygame.font.Font(None, 36)
        text = font.render('Toby achou o osso!', True, WHITE)
        text_rect = text.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2))
        screen.blit(text, text_rect)
        pygame.display.flip()
    else:
        font = pygame.font.Font(None, 36)
        text = font.render('Nenhum caminho foi encontrado!', True, WHITE)
        text_rect = text.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2))
        screen.blit(text, text_rect)
        pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

if __name__ == "__main__":
    main()
