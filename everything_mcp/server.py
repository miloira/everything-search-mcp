from fastmcp import FastMCP
from everytools import Search, SearchBuilder, SortType
from everytools.query.filters import (
    FileFilter, DateFilter, MediaFilter, DocumentFilter, SizeFilter
)
from everytools.core import get_dll_loader

loader = get_dll_loader()
mcp = FastMCP("everything-mcp")


def _format_ascii_table(title: str, columns: list[str], rows: list[dict]) -> str:
    """将结果格式化为 ASCII 表格。"""
    str_rows = [[str(r.get(c, "")) for c in columns] for r in rows if isinstance(r, dict)]
    col_widths = []
    for i, c in enumerate(columns):
        width = len(c)
        for row in str_rows:
            width = max(width, len(row[i]))
        col_widths.append(width)

    def _row_line(cells):
        return "| " + " | ".join(cell.ljust(col_widths[i]) for i, cell in enumerate(cells)) + " |"

    separator = "+-" + "-+-".join("-" * w for w in col_widths) + "-+"
    lines = [title, separator, _row_line(columns), separator]
    for row in str_rows:
        lines.append(_row_line(row))
    lines.append(separator)
    return "\n".join(lines)


@mcp.tool()
def get_current_date() -> str:
    """获取当前日期，格式为 YYYY-MM-DD，可用于日期筛选。"""
    from datetime import date
    return date.today().isoformat()


@mcp.tool()
def get_everything_info() -> dict:
    """获取 Everything 工具信息。"""
    return {
        "version": loader.version,
        "is_db_loaded": loader.is_db_loaded(),
        "is_admin": loader.is_admin()
    }


@mcp.tool()
def search(
        query_string: str,
        match_case: bool = False,
        match_path: bool = False,
        match_whole_word: bool = False,
        regex: bool = False,
        sort_type: int = 1,
        max_results: int = 10,
        return_properties: list[str] = None
) -> str:
    """使用 Everything 搜索文件。

    Args:
        query_string: 搜索关键词。
        match_case: 是否区分大小写，默认 False。
        match_path: 是否匹配完整路径，默认 False。
        match_whole_word: 是否全词匹配，默认 False。
        regex: 是否启用正则表达式，默认 False。
        sort_type: 排序类型，默认 1 (名称升序)。可选值:
            1=名称升序, 2=名称降序,
            3=路径升序, 4=路径降序,
            5=大小升序, 6=大小降序,
            7=扩展名升序, 8=扩展名降序,
            9=类型名称升序, 10=类型名称降序,
            11=创建日期升序, 12=创建日期降序,
            13=修改日期升序, 14=修改日期降序,
            15=属性升序, 16=属性降序,
            17=文件列表文件名升序, 18=文件列表文件名降序,
            19=运行次数升序, 20=运行次数降序,
            21=最近更改日期升序, 22=最近更改日期降序,
            23=访问日期升序, 24=访问日期降序,
            25=运行日期升序, 26=运行日期降序。
        max_results: 最大返回结果数，默认 10。
        return_properties: 控制返回的字段列表，可选值:
            name=文件名, path=文件路径, full_path=完整路径（包含文件名）,
            size=文件大小（字节）, date_created=创建日期, date_modified=修改日期,
            date_accessed=访问日期, date_run=运行日期, extension=文件扩展名,
            attributes=文件属性, is_file=是否为文件, is_folder=是否为文件夹,
            is_volume=是否为卷, run_count=运行次数,
            highlighted_name=高亮显示的文件名, highlighted_path=高亮显示的路径。
            默认返回常用字段。

    Returns:
        表格格式的搜索结果字符串。
    """
    return_properties = return_properties or [
        "full_path",
        "size",
        "date_created"
    ]
    sort_type_enum = SortType(sort_type)
    engine = Search(
        query_string=query_string,
        match_case=match_case,
        match_path=match_path,
        match_whole_word=match_whole_word,
        regex=regex,
        sort_type=sort_type_enum,
        max_results=max_results
    )
    engine.execute()
    result_set = engine.get_results()
    results = []
    for item in result_set:
        d = vars(item) if hasattr(item, '__dict__') else item
        if isinstance(d, dict):
            results.append({k: d[k] for k in return_properties if k in d})
        else:
            results.append(d)
    total = result_set.total_results
    total_files = result_set.total_files
    total_folders = result_set.total_folders
    dict_rows = [r for r in results if isinstance(r, dict)]
    title = f"搜索结果: {query_string} (返回 {len(dict_rows)} 条, 总计 {total} 条, 文件 {total_files}, 文件夹 {total_folders})"
    return _format_ascii_table(title, return_properties, dict_rows)


