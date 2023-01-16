import cv2
import kabegami_system

# 入力（引数に検出させたい画像のパスを入れる）
outputs = kabegami_system.suggest("resources/room (1).png", "minimalist")

# 出力
for i, img in enumerate(outputs):
    cv2.imwrite("result_{}.png".format(i+1), img)
