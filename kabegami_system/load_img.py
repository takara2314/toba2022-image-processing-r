import os
import cv2
import numpy as np

# 画像を読み込む
def load_img(img_path):
    if not os.path.exists(img_path):
        raise FileNotFoundError("指定された画像ファイルが見つかりません。")

    img = None
    try:
        img = cv2.imread(img_path)
    except:
        raise ValueError("画像ファイルの形式が不正です。")

    if not (np.all(img.shape[0:2] == np.array([1080, 1920])) or np.all(img.shape[0:2] == np.array([720, 1280]))):
        raise ValueError("画像サイズが不正です。1920×1080または1280×720の画像を指定してください。")

    return img