@mcp.tool()
def complex_search(
        keywords: list[str] = None,
        filters: list[dict] = None,
        match_case: bool = False,
        match_path: bool = False,
        match_whole_word: bool = False,
        regex: bool = False,
        sort_type: int = 1,
        max_results: int = 10,
        return_properties: list[str] = None
) -> str:
    """使用 Everything 进行复杂组合搜索。

    通过 keywords 指定搜索关键词，通过 filters 列表组合多种过滤条件。

    Args:
        keywords: 搜索关键词列表，如 ["test.py", "hello"]。
        filters: 过滤器列表，每个过滤器是一个 dict，包含 type 和 params。支持的类型:
            - file_filter: 文件属性过滤。params 为 dict，可选键:
                - with_extensions: 扩展名列表，如 [".py", ".txt"]
                - with_size_range: {"min_size": 字节数, "max_size": 字节数}
                - with_content: 文件内容关键词（仅文本文件）
                - duplicates_only: 是否仅显示重复文件 (bool)
            - date_filter: 日期过滤。params 为 dict:
                - by_date: "modified_date" 或 "created_date" 或 "accessed_date"
                - in_range: [开始日期, 结束日期]，格式 "YYYY-MM-DD"
            - size_filter: 大小过滤。params 为 dict，可选键:
                - gt: 最小字节数
                - lt: 最大字节数
            - media_filter: 媒体文件过滤。params 为 dict:
                - file_type: "image"/"audio"/"video"/"all"
            - document_filter: 文档文件过滤。params 为 dict:
                - file_type: "office"/"pdf"/"text"/"all"
        match_case: 是否区分大小写，默认 False。
        match_path: 是否匹配完整路径，默认 False。
        match_whole_word: 是否全词匹配，默认 False。
        regex: 是否启用正则表达式，默认 False。
        sort_type: 排序类型，默认 1 (名称升序)。可选值同 search 工具。
        max_results: 最大返回结果数，默认 10。
        return_properties: 返回字段列表，可选值同 search 工具。默认返回常用字段。

    Returns:
        ASCII 表格格式的搜索结果字符串。
    """
    keywords = keywords or []
    filters = filters or []
    return_properties = return_properties or [
        "name", "path", "full_path", "is_file", "is_folder", "is_volume",
        "extension", "size", "date_created", "date_modified", "date_accessed", "date_run"
    ]

    builder = SearchBuilder()
    if keywords:
        builder.keywords(*keywords)
    builder.match_case(match_case)
    builder.match_path(match_path)
    builder.match_whole_word(match_whole_word)
    builder.use_regex(regex)
    builder.sort_by(SortType(sort_type))
    builder.limit(max_results)

    for f in filters:
        f_type = f.get("type")
        params = f.get("params")

        if f_type == "file_filter":
            ff = FileFilter()
            if "with_extensions" in params:
                ff.with_extensions(*params["with_extensions"])
            if "with_size_range" in params:
                sr = params["with_size_range"]
                ff.with_size_range(sr.get("min_size"), sr.get("max_size"))
            if "with_content" in params:
                ff.with_content(params["with_content"])
            if params.get("duplicates_only"):
                ff.duplicates_only()
            builder.filter(ff)

        elif f_type == "date_filter":
            df = DateFilter()
            by_date = params.get("by_date", "modified_date")
            if by_date == "created_date":
                df.by_created_date()
            elif by_date == "accessed_date":
                df.by_accessed_date()
            else:
                df.by_modified_date()
            date_range = params.get("in_range")
            if date_range and len(date_range) == 2:
                df.in_range(date_range[0], date_range[1])
            builder.filter(df)

        elif f_type == "size_filter":
            sf = SizeFilter()
            min_bytes = params.get("gt")
            max_bytes = params.get("lt")
            if min_bytes is not None and max_bytes is not None:
                sf.between(min_bytes, max_bytes)
            elif min_bytes is not None:
                sf.larger_than(min_bytes)
            elif max_bytes is not None:
                sf.smaller_than(max_bytes)
            builder.filter(sf)

        elif f_type == "media_filter":
            mf = MediaFilter(params.get("file_type", "all"))
            builder.filter(mf)

        elif f_type == "document_filter":
            doc_f = DocumentFilter(params.get("file_type", "all"))
            builder.filter(doc_f)

    search_obj = builder.execute()
    result_set = search_obj.get_results()
    results = []
    for item in result_set:
        d = vars(item) if hasattr(item, '__dict__') else item
        if isinstance(d, dict):
            results.append({k: d[k] for k in return_properties if k in d})
        else:
            results.append(d)

    total = result_set.total_results
    total_files = result_set.total_files
    total_folders = result_set.total_folders
    dict_rows = [r for r in results if isinstance(r, dict)]
    query_str = builder.build_query_string()
    title = f"复杂搜索结果: {query_str} (返回 {len(dict_rows)} 条, 总计 {total} 条, 文件 {total_files}, 文件夹 {total_folders})"
    return _format_ascii_table(title, return_properties, dict_rows)
