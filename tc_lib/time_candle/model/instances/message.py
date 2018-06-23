from time_candle.model import logger

# This is the message templates

# project:
USER_ADDED = 'User {} has been added to the project'
PROJECT_REMOVED = 'Project {} has been removed from the history'
USER_INVITED = 'You have been invited to the project: {}'

# user:
USER_JOINED = 'Welcome to your new place, {}!'
PROFILE_CHANGED = 'You have changed your profile'

# task:
TASK_REMOVED = 'Task {} has been removed'
TASK_EXPIRED = 'Task {} has expired status now'


class Message:
    """
    This is simple message class that have only 3 fields to maintain. Just here
    in order to keep code the same structured and organized
    """

    def __init__(self,
                 uid=None,
                 mid=None,
                 content=''):
        self.uid = uid
        self.mid = mid
        self.content = content

    @classmethod
    def make_message(cls, obj):
        """
        This function converts some data type to user
        :type obj: type with fields:
        - mid
        - content
        - user
        :return: Message
        """
        logger.debug('convert storage to model message')

        message = cls(uid=obj.user,
                      mid=obj.mid,
                      content=obj.content)

        return message
