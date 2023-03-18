import pathlib
import subprocess
import sys

#Config
INPUT_DIR_PATH = pathlib.Path(r"b36525d8_windows\tools_x86_64-pc-windows-gnu\in")
SCORE_PATH = r"b36525d8_windows\tools_x86_64-pc-windows-gnu\vis.exe"
OUTPUT_FILE_PATH = "output.txt"
EXECUTE_PATH = "main.py"

scores: list[int] = []
print("Calculating...")

for i,input_file_path in enumerate(INPUT_DIR_PATH.iterdir(),1):
    execute_command = (
        f"{sys.executable} {EXECUTE_PATH} < {input_file_path} > {OUTPUT_FILE_PATH}"
    )
    score_command = f"{SCORE_PATH} {input_file_path} {OUTPUT_FILE_PATH}"
    # shell=Trueでは、インジェクション攻撃が可能となるため、内容不明の変数を含めない
    subprocess.run(
        execute_command,
        shell=True,
    )
    score_equation = subprocess.run(
        score_command, shell=True, stdout=subprocess.PIPE, text=True
    ).stdout.rstrip("\n")
    score = int(score_equation.split()[-1])
    scores.append(score)
    print(f"Case{i} Done")

print(sum(scores))
