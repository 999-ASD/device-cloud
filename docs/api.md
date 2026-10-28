# 设备云监 · 接口契约（REST）

> 第 3 周任务二。路径复数小写；列表统一分页；错误统一 `{detail}`。  
> 字段对齐 `docs/er.md` / `01` 第六节。温度示例使用小数（如 `32.5`）。  
> Base URL（开发）：`http://127.0.0.1:8000`

## 约定

| 项 | 约定 |
|----|------|
| 路径 | 复数小写，如 `/api/devices`；不用 `/api/device`、`/api/getDevices` |
| 分页 | 查询参数 `page`（默认 1）、`size`（默认 20，**上限 100**） |
| 列表成功体 | `{ "items": [...], "total": N, "page": P, "size": S }` |
| 错误体 | `{ "detail": "说明文字" }`（FastAPI 风格） |
| 时间 | `YYYY-MM-DD HH:MM:SS`（UTC，与 DDL 说明一致） |
| `acked` | JSON 用 `0` / `1`（与库 INTEGER 一致；不用 true/false，避免与 DDL 两套口径） |
| 响应信封 | `items` / `total` / `page` / `size` **只存在于 API 响应**，不是数据库新字段，禁止为此改 ER/DDL |
| 报警→工单 | `work_order` **无 `alarm_id` 列**（01/ER 未定义）。由报警建单时：写 `device_id`，在 `content` 注明来源（如「由报警 #12 创建」），**不得新增外键列** |
| 删除策略 | 当前 DDL **无 ON DELETE CASCADE**；删设备前应由应用层处理关联数据或拒绝删除（返回明确 `detail`） |

### 接口清单（共 17）

| # | 方法 | 路径 | 用途 |
|---|------|------|------|
| 1 | GET | `/api/devices` | 分页查询设备台账（可按 code 搜索） |
| 2 | GET | `/api/devices/{id}` | 查询单台设备详情 |
| 3 | POST | `/api/devices` | 新增设备 |
| 4 | PUT | `/api/devices/{id}` | 更新设备台账 |
| 5 | DELETE | `/api/devices/{id}` | 删除设备 |
| 6 | GET | `/api/telemetries` | 分页查询历史遥测 |
| 7 | GET | `/api/telemetries/latest` | 查询指定设备最新一条遥测 |
| 8 | GET | `/api/alarms` | 分页查询报警（acked/level 过滤） |
| 9 | POST | `/api/alarms/{id}/ack` | 确认报警（acked=1） |
| 10 | POST | `/api/alarms/{id}/clear` | 消警（写入 cleared_at） |
| 11 | GET | `/api/workorders` | 分页查询工单 |
| 12 | POST | `/api/workorders` | 创建巡检/报修工单 |
| 13 | PATCH | `/api/workorders/{id}` | 更新工单状态（含关闭写 closed_at） |
| 14 | GET | `/api/spares` | 分页查询备件主数据 |
| 15 | POST | `/api/spares/records` | 登记备件出入库 |
| 16 | GET | `/api/stats` | 利用率/报警/工单统计汇总 |
| 17 | GET | `/api/monitor/latest` | 监控看板最新快照（含 temperature 小数） |

---

## 1. 设备台账（5）

### 1.1 GET `/api/devices`

**说明：** 分页查询设备列表；可按 `code` 模糊搜索（对齐 AC-2）。

**请求参数（Query）**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| code | string | 否 | 按设备编号搜索 |
| page | int | 否 | 默认 1 |
| size | int | 否 | 默认 20，上限 100 |

**成功响应 200**

```json
{
  "items": [
    {
      "id": 1,
      "code": "EQ-001",
      "name": "1号注塑机",
      "model": "X-200",
      "location": "A车间",
      "owner": "张三",
      "status": "running",
      "created_at": "2026-10-20 08:00:00"
    }
  ],
  "total": 1,
  "page": 1,
  "size": 20
}
```

**错误**

| 状态码 | 示例 |
|--------|------|
| 400 | `{ "detail": "size 不能超过 100" }` |

---

### 1.2 GET `/api/devices/{id}`

**说明：** 按主键查询单台设备。

**路径参数：** `id`（int）

**成功响应 200**

```json
{
  "id": 1,
  "code": "EQ-001",
  "name": "1号注塑机",
  "model": "X-200",
  "location": "A车间",
  "owner": "张三",
  "status": "running",
  "created_at": "2026-10-20 08:00:00"
}
```

