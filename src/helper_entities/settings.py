class Settings:
    def __init__(self, password, mail, nickname, time_zone, about):
        self._password = password
        self._mail = mail
        self._nickname = nickname
        self._time_zone = time_zone
        self._about = about

    @property
    def password(self):
        return self._password
