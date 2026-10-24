# 设备云监 · 用户故事（第 2 周 v1）

> 格式：作为 \<角色\>，我想要 \<功能\>，以便 \<价值\>。  
> 优先级：MoSCoW（Must / Should / Could / Won't）；引用表与字段以课程 `01` 约定为准。  
> 角色仅限：设备管理员 / 运维工程师 / 班组长。

## 实时监控

- [ ] 作为 设备管理员，我想要 在监控页看到设备温度/转速/产量/运行状态实时刷新，以便 随时掌握设备状况。（Must；表：telemetry；字段：temperature/speed/output_count/run_status）
- [ ] 作为 运维工程师，我想要 在监控页同时看到安全门开闭状态，以便 判断能否安全启停设备。（Must；表：telemetry；字段：run_status；点位：DI10001）
- [ ] 作为 设备管理员，我想要 Modbus 断线时界面明确提示并在恢复后自动继续刷新数据，以便 避免把过期值当成实时值。（Must；表：telemetry；字段：temperature/speed/output_count/run_status）
- [ ] 作为 运维工程师，我想要 温度按 HR40001×10 存储时在界面与阈值比较前先 ÷10 还原，以便 显示值与真实℃一致。（Must；表：telemetry；字段：temperature）

## 报警管理

- [ ] 作为 运维工程师，我想要 温度还原后 ≥ 60℃ 时自动生成 high 级报警并出现在监控页，以便 第一时间处理过热风险。（Must；表：alarm；字段：type/level/message/ts）
- [ ] 作为 运维工程师，我想要 在监控页确认报警并写入 acked，清除完成后写入 cleared_at，以便 区分「已知晓」与「已消除」。（Must；表：alarm；字段：acked/cleared_at）
- [ ] 作为 设备管理员，我想要 同一设备同一条件短时间重复触发时合并/抑制重复报警，以便 避免报警刷屏干扰处置。（Must；表：alarm；字段：type/level/message/ts/acked）
- [ ] 作为 运维工程师，我想要 报警已关闭或已清除后，在条件未再次满足前不再重复生成同类报警，以便 减少无效工单。（Must；表：alarm；字段：type/acked/cleared_at）

## 巡检/报修工单

- [ ] 作为 班组长，我想要 从一条未关闭报警一键创建报修工单并填写 type/title/assignee，以便 把异常闭环处理。（Must；表：work_order；字段：type/title/status/assignee/content/created_at）
- [ ] 作为 运维工程师，我想要 处理完成后将工单状态改为已关闭并记录 closed_at，以便 统计处理耗时与完成情况。（Must；表：work_order；字段：status/assignee/closed_at）
- [ ] 作为 班组长，我想要 查看工单列表并按 status/assignee 筛选，以便 掌握班组待办与进度。（Must；表：work_order；字段：type/title/status/assignee/created_at/closed_at）
- [ ] 作为 设备管理员，我想要 登记巡检类工单（type=巡检）及 content 结论，以便 留下可追溯的巡检记录。（Should；表：work_order；字段：type/title/status/content/created_at/closed_at）

## 备件管理（Should）

- [ ] 作为 设备管理员，我想要 维护备件主数据（名称/规格/库存），以便 掌握可用备件。（Should；表：spare_part）
- [ ] 作为 运维工程师，我想要 登记备件出入库并关联工单或设备说明，以便 追溯消耗。（Should；表：spare_record；可关联 work_order）

## 报表（Could）

- [ ] 作为 班组长，我想要 按日查看报警次数与已关闭工单数，以便 做班组交接简报。（Could；表：alarm/work_order；字段：type/ts/status/closed_at）

## 明确不做（Won't）

- 真实工业现场硬件接入（本课仅用本机 Modbus 模拟，端口 5020）
- 多租户 / 多工厂云平台对比
- 权限体系、多角色审批流（v1 单角色操作即可）
- 邮件 / 短信 / 微信等站外通知
- 移动 App

## 人工裁剪记录（写清删/改/补的理由）

1. AI：「手机 App 推送实时曲线」（字段 notify_channel）→ **驳回**：移动 App + 幻觉字段 `notify_channel`，列入 Won't。
2. AI：「确认报警后记录 severity_score」→ **驳回**：`severity_score` 不在 01 的 alarm 字段中；改为使用已有 `level` + `acked/cleared_at`。
3. AI：「多级审批关单 + operator_id」→ **驳回**：审批流超出范围；`operator_id` 非约定字段；改为 `assignee` + `status/closed_at`。
4. AI 原稿缺少边界 → **补充**：断线重连、温度 ×10 还原、报警去重、「关闭/清除后不再重复报警」。
