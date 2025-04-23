import pyxel
import random

pyxel.init(160, 100, title="dotドット")
font = pyxel.Font("k8x12.bdf")

# メロディ（可愛いループ）
pyxel.sounds[0].set(
    "C4 E4 G4 B4 G4 E4 C4 D4 F4 A4 F4 D4 C4 "
    "E4 G4 C4 A4 F4 D4 B3 C4 E4 G4 E4 D4 C4",
    "T",
    "1",
    "F",
    50
)

# ヒビ割れ音（ノイズを使った短いSE）
pyxel.sounds[1].set("C4", "N", "5", "S", 5)  # これが修正された部分

# 画像読み込み（背景・キャラ・卵）
pyxel.images[0].load(0, 0, "assets/room.png")           # 背景
pyxel.images[1].load(0, 0, "assets/kin_top.png")        # 女の子（正面）
pyxel.images[1].load(32, 0, "assets/kin_right.png")     # 右
pyxel.images[1].load(32, 32, "assets/kin_left.png")     # 左
pyxel.images[1].load(0, 32, "assets/kin_back.png")      # 後ろ
pyxel.images[1].load(64, 0, "assets/egg.png")           # 卵

# ゲーム状態管理
scene = "egg"
message = "おや？ 卵の様子が・・・"

# タイマーなど
girl_timer = 0
message_shown = False
egg_shake_timer = 0

# プレイヤー初期位置
player_x = 100
player_y = 60
player_dir = 0

# 各方向のスプライト座標
sprite_positions = [
    (0, 0),    # 正面
    (32, 0),   # 右
    (32, 32),  # 左
    (0, 32)    # 後ろ
]

# 移動関連
move_timer = 0
move_direction = random.randint(0, 4)

def update():
    global scene, message, girl_timer, message_shown
    global player_x, player_y, player_dir, move_timer, move_direction
    global egg_shake_timer

    if scene == "egg":
        egg_shake_timer += 1

        if pyxel.btnp(pyxel.KEY_RETURN):
            scene = "girl"
            message = ""
            girl_timer = pyxel.frame_count
            message_shown = False
            egg_shake_timer = 0
            pyxel.play(1, 1)  # ← ヒビ割れSE再生！

    elif scene == "girl":
        if not message_shown and pyxel.frame_count - girl_timer > 30:  # 約1秒後
            message = "可愛い女の子だ！"
            message_shown = True

        if message_shown and pyxel.btnp(pyxel.KEY_RETURN):
            scene = "game"
            message = ""

    elif scene == "game":
        move_timer += 1
        if move_timer > 30:
            move_direction = random.randint(0, 4)
            move_timer = 0

        if move_direction == 0 and player_y < 60:
            player_y += 1
            player_dir = 0
        elif move_direction == 1:
            player_x += 2
            player_dir = 1
        elif move_direction == 2:
            player_x -= 2
            player_dir = 2
        elif move_direction == 3 and player_y > pyxel.height // 2:
            player_y -= 1
            player_dir = 3

        # 移動制限
        margin_x = 30
        margin_top = pyxel.height // 2
        margin_bottom = 60
        sprite_w, sprite_h = 32, 32

        player_x = max(margin_x, min(player_x, pyxel.width - sprite_w - margin_x))
        player_y = max(margin_top, min(player_y, margin_bottom))

def draw():
    pyxel.cls(0)
    pyxel.blt(0, 0, 0, 0, 0, 160, 100)  # 背景

    if scene == "egg":
        # 卵振動（左右にガタガタ揺らす）
        shake_offset = (-1 if (egg_shake_timer // 2) % 2 == 0 else 1)
        x = pyxel.width // 2 - 16 + shake_offset
        y = pyxel.height // 2 - 16
        pyxel.blt(x, y, 1, 64, 0, 32, 32, 0)

    elif scene == "girl":
        pyxel.blt(pyxel.width // 2 - 16, pyxel.height // 2 - 32, 1, 0, 0, 32, 32, 0)

    elif scene == "game":
        sx, sy = sprite_positions[player_dir]
        pyxel.blt(player_x, player_y, 1, sx, sy, 32, 32, 0)

    # メッセージウィンドウ
    if message:
        pyxel.rect(10, 75, 140, 18, 7)  # 白背景
        pyxel.text(16, 80, message, 0, font)  # 黒文字・フォント指定

# BGMスタート
pyxel.play(0, 0, loop=True)
pyxel.run(update, draw)
