from time_candle.storage.adapter_classes import User
from time_candle.storage.adapter_classes import Message
from time_candle.storage.adapter_classes import Filter as PrimaryFilter
from time_candle.storage.adapter_classes import Adapter as PrimaryAdapter
from time_candle.model.instances.user import User as UserInstance
from time_candle.model.instances.message import Message as MessageInstance
from time_candle.storage import logger
import time_candle.exceptions.db_exceptions as db_e
from peewee import DoesNotExist


class UserFilter(PrimaryFilter):

    def __init__(self):
        super().__init__()

    @staticmethod
    def _union_filter():
        return User.uid.is_null(False)

    def uid(self, uid, op=PrimaryFilter.OP_AND):
        if self.result:
            self.ops.append(op)

        self.result.append(User.uid == uid)
        return self

    def login_substring(self, substring, op=PrimaryFilter.OP_AND):
        if self.result:
            self.ops.append(op)

        self.result.append(User.login.contains(substring))
        return self

    def login_regex(self, regex, op=PrimaryFilter.OP_AND):
        if self.result:
            self.ops.append(op)

        self.result.append(User.login.contains(regex))
        return self

    def nickname_substring(self, substring, op=PrimaryFilter.OP_AND):
        if self.result:
            self.ops.append(op)

        self.result.append(User.nickname.contains(substring))
        return self

    def nickname_regex(self, regex, op=PrimaryFilter.OP_AND):
        if self.result:
            self.ops.append(op)

        self.result.append(User.nickname.contains(regex))
        return self


class UserAdapter(PrimaryAdapter):
    def __init__(self,
                 db_name=None,
                 uid=None,
                 psql_config=None,
                 connect_url=None):
        super().__init__(uid, db_name, psql_config, connect_url)

    @staticmethod
    def get_by_filter(filter_instance):
        """
        This function returns storage objects by the given UserFilter.
        :param filter_instance: UserFilter with defined filters
        :return: List of UserInstance
        """
        query = User.select().where(filter_instance.to_query())

        return [UserInstance.make_user(user) for user in query]

    @staticmethod
    def save(obj):
        """
        This function if checking is current user exists, and if so we are
        raising an exception. Or we are adding it to the database.
        This function is used to store given task to the database. Note, that
        tasks can be with similar names and dates (but on that case I have a
        task below)
        :param obj: type with fields:
         - login
         - nickname,
         - about
        :return: None
        """

        try:
            user = User.select().where(User.uid == obj.uid).get()

            UserAdapter._update(user, obj)

            logger.debug('user updated')
            return

        except DoesNotExist:
            logger.debug('adding user...')

        User.create(uid=obj.uid,
                    login=obj.login,
                    about=obj.about,
                    nickname=obj.nickname)

    @staticmethod
    def _update(user, obj):
        user.nickname = obj.nickname
        user.about = obj.about
        user.save()

    @staticmethod
    def get_id_by_login(login):
        """
        This function checks if user by passed login exists in the database and
        returns user's id, or raises an error
        :param login: User's login
        :return: Int
        """
        try:
            return User.select().where(User.login == login).get().uid

        except DoesNotExist:
            raise db_e.InvalidLoginError(
                db_e.LoginMessages.USER_DOES_NOT_EXISTS)

    @staticmethod
    def get_user_by_id(uid):
        """
        This function returns login of user by id
        :param uid: User's id
        :return: String
        """
        query = User.select().where(User.uid == uid)
        try:
            # user instance
            obj = query.get()

        except DoesNotExist:
            raise db_e.InvalidUidError(
                db_e.LoginMessages.USER_DOES_NOT_EXISTS)

        return UserInstance.make_user(obj)

    ############################################################################
    # MESSAGES (It is better not to create another adapter for this feature)   #
    ############################################################################

    def get_messages(self):
        """
        This function returns all messages for current user
        :return: List of messages
        """
        query = Message.select().where(Message.uid == self.uid)
        return [MessageInstance.make_message(message) for message in query]

    def remove_message(self, mid):
        try:
            message = Message.select().where(
                (Message.mid == mid) & (Message.uid == self.uid)).get()

            message.delete_instance()
            logger.debug('Message has been removed')
        except DoesNotExist:
            raise db_e.InvalidMidError(db_e.MidMessages.DO_NOT_HAVE_RIGHTS)

    @staticmethod
    def send_message(uid, message_str):
        Message.create(uid=uid,
                       content=message_str)
        logger.debug('Message has been sent')
