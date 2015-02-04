import sqlite3

DB = None
CONN = None

def connect_to_db():
    global DB, CONN
    CONN = sqlite3.connect("./hackbright.db")
    DB = CONN.cursor()
    print "connected to database"


def get_student_by_github(github):
    # print "get_student_is_running"
    query = """SELECT first_name, last_name, github FROM Students WHERE github = ?""" 
    DB.execute(query, (github,)) 
    # print query
    # print github
    row = DB.fetchone()
    # print row     #what does the "u" mean in the raw output?
    print """\
    Student: %s %s
    Github account: %s"""%(row[0], row[1], row[2])


def make_new_student(first_name, last_name, github):
    query = """INSERT INTO Students (first_name, last_name, github) VALUES (?,?,?)"""
    DB.execute(query, (first_name, last_name, github) )
    CONN.commit()
    print "Successfully added student: %s %s" % (first_name, last_name)


def make_new_project(title, descript, max_grade):
    query = """INSERT INTO Projects (title, description, max_grade) VALUES (?,?,?)"""
    DB.execute(query, (title, descript, max_grade) )
    CONN.commit()
    print "Successfully added project: %s, %s, %s," % (title, descript, max_grade)


def view_project(project_name):
    query = """SELECT title, description from Projects where title=?""" 
    DB.execute(query, (project_name,))
    row = DB.fetchone()
    print """
    Project name: %s
    Project description: %s
    """ % (row[0], row[1])


def class_report_card():
    query = """SELECT * from ReportCardView""" 
    DB.execute(query)
    results = DB.fetchall()
    print """first_name \t last_name \t title \t grade \t max_grade_class"""
    for each_tuple in results:
        print """%s \t \t %s \t %s \t %r \t %r"""  % each_tuple


def enter_grade(first_name,last_name,project,grade):
    """Query DB if student and project exists. If they do, update the grades table with
     the input the user passed with the enter_grade command. If they don't, 
     call the make_new_student function."""

    student_query_test = """SELECT github from Students WHERE first_name=? AND last_name=?"""
     # This will return none if the student does not exist.
    results = DB.execute(student_query_test,(first_name,last_name)) 
    github_id = results.fetchone()
    
    if github_id is None:
        student_github = raw_input("This student doesn't exist. What is their Github ID, please? > ")
        make_new_student(first_name, last_name, student_github)
        github = student_github
    else:
        github = github_id[0]   #unpack the tuple (u'jhacks',)

    project_query_test = """SELECT title, description, max_grade from Projects WHERE title=?"""
    project_results = DB.execute(project_query_test, (project,))
    project_info = project_results.fetchone()

    if project_info is None:
        print "If statement ran!"
        args = raw_input("""That project does not exist yet. Please enter a project title, description, and max grade.> """)
        project_info = args.split(",") 
        make_new_project(project_info[0], project_info[1], project_info[2]) #title, descript, max_grade
        project = project_info[0]

    query_enter_grade = """INSERT INTO Grades VALUES (?,?,?)"""
    grade_results = DB.execute(query_enter_grade, (github, project, str(grade)) )
    CONN.commit()
    print "Successfully added Grade"
    class_report_card()



def main():
    connect_to_db()
    command = None
    while command != "quit":
        input_string = raw_input("HBA Database> ")
        tokens = input_string.split()
        command = tokens[0]
        args = tokens[1:]

        if command == "student":
            get_student_by_github(*args) 
        elif command == "new_student":
            print "args:",args
            make_new_student(*args)
        elif command == "view_project":
            view_project(*args)
        elif command == "class_report_card":
            class_report_card()
        elif command == "enter_grade":
            enter_grade(*args) #FirstName, LastName, ProjectTitle, Grade
        else:
            print "That is not a valid command.  Please re-enter."

    CONN.close()

if __name__ == "__main__":
    main()
