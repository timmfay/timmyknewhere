"""M1 题库：用固定随机种子从 GSM8K 测试集里抽 40 道题，写进 data/problems.jsonl。

运行：python build_dataset.py
连续运行两次，两次生成的文件 SHA-256 完全相同；提交以后再运行一次，git status 显示没有变化。
这就说明结果可复现。
"""
import json
import random
import re
from fractions import Fraction
from pathlib import Path

SEED = 2026
GSM8K_PATH = Path("data/raw/gsm8k_test.jsonl")
OUT_PATH = Path("data/problems.jsonl")
N_DEV, N_TEST = 20, 20

# 题库里每道题都有这些字段，顺序固定
FIELDS = ["id", "source", "license", "split", "level", "subject", "question", "answer", "solution"]


def read_jsonl(path):
    """读一个 JSONL 文件（每行一个 JSON 对象），返回 list[dict]。"""
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def parse_gsm8k_answer(solution):
    """从 GSM8K 的解答里取出最终答案。

    GSM8K 每道题的 "answer" 字段其实是整段解答，最后一行形如 "#### 1,234"。
    返回 "####" 后面的部分，去掉首尾空白和千分位逗号，例如 "1234"。

    >>> parse_gsm8k_answer("3 + 4 = <<3+4=7>>7\\n#### 7")
    '7'
    >>> parse_gsm8k_answer("...\\n#### 1,234")
    '1234'
    """
    # TODO(M1-1): 用 str.split("####") 取最后一段，strip()，再用 replace 去掉逗号
    raise NotImplementedError


def clean_solution(solution):
    """去掉 GSM8K 解答里的计算器标注 <<16-3-4=9>> 和最后的 "#### 答案" 行，留作参考解答。"""
    text = re.sub(r"<<[^>]*>>", "", solution)
    return text.split("####")[0].strip()


def make_gsm8k_problems(rows, seed=SEED, n_dev=N_DEV, n_test=N_TEST):
    """不放回地抽 n_dev + n_test 道题：前 n_dev 道是 dev，后 n_test 道是 test。

    返回 list[dict]，每个 dict 有 FIELDS 里的全部字段。
    """
    # TODO(M1-2):
    #   1. rng = random.Random(seed)
    #      indices = rng.sample(range(len(rows)), n_dev + n_test)
    #      一次抽完再切开，dev 和 test 才不会有重复的题。
    #   2. 对第 k 个抽到的行号 i（k 从 0 开始）按 FIELDS 的顺序组装一个 dict：
    #        id       = f"gsm8k-{i:04d}"   （用原始行号，以后能追溯到原题）
    #        source   = "gsm8k"
    #        license  = "MIT"
    #        split    = k < n_dev 时为 "dev"，否则为 "test"
    #        level    = None               （GSM8K 没有难度分级）
    #        subject  = None
    #        question = rows[i]["question"]
    #        answer   = parse_gsm8k_answer(rows[i]["answer"])
    #        solution = clean_solution(rows[i]["answer"])
    #   3. 返回这些 dict 组成的 list
    raise NotImplementedError


def write_jsonl(path, rows):
    """把 list[dict] 写成 JSONL：每个 dict 一行。"""
    # TODO(M1-3): open(path, "w", encoding="utf-8", newline="\n") 打开文件，
    #             每个 row 写一行 json.dumps(row, ensure_ascii=False) + "\n"
    #             （ensure_ascii=False 让中文保持原样；newline="\n" 让 Windows 和 macOS 写出一样的文件）
    raise NotImplementedError


def load_problems(path=OUT_PATH):
    """读回题库。以后 run_eval.py 和 make_report.py 都用它。"""
    return read_jsonl(path)


def check_problems(problems):
    """自检，有问题就让程序停下来。"""
    # TODO(M1-4): 用 assert 写四条检查：
    #   - 所有 id 都不重复（提示：比较 len(set(...)) 和 len(...)）
    #   - split 只有 "dev" 和 "test"
    #   - 每个 answer 都能被 Fraction(answer) 解析（解析失败会直接抛异常，这本身就是检查）
    #   - GSM8K 的答案都是整数：Fraction(answer).denominator == 1
    #   最后打印每个 split 各有多少题。
    raise NotImplementedError


def main():
    rows = read_jsonl(GSM8K_PATH)
    print("GSM8K test:", len(rows), "题")
    problems = make_gsm8k_problems(rows)
    check_problems(problems)
    write_jsonl(OUT_PATH, problems)
    print("写入", OUT_PATH, len(problems), "题")


if __name__ == "__main__":
    main()
