
import pygame
import sys

pygame.init()

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (128, 0, 128)

BLOCK_SIZE = 40

# Imagens
GROUND_IMAGE = 'grass.jpg'
WALL_IMAGE = 'wall.png'
DOG_IMAGE = 'dog.webp'
EXIT_IMAGE = 'bone.png'

# Carregar imagens e redimensionar para BLOCK_SIZE x BLOCK_SIZE pixels
ground = pygame.transform.scale(pygame.image.load(GROUND_IMAGE), (BLOCK_SIZE, BLOCK_SIZE))
wall = pygame.transform.scale(pygame.image.load(WALL_IMAGE), (BLOCK_SIZE, BLOCK_SIZE))
dog = pygame.transform.scale(pygame.image.load(DOG_IMAGE), (BLOCK_SIZE, BLOCK_SIZE))
exit_img = pygame.transform.scale(pygame.image.load(EXIT_IMAGE), (BLOCK_SIZE, BLOCK_SIZE))

# Definição do mapa
MAP_FILE = 'mapa.txt'

# Leitura do mapa
def read_map(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        return [list(line.strip()) for line in lines]

game_map = read_map(MAP_FILE)

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

def find_path_dfs(posicao_atual, pos_saida, visited):
    if posicao_atual == pos_saida:
        return [posicao_atual]

    visited.add(posicao_atual)

    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    for direction in directions:
        new_row, new_col = posicao_atual[0] + direction[0], posicao_atual[1] + direction[1]
        new_pos = (new_row, new_col)

        if is_valid_position(new_pos) and new_pos not in visited:
            visited.add(new_pos)  # Adiciona a nova posição antes da exploração
            pygame.time.delay(100)  # Pausa de 100 milissegundos para visualização
            draw_map_with_images(game_map)  # Redesenha o mapa com as explorações
            screen.blit(dog, (new_col * BLOCK_SIZE, new_row * BLOCK_SIZE))  # Desenha o dog na nova posição
            pygame.display.flip()
            path = find_path_dfs(new_pos, pos_saida, visited.copy())
            if path:
                return [posicao_atual] + path

    return []

def main():
    dog_pos = None
    pos_saida = None
    pygame.mixer.init()
    bark_sound = pygame.mixer.Sound('bark.mp3')
    bark_sound.set_volume(5)
    pygame.mixer.music.load('dogsound.mp3')
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.1)
    # Encontrar posição inicial do dog e da saída
    for row in range(rows):
        for col in range(cols):
            if game_map[row][col] == 'm':
                dog_pos = (row, col)
            elif game_map[row][col] == 'e':
                pos_saida = (row, col)

    # Verifique se o dog e a saída foram encontrados
    if dog_pos is None or pos_saida is None:
        print("Erro: Dog ou saída não encontrados no mapa.")
        pygame.quit()
        sys.exit()


    visited = set()
    path_to_exit = find_path_dfs(dog_pos, pos_saida, visited)

    if path_to_exit:
        # Quando o dog encontra a saída
        pygame.mixer.music.stop()
        bark_sound.play()
        font = pygame.font.Font(None, 24)
        text = font.render('Toby encontrou o osso!', True, WHITE)
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