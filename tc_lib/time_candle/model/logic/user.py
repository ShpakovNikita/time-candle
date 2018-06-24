from time_candle.model.instances.user import User as UserInstance
from time_candle.model.instances.message import UserMessages
from time_candle.storage.user_adapter import UserFilter
from . import Logic


class UserLogic(Logic):

    def __init__(self,
                 db_name=None,
                 uid=None,
                 psql_config=None,
                 connect_url=None):
        super().__init__(db_name, uid, psql_config, connect_url)

    def add_user(self,
                 login,
                 external_id,
                 nickname,
                 about):
        # add user to the database
        user = UserInstance(login=login,
                            uid=external_id,
                            nickname=nickname,
                            about=about)

        self.user_adapter.save(user)
        self.queue.append(
            external_id, UserMessages.USER_JOINED.format(login))

        self.queue.flush()

    def get_users(self, substr):
        # get users by passed substring
        fil = UserFilter().nickname_substring(substr)
        users = self.user_adapter.get_by_filter(fil)

        return users

    def get_user(self, uid):
        return self.user_adapter.get_user_by_id(uid)

    def change_user(self, uid, nickname, about):
        user = self.user_adapter.get_user_by_id(uid)
        if nickname is not None:
            user.nickname = nickname

        if about is not None:
            user.about = about

        self.user_adapter.save(user)
        self.queue.append(uid, UserMessages.USER_JOINED)

        self.queue.flush()

    ############################################################################
    # MESSAGES (It is better not to create another logic inst for this feature)#
    ############################################################################

    def get_messages(self):
        return self.user_adapter.get_messages()

    def remove_message(self, mid):
        self.user_adapter.remove_message(mid)
