from llama_index.core.tools.tool_spec.base import BaseToolSpec

class MultiplySpec(BaseToolSpec):

    spec_functions = ["multiply"]

    def multiply(a: int, b: int) -> int:
        """Multiply two numbers and return the result"""
        return a * b
