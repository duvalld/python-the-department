import sqlite3

class DatabaseManager:
    """ A class for managing SQLITE database operations """
    def __init__(self):
        self._database_name = "the_department_db.db"

    def open_db(self):
        """Open a connection to the database."""
        self._conn = sqlite3.connect(self._database_name)
        self._cursor = self._conn.cursor()

    def close_db(self):
        """Close the database connection."""
        self._cursor.close()
        self._conn.close()

    def create_table(self, query):
        """Create a table in the database."""
        self.open_db()
        self._cursor.execute(query)
        self._conn.commit()
        self.close_db()

    def insert_record(self, query, col_values, table):
        """Insert a record into the specified table."""
        self.open_db()
        self._cursor.execute(query, col_values)
        self._conn.commit()
        print(f"{table} successfuly added!")

    def entry_checker(self, table, column, id):
        """
        Check if an entry with the given ID exists in the specified table.

        Returns:
            bool: True if the entry exists, False otherwise.
        """
        query = f"SELECT EXISTS (SELECT 1 FROM {table} WHERE {
            column} = ? LIMIT 1)"
        try:
            self.open_db()
            self._cursor.execute(query, (id))
            result = self._cursor.fetchone()[0]
            return bool(result)
        except sqlite3.Error as e:
            print(f"Error checking entry: {e}")
            return False
        finally:
            self.close_db()

class Employee:
    """ A class representing an Employee with database operations. """
    def __init__(self):
        self._create_table_query = """
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY
                ,first_name TEXT NOT NULL
                ,last_name TEXT NOT NULL
                ,department_id integer
                )
            """
        self._db_manager = DatabaseManager()
        self._db_manager.create_table(self._create_table_query)
        
    def add_new(self):
        """ Add a new employee to the database."""
        try:
            first_name = input("First Name:")
            last_name = input("Last Name:")
            Department().view()
            department_check_loop = True
            while department_check_loop:
                department_id = input("Department ID (Optional):")
                if department_id == None or department_id == "":
                    department_check_loop = False
                else:
                    if employee._db_manager.entry_checker("departments", "id", department_id):
                        department_check_loop = False
                    else:
                        print("Department ID does not exist")
            
            add_new_employee_query = "INSERT INTO employees (first_name, last_name, department_id) VALUES(?, ?, ?)"
            self._db_manager.insert_record(add_new_employee_query, (first_name, last_name, department_id), "Employee")
            self._db_manager._conn.commit()
        except sqlite3.Error as e:
            print(f"Error adding {"sample"}: {e}")
        finally:
            if self._db_manager._conn:
                self._db_manager.close_db()
    
    def view(self, rover = False):
        """
        View employee records with an optional filter for a rover.

        Args:
            rover (bool): Whether to filter employees for a rover.
        """
        try:
            if rover:
                view_employee_query = """
                    SELECT 
                        employees.id
                        ,employees.first_name
                        ,employees.last_name
                        ,departments.department_name 
                    FROM employees
                    LEFT JOIN departments 
                    ON employees.department_id = departments.id
                    WHERE employees.department_id = ''
                """
            else:
                view_employee_query = """
                    SELECT 
                        employees.id
                        ,employees.first_name
                        ,employees.last_name
                        ,departments.department_name 
                    FROM employees
                    LEFT JOIN departments 
                    ON employees.department_id = departments.id
                """
            self._db_manager.open_db()
            self._db_manager._cursor.execute(view_employee_query)
            rows = self._db_manager._cursor.fetchall()
            row_header = f"{'ID':<4} | {'First Name':<10} | {'Last Name':<10} | {'Department':<10}"
            print(row_header)
            print(len(row_header) * "-")
            for row in rows:
                (row_id, row_first_name, row_last_name, row_department) = row
                print(f"{row_id:<4} | {row_first_name:<10} | {row_last_name:<10} | {row_department if row_department != None else "":<10}")
            self._db_manager.open_db()
            print(f"Result(s): {len(rows)}")
        except sqlite3.Error as e:
            print(f"Error adding {"sample"}: {e}")
        finally:
            if self._db_manager._conn:
                self._db_manager.close_db()

