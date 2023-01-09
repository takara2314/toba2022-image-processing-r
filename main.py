import kabegami_system

# 入力（引数に検出させたい画像のパスを入れる）
output = kabegami_system.suggest("resources/input-example.png")

# 出力
print("提案されたの壁紙の色:", output)
