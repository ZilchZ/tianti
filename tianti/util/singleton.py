from threading import Lock


def singleton(cls):
    instance = {}

    def get_instance():
        if not instance.has_key(cls):
            with Lock():
                if not instance.has_key(cls):
                    instance[cls] = cls()
        return instance[cls]

    return get_instance


if __name__ == '__main__':
    a = {singleton: 1}
    print a.has_key(singleton)

