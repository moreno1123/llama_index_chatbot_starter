from typing import List
import os

from llama_index.core.chat_engine.types import BaseChatEngine
from llama_index.core.llms import ChatMessage, MessageRole
from app.engine.index import get_agent

from fastapi.responses import StreamingResponse
from fastapi import APIRouter, Depends, HTTPException, Request, status, BackgroundTasks

from pydantic import BaseModel

model = os.getenv("MODEL")
environment = os.getenv("ENVIRONMENT", "dev")  # Default to 'development' if not set

chat_router = r = APIRouter()

class _Message(BaseModel):
    role: MessageRole
    content: str 

class _ChatData(BaseModel):
    messages: List[_Message]

@r.post("")
async def chat(
    request: Request,
    data: _ChatData,
    agent: BaseChatEngine = Depends(get_agent)
):
    # check preconditions and get last message
    if len(data.messages) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No messages provided",
        )
    lastMessage = data.messages.pop()
    if lastMessage.role != MessageRole.USER:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Last message must be from user",
        )
    
    messages = [
        ChatMessage(
            role=m.role,
            content=m.content,
        ) 
        for m in data.messages
    ]       

    # last message is prompt, messages are memory
    response = agent.stream_chat(lastMessage.content, messages)

    # # more info
    # tasks = agent.list_tasks()
    # if tasks[0].extra_state['sources']:
    #     # # look at the source from vectore, this will crash if some other tool is used instead of query_engine
    #     # sources_nodes = tasks[0].extra_state['sources'][0].raw_output.source_nodes
    #     # for node in sources_nodes:
    #     #     print(node)
    #     #     print("---------------------")

    #     tool_name = tasks[0].extra_state['sources'][0].tool_name
    #     print("tool_name: ", tool_name)


    # stream response
    async def event_generator():
        complete_response = ""
        for token in response.response_gen:
            if await request.is_disconnected():
                break
            complete_response += token
            yield token

    return StreamingResponse(event_generator(), media_type="text/plain")
