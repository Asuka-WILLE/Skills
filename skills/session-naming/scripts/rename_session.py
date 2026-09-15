#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""rename_session.py — ZCode 会话标题适配器。

本脚本只负责 ZCode 的会话库双写；跨 Agent 的统一行为由 SKILL.md 规定：
优先调用当前运行时的原生标题更新能力，不能调用时才输出建议名。

用法:
  python rename_session.py "0913|开发|修复登录超时|进行中" --hint "用户首条消息开头10~20字"
  python rename_session.py "新标题" --session-id sess_xxxxxxxx
  python rename_session.py --list

行为:
  1) 在 ~/.zcode/cli/db/db.sqlite 的 session 表写 title/title_source='custom'/time_title_updated
     （title_source='custom' 可防止标题被自动生成逻辑覆盖）
  2) 在 ~/.zcode/v2/tasks-index.sqlite 的 tasks 表同步 title/title_overridden=1/meta_json
     （桌面 UI 读的是这个库，meta_json 里标题是双写的）
  3) 任何失败 → 打印"建议会话名：xxx"并以退出码 1 结束（降级为手动改名）
  4) 找不到 ZCode 数据库 → 只打印建议名，退出码 0；其他 Agent 不应把本脚本当作通用入口
"""
import argparse
import json
import os
import sqlite3
import sys
import time

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

CLI_DB = os.path.join(os.path.expanduser("~"), ".zcode", "cli", "db", "db.sqlite")
TASK_DB = os.path.join(os.path.expanduser("~"), ".zcode", "v2", "tasks-index.sqlite")
SUBAGENT = "sess_subagent_%"
TRUNC = 40


def short(s):
    s = s or ""
    return s if len(s) <= TRUNC else s[: TRUNC - 1] + "…"


def suggest(new_title, reason, code=1):
    print(f"⚠ {reason}")
    print(f"建议会话名：{new_title}")
    print("（请在会话列表右键手动改名）")
    sys.exit(code)


def connect(path, uri=False):
    con = sqlite3.connect(path, timeout=5, uri=uri)
    con.execute("PRAGMA busy_timeout=5000")
    return con


def locate(cur, args, new_title):
    """返回 (session_id, 旧标题, 定位方式)。找不到即降级退出。"""
    where = "id NOT LIKE ?"
    params_base = [SUBAGENT]
    if args.session_id:
        row = cur.execute(
            f"SELECT id, title FROM session WHERE {where} AND id = ?",
            params_base + [args.session_id],
        ).fetchone()
        if not row:
            suggest(new_title, f"找不到会话 {args.session_id}（或它是子代理会话）")
        return row[0], row[1], "指定id"
    if args.hint:
        row = cur.execute(
            f"SELECT id, title FROM session WHERE {where} AND instr(title, ?) > 0 "
            "ORDER BY time_updated DESC LIMIT 1",
            params_base + [args.hint],
        ).fetchone()
        if row:
            return row[0], row[1], "hint匹配"
    # 无 hint 或 hint 匹配不到（标题可能是 LLM 生成的）→ 取最近更新的普通会话
    row = cur.execute(
        f"SELECT id, title FROM session WHERE {where} ORDER BY time_updated DESC LIMIT 1",
        params_base,
    ).fetchone()
    if not row:
        suggest(new_title, "库里没有任何会话")
    return row[0], row[1], "最近会话（未用hint，注意核对）"


def main():
    ap = argparse.ArgumentParser(description="ZCode 会话标题适配器（按 session-naming 规范）")
    ap.add_argument("new_title", nargs="?", help="新标题，如 0913|开发|修复登录超时|进行中")
    ap.add_argument("--hint", help="本会话用户首条消息开头 10~20 字，用于定位当前会话")
    ap.add_argument("--session-id", help="直接指定会话 id（优先于 --hint）")
    ap.add_argument("--list", action="store_true", help="列出最近 15 个会话后退出")
    args = ap.parse_args()

    if args.list:
        con = connect(f"file:{CLI_DB}?mode=ro", uri=True)
        rows = con.execute(
            "SELECT id, title, title_source, time_updated FROM session "
            "WHERE id NOT LIKE ? ORDER BY time_updated DESC LIMIT 15",
            (SUBAGENT,),
        ).fetchall()
        con.close()
        for sid, title, src, ts in rows:
            t = time.strftime("%m-%d %H:%M", time.localtime(ts / 1000))
            print(f"{sid}  [{src}]  {t}  {short(title)}")
        return

    if not args.new_title:
        ap.error("需要提供新标题，或使用 --list")

    new_title = args.new_title.strip()
    if not os.path.exists(CLI_DB):
        # 本脚本是 ZCode 适配器；没有 ZCode 库时只保留可审查的建议结果。
        print(f"📌 建议会话名：{new_title}")
        return

    now_ms = int(time.time() * 1000)

    # 1) CLI 会话库
    try:
        con = connect(CLI_DB)
        cur = con.cursor()
        sid, old_title, how = locate(cur, args, new_title)
        cur.execute(
            "UPDATE session SET title = ?, title_source = 'custom', time_title_updated = ? "
            "WHERE id = ?",
            (new_title, now_ms, sid),
        )
        # /goal 类会话另有 summary_title，非空则同步，保持显示一致
        cur.execute(
            "UPDATE session_target SET summary_title = ? "
            "WHERE session_id = ? AND summary_title IS NOT NULL",
            (new_title, sid),
        )
        con.commit()
        con.close()
    except sqlite3.OperationalError as e:
        suggest(new_title, f"会话库被锁或不可写：{e}")

    # 2) 桌面任务索引库
    task_note = ""
    try:
        con = connect(TASK_DB)
        cur = con.cursor()
        rows = cur.execute(
            "SELECT meta_json FROM tasks WHERE task_id = ?", (sid,)
        ).fetchall()
        for (meta_json,) in rows:
            try:
                meta = json.loads(meta_json)
            except (TypeError, ValueError):
                meta = {}
            meta["title"] = new_title
            meta["titleOverridden"] = True
            cur.execute(
                "UPDATE tasks SET title = ?, title_overridden = 1, meta_json = ? "
                "WHERE task_id = ?",
                (new_title, json.dumps(meta, ensure_ascii=False), sid),
            )
        con.commit()
        con.close()
        if not rows:
            task_note = "；桌面任务索引中没找到该会话，重启 ZCode 后请核对侧栏"
    except sqlite3.OperationalError as e:
        print(f"⚠ 会话库已改，但桌面任务索引写失败：{e}")
        print(f"建议会话名：{new_title}（如侧栏未更新请手动改）")
        sys.exit(1)

    print(f"✅ 已改名（{how}）{short(old_title)} → {new_title}{task_note}")


if __name__ == "__main__":
    main()
