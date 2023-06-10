import json
from EdgeGPT.EdgeGPT import Chatbot, ConversationStyle, NotAllowedToAccess
import asyncio


async def bingbot(prompt: str, style: ConversationStyle):
    bot = await Chatbot.create()  # Passing cookies is optional

    try:
        response = await bot.ask(prompt=prompt, conversation_style=style, simplify_response=True)
        print(response["text"])
        return response["text"]
    except NotAllowedToAccess:
        # using token here
        print("using token")

    await bot.close()


prompt = "count to 3"
style = ConversationStyle.creative
result = asyncio.run(bingbot(prompt, style))
