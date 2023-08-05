from Findclone import FindcloneApi, is_image, save_image


if __name__ == '__main__':
    login = "123123123"
    password = "foobar"
    file_url = "https://example.com/rick_astley_never_give_u_up.jpg"
    f = FindcloneApi()
    f.login(login, password)
    result = f.upload(file_url)
    # check Profiles object else write file with painted rectangles
    if is_image(result):
        save_image(result, "foobar.jpg")
    else:
        for profile in result:
            print(profile.raw_data)
            for detail in profile.details:
                print(detail.url_source)
