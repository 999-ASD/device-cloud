# AI 初稿 · 验收标准（对照用）

## 不确定点（AI）

1. 恰好等于 60℃ 是否报警？
2. 「推送到监控页」是否等于 WebSocket，还是刷新列表即可？
3. 关闭工单是否必须填写 content？

## AC 草稿（含问题，待裁剪）

### AC-1
Given 设备在跑
When 温度有点高
Then 系统尽快生成报警并通知相关人员

问题：模糊词「有点高/尽快」；引入站外通知；缺量化与字段名。

### AC-2
Given 台账有数据
When 搜索设备
Then 能搜到想要的设备，体验良好

问题：不可测；未指定 code 字段与时限。

### AC-3
Given 有一张工单
When 点关闭
Then 工单关掉，operator_id 记谁关的

问题：幻觉字段 operator_id；缺 status/closed_at 明确值。
