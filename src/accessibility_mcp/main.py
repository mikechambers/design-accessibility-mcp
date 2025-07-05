import sys, os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from shared.consts import CACHE_FILE_NAME
import asyncio
import accessibility_mcp.core as core



async def async_main():
    if len(sys.argv) < 2:
        print("Usage: python main.py '<your question>'")
        return

    user_query = sys.argv[1]

    core.init(CACHE_FILE_NAME)

    out = await core.check_is_on_topic(user_query)
    if not out:
        print("off topic")
        return
    
    print(out)

def main():
    """Sync wrapper for console script"""
    asyncio.run(async_main())

if __name__ == "__main__":
    main()