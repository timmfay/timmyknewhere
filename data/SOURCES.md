# 数据来源与许可证

题库 `data/problems.jsonl` 由 `build_dataset.py` 从下面的原始文件生成，每道题的 `source` 和 `license` 字段注明了出处。

| 文件 | 来源 | 许可证 |
| --- | --- | --- |
| `raw/gsm8k_test.jsonl` | OpenAI GSM8K 测试集，1,319 题。下载自 https://raw.githubusercontent.com/openai/grade-school-math/master/grade_school_math/data/test.jsonl ，SHA-256 `3730d312f6e3440559ace48831e51066acaca737f6eabec99bccb9e4b3c39d14` | MIT |

## GSM8K 许可证原文

```
MIT License

Copyright (c) 2021 OpenAI

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

引用：Cobbe et al., *Training Verifiers to Solve Math Word Problems*, 2021. https://arxiv.org/abs/2110.14168
