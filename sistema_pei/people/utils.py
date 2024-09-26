import datetime

PASSWORD_SEPARATOR_CHAR = "@"
USERNAME_PREFIX_LENGHT = 5


def create_default_password(user):
    username_prefix = user.email[:USERNAME_PREFIX_LENGHT]
    current_year = datetime.date.today().year
    return PASSWORD_SEPARATOR_CHAR.join([username_prefix, str(current_year)])


def has_default_password(user):
    default = create_default_password(user)
    return user.check_password(default)
