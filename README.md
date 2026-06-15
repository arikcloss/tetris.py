# pytris.py

Este é um clone clássico de Tetris feito puramente em **Python**, rodando direto no terminal (TUI - Text User Interface). O código foi escrito pensando em manter as coisas simple

Sem motores gráficos pesados, sem Pygame. Só lógica pura, matrizes e a biblioteca `curses`.

## Destaques de Código
Como o jogo roda no terminal, usei criatividade para os efeitos:
- **Engine de Física de Matriz:** Detecção de colisão clássica comparando índices de listas bidimensionais.
- **Efeito de Explosão Retro:** Quando você completa uma linha, o terminal pisca caracteres `XX` vermelhos antes de deletar a linha e aplicar a gravidade. 
- **Sem Flickering (Tela piscando):** Renderização otimizada atualizando apenas o buffer necessário do terminal a 30 FPS estáveis.

## Como rodar essa belezinha

### No Linux / macOS:
O Python já vem com tudo que você precisa instalado por padrão. Só clonar e rodar:
```bash
python pytris.py
