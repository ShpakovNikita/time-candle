from model import logger


class Project:
    """
    This is the base Project class for the task manager.
    """
    def __init__(self,
                 pid_,
                 admin_uid_,
                 title_,
                 description_=''):
        self.pid = pid_
        self.admin_uid = admin_uid_
        self.tid_list = []

        # this is list of tuples in format (uid , [role_tags] )
        self.uid_roles = []
        self.title = title_
        self.description = description_

    @classmethod
    def make_project(cls, obj):
        """
        This function converts some data type to project
        :type obj: type with fields:
        - pid
        - other obj admin with pid
        - title
        :return: Project
        """
        logger.debug('convert storage to model project')

        project = cls(obj.pid,
                      obj.admin.pid,
                      obj.title)

        return project
