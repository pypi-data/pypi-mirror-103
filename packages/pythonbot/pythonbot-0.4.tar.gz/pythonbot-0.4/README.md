# Python Bot Api Wrapper
Handles messages and other events from the Python Bot api.

Messages are returned as a Message object with the content and a unique id.

When the client if defined and ran, it will start a loop that checks if there is a new message every 0.5 seconds by default.

### Example of usage
```
import pythonbot

client = pythonbot.Client()

@client.event
async def on_message(message):
    print("New message: " + message.content)

client.run()
```