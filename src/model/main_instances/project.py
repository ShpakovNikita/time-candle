class Project:
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
