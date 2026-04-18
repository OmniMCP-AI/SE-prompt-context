三步起手法
Step 1
AGENTS.md
成本：乡零
难度：女文
见效： 当天
Step 2
计算型反馈循环成本：千乡低
难度：女女文
见效：•1周内
Step 3
推理型评估
(LLM as Judge)
成本：乡乡乡中
难度：*大*
见效：
• 需迭代
今天就能开始-Step 1:30分钟，一个文件



三种 Harness 架构模式
模式 1
单Agent强Harness
适合：个人/小团队

模式 2
Orchestrator-Worker
Orchestrator
Agent
W1
强Harness约束
W2
并行执行
W3
比单Agent强90.2%

模式 3
Evaluator-in-loop
Agent
Evaluator
一独立审查
通过才进下一步
精度最高• 成本最高


# AGENTS.md
拼 项目概述
［2-3句：项目是什么、用什么技术栈、核心目标］
拼 禁止触碰
- 不要修改 /config/prod.yamL
- 不要升级 numpy 版本（会破坏依赖）
- 不要直接推送 main 分支
拼 代码规范
- 函数必须有 docstring
- 变量名用英文，注释可以用中文
- commit message fåit: type(scope): description
拼 验证方式
修改后必须运行：pytest tests/ && npm run Lint
