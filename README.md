# 🚩 博客下载助手(CTFer)

![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)
![Target](https://img.shields.io/badge/target-CTF_Knowledge_Base-orange.svg)
![Playwright](https://img.shields.io/badge/powered%20by-Playwright-008080.svg)

**博客下载助手(CTFer)** 是一款专为 CTFer 打造(不仅限于CTFer)的线下赛本地知识库构建工具。它可以快速将先知社区、博客园、CSDN 上的高质量 Writeup、漏洞分析和工具脚本转换为 Markdown 文档，方便在无网环境下通过 Obsidian 或 Typora 等笔记软件进行检索与查阅。

[本项目灵感来自于学长[YZBRH (BR)](https://github.com/YZBRH)的博客下载助手，对其进行了浏览器的脱离]



## 🎯 为什么需要它？

在 AWD、AWDP 或传统的解题赛中，线下环境通常断网或网络极差，如果什么知识点忘了还不能在线搜。
- **离线查阅**：一键同步先知社区、CSDN 、博客园等的深度分析文章。
- **纯净阅读**：自动剔除网页广告福利、评论区、右侧工具栏，只保留核心 Payload 和解析。



## ✨ 特性

- **先知社区专项优化**：
  - **精准定位**：根据前端代码，强制锁定 `.left_container` 核心正文，过滤干扰。
  - **极致去杂(可能还有bug)**：自动清理 `#news_toolbar` (作者信息/浏览量) 和 `.detail_share` (分享/评论)。
- **验证码友好处理**：
  - 下载博客园文章时，程序会自动弹出窗口，方便你在批量下载时快速手动处理滑块验证。
  - 下载先知社区和 CSDN 时使用 **Headless 模式**。
- **可选择本地浏览器**：即可使用**playwright install chromium**，也可自由选择下载浏览器



## ❗目前存在的问题

- **UI界面不够友好**：客户端界面不能很好的突出主题，没做到真正的新手友好。
- **下载的.md文件排版不够美观**：尽管CSDN、博客园的部分文章能很好渲染，但先知社区的文章图片不能很好的渲染，排版接近于原始代码。
- **反应速度较慢**：自动化爬取使得必须模拟人类阅读，拉取页面响应速度被拉下来了。



## 🛠️ 快速部署

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2.启动！

```bash
终端运行：python main.py
```



## 📦 项目清单

- `scraper.py`: 负责各平台搜索接口实现。
- `downloader.py`: 渲染、去杂及 Markdown 转换。
- `gui.py`: 实现简洁的UI界面
- `main.py`: 项目入口
- `requirements.txt`: 所需下载依赖环境。



## 🤝 贡献与反馈

如果你在使用过程中发现新的去杂需求或 Bug，欢迎提交 Issue。



## 📄 许可说明

本项目遵循 MIT 开源协议，仅供技术交流与学习使用，请勿用于大规模商业爬取，并尊重各平台的 Robots 协议；仅限用于个人本地知识库构建。在比赛中请遵守赛制规则，尊重原创内容版权。