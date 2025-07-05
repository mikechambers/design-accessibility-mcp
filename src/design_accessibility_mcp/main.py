import sys, os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
import asyncio
import design_accessibility_mcp.core as core

CACHE_FILE_NAME = "accessibility_vector_cache.pkl"

async def async_main():
    if len(sys.argv) < 2:
        print("Usage: design-accessibility-test '<your question>'")
        return

    user_query = sys.argv[1]

    core.init(CACHE_FILE_NAME)

    out = await core.check_is_on_topic(user_query)
    if not out:
        print("off topic")
        return
    
    #out = await core.review_and_edit_image("review this design for accessibility issues and create a new edit with your suggested changes", "/Users/mesh/Desktop/mcpfiles/photoshop/psd-contrast/alpine_adventures_org.png")

    out = await core.design_accessibility_query(user_query)

    #data = out["image"]["data"]
    #core.write_base64_file(data, "output.jpg")

    
    
    print(out)

def main():
    """Sync wrapper for console script"""
    asyncio.run(async_main())

if __name__ == "__main__":
    main()