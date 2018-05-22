from model import logger


class Project:
    """
    This is the base Project class for the task manager.
    """
    def __init__(self,
                 pid,
                 admin_uid,
                 title,
                 description=''):
        self.pid = pid
        self.admin_uid = admin_uid
        self.tid_list = []

        # this is list of tuples in format (uid , [role_tags] )
        self.uid_roles = []
        self.title = title
        self.description = description

    @classmethod
    def make_project(cls, obj):
        """
        This function converts some data type to project
        :type obj: type with fields:
        - pid
        - other obj admin with pid
        - title
        - description
        :return: Project
        """
        logger.debug('convert storage to model project')

        project = cls(obj.pid,
                      obj.admin.uid,
                      obj.title,
                      obj.description)

        return project
