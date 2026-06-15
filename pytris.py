import curses
import random
import time

# Configurações do Jogo
LARGURA_GRADE = 10
ALTURA_GRADE = 20

# Formatos das peças (Tetrominos) estilo matriz-iniciante
PECAS = [
    [[1, 1, 1, 1]], # I
    [[1, 1, 1], [0, 1, 0]], # T
    [[1, 1, 1], [1, 0, 0]], # L
    [[1, 1, 1], [0, 0, 1]], # J
    [[1, 1], [1, 1]], # O
    [[1, 1, 0], [0, 1, 1]], # Z
    [[0, 1, 1], [1, 1, 0]]  # S
]

class Tetris:
    def __init__(self):
        self.grade = [[0] * LARGURA_GRADE for _ in range(ALTURA_GRADE)]
        self.peca_atual = self.nova_peca()
        self.x = LARGURA_GRADE // 2 - len(self.peca_atual[0]) // 2
        self.y = 0
        self.pontuacao = 0
        self.game_over = False

    def nova_peca(self):
        return random.choice(PECAS)

    def checar_colisao(self, adj_x=0, adj_y=0, peca_substituta=None):
        peca = peca_substituta if peca_substituta is not None else self.peca_atual
        for r, linha in enumerate(peca):
            for c, valor in enumerate(linha):
                if valor:
                    novo_x = self.x + c + adj_x
                    novo_y = self.y + r + adj_y
                    if novo_x < 0 or novo_x >= LARGURA_GRADE or novo_y >= ALTURA_GRADE:
                        return True
                    if novo_y >= 0 and self.grade[novo_y][novo_x]:
                        return True
        return False

    def prender_peca(self):
        for r, linha in enumerate(self.peca_atual):
            for c, valor in enumerate(linha):
                if valor:
                    if self.y + r < 0:
                        self.game_over = True
                        return
                    self.grade[self.y + r][self.x + c] = 1
        self.limpar_linhas()
        self.peca_atual = self.nova_peca()
        self.x = LARGURA_GRADE // 2 - len(self.peca_atual[0]) // 2
        self.y = 0
        if self.checar_colisao():
            self.game_over = True

    def rotacionar_peca(self):
        # Rotaciona a matriz da peça (transposta + reversa)
        peca_rotacionada = [list(x) for x in zip(*self.peca_atual[::-1])]
        if not self.checar_colisao(peca_substituta=peca_rotacionada):
            self.peca_atual = peca_rotacionada

    def mover(self, dx, dy):
        if not self.checar_colisao(adj_x=dx, adj_y=dy):
            self.x += dx
            self.y += dy
            return True
        if dy > 0:
            self.prender_peca()
            return False
        return True

    def limpar_linhas(self):
        linhas_para_limpar = [i for i, linha in enumerate(self.grade) if all(linha)]
        
        if not linhas_para_limpar:
            return

        # Efeito Visual de Explosão (Piscar a linha antes de sumir)
        for _ in range(3):
            for i in lines_para_limpar:
                self.grade[i] = [2] * LARGURA_GRADE # 2 vai ser interpretado como efeito visual
            # O desenho do efeito é controlado na main loop piscando os blocos
            
        # Remove as linhas e adiciona novas vazias no topo
        for i in linhas_para_limpar:
            del self.grade[i]
            self.grade.insert(0, [0] * LARGURA_GRADE)
            self.pontuacao += 100

