from time_candle.model.instances.user import User as UserInstance
import time_candle.exceptions.model_exceptions as m_e
from time_candle.model import logger
import time_candle.model.tokenizer
import time_candle.model.time_formatter
from time_candle.enums.status import Status
from time_candle.storage.user_adapter import UserFilter
from . import Logic


class UserLogic(Logic):

    def __init__(self, db_name=None, uid=None):
        super().__init__(db_name, uid)

    def add_user(self,
                 login,
                 nickname,
                 about):
        # add user to the database
        user = UserInstance(login=login,
                            nickname=nickname,
                            about=about)
        self.user_adapter.save(user)

    def get_users(self, substr):
        # get users by passed substring
        fil = UserFilter().nickname_substring(substr)
        users = self.user_adapter.get_by_filter(fil)

        return [UserInstance.make_user(user) for user in users]

    def get_user(self, uid):
        return UserInstance.make_user(self.user_adapter.get_user_by_id(uid))

    def change_user(self, uid, nickname):
        user = self.user_adapter.get_user_by_id(uid)
        if nickname is not None:
            user.nickname = nickname

        self.user_adapter.save(user)
