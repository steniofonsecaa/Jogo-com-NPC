import pyxel

SCREEN_WIDTH = 160
SCREEN_HEIGHT = 160
TILE_SIZE = 8

# 0 = chão (verde), 1 = muro (marrom)
MAP = [
    [1]*20,
] + [
    [1] + [0]*18 + [1] for _ in range(18)
] + [
    [1]*20,
]

def is_blocked(x, y, blocked_positions):
    # Verifica colisão com paredes (baseado no grid)
    col = x // TILE_SIZE
    row = y // TILE_SIZE
    if not (0 <= row < len(MAP) and 0 <= col < len(MAP[0])):
        return True
    if MAP[row][col] == 1:
        return True

    # Verifica colisão com NPCs (pixel-perfect)
    player_rect = (x, y, TILE_SIZE, TILE_SIZE)
    for npc_x, npc_y in blocked_positions:
        npc_rect = (npc_x * TILE_SIZE, npc_y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        if (player_rect[0] < npc_rect[0] + npc_rect[2] and
            player_rect[0] + player_rect[2] > npc_rect[0] and
            player_rect[1] < npc_rect[1] + npc_rect[3] and
            player_rect[1] + player_rect[3] > npc_rect[1]):
            return True
    return False

class Player:
    def __init__(self):
        self.x = 40
        self.y = 40
        self.color = 12
        self.char = "P"

    def update(self, blocked_positions):
        dx = dy = 0
        if pyxel.btn(pyxel.KEY_LEFT): dx = -1  # Movimento de 1 pixel para a esquerda
        if pyxel.btn(pyxel.KEY_RIGHT): dx = 1   # Movimento de 1 pixel para a direita
        if pyxel.btn(pyxel.KEY_UP): dy = -1     # Movimento de 1 pixel para cima
        if pyxel.btn(pyxel.KEY_DOWN): dy = 1    # Movimento de 1 pixel para baixo

        new_x = self.x + dx
        new_y = self.y + dy

        if not is_blocked(new_x, self.y, blocked_positions):
            self.x = new_x
        if not is_blocked(self.x, new_y, blocked_positions):
            self.y = new_y

    def draw(self):
        pyxel.rect(self.x, self.y, TILE_SIZE, TILE_SIZE, self.color)
        pyxel.text(self.x + 2, self.y + 2, self.char, 0)

class NPC:
    def __init__(self, x, y, npc_type, label):
        self.x = x
        self.y = y
        self.type = npc_type
        self.label = label
        self.color = { "shop": 8, "forge": 10, "info": 7 }[npc_type]

    def draw(self):
        pyxel.rect(self.x, self.y, TILE_SIZE, TILE_SIZE, self.color)
        pyxel.text(self.x + 2, self.y + 2, self.label, 0)

    def get_tile_pos(self):
        return self.x // TILE_SIZE, self.y // TILE_SIZE

def is_near(a, b, distance=8):
    return abs(a.x - b.x) <= distance and abs(a.y - b.y) <= distance

class Game:
    def __init__(self):
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT)
        pyxel.title = "NPC Interação por Proximidade"
        self.player = Player()
        self.npcs = [
            NPC(16, 16, "shop", "L"),
            NPC(136, 16, "info", "I"),
            NPC(16, 136, "forge", "F"),
        ]
        self.active_npc = None
        self.message = ""
        pyxel.run(self.update, self.draw)

    def update(self):
        blocked_positions = [npc.get_tile_pos() for npc in self.npcs]
        self.player.update(blocked_positions)

        self.active_npc = None
        for npc in self.npcs:
            if is_near(self.player, npc):
                self.active_npc = npc
                break

        if self.active_npc and pyxel.btnp(pyxel.KEY_E):
            self.message = f"Você falou com o {self.get_npc_name(self.active_npc)}!"
        elif pyxel.btnp(pyxel.KEY_Q):
            self.message = ""

    def get_npc_name(self, npc):
        return {
            "shop": "vendedor",
            "forge": "ferreiro",
            "info": "informante"
        }.get(npc.type, "NPC")

    def draw(self):
        pyxel.cls(0)
        for row_idx, row in enumerate(MAP):
            for col_idx, tile in enumerate(row):
                x = col_idx * TILE_SIZE
                y = row_idx * TILE_SIZE
                color = 6 if tile == 1 else 3
                pyxel.rect(x, y, TILE_SIZE, TILE_SIZE, color)

        for npc in self.npcs:
            npc.draw()

        self.player.draw()

        if self.active_npc:
            pyxel.text(5, SCREEN_HEIGHT - 15, f"[E] Interagir com {self.get_npc_name(self.active_npc)}", 7)

        if self.message:
            pyxel.text(5, SCREEN_HEIGHT - 8, self.message, 10)

Game()