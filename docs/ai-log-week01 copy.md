# AI 协作日志（第 1 周）

> 任务四：记录 prompt、AI 产出与人工审查。至少修正 1 处 AI 错误或幻觉。

## 日志条目 1

| 项 | 内容 |
|----|------|
| 日期 | 2026-10-13 |
| 工具 | Ollama `qwen2.5-coder:7b`（HTTP `/api/generate`；亦可在 VS Code Continue 中复现） |
| Prompt 原文 | 见下方「三段式提示词」 |
| AI 产出摘要 | 生成了含简介/功能/技术栈/目录/快速开始/环境/FAQ/许可证的 Markdown 初稿；结构完整，但目录与命令多处与真实仓库不符，且未写明 `pymodbus==3.6.9`。原始稿保存在 `docs/README.ai-draft.md`。 |
| 采纳 / 驳回 | **采纳**：项目定位、端口 5020/8000/5173、Python 3.11+ / Node 20+、Vue3+Vite+Element Plus、Docker Compose 方向。**驳回/重写**：虚构目录与文件、根目录 `npm install`、错误 clone 地址、不存在的日志路径、完整 MIT 正文与不存在的 LICENSE、夸大已完成功能。 |
| 幻觉修正示例 | ① AI 把后端写成 `backend/main.py`，并把 `simulator/main.py`、`docs/index.md` 等写进树中 → **改为**实际骨架 `backend/app/main.py`、`simulator/device_server.py`，并补充 `tools/`、`week01-evidence/`。② AI 写 `npm install` 在仓库根目录执行 → **改为** `cd frontend` 后再 `npm install`。③ AI 声称存在 `LICENSE` 与 `backend/logs/app.log` → **删除/更正**，并注明第 1 周状态与真实仓库 URL。 |

### 三段式提示词（原文）

```text
背景：Web 项目「工业设备监控与运维」，项目名「设备云监」。
技术栈：Python 3.11+ + FastAPI + SQLite；Modbus TCP 采集（端口 5020）；
前端 Vue3 + Vite + Element Plus；Docker Compose 部署；Git；全开源。
任务：写 README.md 初稿。
约束：Markdown；章节含：项目简介、功能特性、技术栈、目录结构、
快速开始、环境要求、常见问题、许可证。
目录结构必须与下列一致：
device-cloud/
  backend/
  simulator/
  frontend/
  docs/
  docker-compose.yml
  README.md
请写明 Python 3.11+、Node 20+、pymodbus、端口 5020/8000/5173。
```

### 人工审查核对清单

1. [x] 技术版本：Python 3.11+、Node 20+、**pymodbus==3.6.9**、端口 5020  
2. [x] 目录结构与仓库一致（对照 `tree` / 资源管理器）  
3. [x] 「快速开始」命令可执行、路径正确  
4. [x] 删除不存在依赖、假日志、假 LICENSE  
5. [x] 补充「项目状态：第 1 周 / 环境已就绪」与仓库地址 `https://github.com/999-ASD/device-cloud`

### 结论

任务四要求「AI 出初稿 + 人工至少修 1 处幻觉」已满足；对照文件：

- AI 原稿：`docs/README.ai-draft.md`
- 修订后：`README.md`
- 本日志：`docs/ai-log.md`
