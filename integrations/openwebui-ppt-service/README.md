# OpenWebUI PPT Service

这是给 `ppt-master` 配的一层独立后端，目标是：

- 本地先单独测试 `上传/提交 -> 生成 -> 下载`
- 服务器上独立部署，不改你现有的 OpenWebUI 主程序
- 通过 `openwebui_pipe/ppt_master_pipe.py` 作为 OpenWebUI 里的一个外部模型入口

## 目录说明

- `app/`：FastAPI API、任务存储、执行器、Worker
- `openwebui_pipe/`：导入 OpenWebUI 的 Pipe 文件
- `scripts/`：本地启动脚本
- `deployment/`：`systemd` 和 `nginx` 示例
- `storage/`：任务、日志、导出文件

此外还带一个浏览器管理页：

- `GET /admin`
- 可填写 `LLM Base URL / API Key / 默认模型`
- 可从 OpenAI 兼容接口拉取模型列表
- 保存后写入 `storage/runtime_config.json`

## 工作方式

这套服务分成两部分：

- `ppt-api`：负责接收任务、提供状态查询和下载
- `ppt-worker`：严格串行执行 `ppt-master` 工作流

执行顺序是：

1. 创建项目
2. 导入或转换源文件
3. 调用大模型产出设计规划
4. 顺序生成每一页 SVG
5. 生成讲稿
6. 顺序执行：
   - `total_md_split.py`
   - `finalize_svg.py`
   - `svg_to_pptx.py -s final`

## 本地测试

### 1. 安装依赖

```bash
cd /Users/thanksjing/develope/开源项目/ppt-master/integrations/openwebui-ppt-service
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -r /Users/thanksjing/develope/开源项目/ppt-master/requirements.txt
```

### 2. 配置环境变量

```bash
cp .env.example .env
```

最关键的是这几个：

- `PPT_MASTER_REPO_ROOT`
- `LLM_BASE_URL`
- `LLM_API_KEY`
- `LLM_MODEL`
- `SERVICE_API_KEY`
- `PUBLIC_BASE_URL`

### 3. 启动 API

```bash
./scripts/dev_start.sh
```

### 4. 启动 Worker

新开一个终端：

```bash
cd /Users/thanksjing/develope/开源项目/ppt-master/integrations/openwebui-ppt-service
source .venv/bin/activate
export PYTHONPATH=$PWD
python -m app_worker
```

### 5. 提交一个测试任务

文本输入：

```bash
curl -X POST http://127.0.0.1:8099/api/jobs/json \
  -H "Content-Type: application/json" \
  -H "X-API-Key: change-me" \
  -d '{
    "project_name": "demo_report",
    "source_text": "# Q3 经营复盘\n\n- 收入同比增长 18%\n- 华东区贡献主要增量\n- 新客成本上升，复购改善\n",
    "canvas_format": "ppt169",
    "page_count": 6,
    "style_objective": "general_consulting"
  }'
```

文件上传：

```bash
curl -X POST http://127.0.0.1:8099/api/jobs \
  -H "X-API-Key: change-me" \
  -F "project_name=demo_pdf" \
  -F "canvas_format=ppt169" \
  -F "page_count=8" \
  -F "style_objective=general_consulting" \
  -F "file=@/absolute/path/to/demo.pdf"
```

查询状态：

```bash
curl -H "X-API-Key: change-me" http://127.0.0.1:8099/api/jobs/<job_id>
curl -H "X-API-Key: change-me" http://127.0.0.1:8099/api/jobs/<job_id>/logs
```

下载结果：

```bash
curl -L -H "X-API-Key: change-me" \
  http://127.0.0.1:8099/api/jobs/<job_id>/download/native \
  -o result.pptx
```

## 服务器部署

你现有的 OpenWebUI 保持不动。这个服务单独部署即可。

### 1. 准备目录

把整个仓库放到服务器，例如：

```bash
/opt/ppt-master
```

### 2. 进入集成目录

```bash
cd /opt/ppt-master/integrations/openwebui-ppt-service
cp .env.example .env
```

### 3. 修改 `.env`

至少改这些：

- `SERVICE_API_KEY=你自己的密钥`
- `PUBLIC_BASE_URL=https://你的域名`
- `PPT_MASTER_REPO_ROOT=/opt/ppt-master`
- `LLM_BASE_URL=你的 OpenAI 兼容地址`
- `LLM_API_KEY=你的模型密钥`
- `LLM_MODEL=你要跑 PPT 的模型`

### 4. 启动 Docker Compose

```bash
docker compose up -d --build
```

### 5. 验证

```bash
curl http://127.0.0.1:8099/healthz
```

### 6. 反向代理

可参考：

- `deployment/nginx/ppt-master.conf`

### 7. 打开管理页

部署完成后可以直接访问：

```text
https://你的域名/admin
```

页面里可以直接：

- 配模型地址
- 配 API Key
- 拉取模型列表
- 点选模型回填
- 保存配置

## 接入 OpenWebUI

这套方案不会替代你的 OpenWebUI。

你仍然：

- 在原来的 OpenWebUI 登录
- 在原来的 OpenWebUI 里加 API 模型
- 在原来的 OpenWebUI 里聊天

只是额外导入一个 Pipe，让 OpenWebUI 能把“生成 PPT”这件事转交给本服务。

### 导入步骤

1. 打开 OpenWebUI 后台
2. 进入 `Functions`
3. 选择导入文件
4. 导入 `openwebui_pipe/ppt_master_pipe.py`
5. 在 Pipe 的 Valves 里配置：
   - `service_url`
   - `service_api_key`
   - `canvas_format`
   - `page_count`
   - `style_objective`

### 使用方式

在 OpenWebUI 里选择 `PPT Master Service` 这个模型，然后直接输入你的源材料或 PPT 要求。

当前 Pipe 默认优先支持：

- 粘贴文本
- 粘贴 Markdown
- 粘贴 URL

文件上传这块，这个服务本身已经支持，但不同版本 OpenWebUI 对 Pipe 透传附件的行为不完全一致。所以部署初期建议：

- OpenWebUI 内先用文本 / Markdown / URL
- PDF / DOCX 上传先直接打本服务 API

如果你后面确认你那台 OpenWebUI 的 Pipe 附件字段结构，我可以再把上传透传补进去。

## 重要说明

这是一版“可部署、可验证、可继续迭代”的服务骨架，重点是先把链路打通：

- OpenWebUI -> Pipe -> PPT Service -> ppt-master -> PPTX

当前默认假设：

- 只跑一个 Worker
- 严格串行执行任务
- 使用一个 OpenAI 兼容模型作为生成引擎
- 产出目录保存在 `storage/`

如果你下一步要我继续，我建议继续补两块：

1. 更强的 OpenWebUI 文件上传透传
2. 更细的“八项确认”多轮交互
