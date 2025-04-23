import pyxel
import random

pyxel.init(160, 100, title="tamagocchi")
font = pyxel.Font("k8x12.bdf")

# メロディ
pyxel.sounds[0].set(
    "C4 E4 G4 B4 G4 E4 C4 D4 F4 A4 F4 D4 C4 "
    "E4 G4 C4 A4 F4 D4 B3 C4 E4 G4 E4 D4 C4",
    "T", "1", "F", 50
)

# ヒビ割れ音
pyxel.sounds[1].set("C4", "N", "5", "S", 5)

# ニワトリの鳴き声（こけっこっこー風）
pyxel.sounds[2].set("C4D4E4F4G4", "T", "44444", "N", 15)

# 画像読み込み
pyxel.images[0].load(0, 0, "assets/room.png")
pyxel.images[1].load(0, 0, "assets/kin_top.png")
pyxel.images[1].load(32, 0, "assets/kin_right.png")
pyxel.images[1].load(32, 32, "assets/kin_left.png")
pyxel.images[1].load(0, 32, "assets/kin_back.png")
pyxel.images[1].load(64, 0, "assets/egg.png")
pyxel.images[1].load(96, 0, "assets/esa.png")
pyxel.images[1].load(128, 0, "assets/stg.png")
pyxel.images[1].load(160, 0, "assets/int.png")
pyxel.images[1].load(0, 64, "assets/eat1.png")
pyxel.images[1].load(0, 112, "assets/eat2.png")
pyxel.images[1].load(0, 160, "assets/stg1.png")
pyxel.images[1].load(0, 208, "assets/stg2.png")
pyxel.images[2].load(0, 0, "assets/int1.png")
pyxel.images[2].load(0, 48, "assets/int2.png")

# 状態管理
scene = "egg"
message = "おや？ 卵の様子が・・・"
show_choices = False
choice_made = False
selected_option = 0
options = ["餌をあげる", "運動させる", "勉強させる"]
food = 0
strength = 0
intelligence = 0
choice_image = None
girl_timer = 0
message_shown = False
egg_shake_timer = 0
choice_timer = 0
animating = False
animation_start = 0
day = 1
phase = 0  # 0:朝 1:昼 2:夜

player_x = 100
player_y = 60
player_dir = 0
sprite_positions = [(0, 0), (32, 0), (32, 32), (0, 32)]
move_timer = 0
move_direction = random.randint(0, 4)

