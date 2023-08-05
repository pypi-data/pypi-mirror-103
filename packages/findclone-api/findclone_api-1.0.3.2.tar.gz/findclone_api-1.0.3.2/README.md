# Findclone API by vypivshiy
### Описание
findclone-api - это неофициальное API для взаимодействия с [Findclone](https://findclone.ru) .
Присутствет синхронная и __асинхронная__ версии модулей и типизация объектов 
~~чтобы модная и современная IDE всё подсказывала, да~~ для более удобной
работы.
### Установка через pip
`pip install findclone_api`
### Requirements
```
requests
aiohttp
Pillow
```
### Примеры использования:

```python
# sync findclone example
from Findclone import FindcloneApi, is_image

if __name__ == '__main__':
    phone = "+123456172"
    password = "foobar"
    f = FindcloneApi()
    f.login(phone, password)
    print(f) # get account information
    # upload photo
    profiles = f.upload("test.jpg")
    # or send image url
    # profiles = f.upload("https://example.com/image.png")
    # work with return object:
    if is_image(profiles):  # check return object
        print("write file")
        with open("return_image.jpg", "wb") as file:
            file.write(profiles.getvalue())
    else:
        for profile in profiles:
            print(profile)  # return profile.__str__()
            print(profile.url, profile.score)
    histories = f.history()
    for history in histories:
        print(history)
```

```python
# async findclone example
import asyncio
from Findclone import FindcloneAsync, is_image, save_image

async def main(login, password):
    # контектстный менеджер, который автоматически закроет сессию
    async with FindcloneAsync() as f:
        await f.login(login, password)
        print(await f.info)
        profiles = await f.upload("file.jpg")
        if is_image(profiles):
            save_image(profiles, "out.jpg")
        else:
            for profile in profiles:
                print(profile)
                print(profile.url, profile.score)
    # Или вместо контекстного менеджера можно вручную открывать и закрывать сессию
    f = FindcloneAsync()
    await f.login(login, password)
    # ... какой то код
    await f.close()
        

if __name__ == '__main__':
    login = "123123123"
    password = "foobar"
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(login, password))
```
### Кейс если обнаружены на фото 2 и более лиц
test.jpg:
![img1](https://i.ibb.co/ZN2RM5F/Young-happy-couple-using-two-phones-share-social-media-news-at-home-smiling-husband-and-wife-millenn.jpg)
```python
import Findclone

if __name__ == '__main__':
    phone = "+123456172"
    password = "foobar"
    f = Findclone.FindcloneApi()
    f.login(phone, password)
    profiles = f.upload("test.jpg") 
    # write or send object:
    print("write file")
    if Findclone.is_image(profiles):
        Findclone.save_image(profiles, "out.jpg")
    ...
```
out_image.jpg:
![img2](https://i.ibb.co/SnrGGnD/test-123.png)
Из результата с фотографии, выбираем id лица (указан под квадратом):
```python
...
face_box_id = 0
profiles = f.upload("test.jpg", face_box_id=face_box_id)
for profile in profiles:
    print(profile)
``` 
[Больше примеров](https://github.com/vypivshiy/findclone_api/tree/main/examples)

[Краткое описание объектов](examples/OBJECTS.md)