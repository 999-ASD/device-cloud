# 设备云监 · 工业设备监控与运维管理系统

> **项目状态：第 1 周 / 环境已就绪**  
> 仓库地址：https://github.com/999-ASD/device-cloud

## 项目简介

「设备云监」是一门工业软件课程的全开源 Web 项目，面向工业设备监控与运维场景：后端用 FastAPI + SQLite 提供 API，通过 **Modbus TCP（端口 5020）** 采集设备数据；前端用 Vue3 + Vite + Element Plus；可用 Docker Compose 编排部署，并用 Git 做版本管理。

第 1 周目标是完成全开源工具链验证、环境自检、仓库目录骨架初始化，以及本 README 的 AI 协作撰写与人工修订。业务采集、完整前后端联调等能力将在后续周次逐步补齐。

## 功能特性（规划）

- **设备数据采集**：经 Modbus TCP 从现场/模拟设备读取寄存器数据（课程统一端口 **5020**）
- **后端服务**：FastAPI 提供 REST API、健康检查与后续报警/采集服务扩展点
- **前端监控界面**：Vue3 + Vite + Element Plus 展示设备与状态（后续周次完善）
- **设备模拟器**：`simulator/` 下提供本机可跑的 Modbus 模拟设备
- **容器化部署**：`docker-compose.yml` 统一编排（第 1 周为占位，后续补齐服务定义）

## 技术栈

| 层级 | 技术 | 说明 |
|------|------|------|
| 后端 | Python **3.11+**、FastAPI、SQLite | API 与持久化 |
| 工业协议 | **pymodbus==3.6.9**、Modbus TCP | 采集端口 **5020**（非特权端口 502） |
| 前端 | Vue3、Vite、Element Plus、Node **20+** | 开发默认端口 **5173** |
| API | Uvicorn 开发服务 | 默认端口 **8000** |
| 部署 | Docker / Docker Compose | 对外可映射 **8080**（课程约定） |
| 工程 | Git、全开源工具链 | VS Code / Continue + 本地 Ollama 可选 |

## 目录结构

与第 1 周仓库骨架对齐（勿编造不存在的顶层目录）：

```text
device-cloud/
├── backend/                 # FastAPI 后端
│   ├── app/
│   │   ├── routers/
│   │   ├── services/        # collector.py / alarm.py 等
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   └── database.py
│   ├── tests/
│   ├── requirements.txt
│   └── Dockerfile
├── simulator/               # Modbus 设备模拟
│   └── device_server.py
├── frontend/                # Vue3 + Vite 前端
│   ├── src/
│   │   ├── api/
│   │   ├── views/
│   │   └── components/
│   ├── package.json
│   └── Dockerfile
├── docs/                    # 文档与 AI 协作日志
│   ├── ai-log.md
│   └── README.ai-draft.md   # AI 原始初稿（对照用）
├── tools/
│   └── check_env.py         # 环境自检脚本
├── week01-evidence/         # 第 1 周凭证（如 selfcheck.txt）
├── docker-compose.yml
├── .gitignore
└── README.md
```

## 快速开始

> 第 1 周以「环境就绪 + 仓库骨架」为主；下列命令按真实路径书写。Compose 服务定义尚未补全时，请优先使用本机 venv / npm 方式。

### 1. 克隆仓库

```powershell
git clone https://github.com/999-ASD/device-cloud.git
cd device-cloud
```

### 2. 后端（venv）

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r backend\requirements.txt
pip install "pymodbus==3.6.9"
python tools\check_env.py
```

最小 API（进阶选做，文件写好后）：

```powershell
cd backend
python -m uvicorn app.main:app --reload --port 8000
# 浏览器访问 http://127.0.0.1:8000/health
```

### 3. 前端

```powershell
cd frontend
npm install
npm run dev
# 默认 http://127.0.0.1:5173/
```

### 4. Docker Compose（后续周次完善后）

```powershell
docker compose up --build
```

当前仓库中 `docker-compose.yml` 仍为第 1 周占位，完整 `services` 定义请以后续课程材料为准。

## 环境要求

- Windows 10/11（课程实验以 PowerShell 为主）
- Git 2.40+、Python 3.11+、Node.js 20+、Docker Desktop
- （可选）Ollama + `qwen2.5-coder:7b`、编辑器插件 Continue
- 课程关键端口：`5020` / `8000` / `5173` / `8080`

## 常见问题

| 现象 | 处理 |
|------|------|
| `python` 找不到 | 重装勾选 PATH，或关闭终端重开 |
| venv 无法激活 | `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` |
| Docker 连不上 | 启动 Docker Desktop，等待 Engine 就绪 |
| 端口被占用 | 见指导书 FAQ：查询并结束占用进程，或换端口 |
| Ollama 无响应 | 确认托盘服务运行，访问 `http://127.0.0.1:11434` |

## 许可证

本课程项目为教学用开源示例。仓库根目录**当前未附带 LICENSE 文件**；若课程后续统一许可证，以仓库新增文件及教师说明为准。请勿默认存在 `LICENSE` 文件。
