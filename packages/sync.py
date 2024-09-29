def run(args):
  query = args.get("query", "default")
  text = f"Query received: {query}"

  log(text)
  
  return text
