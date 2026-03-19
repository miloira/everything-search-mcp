# Everything MCP

基于 [Everything](https://www.voidtools.com/) 搜索引擎的 MCP (Model Context Protocol) 服务器。让你的 AI 助手（如 Claude、Kiro 等）能够快速搜索本地文件。

## 前置要求

- **Windows 系统**（Everything 仅支持 Windows）
- **[Everything](https://www.voidtools.com/)** 已安装并正在运行
- **Python >= 3.12**

## 安装

```bash
pip install everything-search-mcp
```

或使用 `uv`：

```bash
uv pip install everything-search-mcp
```

## MCP 配置

### Claude Desktop

编辑 Claude Desktop 配置文件（通常位于 `%APPDATA%\Claude\claude_desktop_config.json`）：

```json
{
  "mcpServers": {
    "everything": {
      "command": "everything-search-mcp",
      "disabled": false
    }
  }
}
```

如果使用 `uvx` 运行（无需预先安装）：

```json
{
  "mcpServers": {
    "everything": {
      "command": "uvx",
      "args": ["everything-search-mcp"],
      "disabled": false
    }
  }
}
```

### Kiro

在项目根目录或用户目录下创建 `.kiro/settings/mcp.json`：

```json
{
  "mcpServers": {
    "everything": {
      "command": "everything-search-mcp",
      "disabled": false
    }
  }
}
```

使用 `uvx`：

```json
{
  "mcpServers": {
    "everything": {
      "command": "uvx",
      "args": ["everything-search-mcp"],
      "disabled": false
    }
  }
}
```

### Cursor

编辑 `~/.cursor/mcp.json`：

```json
{
  "mcpServers": {
    "everything": {
      "command": "everything-search-mcp",
      "disabled": false
    }
  }
}
```

### OpenCode

编辑项目根目录下的 `opencode.json`（或全局配置）：

```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "everything": {
      "type": "local",
      "command": ["everything-search-mcp"],
      "enabled": true
    }
  }
}
```

使用 `uvx`：

```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "everything": {
      "type": "local",
      "command": ["uvx", "everything-search-mcp"],
      "enabled": true
    }
  }
}
```

### VS Code (Copilot)

在 `.vscode/settings.json` 中添加：

```json
{
  "mcp": {
    "servers": {
      "everything": {
        "command": "everything-search-mcp"
      }
    }
  }
}
```

## 提供的工具

### `get_current_date`

获取当前日期（YYYY-MM-DD 格式），方便在日期筛选时使用。

### `get_everything_info`

获取 Everything 的版本、数据库加载状态和管理员权限信息。

### `search`

基础搜索工具，支持以下参数：

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `query_string` | str | 必填 | 搜索关键词 |
| `match_case` | bool | False | 区分大小写 |
| `match_path` | bool | False | 匹配完整路径 |
| `match_whole_word` | bool | False | 全词匹配 |
| `regex` | bool | False | 启用正则表达式 |
| `sort_type` | int | 1 | 排序方式（见下方说明） |
| `max_results` | int | 10 | 最大返回数量 |
| `return_properties` | list | 默认字段 | 返回的字段列表 |

### `complex_search`

高级组合搜索，通过 `filters` 列表组合多种过滤条件：

- **keywords** — 关键词搜索
- **file_filter** — 按扩展名、大小范围、文件内容过滤
- **date_filter** — 按创建/修改/访问日期范围过滤
- **size_filter** — 按文件大小过滤（支持 kb/mb/gb 单位）
- **media_filter** — 按媒体类型过滤（image/audio/video）
- **document_filter** — 按文档类型过滤（office/pdf/text）

## 使用示例

配置完成后，你可以直接在 AI 对话中使用自然语言搜索文件：

> "帮我找一下桌面上所有的 PDF 文件"

> "搜索最近一周修改过的 Python 文件"

> "找出所有大于 100MB 的视频文件"

> "在 D 盘搜索包含 config 的 yaml 文件"

AI 助手会自动调用对应的 MCP 工具完成搜索。

## 排序类型参考

| 值 | 说明 | 值 | 说明 |
|----|------|----|------|
| 1 | 名称升序 | 2 | 名称降序 |
| 3 | 路径升序 | 4 | 路径降序 |
| 5 | 大小升序 | 6 | 大小降序 |
| 11 | 创建日期升序 | 12 | 创建日期降序 |
| 13 | 修改日期升序 | 14 | 修改日期降序 |

## 开发

```bash
git clone https://github.com/miloira/everything-search-mcp.git
cd everything-search-mcp
uv sync
```

本地测试运行：

```bash
uv run everything-search-mcp
```

## License

MIT
