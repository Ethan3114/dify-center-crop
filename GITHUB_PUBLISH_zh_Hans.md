# GitHub 发布 v0.0.5

源码仓库：https://github.com/Ethan3114/dify-center-crop

1. 确认 manifest、provider 和 tool 的 author 为 ethan3114，manifest 版本为 0.0.5。
2. 运行 `dify plugin package . -o center_crop-0.0.5.difypkg`。
3. 创建 v0.0.5 Release，附上安装包与 SHA-256 文件；发布为正式版本。
4. Dify 从 GitHub 安装时填写仓库根地址，选择 v0.0.5 的 .difypkg。
5. 进入已有自主 Agent，启用 center_crop，让模型填写 image_url，ratio=0.85。详见中文 README 和 examples 中的提示词。

GitHub 发布并不意味着 Marketplace 审核通过或云端 Agent 实测通过。版本查询中转服务限流时，可直接下载 Release 安装包，通过本地集成包安装。
