class Role:
    INTERN = "INTERN"
    STAFF_MEMBER = "STAFF_MEMBER"
    SENIOR_STAFF = "SENIOR_STAFF"
    MANAGER = "MANAGER"
    DIRECTOR = "DIRECTOR"
    HEAD_OF_ORGANIZATION = "HEAD_OF_ORGANIZATION"

    @classmethod
    def exists(cls, role):
        return role in {
            cls.INTERN, 
            cls.STAFF_MEMBER, 
            cls.SENIOR_STAFF, 
            cls.MANAGER, 
            cls.DIRECTOR, 
            cls.HEAD_OF_ORGANIZATION
        }

    @classmethod
    def can_manage(cls, role):
        return role in {cls.SENIOR_STAFF, cls.MANAGER, cls.DIRECTOR, cls.HEAD_OF_ORGANIZATION}