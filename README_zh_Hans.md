# 等比中心裁切 v0.0.5

用于自主 Agent：直接接收生图工具返回的 HTTPS 图片 URL，工具自行下载并保留原图中央宽高各 85%，不缩放、不加留白。1024×1024 原图输出 870×870 PNG。

## 安装

Dify「集成 → 安装 → GitHub」输入 `https://github.com/Ethan3114/dify-center-crop`，选择 `v0.0.5` 和 `center_crop-0.0.5.difypkg`。也可以下载该包，通过「本地集成包」安装。此包未签名，尚未经过 Marketplace 审核。

## 自主 Agent 配置

1. 在已有 Agent 的工具列表添加“等比中心裁切 / center_crop”。
2. `image_url` 设为由模型填写；`images` 留空。
3. `ratio` 使用数字 `0.85`。
4. 生图成功后，由 Agent 将查询工具返回的真实图片 URL 传给 center_crop。无需改成 Workflow 或添加下载节点。
5. 最终展示工具返回的真实 PNG 文件；若平台提供裁切文件 URL，可用该 URL 输出图片。没有 URL 时直接展示附件，不编造链接，不复用原图 URL。

[完整热点生图 Agent 提示词](examples/hotspot-agent-prompt-zh.md)

## 输入和输出

- `image_url`：公开 HTTPS 图片 URL，优先于上传文件；原 URL 查询参数会保留。
- `images`：可选，未传 URL 时使用 1–5 个 Dify 文件对象，兼容原文件版。
- `ratio`：保留宽高比例，范围 0.01–1，默认 0.85。
- 返回裁切后的 PNG 文件和 JSON 尺寸信息。

支持静态 PNG、JPEG、WebP；每张不超过 20 MiB 和 2500 万像素。几何裁切不保证移除图片中的文字或水印。

下载目标及重定向必须为公开地址，TLS 证书校验保持开启。下载和裁切在 Dify 插件环境中执行，图片不发送到外部图片处理服务。详见 [隐私说明](PRIVACY.md)。

## 验证状态

本地 SDK 加载、URL 下载模拟、裁切像素一致性、旧文件输入兼容及下载限制检查通过。云端 Agent 调用及图片展示尚未验证。