class Division:
    """ A class representing an Division with database operations. """
    def __init__(self):
        self._create_table_query = """
            CREATE TABLE IF NOT EXISTS divisions (
                id INTEGER PRIMARY KEY
                ,division_name TEXT NOT NULL
                ,head_id integer
                )
            """
        self._db_manager = DatabaseManager()
        self._db_manager.create_table(self._create_table_query)
        self._employee = Employee()

    def add_new(self):
        """ Add a new division to the database."""
        try:
            division_name = input("Division Name:")
            employee_check_loop = True
            while employee_check_loop:
                self._employee.view()
                employee_id = input("Division Head (Employee ID): ")
                if self._db_manager.entry_checker("employees", "id", employee_id):
                    employee_check_loop = False
                else:
                    print("Employee ID does not exist.")
            add_new_division_query = "INSERT INTO divisions (division_name, head_id) VALUES(?, ?)"
            self._db_manager.insert_record(add_new_division_query, (division_name, employee_id), "Division")
            self.view()
        except sqlite3.Error as e:
            print(f"Error adding {"sample"}: {e}")
        finally:
            if self._db_manager._conn:
                self._db_manager.close_db()
    
    def view(self):
        """ View division records """
        try:
            view_division_query = """
                SELECT 
                    divisions.id
                    ,divisions.division_name
                    ,employees.first_name || ' ' || employees.last_name as head_name 
                FROM divisions
                LEFT JOIN employees ON divisions.head_id = employees.id
            """
            self._db_manager.open_db()
            self._db_manager._cursor.execute(view_division_query)
            rows = self._db_manager._cursor.fetchall()
            row_header = f"{'ID':<4} | {'Division Name':<15} | {'Division Head':<15}"
            print(row_header)
            print(len(row_header) * "-")
            for row in rows:
                (row_id, row_division, row_head) = row
                print(f"{row_id:<4} | {row_division:<15} | {row_head:<15}")
            self._db_manager.open_db()
            print(f"Result(s): {len(rows)}")
        except sqlite3.Error as e:
            print(f"Error viewing Division: {e}")
        finally:
            if self._db_manager._conn:
                self._db_manager.close_db()

class Department:
    """ A class representing an Department with database operations. """
    def __init__(self):
        self._create_table_query = """
        CREATE TABLE IF NOT EXISTS departments (
            id INTEGER PRIMARY KEY
            ,division_id TEXT NOT NULL
            ,department_name TEXT NOT NULL
            ,manager_id INTEGER
            )
        """
        self._db_manager = DatabaseManager()
        self._db_manager.create_table(self._create_table_query)
        self._division = Division()
        self._employee = Employee()

    def view(self):
        """ View division records """
        try:
            view_department_query = """
                SELECT 
                    departments.id
                    ,departments.department_name
                    ,divisions.division_name 
                    ,employees.first_name || ' ' || employees.last_name as manager_name
                    ,(SELECT 
                        GROUP_CONCAT(first_name || ' ' || last_name) as member_name 
                        FROM employees 
                        WHERE department_id = departments.id
                    ) as members
                FROM departments 
                LEFT JOIN employees ON departments.manager_id = employees.id 
                LEFT JOIN divisions ON departments.division_id = divisions.id
            """
            self._db_manager.open_db()
            self._db_manager._cursor.execute(view_department_query)
            rows = self._db_manager._cursor.fetchall()
            row_header = f"{'ID':<4} | {'Department':<15} | {'Division':<15} | {'Manager':<15} | {'Members':<30} "
            print(row_header)
            print(len(row_header) * "-")
            for row in rows:
                (row_id, row_department, row_division, row_manager, row_member) = row
                print(f"{row_id:<4} | {row_department:<15} | {row_division:<15} | {row_manager:<15} | {row_member if row_member != None else "":<30}")
            self._db_manager.open_db()
            print(f"Result(s): {len(rows)}")
        except sqlite3.Error as e:
            print(f"Error viewing Department: {e}")
        finally:
            if self._db_manager._conn:
                self._db_manager.close_db()

    def add_new(self):
        """ Add a new department to the database."""
        try:
            department_name = input("Department Name:")
            # Division record checking loop
            division_check_loop = True
            while division_check_loop:
                self._division.view()
                division_id = input("Division  (ID): ")
                if self._db_manager.entry_checker("divisions", "id", division_id):
                    division_check_loop = False
                else:
                    print("Division ID does not exist.")
            # Employee record checking loop
            employee_check_loop = True
            while employee_check_loop:
                self._employee.view()
                employee_id = input("Department Manager (Employee ID): ")
                if self._db_manager.entry_checker("employees", "id", employee_id):
                    employee_check_loop = False
                else:
                    print("Employee ID does not exist.")
            self._db_manager.open_db()
            add_new_division_query = "INSERT INTO departments (department_name, division_id, manager_id) VALUES(?, ?, ?)"
            self._db_manager.insert_record(add_new_division_query, (department_name, division_id, employee_id), "Department")
            
        except sqlite3.Error as e:
            print(f"Error adding Department: {e}")
        finally:
            if self._db_manager._conn:
                self._db_manager.close_db()
                self.view()