**错误**

| 状态码 | 示例 |
|--------|------|
| 404 | `{ "detail": "设备不存在" }` |

---

### 1.3 POST `/api/devices`

**说明：** 新增设备；`code` 全局唯一。

**请求体**

```json
{
  "code": "EQ-002",
  "name": "2号注塑机",
  "model": "X-200",
  "location": "B车间",
  "owner": "李四",
  "status": "idle"
}
```

**成功响应 201**

```json
{
  "id": 2,
  "code": "EQ-002",
  "name": "2号注塑机",
  "model": "X-200",
  "location": "B车间",
  "owner": "李四",
  "status": "idle",
  "created_at": "2026-10-27 10:00:00"
}
```

**错误**

| 状态码 | 示例 |
|--------|------|
| 400 | `{ "detail": "code 不能为空" }` |
| 409 | `{ "detail": "设备编号已存在" }` |

---

### 1.4 PUT `/api/devices/{id}`

**说明：** 全量更新设备台账字段（不含改 `id` / `code` 冲突由服务端校验）。

**请求体**

```json
{
  "code": "EQ-001",
  "name": "1号注塑机",
  "model": "X-200",
  "location": "A车间-东",
  "owner": "张三",
  "status": "running"
}
```

**成功响应 200：** 返回更新后的设备对象（字段同 1.2）。

**错误：** `404` 设备不存在；`409` code 与其它设备冲突。

---

### 1.5 DELETE `/api/devices/{id}`

**说明：** 删除设备台账记录。DDL **无级联删除**；若仍存在关联遥测/报警/工单，应返回 409，由应用层先处理关联数据（本契约不自动 CASCADE）。

**成功响应 204：** 无响应体。

**错误**

| 状态码 | 示例 |
|--------|------|
| 404 | `{ "detail": "设备不存在" }` |
| 409 | `{ "detail": "存在关联遥测/报警/工单，无法删除" }` |

---

## 2. 遥测（2）

### 2.1 GET `/api/telemetries`

**说明：** 分页查询历史遥测；可按设备与时间过滤。温度已为还原后的 ℃（`REAL`）。

**请求参数（Query）**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| device_id | int | 否 | 设备主键 |
| from_ts | string | 否 | 起始时间 |
| to_ts | string | 否 | 结束时间 |
| page | int | 否 | 默认 1 |
| size | int | 否 | 默认 20，上限 100 |

**成功响应 200**

```json
{
  "items": [
    {
      "id": 101,
      "device_id": 1,
      "ts": "2026-10-27 09:00:00",
      "temperature": 32.5,
      "speed": 1200,
      "output_count": 100,
      "run_status": 1
    }
  ],
  "total": 1,
  "page": 1,
  "size": 20
}
```

**错误：** `400` `{ "detail": "size 不能超过 100" }`

---

### 2.2 GET `/api/telemetries/latest`

**说明：** 查询指定设备最新一条遥测（曲线/详情页用）。

**请求参数（Query）**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| device_id | int | 是 | 设备主键 |

**成功响应 200**

```json
{
  "id": 101,
  "device_id": 1,
  "ts": "2026-10-27 09:00:00",
  "temperature": 32.5,
  "speed": 1200,
  "output_count": 100,
  "run_status": 1
}
```

**错误**

| 状态码 | 示例 |
|--------|------|
| 400 | `{ "detail": "device_id 必填" }` |
| 404 | `{ "detail": "暂无遥测数据" }` |

---

## 3. 报警（3）

### 3.1 GET `/api/alarms`（完整示例）

**说明：** 分页查询报警列表；可按确认状态、级别过滤。

**请求参数（Query）**

| 参数 | 类型 | 必填 | 默认 | 说明 |
|------|------|------|------|------|
| acked | int | 否 | — | `0` 未确认 / `1` 已确认；不传则不过滤 |
| level | string | 否 | — | 如 `high` / `medium` / `low` |
| page | int | 否 | 1 | 页码，从 1 起 |
| size | int | 否 | 20 | 每页条数，**上限 100** |

**请求示例**

```http
GET /api/alarms?acked=0&level=high&page=1&size=20
```

**成功响应 200**

```json
{
  "items": [
    {
      "id": 12,
      "device_id": 1,
      "type": "temperature_high",
      "level": "high",
      "message": "温度超过 60℃",
      "ts": "2026-10-27 09:01:00",
      "acked": 0,
      "cleared_at": null
    }
  ],
  "total": 1,
  "page": 1,
  "size": 20
}
```

