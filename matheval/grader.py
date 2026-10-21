"""判分器：从模型的回答里取出最终答案，和标准答案比较。

全部是纯函数，不调用任何 API，所以可以离线写单元测试。
判分结果不存进缓存：改了判分器，只需要重新出报告，不用重新调用模型。

本项目的标准答案只有三种形式：整数（"42"）、分数（"-7/2"）、有限小数（"0.25"）。
"""
import re
from fractions import Fraction

# 一个「数」：可选负号，数字（中间可以有千分位逗号），可选小数部分，可选 "/分母"。
# 例如能匹配 "42"、"-3"、"1,000"、"0.25"、"14/3"。
NUMBER_RE = re.compile(r"-?\d[\d,]*(?:\.\d+)?(?:/\d+)?")

# 预测是小数、标准答案不是整数（例如 0.333333 对 1/3）时允许的相对误差
DECIMAL_TOLERANCE = Fraction(1, 10**6)


def extract_boxed(text):
    r"""返回最后一个 \boxed{...} 花括号里的内容；没有就返回 None。

    >>> extract_boxed(r"so the answer is \boxed{42}.")
    '42'
    >>> extract_boxed(r"\boxed{\frac{14}{3}}")
    '\\frac{14}{3}'
    """
    # TODO(M2-1):
    #   1. start = text.rfind(r"\boxed{")，找不到（-1）就返回 None
    #   2. 从 i = start + len(r"\boxed{") 开始往后走，depth 从 1 开始：
    #      遇到 "{" depth += 1，遇到 "}" depth -= 1，depth 变成 0 时，
    #      这个 "}" 就是配对的右括号，返回两者之间的内容
    #   3. 走到结尾 depth 还没归零（括号不配对），返回 None
    #   为什么不用正则：\frac{14}{3} 里有嵌套的花括号，正则数不清楚
    #   注意：含反斜杠的字符串一律写成 r"..."。普通字符串里 "\b" 是退格符，
    #   所以 len("\boxed{") 是 6，len(r"\boxed{") 才是 7。
    raise NotImplementedError


def last_number(text):
    """后备方案：返回文本里最后一个「数」（字符串），没有就返回 None。

    >>> last_number("so she has 18 dollars, then 20.")
    '20'
    >>> last_number("I am not sure.") is None
    True
    """
    # TODO(M2-2): 用 NUMBER_RE.findall(text) 找出所有的数，得到一个列表；
    #             列表为空就返回 None，否则返回最后一个
    raise NotImplementedError


def normalize(s):
    r"""把答案字符串整理成 Fraction 能解析的样子。

    >>> normalize(r"$\dfrac{14}{3}$")
    '14/3'
    >>> normalize("1,000.")
    '1000'
    >>> normalize(r"x = -\frac{7}{2}")
    '-7/2'
    """
    # TODO(M2-3): 依次做这些替换（顺序有讲究，想想为什么）：
    #   - 去掉 "$"、r"\!"、全部空格
    #   - 去掉千分位逗号 ","
    #   - r"\dfrac" 和 r"\tfrac" 换成 r"\frac"（一定要加 r，普通字符串里 "\f" 是换页符、"\t" 是制表符）
    #   - 把 \frac{a}{b} 换成 a/b：re.sub(r"\\frac\{([^{}]*)\}\{([^{}]*)\}", r"\1/\2", s)
    #   - 去掉开头的 "x=" 和末尾的 "."
    #   返回整理后的字符串
    raise NotImplementedError


def to_fraction(s):
    """把字符串解析成 Fraction，失败就返回 None。

    >>> to_fraction("14/3")
    Fraction(14, 3)
    >>> to_fraction("abc") is None
    True
    """
    # TODO(M2-4): try: return Fraction(s)，捕获 ValueError 和 ZeroDivisionError 返回 None。
    #             s 是 None 时也返回 None。
    raise NotImplementedError


def grade(response, gold):
    r"""判一道题。

    参数：
        response: 模型的原始回答（字符串，可能是 None）
        gold: 标准答案（字符串，例如 "18"、"-7/2"）
    返回 (pred, correct, how)：
        pred: 取出的答案（normalize 之后的字符串），取不到就是 None
        correct: True / False
        how: 答案是怎么取到的："boxed"、"fallback"（没有 boxed，用了最后一个数）或 "none"

    >>> grade(r"... so \boxed{18}", "18")
    ('18', True, 'boxed')
    """
    # TODO(M2-5):
    #   1. response 为 None 时当成空字符串
    #   2. 先 extract_boxed；取到了 how="boxed"
    #      取不到就 last_number，取到了 how="fallback"，都取不到 how="none"，直接返回 (None, False, "none")
    #   3. pred = normalize(取到的字符串)，再用 to_fraction 把 pred 和 gold 都变成 Fraction
    #   4. 两边都解析成功并且相等，就是对的
    #   5. 例外：pred 里有小数点、标准答案不是整数时（例如 0.333333 对 1/3），
    #      |pred - gold| <= DECIMAL_TOLERANCE * max(1, |gold|) 也算对。
    #      「不是整数」可以这样判断：gold 的 Fraction 的 .denominator 不等于 1
    #   6. 返回 (pred, correct, how)
    raise NotImplementedError
