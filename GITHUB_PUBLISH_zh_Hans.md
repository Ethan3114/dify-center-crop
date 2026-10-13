# 按 Dify 官网发布到 GitHub，并验证云端 Agent

核对日期：2026-10-13。

## 官方流程

Dify 支持从个人 GitHub 仓库安装插件，无需先完成 Marketplace 审核。安装器从 GitHub Release 的附件中读取 `.difypkg`，不是从源码目录临时编译插件。

1. 公开仓库为 `https://github.com/Ethan3114/dify-center-crop`。当前包的作者为仓库所属用户 `Ethan3114`。
2. 将本目录的源码放在仓库根目录。包含 manifest、main、provider、tools、crop_image、requirements、pyproject、图标、README 和隐私说明。不要上传原始用户图片、`.env`、调试密钥、虚拟环境或缓存。本目录已提供 `.gitignore`。
3. `manifest.yaml`、`provider/center_crop.yaml` 和 `tools/center_crop.yaml` 的 `author` 均为 `Ethan3114`。如果更换仓库所属用户，同步修改并重新打包，不能继续使用旧 `.difypkg`。
4. 在仓库页面选择「Releases → Draft a new release」，创建标签 `v0.0.2`，对应 manifest 版本 `0.0.2`。
5. 将 `center_crop-0.0.2.difypkg` 上传到该 Release 的 **Assets**，不要只依赖 GitHub 自动生成的 Source code.zip/tar.gz。把 `RELEASE_NOTES.md` 的内容填入说明，然后正式发布 Release。草稿发布不能作为最终验收。
6. 进入 Dify 云端「插件 → 安装插件 → 通过 GitHub 安装」，输入你的实际仓库 URL，选择 `v0.0.2` 及其 `.difypkg` 附件，查看信息后安装。

### 本地 Git 命令

如需将本地源码推送到该仓库，在源码目录执行以下命令。已有远程提交时应先克隆仓库并修改后推送，避免覆盖远程历史。

```sh
git init
git add .
git commit -m "Prepare Center Crop v0.0.2"
git branch -M main
git remote add origin https://github.com/Ethan3114/dify-center-crop.git
git push -u origin main
```

公开推送会公开本目录源码，用户图片不在源码包内。

### 重新打包

在项目目录的上一层运行：

```sh
dify plugin package ./center-crop-plugin -o center_crop-0.0.2.difypkg
```

之后每次更新都要先增加 manifest 和 pyproject 中的项目版本，再重新打包、创建对应标签和 Release、上传新包。不要覆盖旧版本而继续沿用同一个标签。

## 什么才算“云端 Dify 能用”

发布和打包检查只能证明格式与发布入口符合要求。以下云端实测全部通过，才可以确认本插件在该工作空间的所选 Agent 中可用：

1. Dify 的 GitHub 安装弹窗能列出 `v0.0.2` 和包文件，且安装完成后插件显示正常。
2. 新建测试 Chatflow，启用图片上传，在 Agent 节点添加「等比中心裁切」。`images` 绑定 `sys.files`，`ratio` 设为手动固定 `0.85`。
3. 上传最初的 1024×1024 原图，输入「将这张图四边向内裁切，保留中央宽高各 85%」。确认运行记录里确实发生工具调用。
4. 检查工具返回 PNG 文件和 870×870 的尺寸 JSON。下载 PNG，核对尺寸；底部应裁到原图「AI生成」文字上方，四周没有新留边。
5. 在回答节点绑定 Agent 的图片/文件输出，确认用户能够看到或下载结果。文件是否正常显示需要所选 Agent 策略的实际运行证明；本地 SDK 的 BLOB 消息验证不能代替这一步。
6. 再上传一张不同尺寸的图片，核对保留宽高各 85% 的输出尺寸，以排除只对固定原图有效。

## 签名与安装失败

官网说明 GitHub 是无需 Marketplace 审核的分发方式，但这不等于已经取得 Marketplace 官方签名。Dify Cloud 集中管理签名，用户不能自行添加受信任公钥或调整社区版的验证环境变量。不要把自部署的签名配置教程用到云端。

本包未签名，尚未在你的云端工作空间安装。若 GitHub 安装遇到签名或策略错误，记录原始报错并按云端支持渠道确认允许的安装路径；必要时走官方 Marketplace 审核与签名流程。仅把未签名包放到 GitHub，不能证明或改变云端的签名接受策略。

## 验证范围

本地验证包括：三个 YAML 作者字段一致、Python 3.12 和真实 SDK 配置加载与工具调用、实际附件的裁切结果、官方 CLI 打包。

本地和 GitHub 发布检查不能代替 Dify 云端安装、Agent 端到端测试或 Marketplace 审核。官方打包指南也要求在 Dify 实例远程调试后再发布；本包目前只有本地 SDK 验证，尚未完成云端远程调试。

## 官方来源

- [发布到个人 GitHub 仓库](https://docs.dify.ai/en/develop-plugin/publishing/marketplace-listing/release-to-individual-github-repo)：公开仓库、作者匹配、Release 版本和 `.difypkg` 附件、通过 GitHub 安装。
- [本地文件打包与分享](https://docs.dify.ai/en/develop-plugin/publishing/marketplace-listing/release-by-file)：打包前先远程调试。
- [第三方签名验证](https://docs.dify.ai/en/develop-plugin/publishing/standards/third-party-signature-verification)：云端签名由平台集中管理，不提供社区版的验证控制。
- [工具插件开发](https://docs.dify.ai/en/develop-plugin/dev-guides-and-walkthroughs/tool-plugin)：插件结构和远程调试流程。
