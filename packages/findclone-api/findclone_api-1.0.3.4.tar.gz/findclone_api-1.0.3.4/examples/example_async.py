import asyncio
from Findclone import FindcloneAsync


async def main(login, password):
    async with FindcloneAsync() as findclone:
        await findclone.login(login=login, password=password)
        print(await findclone.info)
        histories = await findclone.history()
        # get history search
        for history in histories:
            h_id = history.id
            profiles = await findclone.search(h_id)
            for profile in profiles:
                print(profile.raw_data)
    findclone = FindcloneAsync()
    await findclone.login(login, password)
    profiles = await findclone.upload("head.jpg")
    # do something
    await findclone.close()


if __name__ == '__main__':
    login = "123123123"
    password = "foobar"
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(login, password))