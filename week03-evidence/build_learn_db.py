# -*- coding: utf-8 -*-
"""演示：从 er.md 里的 DDL 文本 → 真正的 SQLite .db 文件（不会自动发生，要执行这段脚本）。"""
import re
import sqlite3
from pathlib import Path

root = Path(__file__).resolve().parents[1]
er_md = root / "docs" / "er.md"
db_path = Path(__file__).with_name("learn.db")

text = er_md.read_text(encoding="utf-8")
m = re.search(r"```sql\n(.*?)```", text, re.S)
if not m:
    raise SystemExit("er.md 里没找到 sql 代码块")
ddl = m.group(1)

if db_path.exists():
    db_path.unlink()

con = sqlite3.connect(db_path)
try:
    con.executescript(ddl)
    tables = [
        r[0]
        for r in con.execute(
            "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
        )
    ]
    print("1) 读到的是文本：docs/er.md 里的 CREATE TABLE ...")
    print("2) 由 sqlite3 执行后，才生成文件：", db_path)
    print("3) 库里真实存在的表：", tables)

    # 插两条演示数据，证明这是“真库”而不只是文档
    con.execute(
        "INSERT INTO device (id, code, name, status) VALUES (1, 'EQ-001', '1号注塑机', 'running')"
    )
    con.execute(
        "INSERT INTO telemetry (device_id, ts, temperature, speed, output_count, run_status) "
        "VALUES (1, '2026-10-27 09:00:00', 32.5, 1200, 100, 1)"
    )
    con.commit()
    row = con.execute(
        "SELECT d.code, t.temperature FROM device d "
        "JOIN telemetry t ON t.device_id = d.id"
    ).fetchone()
    print("4) 查询示例：设备", row[0], "温度", row[1], "℃")
finally:
    con.close()