def desenhar_tela(stdscr, jogo, efeito_pisca):
    stdscr.clear()
    
    # Desenha as bordas da TUI
    stdscr.addstr(0, 0, "+--------------------+")
    for i in range(ALTURA_GRADE):
        stdscr.addstr(i + 1, 0, "|")
        stdscr.addstr(i + 1, 21, "|")
    stdscr.addstr(ALTURA_GRADE + 1, 0, "+--------------------+")

    # Desenha o Tabuleiro / Grade fixada
    for r in range(ALTURA_GRADE):
        for c in range(LARGURA_GRADE):
            if jogo.grade[r][c] == 1:
                stdscr.addstr(r + 1, c * 2 + 1, "[]", curses.color_pair(1))
            elif jogo.grade[r][c] == 2:
                # Efeito de brilho/explosão ao limpar linha
                char_efeito = "XX" if efeito_pisca else "  "
                stdscr.addstr(r + 1, c * 2 + 1, char_efeito, curses.color_pair(2))

    # Desenha a peça caindo atual
    for r, linha in enumerate(jogo.peca_atual):
        for c, valor in enumerate(linha):
            if valor and (jogo.y + r) >= 0:
                stdscr.addstr(jogo.y + r + 1, (jogo.x + c) * 2 + 1, "[]", curses.color_pair(3))

    # Interface de Texto lateral
    stdscr.addstr(2, 25, f"SCORE: {jogo.pontuacao}", curses.A_BOLD)
    stdscr.addstr(4, 25, "CONTROLES:")
    stdscr.addstr(5, 25, "-> Setas Esq / Dir: Mover")
    stdscr.addstr(6, 25, f"-> Seta Cima: Rotacionar")
    stdscr.addstr(7, 25, "-> Seta Baixo: Cair mais rápido")
    stdscr.addstr(8, 25, "-> Q: Sair do Jogo")
    
    if jogo.game_over:
        stdscr.addstr(11, 25, "GAME OVER!", curses.color_pair(2) | curses.A_BLINK)
        stdscr.addstr(12, 25, "Pressione 'q' para sair.")

    stdscr.refresh()

def main(stdscr):
    # Configurações do terminal via curses
    curses.curs_set(0) # Esconde o cursor piscante do terminal
    stdscr.nodelay(True) # Não pausa o código esperando o input do usuário
    stdscr.keypad(True) # Ativa a leitura de setas do teclado

    # Cores (Estilo Retro)
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)  # Blocos fixos
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)   # Game over / Efeitos
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK) # Bloco caindo

    jogo = Tetris()
    ultimo_drop = time.time()
    tempo_efeito = time.time()
    efeito_pisca = True
    velocidade_queda = 0.5 # Segundos por linha

    while True:
        # Se houver alguma linha marcada com efeito (valor 2), limpa ela de fato após o flash
        for r in range(ALTURA_GRADE):
            if index_2 := [c for c, x in enumerate(jogo.grade[r]) if x == 2]:
                time.sleep(0.1) # Pausa dramática pro efeito
                jogo.grade[r] = [0] * LARGURA_GRADE
                # Força um redesenho rápido para sumir com o efeito
                
        desenhar_tela(stdscr, jogo, efeito_pisca)
        
        # Alterna o estado do pisca para o efeito visual
        if time.time() - tempo_efeito > 0.1:
            efeito_pisca = not efeito_pisca
            tempo_efeito = time.time()

        # Input do Usuário
        try:
            tecla = stdscr.getch()
        except Exception:
            tecla = -1

        if tecla == ord('q') or tecla == ord('Q'):
            break

        if not jogo.game_over:
            if tecla == curses.KEY_LEFT:
                jogo.mover(-1, 0)
            elif tecla == curses.KEY_RIGHT:
                jogo.mover(1, 0)
            elif tecla == curses.KEY_UP:
                jogo.rotacionar_peca()
            elif tecla == curses.KEY_DOWN:
                jogo.mover(0, 1)

            # Gravidade (Queda automática da peça baseado no tempo)
            if time.time() - ultimo_drop > velocidade_queda:
                jogo.mover(0, 1)
                ultimo_drop = time.time()
        else:
            # Se deu game over, só aceita a tecla Q para sair
            if tecla == ord('q') or tecla == ord('Q'):
                break

        time.sleep(0.03) # Controla o framerate do loop (aprox. 30 FPS)

if __name__ == "__main__":
    curses.wrapper(main)
