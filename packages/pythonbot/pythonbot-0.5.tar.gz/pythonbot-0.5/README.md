# Python Bot Api Wrapper
Handles messages and other events from the Python Bot api.

Messages are returned as a Message object with the content and a unique id.

When the client if defined and ran, it will asynchronously check for new messages in the api.

There are two types of events currently: `on_ready` and `on_message`

`on_ready` is used to check if the api is up and that everything is working correctly.

`on_message` is used to perform certain actions when a message is received.

### Example of usage
```
import pythonbot

client = pythonbot.Client()

@client.event
async def on_ready():
    print("Client is ready.")

@client.event
async def on_message(message):
    print("New message: " + message.content)

client.run()
```