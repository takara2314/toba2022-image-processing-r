import cv2
import os
import kabegami_system

imgs = ["room (1).png", "room (4).png", "room (7).png", "room (8).png", "room (10).png"]
themes = ["warm", "cool", "minimalist"]

for p in imgs:
    for t in themes:
        os.makedirs(f"results/{p}/{t}", exist_ok=True)

        # 入力（引数に検出させたい画像のパスを入れる）
        outputs = kabegami_system.suggest(f"resources/{p}", t)

        # 出力
        for i, img in enumerate(outputs):
            cv2.imwrite(f"results/{p}/{t}/{i+1}.png", img)
