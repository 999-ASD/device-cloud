# 设备云监（Device Cloud Monitor）

> 以下为本地模型 `qwen2.5-coder:7b`（Ollama API）生成的原始初稿，未经人工修改，供对照审查。

## 项目简介

设备云监是一个基于 FastAPI 和 SQLite 的工业设备监控与运维平台。前端采用 Vue3 和 Element Plus 开发，通过 Modbus TCP 协议采集设备数据，并通过 Docker Compose 进行部署。本项目旨在提供一个高效、可靠、可扩展的工业设备监控系统。

## 功能特性

1. **设备数据采集**：通过 Modbus TCP 协议从设备收集实时数据。
2. **数据可视化**：前端展示设备运行状态和历史数据。
3. **报警系统**：实时监控设备状态，当发生异常时发出警报。
4. **设备维护管理**：记录设备维护记录和故障历史。
5. **用户权限管理**：多用户权限控制，确保数据安全。

## 技术栈

- **后端**：
  - Python 3.11+
  - FastAPI
  - SQLite
  - Modbus TCP (端口 5020)

- **前端**：
  - Vue3
  - Vite
  - Element Plus

- **部署**：
  - Docker Compose

## 目录结构

```
device-cloud/
  backend/
    main.py
    models.py
    schemas.py
    routers/
      __init__.py
      devices.py
      alarms.py
  simulator/
    main.py
    modbus_server.py
  frontend/
    public/
    src/
      assets/
      components/
      router/
      views/
      App.vue
      main.js
  docs/
    index.md
  docker-compose.yml
  README.md
```

## 快速开始

1. **克隆项目**：
   ```bash
   git clone https://github.com/your-repo/device-cloud.git
   cd device-cloud
   ```

2. **安装依赖**：
   ```bash
   pip install -r backend/requirements.txt
   npm install
   ```

3. **启动服务**：
   ```bash
   docker-compose up --build
   ```

4. **访问应用**：
   - 后端服务：http://localhost:8000
   - 前端服务：http://localhost:5173

## 环境要求

- **Python**：3.11+
- **Node.js**：20+
- **Docker**：最新版本
- **Docker Compose**：最新版本

## 常见问题

1. **启动失败**：检查日志文件 `backend/logs/app.log` 和 `frontend/logs/dev.log` 以获取更多信息。
2. **端口冲突**：确保端口 5020、8000 和 5173 没有被其他应用占用。

## 许可证

本项目采用 MIT 许可证，详情请参阅 LICENSE 文件。
