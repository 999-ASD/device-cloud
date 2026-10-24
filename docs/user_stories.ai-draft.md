# AI 初稿 · 用户故事（对照用，未裁剪）

> 按任务二三段式 prompt 的典型产出：含不确定点、部分幻觉字段与超范围故事，供人工审查对照。

## 不确定点（AI）

1. 温度报警阈值是否统一 60℃？
2. 安全门是否单独进 telemetry 还是只作 DI 点位展示？
3. 工单指派人是否需要登录账号体系？

## 实时监控

1. 作为设备管理员，我想要在监控页看到温度/转速/产量/运行状态实时刷新，以便掌握工况。（Must；表：telemetry；字段：temperature/speed/output_count/run_status）
2. 作为运维工程师，我想要断线时弹窗并自动重连，以便采集不中断。（Must；表：telemetry）
3. 作为班组长，我想要手机 App 推送实时曲线，以便不在岗也能看。（Could；表：telemetry；字段：notify_channel）← 超范围+幻觉字段

## 报警管理

1. 作为运维工程师，我想要温度≥60℃自动生成 high 级报警，以便及时处理过热。（Must；表：alarm；字段：type/level/message/ts）
2. 作为设备管理员，我想要确认报警后记录 severity_score，以便考核风险。（Should；表：alarm；字段：severity_score）← 幻觉字段
3. 作为运维工程师，我想要同类报警短时间合并，以便避免刷屏。（Must；表：alarm；字段：type/ts/acked）

## 巡检/报修工单

1. 作为班组长，我想要从报警一键创建报修工单并指派处理人，以便闭环处理。（Must；表：work_order；字段：type/title/status/assignee/created_at）
2. 作为运维工程师，我想要处理完成后关闭工单并写 closed_at，以便统计耗时。（Must；表：work_order；字段：status/closed_at）
3. 作为设备管理员，我想要多级审批后才能关单，以便管控质量。（Must；表：work_order；字段：operator_id）← 超范围+幻觉

## 其他（AI 顺带写的）

- 作为设备管理员，我想要微信通知报警，以便随时响应。（Could；字段：notify_channel）← Won't
