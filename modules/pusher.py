import os
from pusher import Pusher

pusher_client = None
if pusher_client is None and os.getenv('PUSHER', 'False').lower() == 'true':
    pusher_client = Pusher(
        app_id=os.getenv('PUSHER_APP_ID'),
        key=os.getenv('PUSHER_KEY'),
        secret=os.getenv('PUSHER_SECRET'),
        cluster=os.getenv('PUSHER_CLUSTER'),
        ssl=True
    )
    print("Pusher configured successfully.")

def pusher(channel, event, data):
    try:
        pusher_client.trigger(channel, event, data)
        return True
    except Exception as e:
        print(f"Pusher event trigger error: {str(e)}")
        return False