**错误码**

| 状态码 | 条件 | 响应示例 |
|--------|------|----------|
| 400 | `size > 100` | `{ "detail": "size 不能超过 100" }` |
| 400 | `acked` 非 0/1 | `{ "detail": "acked 只能为 0 或 1" }` |
| 500 | 服务异常 | `{ "detail": "内部错误" }` |

---

### 3.2 POST `/api/alarms/{id}/ack`

**说明：** 确认报警，将 `acked` 置为 `1`（对齐 PRD「确认」）。

**请求体：** 无（或空对象 `{}`）。

**成功响应 200**

```json
{
  "id": 12,
  "device_id": 1,
  "type": "temperature_high",
  "level": "high",
  "message": "温度超过 60℃",
  "ts": "2026-10-27 09:01:00",
  "acked": 1,
  "cleared_at": null
}
```

**错误**

| 状态码 | 示例 |
|--------|------|
| 404 | `{ "detail": "报警不存在" }` |
| 409 | `{ "detail": "报警已确认" }` |

---

### 3.3 POST `/api/alarms/{id}/clear`

**说明：** 消警：写入 `cleared_at`（当前 UTC 时间）。不新增表字段；仅更新 `alarm.cleared_at`。

**请求体：** 无（或空对象 `{}`）。

**成功响应 200**

```json
{
  "id": 12,
  "device_id": 1,
  "type": "temperature_high",
  "level": "high",
  "message": "温度超过 60℃",
  "ts": "2026-10-27 09:01:00",
  "acked": 1,
  "cleared_at": "2026-10-27 09:20:00"
}
```

**错误**

| 状态码 | 示例 |
|--------|------|
| 404 | `{ "detail": "报警不存在" }` |
| 409 | `{ "detail": "报警已消警" }` |

---

## 4. 工单（3）

### 4.1 GET `/api/workorders`

**说明：** 分页查询工单；可按状态、设备过滤。

**请求参数（Query）**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| status | string | 否 | 如 `待处理` / `处理中` / `已关闭` |
| device_id | int | 否 | 设备主键 |
| page | int | 否 | 默认 1 |
| size | int | 否 | 默认 20，上限 100 |

**成功响应 200**

```json
{
  "items": [
    {
      "id": 3,
      "device_id": 1,
      "type": "报修",
      "title": "温度偏高检修",
      "status": "处理中",
      "assignee": "运维-王五",
      "content": "由报警 #12 创建",
      "created_at": "2026-10-27 09:05:00",
      "closed_at": null
    }
  ],
  "total": 1,
  "page": 1,
  "size": 20
}
```

**错误：** `400` `{ "detail": "size 不能超过 100" }`

---

### 4.2 POST `/api/workorders`

**说明：** 创建巡检/报修工单（可由报警触发，本接口只负责落库）。  
**注意：** 请求体**不含** `alarm_id`（表无此列）。与报警的追溯写在 `content` 文本中，设备关联只用 `device_id`。

**请求体**

```json
{
  "device_id": 1,
  "type": "报修",
  "title": "温度偏高检修",
  "status": "待处理",
  "assignee": "运维-王五",
  "content": "由报警 #12 创建"
}
```

**成功响应 201**

```json
{
  "id": 3,
  "device_id": 1,
  "type": "报修",
  "title": "温度偏高检修",
  "status": "待处理",
  "assignee": "运维-王五",
  "content": "由报警 #12 创建",
  "created_at": "2026-10-27 09:05:00",
  "closed_at": null
}
```

**错误：** `400` 参数不合法；`404` 设备不存在。

---

### 4.3 PATCH `/api/workorders/{id}`

**说明：** 更新工单状态/指派人等；关闭时 `status=已关闭` 并写入 `closed_at`（对齐 AC-3）。

**请求体（示例：关闭）**

```json
{
  "status": "已关闭",
  "assignee": "运维-王五",
  "content": "已更换冷却风扇"
}
```

**成功响应 200**

```json
{
  "id": 3,
  "device_id": 1,
  "type": "报修",
  "title": "温度偏高检修",
  "status": "已关闭",
  "assignee": "运维-王五",
  "content": "已更换冷却风扇",
  "created_at": "2026-10-27 09:05:00",
  "closed_at": "2026-10-27 11:00:00"
}
```

**错误：** `404` 工单不存在；`400` 状态非法。

