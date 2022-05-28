

# 返回文件是否被锁定
def is_lock(file):
    return file.using is not None


# 尝试给文件上锁，返回是否成功上锁
def lock(file, user):
    if file.using is None:
        file.using = user
        file.save()
        return True
    return False


# 尝试给文件解锁，返回是否成功解锁
def unlock(file, user):
    print(type(user))
    if file.using is not None and file.using.userID == user.userID:
        file.using = None
        file.save()
        return True
    return False
