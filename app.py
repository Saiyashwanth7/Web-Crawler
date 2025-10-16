import asyncio

async def fetch_data(id,sleep_time):
    print(f"Fetchind the data for id:{id}")
    await asyncio.sleep(sleep_time)
    return {"id":id,"data":f"sample data for id {id}"}

async def main():
    tasks=[]
    async with asyncio.TaskGroup() as tg:
        for i,e in enumerate([1,2,5], start=1):
            task=tg.create_task(fetch_data(i,e))
            tasks.append(task)

    result=[task.result() for task in tasks]
    print(result)
    """ task1=asyncio.create_task(fetch_data(1,2))
    task2=asyncio.create_task(fetch_data(2,3))
    task3=asyncio.create_task(fetch_data(3,1))
    result1 = await task1
    result2 = await task2 
    result3 = await task3
    print(result1,result2,result3)"""

asyncio.run(main())