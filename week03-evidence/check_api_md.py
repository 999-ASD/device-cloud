# -*- coding: utf-8 -*-
"""任务二：对照指导书验证方法检查 docs/api.md（查文档，不是调 HTTP）"""
from __future__ import annotations

import re
from pathlib import Path

root = Path(__file__).resolve().parents[1]
api_path = root / "docs" / "api.md"
text = api_path.read_text(encoding="utf-8")

print("工作目录:", root)
print("检查文件:", api_path)
print()

print("=== 1) 统计接口条数 ===")
endpoints = re.findall(
    r"(?m)^###\s+\d+\.\d+\s+(GET|POST|PUT|PATCH|DELETE)\s+`([^`]+)`",
    text,
)
print(f"找到 {len(endpoints)} 条（指导书期望约 17）")
for method, path in endpoints:
    print(f"  - {method} {path}")

print()
print("=== 2) 每个接口是否含：说明 / 请求 / 响应 ===")
parts = re.split(
    r"(?m)(?=^###\s+\d+\.\d+\s+(?:GET|POST|PUT|PATCH|DELETE)\s+)",
    text,
)
sections = [p for p in parts if re.match(r"^###\s+\d+\.\d+", p)]
for s in sections:
    title = s.splitlines()[0]
    has_desc = "**说明：**" in s or "**说明:**" in s
    has_req = any(k in s for k in ("请求参数", "请求体", "路径参数"))
    has_resp = "成功响应" in s or "响应" in s
    mark = "OK" if (has_desc and has_req and has_resp) else "缺项"
    print(f"  [{mark}] {title}")
    if mark != "OK":
        print(f"         说明={has_desc} 请求={has_req} 响应={has_resp}")

print()
print("=== 3) 列表结构 items/total/page/size ===")
for key in ('"items"', '"total"', '"page"', '"size"'):
    print(f"  含 {key}: {key in text}")

print()
print("=== 4) 错误体 detail ===")
print(f'  出现 "detail" 次数: {text.count(chr(34) + "detail" + chr(34))}')

print()
print("=== 5) 路径复数小写 / 禁止动词路径 ===")
bad = re.findall(r"/api/device`|/api/alarm`|/api/get[A-Za-z]+", text)
good = re.findall(
    r"/api/devices|/api/alarms|/api/workorders|/api/telemetries|/api/spares|/api/monitor",
    text,
)
print(f"  合规路径命中: {len(good)}")
print(f"  可疑单数/动词路径: {len(bad)}")
for b in bad:
    print(f"    !! {b}")

print()
print("=== 6) temperature 小数示例 ===")
print(f"  含 32.5: {'32.5' in text}")

print()
print("=== 7) 分页默认值与上限 ===")
print(f"  提到默认 1: {'默认 1' in text}")
print(f"  提到默认 20: {'默认 20' in text}")
print(f"  提到上限/不超过 100: {'上限 100' in text or '不能超过 100' in text}")

print()
print("=== 完成 ===")
print("本脚本只检查契约文档。curl 调 8000 端口要等后端实现之后。")
