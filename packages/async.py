import asyncio

async def run(args):
    query = args.get("query", "default")
    text = f"Query received: {query}"

    await asyncio.sleep(5)
    
    log(text)
