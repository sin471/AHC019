import pathlib
import subprocess as sub
import sys
from typing import List

# Config
INPUT_DIR_PATH = pathlib.Path(r"b36525d8_windows\tools_x86_64-pc-windows-gnu\in")
SCORE_PATH = r"b36525d8_windows\tools_x86_64-pc-windows-gnu\vis.exe"
OUTPUT_FILE_PATH = "output.txt"
EXECUTE_PATH = "main.py"

def format_score(score_process_output: str):
    # 出力形式によってここを変更する
    output = score_process_output.rstrip("\n")
    try:
        score = int(output.split()[-1])
    except ValueError as e:
        print(f"LocalTestError\n<{output}>")
        raise e

    return int(score)


scores: List[int] = []
print("Calculating...")

for i, input_file_path in enumerate(INPUT_DIR_PATH.iterdir(), 1):
    execute_command = (
        f"{sys.executable} {EXECUTE_PATH} < {input_file_path} > {OUTPUT_FILE_PATH}"
    )
    score_command = f"{SCORE_PATH} {input_file_path} {OUTPUT_FILE_PATH}"
    # shell=Trueでは、インジェクション攻撃が可能となるため、内容不明の変数を含めない
    sub.run(execute_command, shell=True)
    score_process = sub.run(
        score_command,
        shell=True,
        stdout=sub.PIPE,
        text=True,
    )
    score = format_score(score_process.stdout)
    scores.append(score)
    print(f"Case{i} Done")

with open("score.txt", "a") as f:
    print(f"score = {sum(scores)}", file=f)