---

## 5. 备件（2）

### 5.1 GET `/api/spares`

**说明：** 分页查询备件主数据（`spare_part`）。

**请求参数：** `page`、`size`（默认/上限同前）；可选 `name` 模糊搜索。

**成功响应 200**

```json
{
  "items": [
    {
      "id": 1,
      "name": "冷却风扇",
      "spec": "120mm/220V",
      "qty": 8,
      "location": "备件仓-A1"
    }
  ],
  "total": 1,
  "page": 1,
  "size": 20
}
```

---

### 5.2 POST `/api/spares/records`

**说明：** 登记出入库（写 `spare_record`，并按 `in`/`out` 调整库存 `qty`）。

**请求体**

```json
{
  "part_id": 1,
  "type": "out",
  "qty": 1,
  "note": "工单 #3 领用"
}
```

**成功响应 201**

```json
{
  "id": 20,
  "part_id": 1,
  "type": "out",
  "qty": 1,
  "ts": "2026-10-27 11:05:00",
  "note": "工单 #3 领用"
}
```

**错误**

| 状态码 | 示例 |
|--------|------|
| 400 | `{ "detail": "type 只能为 in 或 out" }` |
| 404 | `{ "detail": "备件不存在" }` |
| 409 | `{ "detail": "库存不足" }` |

---

## 6. 报表（1）

### 6.1 GET `/api/stats`

**说明：** 简易统计：利用率（基于 `run_status`）、报警次数、工单关闭情况（P1）。

**请求参数（Query，可选）**

| 参数 | 类型 | 说明 |
|------|------|------|
| from_ts | string | 统计起始 |
| to_ts | string | 统计结束 |
| device_id | int | 限定单设备 |

**成功响应 200**

```json
{
  "utilization": 0.82,
  "alarm_count": 15,
  "workorder_closed_count": 7,
  "workorder_open_count": 3,
  "from_ts": "2026-10-01 00:00:00",
  "to_ts": "2026-10-27 23:59:59"
}
```

**错误：** `400` 时间范围非法。

---

## 7. 实时监控（1）

### 7.1 GET `/api/monitor/latest`

**说明：** 监控看板一次拉取「设备 + 最新工况」；供 Dashboard 刷新（≤3s 周期）。含断线相关状态字段（由采集服务维护）。

**请求参数：** 无（或可选 `device_id`；不传则返回全部设备最新快照列表——本约定：**返回列表分页结构**，默认第一页）。

**请求参数（Query）**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| page | int | 否 | 默认 1 |
| size | int | 否 | 默认 20，上限 100 |

**成功响应 200**（注意 temperature 为小数 **32.5**，不是 32）

```json
{
  "items": [
    {
      "device_id": 1,
      "code": "EQ-001",
      "name": "1号注塑机",
      "status": "running",
      "online": true,
      "ts": "2026-10-27 09:00:00",
      "temperature": 32.5,
      "speed": 1200,
      "output_count": 100,
      "run_status": 1,
      "door_open": 0
    }
  ],
  "total": 1,
  "page": 1,
  "size": 20
}
```

**错误**

| 状态码 | 示例 |
|--------|------|
| 503 | `{ "detail": "采集服务不可用，请检查 Modbus 5020 与后端 8000 端口" }` |

---

## 附录 A：拆分说明

- 合计 **17** 条：设备 5 + 遥测 2 + 报警 3（查询/确认/消警）+ 工单 3 + 备件 2 + 报表 1 + 监控 1。
- 工单路径使用 `/api/workorders`（对齐 `01` routers 命名），不用动词路径。
- 列表接口均含 `page`/`size` 默认值与上限 100；错误体统一 `{detail}`。

## 附录 B：对照任务一 / 第 2 周自检

每个模块写完后用三问核对：

1. **字段落点：** 请求/响应字段能否映射到六表（`device` / `telemetry` / `alarm` / `work_order` / `spare_part` / `spare_record`）？有无擅自新增列（如 `alarm_id`、`items` 当库字段）？
2. **行为对齐：** 是否覆盖 PRD/AC（按 code 搜设备、温度用小数、报警确认/消警、关单写 `closed_at`）？
3. **错误说清：** 编号冲突、库存不足、资源不存在等是否给出明确 `{detail}`，而不是空 500？

**本文件自检结论：** 三问均已按约定处理；分页信封与报警→工单追溯方式已在「约定」中写死，避免后续改表。