def get_ending(food, strength, intelligence):
    if food >= 14:
        return "食べ過ぎて風船のように膨らみ、ついに宇宙に飛び出してしまう。宇宙で新たな食材を発見し、地球に戻ってから宇宙食の研究者として新たな冒険が始まる。彼女は宇宙での孤独な時間を経て、自分の食への情熱を再確認し、地球に戻ったときには新たな決意を胸に抱いていた<END>"
    elif food >= 10:
        return "フードファイターとして世界中の食べ物大会に出場し、伝説の大食いチャンピオンになる。彼女は勝利の喜びとともに、食べ物に対する感謝の気持ちを深める。彼女の名は歴史に刻まれ、食べ物の祭典で毎年祝われる。彼女はまた、自身の大食いテクニックを教える学校を設立し、多くの弟子を育てる中で、師としての責任感と誇りを感じることとなった<END>"
    elif food >= 7 and strength >= 7:
        return "バランスの取れた健康的な生活を送り、健康雑誌の表紙を飾る。彼女のライフスタイルは多くの人々に影響を与え、健康ブームを巻き起こす。彼女はまた、健康に関する本を執筆し、ベストセラー作家となる。彼女は自分の経験を通じて、多くの人々に健康の大切さを伝えることに喜びを感じたのだった<END>"
    elif food >= 7 and intelligence >= 7:
        return "グルメ科学者として新しい料理を発明し、ミシュラン星を獲得する。彼女のレストランは世界中から訪れる人々で賑わい、グルメ界の革命児として称賛される。彼女はまた、料理に関するテレビ番組を持ち、多くの視聴者に愛される。彼女は自分の料理が人々に喜びをもたらすことに深い満足感を感じたのだった<END>"
    elif strength >= 17 and intelligence >= 7:
        return "スポーツ科学者として新しいトレーニング方法を開発し、オリンピックチームのコーチになる。彼女の指導のもと、多くの選手が金メダルを獲得する。彼女はまた、スポーツに関する本を執筆し、多くの人々に影響を与える。彼女は選手たちの成長を見守る中で、深い感動と誇りを感じる<END>"
    elif strength >= 14:
        return "筋肉隆々のボディビルダーになり、映画のアクションスターとしてデビューする。彼女の映画は大ヒットし、アクション映画の新たなアイコンとなる。彼女はまた、フィットネスに関する本を執筆し、多くの人々に影響を与える。彼女は自分の体を鍛える過程で得た自信と達成感を、多くの人々と共有することに喜びを感じることとなった<END>"
    elif strength >= 10:
        return "人気モデルとして活躍し、ファッションブランドを立ち上げる。彼女のブランドは瞬く間に世界中で人気となり、ファッション業界のトップに君臨する。彼女はまた、ファッションに関する本を執筆し、多くの人々に影響を与える。彼女は自分の創造力を形にする喜びと、それが人々に与える影響に感動する<END>"
    elif intelligence >= 14:
        return "ノーベル賞を受賞し、世界中の大学で講演を行う。彼女の研究は多くの人々に影響を与え、科学の進歩に大きく貢献する。彼女はまた、科学に関する本を執筆し、多くの人々に影響を与える。彼女は自分の研究が世界を変えることに対する責任感と誇りを感じる<END>"
    elif intelligence >= 10:
        return "クイズノックのメンバーとして活躍し、テレビ番組の司会者になる。彼女の知識とユーモアは視聴者に愛され、番組は高視聴率を記録する。彼女はまた、クイズに関する本を執筆し、多くの人々に影響を与える。彼女は自分の知識が人々に楽しみと学びを提供することに喜びを感じる<END>"
    else:
        return "◆凡庸な日常 〜伝説になれなかった者〜　特に目立つ才能もなく、夢を追うこともなく、ただ淡々と生きてきたあなた。ある日テレビをつけると、かつての友人がトップモデルとして輝いていた。別のチャンネルでは、スポーツ科学者としてオリンピック選手と並ぶ知人の姿が。「あれ…自分は？」とふと考えるが、特に語ることがない。ポテトを口に運びながら考える…「まあ、安定してるし悪くはない。」しかし、一瞬「もしあの時もっと努力していたら？」という考えが頭をよぎる。時間は過ぎる…流されるままに仕事をこなし、何の変哲もない人生を送り続ける。「まあ、それなりに悪くない人生だったな。」と呟くが、どこか虚しさが残る――。<END>"

def update():
    global scene, message, girl_timer, message_shown
    global player_x, player_y, player_dir, move_timer, move_direction
    global egg_shake_timer, show_choices, choice_made, selected_option
    global food, strength, intelligence, choice_image
    global animating, animation_start, day, phase

    if scene == "egg":
        egg_shake_timer += 1
        if pyxel.btnp(pyxel.KEY_RETURN):
            scene = "girl"
            message = ""
            girl_timer = pyxel.frame_count
            message_shown = False
            egg_shake_timer = 0
            pyxel.play(1, 1)

    elif scene == "girl":
        if not message_shown and pyxel.frame_count - girl_timer > 30:
            message = "可愛い女の子だ！"
            message_shown = True
        if message_shown and pyxel.btnp(pyxel.KEY_RETURN):
            scene = "game"
            message = ""
            show_choices = True
            choice_made = False
            selected_option = 0
            choice_image = None
            choice_timer = pyxel.frame_count

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

        margin_x = 30
        margin_top = pyxel.height // 2
        margin_bottom = 60
        sprite_w, sprite_h = 32, 32
        player_x = max(margin_x, min(player_x, pyxel.width - sprite_w - margin_x))
        player_y = max(margin_top, min(player_y, margin_bottom))

        if animating:
            if pyxel.frame_count - animation_start > 30 * 2:
                animating = False
                choice_image = None
                choice_made = False
                show_choices = True
                phase += 1
                if phase > 2:
                    phase = 0
                    day += 1
                    pyxel.play(2, 2)
                    if day > 5:
                        scene = "ending"
            return

        if show_choices and not choice_made:
            if pyxel.btnp(pyxel.KEY_UP):
                selected_option = (selected_option - 1) % len(options)
            elif pyxel.btnp(pyxel.KEY_DOWN):
                selected_option = (selected_option + 1) % len(options)
            elif pyxel.btnp(pyxel.KEY_RETURN):
                choice_made = True
                show_choices = False
                choice_timer = pyxel.frame_count
                animating = True
                animation_start = pyxel.frame_count
                if selected_option == 0:
                    food += 1
                    choice_image = "eat"
                elif selected_option == 1:
                    strength += 1
                    choice_image = "stg"
                elif selected_option == 2:
                    intelligence += 1
                    choice_image = "int"

