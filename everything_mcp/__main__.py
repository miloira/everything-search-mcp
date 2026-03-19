"""允许通过 python -m everything_mcp 启动服务器。"""
from everything_mcp.server import mcp


def main():
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
