from agno.models.openai import OpenAIChat
from agno.models.groq import Groq

model_openai_teams_agent =OpenAIChat(id ="gpt-4o", temperature=0)
model_openai =OpenAIChat(id ="gpt-4o", temperature=0)
model_groq_qwen  = Groq(api_key="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", id="qwen-qwq-32b")
model_groq_llama70  = Groq(api_key="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", id="llama-3.3-70b-versatile")