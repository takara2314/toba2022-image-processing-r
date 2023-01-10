import cv2
from kabegami_system.load_img import load_img
from kabegami_system.get_img_color import get_color

# 壁紙の色を提案する
def suggest(img_path):
    img = load_img(img_path)

    # グレースケールに変換
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 平滑化 (ガウシアンフィルタを適応)
    blurred = cv2.GaussianBlur(gray, (3, 3), 0)

    # エッジを検出 (Canny法)
    edges = cv2.Canny(blurred, 50, 150)

    # エッジを輪郭として抽出
    contours, hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # エッジが大きい順にソート
    contours = sorted(contours, key=cv2.contourArea, reverse=True)

    for i, contour in enumerate(contours):
        # contourを囲む最小の矩形を取得する
        x, y, w, h = cv2.boundingRect(contour)
        # 切り取る領域を設定する
        region = img[y:y+h, x:x+w]
        print(get_color(region))
        # 領域を切り取る
        cv2.imwrite("output/{}.png".format(i), region)

    return "rgb(0, 0, 0)"
