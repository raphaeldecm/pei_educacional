profile_groups = set()


def profile(cls):
    def inner():
        profile_groups.add(cls.__name__)
        return cls

    return inner()
