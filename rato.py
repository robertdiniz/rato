
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
pygame.display.set_caption('Toby caçando osso')

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
                screen.blit(ground, (x, y))  # Desenha o chão no lugar do 'm'
            elif map_array[row][col] == 'e':
                screen.blit(ground, (x, y))  # Desenha o chão
                screen.blit(exit_img, (x, y))  # Desenha o osso acima do chão


# Função para verificar se uma posição é válida no mapa
def is_valid_position(pos):
    row, col = pos
    return 0 <= row < rows and 0 <= col < cols and game_map[row][col] != '1'

# Função para encontrar o caminho usando busca em profundidade (Depth-First Search - DFS)
def find_path_dfs(current_pos, exit_pos, visited):
    if current_pos == exit_pos:
        return [current_pos]

    visited.add(current_pos)

    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    for direction in directions:
        new_row, new_col = current_pos[0] + direction[0], current_pos[1] + direction[1]
        new_pos = (new_row, new_col)

        if is_valid_position(new_pos) and new_pos not in visited:
            visited.add(new_pos)  # Adiciona a nova posição antes da exploração
            pygame.time.delay(100)  # Pausa de 100 milissegundos para visualização
            draw_map_with_images(game_map)  # Redesenha o mapa com as explorações
            screen.blit(rat, (new_col * BLOCK_SIZE, new_row * BLOCK_SIZE))  # Desenha o dog na nova posição
            pygame.display.flip()
            path = find_path_dfs(new_pos, exit_pos, visited.copy())
            if path:
                return [current_pos] + path

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


    visited = set()
    path_to_exit = find_path_dfs(rat_pos, exit_pos, visited)

    if path_to_exit:
        # Quando o dog encontra a saída
        font = pygame.font.Font(None, 24)
        text = font.render('Toby encontrou a saída!', True, WHITE)
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