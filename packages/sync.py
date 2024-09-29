def run(args):
    query = args.get("query", "default")
    text = f"Query received: {query}"

    # log function accepts str, int, list or dict
    log(text)

    return text
