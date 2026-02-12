class Role:
    """Defines employee roles and their management capabilities.

    Attributes:
        INTERN (str): Intern role.
        STAFF_MEMBER (str): Staff member role.
        SENIOR_STAFF (str): Senior staff role that can manage.
        MANAGER (str): Manager role that can manage.
        DIRECTOR (str): Director role that can manage.
        HEAD_OF_ORGANIZATION (str): Head of organization role that can manage.
    """

    INTERN = "INTERN"
    STAFF_MEMBER = "STAFF_MEMBER"
    SENIOR_STAFF = "SENIOR_STAFF"
    MANAGER = "MANAGER"
    DIRECTOR = "DIRECTOR"
    HEAD_OF_ORGANIZATION = "HEAD_OF_ORGANIZATION"

    @classmethod
    def exists(cls, role):
        """Check if the given role is valid.

        Args:
            role (str): The role to validate.

        Returns:
            bool: True if the role is valid, False otherwise.
        """
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
        """Check if the given role can manage other employees.

        Args:
            role (str): The role to check.

        Returns:
            bool: True if the role can manage, False otherwise.
        """
        return role in {cls.SENIOR_STAFF, cls.MANAGER, cls.DIRECTOR, cls.HEAD_OF_ORGANIZATION}