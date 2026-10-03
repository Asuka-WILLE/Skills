# Skills

个人 Agent Skills 集合。

本仓库的用途是**在不同 Agent 运行时之间同步同一套 Skill**（Codex / ZCode / opencode / Claude Code 等），因此每个 Skill 都保持运行时可加载的原始目录结构，并在此标注**上游出处**，便于按需回源更新或迁移到新的 Agent。

> 快照来源：`~/.codex/skills`（Codex 用户技能目录）。

## 目录结构

```text
.
├── .gitattributes
├── .gitignore
├── README.md
└── skills/
    └── <skill-name>/
        ├── SKILL.md      # 入口文件（front-matter 内含 name / description 等元数据）
        ├── references/   # 参考资料（可选）
        ├── scripts/      # 可执行脚本（可选）
        └── ...           # 其余资源与入口文件同目录
```

每个 Skill 位于 `skills/<skill-name>/` 目录，入口文件是该目录下的 `SKILL.md`，其脚本与资源与入口文件同目录；具体加载方式以使用它的 Agent 运行时规则为准。

## 来源与许可总览

| 分组 | 数量 | 上游出处 | 许可 |
| --- | --- | --- | --- |
| 自建 | 10 | 本仓库，无外部上游 | 未单独声明 |
| 中译 / 改编 | 1 | [`blader/humanizer`](https://github.com/blader/humanizer)（参考 `hardikpandya/stop-slop`） | 未标注 |
| Anthropic 示例技能 | 11 | [`anthropics/skills`](https://github.com/anthropics/skills) → `skills/` | Apache-2.0 |
| 独立开源项目 | 1 | [`hugohe3/ppt-master`](https://github.com/hugohe3/ppt-master) | MIT |
| 未标注 | 1 | `doc-coauthoring` ← `anthropics/skills` | 未标注（上游该目录亦无许可文件） |

因上游许可限制**不予收录**的 Skill（含 Anthropic 文档技能与 MiniMax 开源技能）见下方「未收录 Skill」。

## 未收录 Skill（仅记录出处）

以下 Skill 不在本仓库中存放文件，只记录获取地址。

### Anthropic 文档技能（专有 · source-available）

| Skill | GitHub 仓库地址 |
| --- | --- |
| `docx` | <https://github.com/anthropics/skills/tree/main/skills/docx> |
| `pdf` | <https://github.com/anthropics/skills/tree/main/skills/pdf> |
| `pptx` | <https://github.com/anthropics/skills/tree/main/skills/pptx> |
| `xlsx` | <https://github.com/anthropics/skills/tree/main/skills/xlsx> |

- 仓库根：<https://github.com/anthropics/skills>
- 许可：© 2025 Anthropic, PBC. All rights reserved. 上游 README 明确「These are source-available, not open source.」，并禁止向第三方分发、再许可或转让，故不收录、不提供文件。
- Codex 用户通常无需自行获取：主运行时已内置等价实现（插件 `openai-primary-runtime` 的 `documents` / `pdf` / `presentations` / `spreadsheets`），随应用自动安装。

### MiniMax 开源技能（MIT）

统一仓库地址：<https://github.com/minimax-ai/skills>

| Skill |
| --- |
| `android-native-dev` |
| `flutter-dev` |
| `fullstack-dev` |
| `ios-application-dev` |
| `react-native-dev` |
| `shader-dev` |

该仓库同时提供 `minimax-docx`、`minimax-pdf`、`minimax-xlsx`、`pptx-generator` 等文档类技能，按需自行获取。

## 已收录 Skill

### 自建 Skill

- [`artifact-and-dependency-hygiene`](skills/artifact-and-dependency-hygiene/)：清理项目文件、排查依赖/构建异常、决定哪些产物应提交、迁移工程或重建环境时使用。先区分事实源、可再生生成物、环境状态与验证证据，再做最小化处理。
- [`evidence-driven-debugging`](skills/evidence-driven-debugging/)：程序出现异常、偶发错误、性能退化、状态不一致或「看起来不对但原因未知」时使用。以可复现现象、数据与控制流证据、可证伪假设定位根因。
- [`interface-contract-evolution`](skills/interface-contract-evolution/)：修改 API、事件、消息、数据库字段、文件格式、配置格式或多服务数据结构时使用。以兼容、可观测、可回滚的方式演进跨层接口。
- [`layered-verification-and-reporting`](skills/layered-verification-and-reporting/)：完成代码变更、修复缺陷、发布功能，或回答「验证了吗」「能上线吗」时使用。按证据强度组织静态检查、测试、构建、集成与真实环境验证。
- [`regression-safe-feature-development`](skills/regression-safe-feature-development/)：新增功能、修改行为、优化性能或修复缺陷时使用。把需求转化为可验证的旧行为不变量、变更影响图与回归检查。
- [`resilient-state-machine-design`](skills/resilient-state-machine-design/)：设计或修复带状态、异步事件、超时、重试、权限、设备控制、任务编排或安全降级逻辑时使用。
- [`safe-change-delivery`](skills/safe-change-delivery/)：提交、合并、推送、发布或整理任何代码改动时使用。通过基线核实、变更范围审阅、最小提交与远端确认防止误交付。
- [`session-naming`](skills/session-naming/)：为所有 Agent 统一生成会话标题（`MMDD|类型|内容|状态`），优先调用当前运行时的原生标题更新能力；ZCode 会话库脚本位于其 `scripts/` 目录。
- [`source-of-truth-documentation`](skills/source-of-truth-documentation/)：编写、更新、审查或纠正 README、架构说明、接口文档、运维手册、变更说明与技术决策记录时使用。
- [`timing-and-concurrency-precision`](skills/timing-and-concurrency-precision/)：分析或修改并发、异步、轮询、消息顺序、延时、同步、定时任务或性能时使用。

### 中译 / 改编

- [`humanizer-zh`](skills/humanizer-zh/)：去除文本中的 AI 生成痕迹。检测并修复夸大象征、宣传性语言、模糊归因、破折号滥用、三段式法则等模式。上游：`blader/humanizer`（中译，参考 `hardikpandya/stop-slop`）。

### 第三方 Skill — Apache-2.0（上游：[`anthropics/skills`](https://github.com/anthropics/skills)）

- [`algorithmic-art`](skills/algorithmic-art/)：用 p5.js 创作算法艺术，支持种子随机与交互式参数探索。
- [`brand-guidelines`](skills/brand-guidelines/)：为产出物套用 Anthropic 官方品牌配色与字体。
- [`canvas-design`](skills/canvas-design/)：用设计方法创作 .png / .pdf 视觉作品（海报、艺术、设计稿等）。
- [`frontend-design`](skills/frontend-design/)：构建有辨识度、生产级的前端界面，避免千篇一律的 AI 风格。
- [`internal-comms`](skills/internal-comms/)：撰写各类内部沟通文案（状态报告、管理层更新、公司通讯、FAQ、事故报告等）。
- [`mcp-builder`](skills/mcp-builder/)：构建高质量 MCP 服务器（Python FastMCP / Node TypeScript MCP SDK）。
- [`skill-creator`](skills/skill-creator/)：创建新 Skill、改进已有 Skill，并用 eval 衡量与优化触发准确率。
- [`slack-gif-creator`](skills/slack-gif-creator/)：为 Slack 制作经过校验与优化的动图 GIF。
- [`theme-factory`](skills/theme-factory/)：为幻灯片、文档、报告、HTML 落地页等成品套用主题（内置 10 套，也可即时生成）。
- [`web-artifacts-builder`](skills/web-artifacts-builder/)：用 React + Tailwind CSS + shadcn/ui 构建多组件复杂 HTML artifact。
- [`webapp-testing`](skills/webapp-testing/)：用 Playwright 与本地 Web 应用交互并测试，支持前端验证、UI 调试、截图与浏览器日志。

### 第三方 Skill — MIT（独立项目）

- [`ppt-master`](skills/ppt-master/)：AI 驱动的演示文稿工作流，生成可编辑 PPTX、重建页面视觉、填充原生模板、增强成品。上游：[`hugohe3/ppt-master`](https://github.com/hugohe3/ppt-master)。

### 第三方 Skill — 未标注许可

- [`doc-coauthoring`](skills/doc-coauthoring/)：引导用户按结构化流程协作撰写文档、提案、技术规格与决策记录。上游 `anthropics/skills` 该目录下亦无许可文件。
