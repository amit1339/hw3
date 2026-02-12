class Unit:
    """Represents a unit/department in the organization.

    Attributes:
        name (str): The name of the unit.
        employees (list): List of employees in this unit, sorted by employee ID.
    """

    def __init__(self, name):
        """Initialize a unit.

        Args:
            name (str): The name of the unit.
        """
        self.name = name
        self.employees = []

    def add_employee(self, employee):
        """Add an employee to the unit and maintain sorted order by ID.

        Args:
            employee (Employee): The employee to add to the unit.
        """
        self.employees.append(employee)
        self.employees.sort(key=lambda x: x.id)

    def remove_employee(self, emp_id):
        """Remove an employee from the unit by ID.

        Args:
            emp_id (int): The ID of the employee to remove.
        """
        self.employees = [e for e in self.employees if e.id != emp_id]

    def __iter__(self):
        """Iterate over employees in the unit.

        Returns:
            iterator: Iterator over the employees list.
        """
        return iter(self.employees)

    def __len__(self):
        """Get the number of employees in the unit.

        Returns:
            int: Number of employees in the unit.
        """
        return len(self.employees)

    def __str__(self):
        """Return the unit name.

        Returns:
            str: The name of the unit.
        """
        return self.name