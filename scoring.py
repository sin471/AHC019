import pathlib
import shutil
import subprocess as sub
import sys

# Config
INPUT_DIR_PATH = pathlib.Path(r"b36525d8_windows\tools_x86_64-pc-windows-gnu\in")
SCORE_PATH = pathlib.Path(r"b36525d8_windows\tools_x86_64-pc-windows-gnu\vis.exe")
OUTPUT_FILE_PATH = pathlib.Path(r"output.txt")
EXECUTE_PATH = pathlib.Path(r"main.py")
SEED_PATH = pathlib.Path(r"b36525d8_windows\tools_x86_64-pc-windows-gnu\seeds.txt")
GENERATOR_PATH = pathlib.Path(r"b36525d8_windows\tools_x86_64-pc-windows-gnu\gen.exe")
SEED_CNT = 100
# 大して時間はかからないし、生成し忘れることもなくなるので入力のテキストファイルは毎回生成することにした


def format_score(score_process_output: str):
    # 出力形式によってここを変更する
    output = score_process_output.rstrip("\n")
    try:
        score = int(output.split()[-1])
    except ValueError as e:
        print(f"LocalTestError\n<{output}>")
        raise e

    return int(score)


def generate_testcase(SEED_CNT: int):
    print(f"Generating {SEED_CNT}Case")
    shutil.rmtree(INPUT_DIR_PATH)
    INPUT_DIR_PATH.mkdir()
    with open(SEED_PATH, mode="w") as f:
        f.write("\n".join(map(str, range(SEED_CNT))))

    generate_command = f"{GENERATOR_PATH} {SEED_PATH} --dir={INPUT_DIR_PATH}"
    sub.run(generate_command)


generate_testcase(SEED_CNT)

print("Calculating...")
score: int = 0
input_files = list(INPUT_DIR_PATH.iterdir())
for i, input_file_path in enumerate(input_files):
    execute_command = (
        f"{sys.executable} {EXECUTE_PATH} < {input_file_path} > {OUTPUT_FILE_PATH}"
    )
    score_command = f"{SCORE_PATH} {input_file_path} {OUTPUT_FILE_PATH}"
    # shell=Trueでは、インジェクション攻撃が可能となるため、内容不明の変数を含めない
    sub.run(execute_command, shell=True)
    score_process = sub.run(
        score_command, shell=True, stdout=sub.PIPE, universal_newlines=True
    )
    score += format_score(score_process.stdout)
    print(f"Seed{i} Done")

with open("score.txt", "a") as f:
    print(f"score = {score}({len(input_files)}case)", file=f)
