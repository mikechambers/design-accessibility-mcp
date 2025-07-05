import context_augment
from openai import OpenAI;
from dotenv import load_dotenv
from pydantic import BaseModel
import context_augment.core as context_augment
import base64
import sys, os


#sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

load_dotenv()

MODEL = "gpt-4.1"
openai = OpenAI()

instructions_template = None
context_data = None

def init(cache_name:str):
    global instructions_template, context_data

    script_dir = os.path.dirname(os.path.abspath(__file__))
    cache_abs_path = os.path.join(script_dir, cache_name)

    instructions_template = load_instructions()
    context_data = load_context_data(cache_abs_path)

def load_instructions() -> str:

    script_dir = os.path.dirname(os.path.abspath(__file__))
    instructions_path = os.path.join(script_dir, 'instructions.md')

    with open(instructions_path, 'r') as file:
        instructions = file.read()
        return instructions

def load_context_data(cache_path:str):
    data = context_augment.load_cached_embeddings(cache_path)
    return data

async def create_image_reference(path:str):
  with open(path, "rb") as file_content:
    result = openai.files.create(
        file=file_content,
        purpose="vision",
    )
    return result.id

def build_instructions(user_query:str) -> str:

    relevant_chunks = context_augment.retrieve_relevant_chunks(context_data, user_query, k=3)
    context = "\n\n".join(relevant_chunks)

    result = instructions_template.format(user_instructions=user_query, context=context)
    return result


def generate_response(response:str, image_id:str = None) -> dict:

    out = {"response":response}

    if image_id:
        out["image_id"] = image_id

    return out

def write_base64_file(base64data:str, file_path:str):
    with open(file_path, "wb") as f:
        f.write(base64.b64decode(base64data))

async def review_and_edit_image(user_query: str, file_path:str) -> dict:
    response = await review_image(user_query, file_path)

    input = f"Edit this image to incorporate the following accessibility feedback and suggestions:\n**Feedback & Suggestions**\n{response['response']}"

    editResponse = openai.responses.create(
        model="gpt-4.1-mini",
        input=[{
            "role": "user",
            "content": [
                {"type": "input_text", "text": input},
                {
                    "type": "input_image",
                    "file_id": response["image_id"],
                },
            ],
        }],
        tools=[{
            "type": "image_generation", 
            #"quality":"medium",
            "output_format":"jpeg",
            "output_compression":90
        }],
    )

    image_data = [
        output.result
        for output in editResponse.output
        if output.type == "image_generation_call"
    ]

    image_base64 = None
    if image_data:
        image_base64 = image_data[0]
        #write_base64_file(image_base64, "output_2.jpg")

    return {
        "response":response,
        "image": {
            "data":image_base64,
            "type":"image/jpeg"
        }
    }


async def review_image(user_query: str, file_path: str) -> dict:

    image_id = await create_image_reference(file_path)

    user_query = f"{user_query}\n Analyze the attached design for accessibility."
    input = build_instructions(user_query)

    response = openai.responses.create(
        model=MODEL,
        input=[{
            "role": "user",
            "content": [
                {"type": "input_text", "text": user_query},
                {
                    "type": "input_image",
                    "file_id": image_id,
                },
            ],
        }],
    )

    return generate_response(response.output_text, image_id)


async def design_accessibility_query(user_query:str) -> dict:

    input = build_instructions(user_query)

    response = openai.responses.create(
        model = MODEL,
        input=input
    )

    return generate_response(response.output_text, input)


class GuardrailResponse(BaseModel):
    is_related: bool
    reason: str
    confidence: float

async def check_is_on_topic(prompt:str) -> bool:
    response = openai.responses.parse(
        model="gpt-4.1-nano",
        input=[
            {"role":"system", "content":"Determine whether the user input is related to design accessibility topics. If asked to review an image or design, assume its its asking for a review for accessibility."},
            {"role":"user", "content": prompt}
        ],
        text_format=GuardrailResponse,
    )

    return response.output_parsed.is_related