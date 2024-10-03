from llama_index.core.tools.tool_spec.base import BaseToolSpec
from llama_index.llms.openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
model = os.getenv("MODEL")

class DirectionsSpec(BaseToolSpec):

    spec_functions = ["directions"]

    def directions(self, location:str):
        "A tool for checking directions or geographical position of Zagreb. Point A is Zagreb and Point B is the user input. Use a detailed plain text question as input to the tool."
        res = OpenAI(
            model=model,
        ).complete(f"What is the best way to go from Zagreb, Croatia to {location}")

        return res
