# Organization Management System - Design Document

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   Organization (Main Logic)                 │
│  - employees_by_id: dict[int, Employee]                     │
│  - units_by_name: dict[str, Unit]                           │
│  - next_id: int (auto-increment)                            │
│  - head_id: int (single HEAD_OF_ORGANIZATION)               │
│                                                             │
│  + add_unit(name) / add_employee(...) / delete_employee()   │
│  + assign_manager() / move_to_unit()                        │
│  + print_org() / print_units() / print_employee()           │
└─────────────────┬────────────────────────────┬──────────────┘
                  │                            │
        ┌─────────▼────────┐          ┌────────▼────────┐
        │   Employee       │          │      Unit       │
        │ ─────────────    │          │  ───────────    │
        │ - id: int        │          │  - name: str    │
        │ - name: str      │          │  - employees:   │
        │ - age: int       │          │    list[Emp]    │
        │ - role: Role     │          │                 │
        │ - unit_name: str │          │  + add_emp()    │
        │ - manager_id:int │          │  + remove_emp() │
        │ - children_ids:  │          │  + __iter__()   │
        │   list[int]      │          │  + __len__()    │
        └──────────────────┘          └─────────────────┘
                  △                           △
                  │ has_role                  │ belongs_to
                  │                           │
        ┌─────────▼────────────────┐
        │       Role (Enum)        │
        │  ──────────────────────  │
        │  INTERN                  │
        │  STAFF_MEMBER            │
        │  SENIOR_STAFF (manages)  │
        │  MANAGER (manages)       │
        │  DIRECTOR (manages)      │
        │  HEAD_OF_ORGANIZATION    │
        │    (manages, unique)     │
        │                          │
        │  + exists() - validates  │
        │  + can_manage() - checks │
        │    authority             │
        └──────────────────────────┘
```

## Design Principles

| Aspect | Design Decision | Rationale |
|--------|-----------------|-----------|
| **Separation of Concerns** | Each class has single responsibility | Role: constants only; Employee: data; Unit: collection; Organization: business logic |
| **Data Storage** | Dictionaries for O(1) lookup (employees & units) | Fast queries by ID or unit name |
| **Hierarchy** | Tree structure via manager/children IDs | Enables print_org() traversal and role-based constraints |
| **Validation** | Business logic centralized in Organization | Ensures constraints (one HEAD, managers can only be certain roles, etc.) |
| **Immutable Roles** | Role class with constants & class methods | Type-safe role checking, centralized role logic |
| **Insertion Order** | Units maintain insertion order (dict preserves order in Python 3.7+) | print_units() displays units in creation order, not alphabetically |

## Key Relationships

- **Employee → Manager**: manager_id references another Employee (hierarchical)
- **Employee → Unit**: unit_name references a Unit (many-to-one)
- **Employee → Role**: role is a Role constant (one-to-one, validates on add)
- **Organization → Employees/Units**: owns collections, enforces constraints
- **Unit → Employees**: maintains sorted list by employee ID

## Constraints

1. Only ONE `HEAD_OF_ORGANIZATION` exists (enforced in add_employee)
2. Only roles {SENIOR_STAFF, MANAGER, DIRECTOR, HEAD_OF_ORGANIZATION} can manage
3. Non-HEAD employees MUST have a manager
4. HEAD cannot be deleted or reassigned a manager
5. Employee with direct reports cannot be deleted
