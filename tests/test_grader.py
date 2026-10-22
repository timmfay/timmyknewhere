"""判分器的单元测试。运行：python -m pytest -q

下面 5 个是示例。M2 的要求是你自己再加到至少 15 个，
想想模型的回答可能长成什么奇怪的样子，每种情况写一个测试。
"""
from fractions import Fraction

from matheval.grader import extract_boxed, grade, normalize, to_fraction


def test_boxed_simple():
    assert extract_boxed(r"The answer is \boxed{42}.") == "42"


def test_boxed_nested_braces():
    assert extract_boxed(r"\boxed{\frac{14}{3}}") == r"\frac{14}{3}"


def test_normalize_frac_to_slash():
    assert to_fraction(normalize(r"\frac{14}{3}")) == Fraction(14, 3)


def test_grade_decimal_equals_fraction():
    pred, correct, how = grade(r"So the probability is \boxed{0.5}.", "1/2")
    assert correct and how == "boxed"


def test_grade_no_number_at_all():
    assert grade("I am not sure.", "7") == (None, False, "none")


# TODO(M2-6): 在这里继续写你自己的测试，至少再加 10 个。
# 断言时尽量把整个 (pred, correct, how) 都检查：只看 correct 的话，
# 后备方案碰巧取到同一个数，测试也会通过。一些值得测的情况：
#   - 回答里有两个 \boxed{}，应该取最后一个（how 应该是 "boxed"）
#   - 千分位逗号 "1,000" 和 "1000" 相等
#   - 负分数 \boxed{-\frac{7}{2}}
#   - \dfrac 和 \tfrac
#   - 没有 \boxed{}，只能用最后一个数（how 应该是 "fallback"）
#   - 括号不配对的 \boxed{12
#   - response 是 None 或空字符串
#   - 答案错了的情况（correct 应该是 False）
#   - 0.333333 对 1/3 算对，0.33 对 1/3 算错
#   - 钱、百分数和 LaTeX 千分位："\boxed{\$18}"、"\boxed{25\%}"、"\boxed{1{,}000}"
#   - 带单位的回答 "\boxed{18 \text{ dollars}}" 应该算对
#   - 带分数 "\boxed{2\frac{1}{2}}"：想想现在会判成什么，应不应该算对
