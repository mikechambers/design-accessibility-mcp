from fastmcp import FastMCP
from fastmcp.utilities.types import Image
import os
import sys
import base64
import design_accessibility_mcp.core as core

#sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

CACHE_FILE_NAME = "accessibility_vector_cache.pkl"

mcp_name = "Design Accessibility MCP"
mcp = FastMCP(
    name=mcp_name,
    log_level="ERROR",
    instructions="""
        This server provides design accessibility analysis tools.
        For any queries related to design accessibility, including:
        - Color contrast checking
        - Accessibility compliance reviews
        - WCAG guideline questions
        - Inclusive design recommendations
        - Accessibility best practices
        - Image accessibility analysis
        - Design accessibility audits
        
        Use the appropriate accessibility functions to provide expert guidance and analysis.
    """,
)

print(f"{mcp_name} running on stdio", file=sys.stderr)

core.init(CACHE_FILE_NAME)

def check_guardrails(user_query:str):

    is_on_topic = core.check_is_on_topic(user_query)

    if not is_on_topic:  # Should use the variable name, not the function name
        raise Exception("Off-topic query detected:  Request is not related to design accessibility. Query must relate to making designs more accessible or evaluating accessibility compliance.")



@mcp.tool()
async def review_image(user_query: str, file_path: str):
    """
    Analyzes an image for accessibility compliance and design issues.
    
    Evaluates images against accessibility standards including contrast ratios,
    color usage, text readability, and visual design principles. Provides
    specific recommendations for improving accessibility compliance.
    
    Args:
        user_query (str): Specific accessibility question or area of focus 
                         (e.g., "Check contrast ratios", "Evaluate for color blindness",
                         "Review text readability", "General accessibility audit")
        file_path (str): Path to the image file to analyze
                        Supported formats: .jpg, .jpeg, .png
    """
    check_guardrails(user_query)
    
    out = await core.review_image(user_query, file_path)

    return out


@mcp.tool()
async def review_and_edit_image(user_query: str, file_path: str):
    """
    Analyzes an image for accessibility compliance and design issues.
    
    Performs comprehensive design accessibility evaluation,
    then generates an enhanced version of the image with accessibility improvements
    applied. Returns both detailed analysis and a visually improved image.
    
    Args:
        user_query (str): Specific accessibility question or area of focus 
                         (e.g., "Check contrast ratios", "Evaluate for color blindness",
                         "Review text readability", "General accessibility audit")
        file_path (str): Path to the image file to analyze
    """
    check_guardrails(user_query)

    response = await core.review_and_edit_image(user_query, file_path)

    data = response["image"]["data"]

    #core.write_base64_file(data, "/Users/mesh/tmp/output.jpg")
    image_bytes = base64.b64decode(data)

    image = Image(data=image_bytes, format="jpeg")

    return [response["response"], image]


@mcp.tool()
async def accessibility_query(user_query: str):
    """
    Provides expert guidance on accessibility best practices and standards.
    
    Comprehensive knowledge base covering WCAG guidelines, inclusive design principles,
    assistive technology compatibility, and practical implementation strategies.
    Answers both general questions and specific technical queries about accessibility.
    
    Args:
        user_query (str): Accessibility question or topic to address
                         (e.g., "What are WCAG AA requirements for buttons?",
                         "How to make forms accessible to screen readers?",
                         "Best practices for mobile accessibility",
                         "Color palette recommendations for accessibility")
    """
    check_guardrails(user_query)

    out = await core.design_accessibility_query(user_query)

    return out

if __name__ == "__main__":
    mcp.run()
