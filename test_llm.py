from llm import llm

response = llm.invoke("Reply with only: LLM OK")
print(response.content)
