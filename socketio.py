import asyncio
import socketio

sio = socketio.AsyncClient()


"EXAMPLE"
@sio.event
async def connect():
    pass

@sio.event
async def my_message(data):
    print('message received with ', data)
    await sio.emit('my response', {'response': 'my response'})

@sio.event
async def disconnect():
    pass

async def main():
    await sio.connect('http://localhost:5000')
    await sio.wait()

if __name__ == '__main__':
    asyncio.run(main())

#Emitting
'''
await sio.emit('my event', {'data': 'my data'})
'''


#Receiving
'''
event = await sio.receive()
print(f'received event: "{event[0]}" with arguments {event[1:]}')
'''

