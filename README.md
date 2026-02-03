# TVBox 奈飞工厂源

[![GitHub Stars](https://img.shields.io/github/stars/yourusername/tvbox-netflixgc?style=flat-square)](https://github.com/yourusername/tvbox-netflixgc/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/yourusername/tvbox-netflixgc?style=flat-square)](https://github.com/yourusername/tvbox-netflixgc/network/members)
[![GitHub Issues](https://img.shields.io/github/issues/yourusername/tvbox-netflixgc?style=flat-square)](https://github.com/yourusername/tvbox-netflixgc/issues)

## 简介

本项目提供 **奈飞工厂** (netflixgc.com) 的 TVBox 爬虫源，支持视频搜索、分类浏览、视频详情等功能。通过 GitHub Raw 托管，你可以直接在 TVBox 中配置使用。

**主要特性：**

- 🔍 全功能视频搜索，支持中文关键词
- 📂 完整的分类体系
- 🎬 视频详情获取，包括播放列表
- 🛡️ Cloudflare 防护绕过
- 🚀 GitHub Raw 托管，免服务器部署
- 📱 兼容最新版本 TVBox

## 使用方法

### 方法一：TVBox 一键配置

在 TVBox 中添加以下配置源地址：

```
https://raw.githubusercontent.com/yourusername/tvbox-netflixgc/main/tvbox_source.json
```

**添加步骤：**

1. 打开 TVBox 应用
2. 进入「设置」→「数据源」或「源配置」
3. 点击「添加源」或「新建源」
4. 粘贴上述 URL
5. 确认添加并刷新

### 方法二：手动配置 JSON

如果你需要自定义配置，可以将 `tvbox_source.json` 的内容复制到你的配置中：

```json
{
  "spider": "https://raw.githubusercontent.com/yourusername/tvbox-netflixgc/main/netflixgc_spider.py",
  "wallpaper": "https://bing.img.run/uhd.php",
  "sites": [
    {
      "key": "netflixgc",
      "name": "奈飞工厂",
      "type": 2,
      "api": "https://raw.githubusercontent.com/yourusername/tvbox-netflixgc/main/app.py",
      "searchable": 1,
      "quickSearch": 1,
      "filterable": 0,
      "playerType": 2,
      "timeout": 30
    }
  ],
  "parses": [
    {
      "name": "自动解析",
      "type": 2,
      "url": "Sequence"
    },
    {
      "name": "综合解析",
      "type": 1,
      "url": "https://jx.xmlyapi.com/?url="
    }
  ],
  "lives": [
    {
      "group": "redirect",
      "channels": [
        {
          "name": "redirect",
          "urls": ["proxy://do=live&type=txt&ext="]
        }
      ]
    }
  ],
  "flags": ["youku", "qq", "iqiyi", "xigua", "m1905", "pptv", "wasu", "bilibili"]
}
```

## 自托管部署

如果你想要自己部署爬虫服务（获得更稳定的访问速度），可以按照以下步骤操作：

### 环境要求

- Python 3.8+
- 群晖 NAS 或任意 Linux 服务器
- 至少 512MB 内存
- 至少 1GB 存储空间

### 快速部署（群晖 NAS）

```bash
# 1. SSH 连接到 NAS
ssh admin@your-nas-ip

# 2. 创建工作目录
mkdir -p /volume1/tvbox
cd /volume1/tvbox

# 3. 下载部署文件
git clone https://github.com/yourusername/tvbox-netflixgc.git
cd tvbox-netflixgc

# 4. 创建 Python 虚拟环境
python3 -m venv venv
source venv/bin/activate

# 5. 安装依赖
pip install -r requirements.txt

# 6. 启动服务
bash start.sh

# 7. 验证服务
curl http://localhost:8000/api
```

### 群晖 NAS 套件部署

1. **安装必需套件**（通过套件中心）：
   - Python 3
   - Git Server（可选）

2. **配置启动脚本**：
   - 将文件上传到 `/volume1/tvbox/`
   - 设置执行权限：`chmod +x *.sh`
   - 添加定时任务或使用控制面板的「任务计划」

### 自定义配置

修改 `config.env` 文件：

```bash
# 服务端口
PORT=8000

# 绑定地址（0.0.0.0 表示所有网络接口）
HOST=0.0.0.0

# 日志级别（DEBUG, INFO, WARNING, ERROR）
LOG_LEVEL=INFO

# 缓存时间（秒）
CACHE_DURATION=300

# 请求超时（秒）
REQUEST_TIMEOUT=30

# 重试次数
RETRY_COUNT=3
```

### 使用 Systemd 服务（Linux）

```bash
# 复制服务文件
sudo cp tvbox.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable tvbox
sudo systemctl start tvbox

# 查看状态
sudo systemctl status tvbox

# 查看日志
sudo journalctl -u tvbox -f
```

### 使用 PM2 管理（Node.js 环境）

```bash
# 安装 PM2
npm install -g pm2

# 启动服务
pm2 start "python3 app.py" --name tvbox-netflixgc

# 设置开机自启
pm2 startup
pm2 save
```

## API 文档

### 基础地址

```
https://your-domain.com/api
```

### 接口列表

#### 1. 首页数据

```
GET /?ac=list
GET /?ac=home
```

**响应示例：**

```json
{
  "class": [
    {"type_id": 1, "type_name": "电影"},
    {"type_id": 2, "type_name": "电视剧"},
    {"type_id": 3, "type_name": "综艺"}
  ],
  "list": {
    "首页": [
      {
        "vod_id": 0,
        "vod_name": "鱿鱼游戏",
        "vod_pic": "https://example.com/cover.jpg",
        "vod_remarks": "更新至第9集"
      }
    ]
  }
}
```

#### 2. 视频搜索

```
GET /?ac=search&wd=关键词
GET /?wd=关键词
```

**示例：**

```
/?wd=鱿鱼游戏
/?wd=庆余年
```

**响应示例：**

```json
{
  "list": [
    {
      "vod_id": 0,
      "vod_name": "鱿鱼游戏",
      "vod_pic": "https://example.com/cover.jpg",
      "vod_remarks": "全9集"
    },
    {
      "vod_id": 1,
      "vod_name": "鱿鱼游戏第二季",
      "vod_pic": "https://example.com/cover2.jpg",
      "vod_remarks": "预告"
    }
  ]
}
```

#### 3. 视频详情

```
GET /?ac=detail&url=视频详情页URL
GET /?url=视频详情页URL
```

**示例：**

```
/?url=https://www.netflixgc.com/detail/123.html
```

**响应示例：**

```json
{
  "vod_name": "鱿鱼游戏",
  "vod_pic": "https://example.com/cover.jpg",
  "vod_actor": "李政宰,朴海秀",
  "vod_director": "黄东赫",
  "vod_year": "2021",
  "vod_area": "韩国",
  "vod_type": "剧情/悬疑",
  "vod_content": "一群走投无路的生存游戏参与者...",
  "vod_play_from": "奈飞工厂",
  "vod_play_url": "第1集$$https://example.com/play/1#第2集$$https://example.com/play/2"
}
```

#### 4. 分类列表

```
GET /?ac=category
```

## 配置说明

### TVBox 源配置参数

| 参数 | 必填 | 说明 |
|------|------|------|
| `key` | 是 | 源唯一标识，不可重复 |
| `name` | 是 | 源名称，显示在 TVBox 源列表中 |
| `type` | 是 | 源类型：2 表示爬虫源 |
| `api` | 是 | API 地址（GitHub Raw 或自托管地址） |
| `searchable` | 否 | 是否支持搜索：1 支持，0 不支持 |
| `quickSearch` | 否 | 是否支持快捷搜索：1 支持，0 不支持 |
| `filterable` | 否 | 是否支持筛选：1 支持，0 不支持 |
| `playerType` | 否 | 播放器类型：2 通用，4 投屏 |
| `timeout` | 否 | 请求超时时间（秒） |

### 播放器配置

源文件中包含两种播放器配置：

- **软解码**：适用于不支持硬件解码的设备
- **硬解码**：适用于支持硬件解码的设备（性能更优）

## 常见问题

### Q: 搜索结果显示为空？

**A:** 请检查以下几点：

1. 确认网络连接正常
2. 尝试使用其他关键词（如「鱿鱼游戏」「庆余年」）
3. 如果是自托管版本，查看服务端日志
4. 可能是 Cloudflare 验证导致，暂时等待后重试

### Q: 视频无法播放？

**A:** 可能的原因：

1. 解析器失效，尝试更换其他解析源
2. 视频源服务器维护中
3. 网络连接问题
4. 某些视频需要特定解析器

### Q: GitHub Raw 访问慢？

**A:** 解决方案：

1. 使用自托管部署
2. 切换到其他 GitHub 镜像
3. 使用 CDN 加速服务

### Q: 如何添加更多解析器？

**A:** 在 `tvbox_source.json` 的 `parses` 数组中添加：

```json
{
  "name": "自定义解析",
  "type": 1,
  "url": "https://your-jx-url.com/?url="
}
```

## 更新日志

### v1.0.0 (2024-01-01)

- 初始版本发布
- 实现基础搜索功能
- 支持视频详情获取
- 包含分类浏览功能

## 贡献指南

欢迎提交 Issue 和 Pull Request！

### 提交 Issue

如果你发现了 bug 或有功能建议，请：

1. 搜索是否已有相同问题
2. 如果没有，创建新的 Issue
3. 描述问题或建议
4. 附上相关日志（如有）

### 提交 Pull Request

1. Fork 本仓库
2. 创建你的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交你的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建一个 Pull Request

## 许可证

本项目基于 MIT 许可证开源，详见 [LICENSE](LICENSE) 文件。

## 免责声明

1. 本项目仅供学习和研究使用
2. 请勿将本项目用于商业用途
3. 使用本项目产生的任何法律问题由用户自行承担
4. 视频版权归原作者所有

## 联系方式

- GitHub Issues：[提交问题](https://github.com/yourusername/tvbox-netflixgc/issues)
- 作者邮箱：your-email@example.com

---

**如果对你有帮助，请给个 Star ⭐ 支持一下！**
