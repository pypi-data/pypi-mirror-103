from Findclone import aiofindclone, findclone, models


if __name__ == '__main__':
    # get models attributes
    models_ = [models.Account, models.Profiles, models.Histories, models.Profile, models.History, models.Detail]
    print("MODELS:")
    [help(model) for model in models_]
    # get findclone attributes and methods
    libs = [findclone.FindcloneApi, aiofindclone.FindcloneAsync]
    print("LIBS:")
    [help(lib) for lib in libs]
