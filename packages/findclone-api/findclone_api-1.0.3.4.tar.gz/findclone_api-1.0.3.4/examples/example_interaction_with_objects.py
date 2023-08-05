from Findclone import FindcloneApi


def main(login, password):
    f = FindcloneApi()
    f.login(login, password)
    account = f.info  # get account object
    print(account)
    print(account.userid, account.period_days, account.quantity)  # get Account attributes
    print(account.raw_data)  # raw response
    histories = f.history()  # get history search
    for history in histories:
        print(history.id, history.unix_to_date())
        search_results = f.search(history.id)
        print(search_results.raw_data)  # get raw response
        # iteration Profiles object
        for profile in search_results:
            print(profile.raw_details)
            print(profile.score, profile.firstname)
            # iteration Detail objects
            for detail in profile:
                print(detail.url)


if __name__ == '__main__':
    login = "123123123"
    password = "foobar"
    main(login, password)
