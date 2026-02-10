class Employee:
    def __init__(self, emp_id, name, unit_name, age, role, manager_id):
        self.id = emp_id
        self.name = name
        self.unit_name = unit_name
        self.age = age
        self.role = role
        self.manager_id = manager_id
        self.children_ids = []

    def __str__(self):
        return f"|--{self.role} | {self.unit_name} | {self.id} | {self.name} - {self.age}"