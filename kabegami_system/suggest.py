import cv2
import numpy as np

# HSVの色相と彩度を指定
theme_color = {
    "warm": [
        [0, 150],
        [5, 150],
        [10, 150],
        [15, 150],
        [20, 150],
        [25, 150],
        [30, 150],
        [35, 150]
    ],
    "minimalist": [
        [10, 100],
        [15, 100],
        [20, 100],
        [25, 100]
    ],
    "cool": [
        [90, 150],
        [95, 150],
        [100, 150],
        [105, 150],
        [110, 150],
        [115, 150],
        [120, 150],
        [125, 150]
    ]
}


def suggest(img_path, theme):
    print("Start processing...")

    # 画像の読み込み
    img = cv2.imread(img_path)
    # HSVに変換
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    original_hsv = img_hsv.copy()

    # 一番多い色相を取得 (色相ヒストグラムを生成)
    h, _, _ = cv2.split(img_hsv)
    h_raveled = h.ravel()
    h_hist = get_histogram_array(h_raveled, 180)

    # 一番多い色相に近い色相をマスク
    h_max = np.argmax(h_hist)

    hsv_min = np.array([
        h_max - 30 if h_max - 30 >= 0 else 0,
        0,
        0
    ])

    hsv_max = np.array([
        h_max + 30 if h_max + 30 <= 180 else 0,
        255,
        255
    ])

    masked = cv2.inRange(img_hsv, hsv_min, hsv_max)

    cv2.imwrite("masked1.png", masked)

    # マスクされなかったところを黒く塗りつぶす
    img_masked = img.copy()
    img_masked[masked == 0] = [0, 0, 0]

    # マスクされた部分から一番多い彩度を取得 (0(黒)の場合は2番目に多い彩度)
    img_hsv = cv2.cvtColor(img_masked, cv2.COLOR_BGR2HSV)
    _, s, _ = cv2.split(img_hsv)
    s_raveled = s.ravel()
    s_hist = get_histogram_array(s_raveled, 256)

    s_hist_sorted = s_hist.argsort()[::-1]

    s_max = 0
    if s_hist_sorted[0] == 0:
        s_max = s_hist_sorted[1]
    else:
        s_max = s_hist_sorted[0]

    # 元画像の色相と、マスクされた部分の中で一番多い彩度から近い色をマスク
    hsv_min = np.array([
        h_max - 30 if h_max - 30 >= 0 else 0,
        s_max - 30 if s_max - 30 >= 0 else 0,
        0
    ])

    hsv_max = np.array([
        h_max + 30 if h_max + 30 <= 180 else 0,
        s_max + 30 if s_max + 30 <= 255 else 0,
        255
    ])

    masked = cv2.inRange(img_hsv, hsv_min, hsv_max)

    cv2.imwrite("masked2.png", masked)

    print("Wallpaper detected.")

    # マスクした領域を指定したテーマの色に変換し、画像に反映させる
    if theme != "minimalist":
        results = [None] * len(theme_color[theme])

        for i, hsv in enumerate(theme_color[theme]):
            print(f"{theme} theme: {i + 1} / {len(results)}")

            retouched = original_hsv.copy()
            for y, row in enumerate(masked):
                for x, col in enumerate(row):
                    if col == 255:
                        retouched[y][x][0:2] = hsv
            results[i] = cv2.cvtColor(retouched, cv2.COLOR_HSV2BGR)

            print("done.")

    elif theme == "minimalist":
        results = [None] * len(theme_color[theme]) * 2

        for i in range(len(results)):
            print(f"{theme} theme: {i + 1} / {len(results)}")

            retouched = original_hsv.copy()
            for y, row in enumerate(masked):
                for x, col in enumerate(row):
                    if col == 255:
                        retouched[y][x][0:2] = theme_color[theme][i//2]
                        value = retouched[y][x][2]
                        adding = ((i % 2) + 1) * 20
                        after = retouched[y][x][2] + adding
                        retouched[y][x][2] = after if after <= 255 else 255

            results[i] = cv2.cvtColor(retouched, cv2.COLOR_HSV2BGR)

            print("done.")

    print("Finished processing.")
    return results


def get_histogram_array(arr, max_num):
    hist = np.zeros(max_num + 1, dtype=np.int32)

    for i in range(max_num + 1):
        hist[i] = arr[arr == i].shape[0]

    return hist