class Project:
    """ A class representing an Projects with database operations. """
    def __init__(self):
        self._create_table_query = """
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY
            ,project_name TEXT NOT NULL
            )
        """
        self._create_table_query_project_assignments = """
        CREATE TABLE IF NOT EXISTS project_assignments (
            id INTEGER PRIMARY KEY
            ,project_id TINTEGER NOT NULL
            ,employee_id INTGER NOT NULL
            )
        """
        self._db_manager = DatabaseManager()
        self._db_manager.create_table(self._create_table_query)
        self._db_manager.create_table(self._create_table_query_project_assignments)
        self._employee = Employee()
    def view(self):
        """ View project records"""
        try:
            view_project_query = """
                SELECT 
                    projects.id
                    ,projects.project_name
                    ,(SELECT 
                        GROUP_CONCAT(first_name || ' ' || last_name) as member_name 
                        FROM project_assignments as pa
                        LEFT JOIN employees as emp ON pa.employee_id = emp.id 
                        WHERE pa.project_id = projects.id
                    ) as members
                FROM projects 
            """
            self._db_manager.open_db()
            self._db_manager._cursor.execute(view_project_query)
            rows = self._db_manager._cursor.fetchall()
            row_header = f"{'ID':<4} | {'Project':<30} | {'Assigned':<30}  "
            print(row_header)
            print(len(row_header) * "-")
            for row in rows:
                (row_id, row_project, row_assignment) = row
                print(f"{row_id:<4} | {row_project:<30} | {row_assignment if row_assignment != None else "":<30}")
            self._db_manager.open_db()
            print(f"Result(s): {len(rows)}")
        except sqlite3.Error as e:
            print(f"Error viewing Project: {e}")
        finally:
            if self._db_manager._conn:
                self._db_manager.close_db()
    def add_new(self):
        """ Add new project record tp the database"""
        try:
            project_name = input("Project Name: ")
            self._db_manager.open_db()
            add_new_project_query = "INSERT INTO projects (project_name) VALUES (?)"
            self._db_manager.insert_record(add_new_project_query, (project_name,), "Projects")
        except sqlite3.Error as e:
            print(f"Error adding Department: {e}")
        finally:
            if self._db_manager._conn:
                self._db_manager.close_db()
                self.view()
    def assign_project(self):
        """ Assign employee to a project"""
        try:
            self.view()
            # Check if project id exist
            project_check_loop = True
            while project_check_loop:
                project_id = input("Project ID : ")
                if self._db_manager.entry_checker("projects", "id", project_id):
                    project_check_loop = False
                else:
                    print("Project ID does not exist.")
            # Employee record checking loop
            employee_check_loop = True
            while employee_check_loop:
                self._employee.view()
                employee_id = input("Assign (Employee ID): ")
                if self._db_manager.entry_checker("employees", "id", employee_id):
                    employee_check_loop = False
                else:
                    print("Employee ID does not exist.")
            self._db_manager.open_db()
            add_new_project_query = "INSERT INTO project_assignments (project_id, employee_id) VALUES(?, ?)"
            self._db_manager.insert_record(add_new_project_query, (project_id, employee_id), "Project Assignment")
        except sqlite3.Error as e:
            print(f"Error adding Department: {e}")
        finally:
            if self._db_manager._conn:
                self._db_manager.close_db()
                self.view()

# object instance
employee = Employee()
division = Division()
department = Department()
project = Project()

program_running = True
while program_running:
    try:
        print("Main Menu:")
        # Main menu input and options based on user choice
        main_menu_input = int(input("Enter 1: Employee, 2: Division, 3: Department, 4:Project, 5: Rover, 6: Exit : "))
        if main_menu_input == 1:
            try:
                print("Employee Menu:")
                # Employee menu option
                employee_menu_loop = True
                while employee_menu_loop:
                    employee_menu_input = int(input("Enter 1: View Employee Records, 2: Add New Employee Record, 3: Back to Main Menu : "))
                    if employee_menu_input == 1:
                        employee.view()
                    elif employee_menu_input == 2:
                        employee.add_new()
                    elif employee_menu_input == 3:
                        employee_menu_loop = False
                    else:
                        print("Invalid input: Please enter 1 or 2 only.")
            except ValueError:
                print("Invalid Input: Please input numerical value only")
        elif main_menu_input == 2:
            try:
                print("Division")
                # Division menu option
                division_menu_loop = True
                while division_menu_loop:
                    division_menu_input = int(input("Enter 1: View Division Records, 2: Add New Division Record, 3: Back to Main Menu : "))
                    if division_menu_input == 1:
                        division.view()
                    elif division_menu_input == 2:
                        division.add_new()
                    elif division_menu_input == 3:
                        division_menu_loop = False
                    else:
                        print("Invalid input: Please enter 1 to 3 only.")
            except ValueError:
                print("Invalid Input: Please input numerical value only")
        elif main_menu_input == 3:
            try:
                print("Department")
                # Department menu option
                department_menu_loop = True
                while department_menu_loop:
                    department_menu_input = int(input("Enter 1: View Department Records, 2: Add New Department Record, 3: Back to Main Menu : "))
                    if department_menu_input == 1:
                        department.view()
                    elif department_menu_input == 2:
                        department.add_new()
                    elif department_menu_input == 3:
                        department_menu_loop = False
            except ValueError:
                print("Invalid Input: Please input numerical value only")
        elif main_menu_input == 4:
            try:
                print("Project")
                # project menu option
                project_menu_loop = True
                while project_menu_loop:
                    project_menu_input = int(input("Enter 1: View Project Records, 2: Add New Project Record, 3: Assign Project, 4: Back to Main Menu : "))
                    if project_menu_input == 1:
                        project.view()
                    elif project_menu_input == 2:
                        project.add_new()
                    elif project_menu_input == 3:
                        project.assign_project()
                    elif project_menu_input == 4:
                        project_menu_loop = False
            except ValueError:
                print("Invalid Input: Please input numerical value only")
        elif main_menu_input == 5:
            employee.view(True)
    except ValueError:
        print("Invalid Input: Please input numerical value only")