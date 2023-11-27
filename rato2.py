
import pygame
import sys

# Inicialização do Pygame
pygame.init()

# Definição de cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (128, 0, 128)

# Tamanho da tela e do bloco
BLOCK_SIZE = 40

# Caminhos das imagens
GROUND_IMAGE = 'grass.jpg'
WALL_IMAGE = 'wall.png'
RAT_IMAGE = 'dog.webp'
EXIT_IMAGE = 'bone.png'

# Carregar imagens e redimensionar para BLOCK_SIZE x BLOCK_SIZE pixels
ground = pygame.transform.scale(pygame.image.load(GROUND_IMAGE), (BLOCK_SIZE, BLOCK_SIZE))
wall = pygame.transform.scale(pygame.image.load(WALL_IMAGE), (BLOCK_SIZE, BLOCK_SIZE))
rat = pygame.transform.scale(pygame.image.load(RAT_IMAGE), (BLOCK_SIZE, BLOCK_SIZE))
exit_img = pygame.transform.scale(pygame.image.load(EXIT_IMAGE), (BLOCK_SIZE, BLOCK_SIZE))

# Definição do mapa
MAP_FILE = 'mapa3.txt'

# Leitura do mapa do arquivo
def read_map(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        return [list(line.strip()) for line in lines]

# Inicialização do mapa
game_map = read_map(MAP_FILE)

# Inicialização do Pygame
rows = len(game_map)
cols = len(game_map[0])
SCREEN_SIZE = (cols * BLOCK_SIZE, rows * BLOCK_SIZE)
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption('Labirinto')

# Função para desenhar o mapa com imagens
def draw_map_with_images(map_array):
    for row in range(rows):
        for col in range(cols):
            x = col * BLOCK_SIZE
            y = row * BLOCK_SIZE

            if map_array[row][col] == '0':
                screen.blit(ground, (x, y))
            elif map_array[row][col] == '1':
                screen.blit(wall, (x, y))
            elif map_array[row][col] == 'm':
                screen.blit(rat, (x, y))
            elif map_array[row][col] == 'e':
                screen.blit(exit_img, (x, y))

# Função para verificar se uma posição é válida no mapa
def is_valid_position(pos):
    row, col = pos
    return 0 <= row < rows and 0 <= col < cols and game_map[row][col] != '1'

# Função para encontrar o caminho usando backtracking com prioridade nas direções
def find_path_backtracking(current_pos, exit_pos, visited, last_direction=None):
    row, col = current_pos

    if current_pos == exit_pos:
        return [current_pos]

    visited.add(current_pos)

    # Ordem de movimento: direita, esquerda, baixo e cima
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    for direction in directions:
        if last_direction is not None and direction == (-last_direction[0], -last_direction[1]):
            continue

        new_row, new_col = row + direction[0], col + direction[1]
        new_pos = (new_row, new_col)

        if is_valid_position(new_pos) and new_pos not in visited:
            path = find_path_backtracking(new_pos, exit_pos, visited.copy(), direction)
            if path:
                return [current_pos] + path

    if (row, col) != (0, 0) and last_direction is not None:
        opposite_direction = (-last_direction[0], -last_direction[1])
        path_to_corner = find_path_backtracking((0, 0), exit_pos, visited.copy(), opposite_direction)
        return [current_pos] + path_to_corner if path_to_corner else []

    return []


# Função principal do jogo
def main():
    rat_pos = None
    exit_pos = None

    # Encontrar posição inicial do dog e da saída
    for row in range(rows):
        for col in range(cols):
            if game_map[row][col] == 'm':
                rat_pos = (row, col)
            elif game_map[row][col] == 'e':
                exit_pos = (row, col)

    # Verifique se o dog e a saída foram encontrados
    if rat_pos is None or exit_pos is None:
        print("Erro: Dog ou saída não encontrados no mapa.")
        pygame.quit()
        sys.exit()

    clock = pygame.time.Clock()

    visited = set()
    path_to_exit = find_path_backtracking(rat_pos, exit_pos, visited)

    while path_to_exit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Atualize a posição do dog para o próximo passo no caminho
        rat_pos = path_to_exit.pop(0)

        # Adicione a posição atual à lista de visitados
        visited.add(rat_pos)

        # Desenhe o mapa com imagens
        draw_map_with_images(game_map)

        # Pinte a trilha percorrida de roxo
        for pos in visited:
            pygame.draw.rect(screen, PURPLE, (pos[1] * BLOCK_SIZE, pos[0] * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

        # Desenhe o dog e a saída
        screen.blit(rat, (rat_pos[1] * BLOCK_SIZE, rat_pos[0] * BLOCK_SIZE))
        screen.blit(exit_img, (exit_pos[1] * BLOCK_SIZE, exit_pos[0] * BLOCK_SIZE))

        pygame.display.flip()
        clock.tick(5)  # 5 FPS para melhor visualização

    # Quando o dog chegar à saída
    font = pygame.font.Font(None, 36)
    text = font.render('Dog encontrou a saída! Pressione R para reiniciar ou Q para sair.', True, WHITE)
    screen.blit(text, (50, 50))
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Reiniciar
                    main()  # Chamando main novamente para reiniciar
                elif event.key == pygame.K_q:  # Sair
                    pygame.quit()

# Execute o jogo
if __name__ == "__main__":
    main()