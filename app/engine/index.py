import os
from llama_index.core import VectorStoreIndex
from llama_index.core.tools import QueryEngineTool, ToolMetadata, FunctionTool
from llama_index.agent.openai import OpenAIAgent
from dotenv import load_dotenv
from llama_index.llms.openai import OpenAI
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from app.engine.propmts import get_system_prompt

from app.engine.tools.directions import DirectionsSpec
from app.engine.tools.multiply import MultiplySpec
from llama_index.core.agent import FunctionCallingAgentWorker
from llama_index.llms.groq import Groq
from app.engine.get_index import get_index

load_dotenv()

model = os.getenv("MODEL")
llama_llm = Groq(model="llama3-70b-8192", api_key=os.getenv("GROQ_API_KEY"))

def get_agent():
    index = get_index()
    query_engine = index.as_query_engine(similarity_top_k=4, llm=llama_llm)
    
    query_engine_tools = [
        QueryEngineTool(
            query_engine=query_engine,
            metadata=ToolMetadata(
                name="Croatia_Airlines_business_report_2023",
                description=(
                    "Provides information business report from Croatia Airlines for 2023."
                    "Use a detailed plain text question as input to the tool."
                ),
            ),
        ),
    ]

    directions_tool = DirectionsSpec().to_tool_list()
    multiply_tool = MultiplySpec().to_tool_list()

    tools = query_engine_tools + directions_tool + multiply_tool

    agent = OpenAIAgent.from_tools(
        tools=tools, 
        llm=OpenAI(model=model),
        verbose=True,
        system_prompt=get_system_prompt(),
        max_function_calls=1
    )

    return agent

def get_agent_no_stream():
    index = get_index()
    query_engine = index.as_query_engine(similarity_top_k=4, llm=llama_llm)
    
    query_engine_tool = QueryEngineTool(
        query_engine=query_engine,
        metadata=ToolMetadata(
            name="Croatia_Airlines_business_report_2023",
            description=(
                "Provides information business report from Croatia Airlines for 2023."
                "Use a detailed plain text question as input to the tool."
            ),
        ),
    )

    tools = [
        query_engine_tool, 
        FunctionTool.from_defaults(fn=DirectionsSpec().directions), 
        FunctionTool.from_defaults(fn=MultiplySpec().multiply), 
    ]

    agent = FunctionCallingAgentWorker.from_tools(
        tools, 
        llm=llama_llm,
        verbose=True, 
        system_prompt=get_system_prompt()
    ).as_agent()

    return agent
