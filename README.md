# Skills

个人 Agent Skills 集合。

每个 Skill 都位于 `skills/<skill-name>/` 目录中，入口文件是该目录下的 `SKILL.md`。Skill 所需的脚本和其他资源与入口文件放在同一个目录内；具体加载方式以使用它的 Agent 运行时规则为准。

## 当前目录结构

```text
.
├── README.md
└── skills/
    └── session-naming/
        ├── SKILL.md
        └── scripts/
            └── rename_session.py
```

## 已收录 Skill

- [`session-naming`](skills/session-naming/)：为所有 Agent 统一生成会话标题，并优先调用当前运行时的原生标题更新能力；ZCode 会话库脚本位于其 `scripts/` 目录中。
