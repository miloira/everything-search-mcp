# Everything MCP

基于 [Everything](https://www.voidtools.com/) 搜索引擎的 MCP (Model Context Protocol) 服务器。让你的 AI 助手（如 Claude、Kiro 等）能够快速搜索本地文件。

## 前置要求

- **Windows 系统**（Everything 仅支持 Windows）
- **[Everything](https://www.voidtools.com/)** 已安装并正在运行
- **[uv](https://docs.astral.sh/uv/getting-started/installation/)** 已安装（提供 `uvx` 命令）

## MCP 配置

### Claude Desktop

编辑 Claude Desktop 配置文件（通常位于 `%APPDATA%\Claude\claude_desktop_config.json`）：

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
      "command": "uvx",
      "args": ["everything-search-mcp"],
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
        "command": "uvx",
        "args": ["everything-search-mcp"]
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

高级组合搜索，通过 `filters` 列表组合多种过滤条件。

基础参数：

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `keywords` | list[str] | `[]` | 搜索关键词列表，如 `["test.py", "hello"]` |
| `filters` | list[dict] | `[]` | 过滤器列表，详见下方 |
| `match_case` | bool | False | 区分大小写 |
| `match_path` | bool | False | 匹配完整路径 |
| `match_whole_word` | bool | False | 全词匹配 |
| `regex` | bool | False | 启用正则表达式 |
| `sort_type` | int | 1 | 排序方式（见排序类型参考） |
| `max_results` | int | 10 | 最大返回数量 |
| `return_properties` | list[str] | 默认字段 | 返回的字段列表 |

每个 filter 是一个 `{"type": "...", "params": ...}` 结构，支持以下类型：

#### file_filter — 文件属性过滤

| params 键 | 类型 | 说明 |
|-----------|------|------|
| `with_extensions` | list[str] | 扩展名列表，如 `[".py", ".txt"]` |
| `with_size_range` | dict | `{"min_size": 字节数, "max_size": 字节数}` |
| `with_content` | str | 文件内容关键词（仅文本文件） |
| `duplicates_only` | bool | 是否仅显示重复文件 |

```json
{"type": "file_filter", "params": {"with_extensions": [".py"], "with_content": "import"}}
```

#### date_filter — 日期过滤

| params 键 | 类型 | 说明 |
|-----------|------|------|
| `by_date` | str | `"modified_date"` / `"created_date"` / `"accessed_date"` |
| `in_range` | list[str] | `["开始日期", "结束日期"]`，格式 `YYYY-MM-DD` |

```json
{"type": "date_filter", "params": {"by_date": "modified_date", "in_range": ["2025-01-01", "2025-12-31"]}}
```

#### size_filter — 大小过滤

通过 `gt`（大于）和 `lt`（小于）设置范围，单位为字节。

| params 键 | 类型 | 说明 |
|-----------|------|------|
| `gt` | int | 最小字节数 |
| `lt` | int | 最大字节数 |

```json
{"type": "size_filter", "params": {"gt": 104857600}}
```

#### media_filter — 媒体文件过滤

| params 键 | 类型 | 可选值 |
|-----------|------|--------|
| `file_type` | str | `"image"` / `"audio"` / `"video"` / `"all"` |

```json
{"type": "media_filter", "params": {"file_type": "video"}}
```

#### document_filter — 文档文件过滤

| params 键 | 类型 | 可选值 |
|-----------|------|--------|
| `file_type` | str | `"office"` / `"pdf"` / `"text"` / `"all"` |

```json
{"type": "document_filter", "params": {"file_type": "pdf"}}
```

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
| 7 | 扩展名升序 | 8 | 扩展名降序 |
| 9 | 类型名称升序 | 10 | 类型名称降序 |
| 11 | 创建日期升序 | 12 | 创建日期降序 |
| 13 | 修改日期升序 | 14 | 修改日期降序 |
| 15 | 属性升序 | 16 | 属性降序 |
| 17 | 文件列表文件名升序 | 18 | 文件列表文件名降序 |
| 19 | 运行次数升序 | 20 | 运行次数降序 |
| 21 | 最近更改日期升序 | 22 | 最近更改日期降序 |
| 23 | 访问日期升序 | 24 | 访问日期降序 |
| 25 | 运行日期升序 | 26 | 运行日期降序 |

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