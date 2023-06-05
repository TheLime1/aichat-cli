from EdgeGPT import Chatbot, ConversationStyle


async def bingbot(prompt: str, style: ConversationStyle):
    bot = await Chatbot.create()  # Passing cookies is optional
    response = await bot.ask(prompt=prompt, conversation_style=style)
    print(response['item']['messages'][1]['text'])
    await bot.close()
    return response['item']['messages'][1]['text']

# ConversationStyle.creative
# ConversationStyle.balanced
# ConversationStyle.precise


# prompt = "count to 3"
# style = ConversationStyle.creative
# asyncio.run(bingbot(prompt, style))
