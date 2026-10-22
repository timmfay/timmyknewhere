# 用数学题评测国产大模型：直答、思维链、写代码执行

> 进行中。当前进度：M0（环境与第一次调用）。v1.0 计划 2026 年 11 月 19 日完成。

## 研究问题

关掉思考模式以后，在同一批能自动判分的数学题上，让大模型「直接给答案」「一步一步推理（思维链）」「写 Python 程序算出答案」，三种做法的准确率、成本和错误类型差多少？写代码带来的提升来自消除哪类错误，又引入了哪类新错误？哪些差异在配对检验下站得住？

## 设计

| 项目 | v1 的做法 |
| --- | --- |
| 题目 | dev 30 题（只用来调提示词和判分器）+ test 150 题。test 来自 GSM8K（20 题）和 MATH-500 难度 3–5 级（130 题），按难度分层抽样，固定随机种子 2026。答案都是整数、分数或有限小数，可以精确判分 |
| 模型 | 一强一弱：DeepSeek-V4-Pro 和智谱 GLM-4-Flash（免费）。DeepSeek 显式关闭思考模式，GLM-4-Flash 本身不带思考模式，两者都逐条检查推理 token 为 0。每条记录都存调用日期和服务器返回的模型名 |
| 方法 | direct：只给答案；cot：先推理再给答案；code：只写一段 Python，在本地子进程里执行（10 秒超时） |
| 判分 | 自己写的确定性判分器：取最后一个 `\boxed{}`，规范化后用 `Fraction` 做精确的有理数比较；带单元测试，最后做人工审计 |
| 统计 | 准确率给 Wilson 95% 置信区间；方法之间做精确 McNemar 配对检验，3 个主要比较在跑测试集之前预注册，并做 Holm 校正；用蒙特卡洛模拟做功效分析 |
| 归因 | 人工阅读错题，归纳错误类别，把「写代码」的净提升拆成「修好了哪些错」减「新增了哪些错」 |
| 复现 | 所有原始回答缓存在 JSONL 里并提交；一条命令从缓存重算全部表格和图，不需要 API key |

## 里程碑

- [ ] M0 环境 + 第一次调用两家大模型（10/22–10/23）
- [ ] M1 题库 v0：用固定种子从 GSM8K 抽 40 题（10/24）
- [ ] M2 判分器 + 单元测试（10/25–10/27）
- [ ] M3 评测循环 + JSONL 缓存：direct / cot（10/28–10/30）
- [ ] M4 第三种方法：写 Python 并在子进程执行（10/31–11/01）
- [ ] M5 第一张结果表：准确率 + Wilson 95% CI，打 tag v0.1（11/02–11/03）
- [ ] M6 配对检验 + 预注册 + 结果写入 SQLite（11/04–11/06）
- [ ] M7 题库 v1：加入 MATH-500，冻结提示词，跑正式测试集（11/07–11/10）
- [ ] M8 错题归类与归因（11/11–11/14）
- [ ] M9 成本 / 延迟 + 一页评测报告，打 tag v1.0（11/15–11/19）

v1.0 之后按顺序做：原生思考模式对比、改数字和加无关句的扰动题（检验数据污染）、改条件让原方法失效的扰动题、多轮工具调用、中文高考题切片。

## 怎么运行

需要 Python 3.12 及以上（推荐 3.14）。在仓库根目录：

```bash
python -m venv .venv
# Windows: .\.venv\Scripts\Activate.ps1    macOS: source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env        # 然后在 .env 里填上自己的 API key
python check_setup.py       # 环境自检
python build_dataset.py     # 生成题库 data/problems.jsonl
python -m pytest -q         # 运行单元测试
```

## 目录

```
check_setup.py      环境自检，两家 API 各调用一次
build_dataset.py    原始数据 → data/problems.jsonl（固定种子，可重跑）
matheval/           核心代码
  grader.py         判分器
tests/              单元测试
data/
  raw/              原始数据
  SOURCES.md        数据来源与许可证
```

## 数据与许可证

目前用 GSM8K（MIT），M7 起加入 MATH-500（经 PRM800K，MIT），详见 [data/SOURCES.md](data/SOURCES.md)。
