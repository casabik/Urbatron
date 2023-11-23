import asyncio 

async def f():
    while True:
        print('f')
        await asyncio.sleep(4)
        print('f2')

async def g():
    while True:
        print('g')
        await asyncio.sleep(1)  

async def main():
    main_loop.create_task(f())
    await g()

main_loop = asyncio.get_event_loop()
main_loop.run_until_complete(main())
main_loop.run_forever()