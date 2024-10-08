from highrise import *
from highrise.models import *
import asyncio
from asyncio import Task

async def follow(self: BaseBot, user: User, message: str) -> None:
    async def following_loop(self: BaseBot, user: User, message: str) -> None:
        if message.startswith("/following_loop"):
            await self.highrise.chat("Неверная команда, используйте /follow ")
            return
        while True:
            #gets the user position
            room_users = (await self.highrise.get_room_users()).content
            for room_user, position in room_users:
                if room_user.id == user.id:
                    user_position = position
                    break
            print(user_position)
            if type(user_position) != AnchorPosition:
                await self.highrise.walk_to(Position(user_position.x + 1, user_position.y, user_position.z))
            await asyncio.sleep(0.5)
    taskgroup = self.highrise.tg
    task_list = list(taskgroup._tasks)
    for task in task_list:
        if task.get_name() == "following_loop":
            await self.highrise.chat("я уже подписан на кого-то  ")
            return
    #checks if this function is already in the Highrise class tg (task group).
    taskgroup.create_task(coro=following_loop(self, user, message))
    task_list : list[Task] = list(taskgroup._tasks)
    # Sets the name of the task who has the following_loop function to "following_loop"
    for task in task_list:
        if task.get_coro().__name__ == "following_loop":
            task.set_name("following_loop")
    await self.highrise.chat(f"я следую   {user.username} 🚶‍♂️")
    
async def stop(self: BaseBot, user: User, message: str) -> None:
    taskgroup = self.highrise.tg
    task_list = list(taskgroup._tasks)
    for task in task_list:
        if task.get_name() == "following_loop":
            task.cancel()
            await self.highrise.chat(f"Отписаться   {user.username}")
            return
    await self.highrise.chat("я ни за кем не слежу  ")
    return