def draw():
    global scene, message, food, strength, intelligence, day, phase, choice_made, show_choices
    pyxel.cls(0)
    pyxel.blt(0, 0, 0, 0, 0, 160, 100)

    if scene == "egg":
        shake_offset = (-1 if (egg_shake_timer // 2) % 2 == 0 else 1)
        x = pyxel.width // 2 - 16 + shake_offset
        y = pyxel.height // 2 - 16
        pyxel.blt(x, y, 1, 64, 0, 32, 32, 0)

    elif scene == "girl":
        pyxel.blt(pyxel.width // 2 - 16, pyxel.height // 2 - 32, 1, 0, 0, 32, 32, 0)

    elif scene == "game":
        sx, sy = sprite_positions[player_dir]
        pyxel.blt(player_x, player_y, 1, sx, sy, 32, 32, 0)

        if animating:
            frame = (pyxel.frame_count // 10) % 2
            draw_x = (pyxel.width - 160) // 2
            draw_y = (pyxel.height - 47) // 2

            if choice_image == "eat":
                img_y = 64 if frame == 0 else 112
                pyxel.blt(draw_x, draw_y, 1, 0, img_y, 160, 47, 0)
            elif choice_image == "stg":
                img_y = 160 if frame == 0 else 208
                pyxel.blt(draw_x, draw_y, 1, 0, img_y, 160, 47, 0)
            elif choice_image == "int":
                img_y = 0 if frame == 0 else 48
                pyxel.blt(draw_x, draw_y, 2, 0, img_y, 160, 47, 0)

        elif show_choices:
            pyxel.text(16, 10, f"{day}日目 - {'朝' if phase==0 else '昼' if phase==1 else '夜'}", 0, font)
            pyxel.text(16, 24, "選択肢を選んでください", 0, font)
            for i, option in enumerate(options):
                y = 40 + i * 14
                pyxel.text(16, y, option, 0, font)
                if i == selected_option:
                    pyxel.text(10, y, "→", 0, font)

    elif scene == "ending":
        pyxel.text(16, 10, "5日間が終わったよ！", 0, font)
        pyxel.text(16, 20, f"食: {food} 体: {strength} 知: {intelligence}", 0, font)

        

        ending_text = get_ending(food, strength, intelligence)
        if not hasattr(pyxel, 'ending_scroll'):
            pyxel.ending_scroll = 0

        if pyxel.btnp(pyxel.KEY_RETURN):
            pyxel.ending_scroll += 4
            if pyxel.ending_scroll >= len(ending_text) // 19:
                pyxel.ending_scroll = 'END'

        lines = [ending_text[i:i+19] for i in range(0, len(ending_text), 19)]

        if pyxel.ending_scroll == 'END':
            text = "END"
            x = pyxel.width // 2 - len(text) * 4
            y = pyxel.height // 2 - 4
            pyxel.text(x, y, text, 0, font)
            if pyxel.btnp(pyxel.KEY_RETURN):
                scene = "egg"
                message = "おや？ 卵の様子が・・・"
                food = strength = intelligence = 0
                day = 1
                phase = 0
                choice_made = False
                show_choices = False
                pyxel.ending_scroll = 0
        else:
            for i, line in enumerate(lines[pyxel.ending_scroll:pyxel.ending_scroll+4]):
                y = 40 + i * 12  # 行間を広めに調整
                pyxel.text(4, y, line[:19], 0, font)

    if message:
        pyxel.text(16, 80, message, 0, font)

pyxel.play(0, 0, loop=True)
pyxel.run(update, draw)