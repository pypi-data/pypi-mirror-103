from Findclone import FindcloneApi


def auth_1(login, password):
    f = FindcloneApi()
    f.login(login, password)
    f.session.headers.update({"foo": "bar"})  # config requests.Session() object
    session_auth = f.get_session  # return dict
    print(session_auth)
    return session_auth


def auth_2(userid, session_key):
    f = FindcloneApi()
    f.login(session_key=session_key, userid=userid)
    print(f.info)


if __name__ == '__main__':
    phone = "123123123123"
    password = "foobar"
    # auth with phone and password
    session = auth_1(phone, password)
    # auth with session-key and user-id
    auth_2(session["user-id"], session["session-key"])