# tools/check_env.py —— 设备云监 开发环境自检（Windows 适用）
# 用法：在已激活的 venv 中执行  python tools\check_env.py
# 依赖：仅用 Python 标准库，无需额外安装

import json
import socket
import subprocess
import sys
import urllib.request

OK, WARN, FAIL = "OK", "WARN", "FAIL"
results = []


def run(cmd):
    """执行命令并返回 (成功?, 输出文本)。"""
    try:
        p = subprocess.run(
            cmd, shell=True, capture_output=True, text=True, timeout=30
        )
        out = (p.stdout or p.stderr or "").strip().splitlines()
        return p.returncode == 0, (out[0] if out else "")
    except Exception as e:  # noqa: BLE001
        return False, str(e)


def record(name, status, detail):
    results.append((name, status, detail))
    color = {"OK": "\033[92m", "WARN": "\033[93m", "FAIL": "\033[91m"}[status]
    print(f"{color}[{status:4}]\033[0m {name:<22} {detail}")


def check_cmd(name, cmd, hint):
    ok, out = run(cmd)
    if ok and out:
        record(name, OK, out)
    else:
        record(name, FAIL, f"未安装或异常（{hint}）")


def check_python_version():
    v = ".".join(map(str, sys.version_info[:3]))
    if sys.version_info[:2] >= (3, 11):
        record("Python 版本", OK, f"{v} (>=3.11)")
    else:
        record("Python 版本", FAIL, f"{v}，需 3.11+")


def check_sqlite():
    try:
        import sqlite3

        record("SQLite(免装)", OK, sqlite3.sqlite_version)
    except Exception as e:  # noqa: BLE001
        record("SQLite(免装)", FAIL, str(e))


def check_pymodbus():
    try:
        import pymodbus

        record("pymodbus", OK, pymodbus.__version__)
    except Exception:
        record("pymodbus", WARN, '未安装（pip install "pymodbus==3.6.9"）')


def check_docker_engine():
    ok, _ = run("docker info")
    record(
        "Docker Engine",
        OK if ok else FAIL,
        "运行中" if ok else "未运行：请启动 Docker Desktop",
    )


def check_ollama():
    """检查 Ollama 服务、模型列表与一次真实对话连通性。"""
    base = "http://127.0.0.1:11434"
    try:
        with urllib.request.urlopen(f"{base}/api/tags", timeout=5) as r:
            data = json.load(r)
        names = [m.get("name", "") for m in data.get("models", [])]
        record("Ollama 服务", OK, "在线")
        record("已下载模型", OK if names else WARN, ", ".join(names) or "无")
        has_model = any("qwen2.5-coder" in n for n in names)
        record(
            "Qwen2.5-Coder",
            OK if has_model else WARN,
            "已就绪" if has_model else "未发现：ollama pull qwen2.5-coder:7b",
        )
        payload = json.dumps(
            {
                "model": "qwen2.5-coder:7b",
                "prompt": "只回复两个字：就绪",
                "stream": False,
            }
        ).encode()
        req = urllib.request.Request(
            f"{base}/api/generate",
            data=payload,
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=120) as r:
            resp = json.load(r)
        text = (resp.get("response") or "").strip().replace("\n", " ")[:30]
        record("Ollama 推理连通", OK, text or "(空响应)")
    except Exception as e:  # noqa: BLE001
        record("Ollama 服务", FAIL, f"未响应（启动 Ollama）：{e}")


def check_ports(ports=(5020, 8000, 5173, 8080)):
    for p in ports:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)
        busy = s.connect_ex(("127.0.0.1", p)) == 0
        s.close()
        record(
            f"端口 {p}",
            WARN if busy else OK,
            "被占用（注意）" if busy else "空闲",
        )


def main():
    print("===== 设备云监 环境自检（Python 版）=====\n")
    print("--- 命令行工具 ---")
    check_cmd("Git", "git --version", "安装 Git 并加入 PATH")
    check_cmd("编辑器", "codium --version || code --version", "装 VSCodium/VS Code")
    check_cmd("Python", "python --version", "安装 Python 并勾选 PATH")
    check_cmd("pip", "pip --version", "pip 异常")
    check_cmd("Node", "node --version", "装 Node.js 20+")
    check_cmd("npm", "npm --version", "npm 异常")
    check_cmd("Docker", "docker --version", "装/启动 Docker Desktop")
    check_cmd("Compose", "docker compose version", "compose 插件缺失")
    check_cmd("Ollama", "ollama --version", "装 Ollama")
    print("\n--- 深度检查 ---")
    check_python_version()
    check_sqlite()
    check_pymodbus()
    check_docker_engine()
    check_ollama()
    print("\n--- 端口占用 ---")
    check_ports()
    n_fail = sum(1 for _, s, _ in results if s == FAIL)
    n_warn = sum(1 for _, s, _ in results if s == WARN)
    print(
        f"\n===== 结果：{len(results) - n_fail - n_warn} 通过 / "
        f"{n_warn} 警告 / {n_fail} 失败 ====="
    )
    if n_fail == 0:
        print("环境就绪，可以开始第 1 周课程！")
        return 0
    print("请按 FAIL/WARN 提示逐项修复后重跑。")
    return 1


if __name__ == "__main__":
    sys.exit(main())
