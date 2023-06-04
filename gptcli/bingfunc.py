import asyncio
from EdgeGPT import Chatbot, ConversationStyle


async def bingbot(prompt: str, style: ConversationStyle):
    bot = await Chatbot.create()  # Passing cookies is optional
    response = await bot.ask(prompt=prompt, conversation_style=style)
    print(response['item']['messages'][1]['text'])
    await bot.close()

# ConversationStyle.creative
# ConversationStyle.balanced
# ConversationStyle.precise

if __name__ == "__main__":
    prompt = "count to 3"
    style = ConversationStyle.creative
    asyncio.run(bingbot(prompt, style))
