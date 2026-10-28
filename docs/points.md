# 设备云监 · Modbus 点位表

> 第 3 周任务四。对齐 `01_项目设定与工具栈.md` 第三节与教材 3.6。  
> 通信：Modbus TCP，`127.0.0.1:5020`，从站 `slave_id=1`（课程约定）。  
> **双列地址：** 传统地址为 1 基展示；pymodbus 使用 0 基偏移（禁止把 40001 直接写进 `address=`）。

## 1. 点位表（7 行）

| 类型 | 传统地址（1 基） | 名称 | 含义 | 功能码 | pymodbus 偏移（0 基） |
|------|------------------|------|------|--------|------------------------|
| HR（保持寄存器，4x） | 40001 | temperature | 设备温度（℃×10 存储） | 03 读 / 06·16 写 | 0 |
| HR（保持寄存器，4x） | 40002 | speed | 转速（rpm） | 03 读 / 06·16 写 | 1 |
| HR（保持寄存器，4x） | 40003 | output_count | 产量计数（件） | 03 读 / 06·16 写 | 2 |
| HR（保持寄存器，4x） | 40004 | run_status | 运行状态：0 停机 / 1 运行 / 2 故障 | 03 读 / 06·16 写 | 3 |
| DI（离散输入，1x） | 10001 | door_open | 安全门是否打开：0/1 | 02 读 | 0 |
| Coil（线圈，0x） | 00001 | start_cmd | 启动命令（可写）：0/1 | 01 读 / 05 写 | 0 |
| Coil（线圈，0x） | 00002 | stop_cmd | 停止命令（可写）：0/1 | 01 读 / 05 写 | 1 |

## 2. 偏移核算（必核）

| 传统地址 | 换算 | pymodbus `address` |
|----------|------|---------------------|
| 40001 | 40001 − 40001 = 0 | **0** |
| 40002 | 40002 − 40001 = 1 | **1** |
| 40003 | 40003 − 40001 = 2 | **2** |
| 40004 | 40004 − 40001 = 3 | **3** |
| 10001 | 10001 − 10001 = 0 | **0** |
| 00001 | 00001 − 00001 = 0 | **0** |
| 00002 | 00002 − 00001 = 1 | **1** |

> 常见错误：把传统地址 `40001` 直接传给 pymodbus → 读错寄存器。正确写法见下一节。

## 3. 温度换算说明（℃ × 10）

- 保持寄存器 **40001 / 偏移 0** 中的整数值按 **℃ × 10** 存放。  
  - 例：寄存器值 `325` → 真实温度 **32.5℃**  
- **入库 / 显示 / 与阈值比较前必须 ÷10**（对齐 PRD、AC-1：还原后再与 60℃ 比较）。  
- `telemetry.temperature` 类型为 `REAL`，应存还原后的小数（如 `32.5`），不是 `325`。

## 4. 采集调用对照（第 4 周可直接照抄）

一次读齐 4 个保持寄存器（温度、转速、产量、运行状态）：

```python
# 正确：address 用 0 基偏移，不是 40001
result = client.read_holding_registers(address=0, count=4, slave=1)
# result.registers == [325, 1450, 128, 1] 时：
# temperature = 325 / 10  →  32.5
# speed = 1450
# output_count = 128
# run_status = 1
```

读安全门（DI）：

```python
client.read_discrete_inputs(address=0, count=1, slave=1)
```

写启动 / 停止线圈（若后续做写控）：

```python
client.write_coil(address=0, value=True, slave=1)   # start_cmd
client.write_coil(address=1, value=True, slave=1)   # stop_cmd
```

## 5. 自检清单

- [x] 表格 **7 行**齐全，含 HR×4、DI×1、Coil×2  
- [x] **双列地址**（1 基传统地址 + 0 基偏移）都在  
- [x] 偏移列已逐一核算，无「40001 写进偏移列」  
- [x] 有「温度 ×10 / 入库前 ÷10」说明  
- [x] 能直接写出 `read_holding_registers(address=0, count=4)`  

## 6. 与任务一 / 任务二的对应

| 点位 | 落库 / 接口字段 |
|------|-----------------|
| temperature（÷10 后） | `telemetry.temperature`；监控示例用 `32.5` |
| speed | `telemetry.speed` |
| output_count | `telemetry.output_count` |
| run_status | `telemetry.run_status` |
| door_open | 监控快照可展示；不单独扩表 |
| start_cmd / stop_cmd | v1 以监控读为主，写操作可后续扩展 |
