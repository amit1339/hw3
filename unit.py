class Unit:
    def __init__(self, name):
        self.name = name
        self.employees = []

    def add_employee(self, employee):
        self.employees.append(employee)
        self.employees.sort(key=lambda x: x.id)

    def remove_employee(self, emp_id):
        self.employees = [e for e in self.employees if e.id != emp_id]

    def __iter__(self):
        return iter(self.employees)

    def __len__(self):
        return len(self.employees)

    def __str__(self):
        return self.name