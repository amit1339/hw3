import sys
# Ensure organization.py is in the same directory
from organization import Organization

def main():
    org = Organization()

    while True:
        print("Please enter a command:")
        try:
            user_input = input()
            parts = user_input.strip().split()
            
            if not parts:
                continue

            command = parts[0]

            if command == "quit":
                break

            elif command == "welcome":
                print("WELCOME!")
                # Personal details as per PDF example
                print("submitter 1: Amit Ben Yosef amit1339@gmail.com 314649187")
                print("submitter 2: Idan Asulin asulinidan15@gmail.com 313571838")

            elif command == "add_unit":
                if len(parts) < 2:
                    print("Usage: add_unit <unit_name>")
                    continue
                org.add_unit(parts[1])

            elif command == "add_employee":
                # Expected: add_employee <name> <unit> <age> <role> [manager_id]
                if len(parts) < 5:
                    # Special check for validation error message parity if needed
                    # But prompt implies we assume correct number of parameters usually,
                    # EXCEPT where error messages are defined.
                    print("Wrong format for add employee command.")
                    continue
                
                name = parts[1]
                unit = parts[2]
                # Prompt says "assume safe casting... if something should be int - it will be int" [cite: 51]
                age = int(parts[3])
                role = parts[4]
                
                manager_id = None
                if len(parts) > 5:
                    manager_id = int(parts[5])
                
                org.add_employee(name, unit, age, role, manager_id)

            elif command == "delete_employee":
                if len(parts) < 2:
                    continue
                emp_id = int(parts[1])
                org.delete_employee(emp_id)

            elif command == "print_employee":
                if len(parts) < 2:
                    continue
                emp_id = int(parts[1])
                org.print_employee(emp_id)

            elif command == "assign_manager":
                if len(parts) < 3:
                    continue
                emp_id = int(parts[1])
                mgr_id = int(parts[2])
                org.assign_manager(emp_id, mgr_id)

            elif command == "move_to_unit":
                if len(parts) < 3:
                    continue
                emp_id = int(parts[1])
                target_unit = parts[2]
                org.move_to_unit(emp_id, target_unit)

            elif command == "print_org":
                org.print_org()

            elif command == "print_units":
                org.print_units()

            else:
                print(f"The command {command} is unknown.")

        except EOFError:
            break
        except Exception as e:
            # Fallback for unexpected errors
            print(f"Error: {e}")

if __name__ == "__main__":
    main()