import sqlite3

DB = None
CONN = None

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

def connect_to_db():
    global DB, CONN
    CONN = sqlite3.connect("./hackbright.db")
    DB = CONN.cursor()
    print "connected to database"

def make_new_student(first_name, last_name, github):
    print "new_student_is_running"
    # first_name, last_name, github = arg_list
    query = """INSERT INTO Students (first_name, last_name, github) VALUES (?,?,?)"""
    print "our query is", (query, (first_name, last_name, github) )
    DB.execute(query, (first_name, last_name, github) )
    CONN.commit()


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

    CONN.close()

if __name__ == "__main__":
    main()
