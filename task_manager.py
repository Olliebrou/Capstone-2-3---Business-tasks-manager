#=====importing libraries===========
# Need datetime to get today's date
from datetime import datetime, date


#======Functions=========
def get_users():
    """fetches a current dictionary of users and passwords"""
    users = {}
    with open('user.txt', 'r') as f:
        for line in f:
            line = line.strip()
            line = line.split(", ")
            users.update({line[0]: line[1]})
    return(users)

# It checks if new username exists already
# If it doesnt exist, a password is requested and then confirmed
# The new user and password is then appended to user.txt
def reg_user():
    """Adds new user to user file"""
    print("\t CREATING NEW USER\n\n")
    while True:
        new_username = input("Enter a new username\t")
        if new_username in get_users():
            print("User already registered\nPlease register a new user")
            continue
        password = input("Please enter a new password\t")
        if password == input("Please confirm password\t"):
            with open('user.txt', 'a') as f:
                f.write(f"\n{new_username}, {password}")
                print("\nUSER SUCCESSFULLY ADDED\n")
            break
        else:
            print("Passwords do not match. Please try again")

# The user is asked to enter information about the task
# The information is added to a string in the specified format
# The new task string is appended to the tasks.txt file
def add_task():
    """Adds new task to task file in correct format"""
    print("\tADDING NEW TASK\n\n")
    while True:
        username = input("Enter the username the task will be assigned to\t")
        if username in get_users():
            new_task = "\n" + username
            new_task += ", " + input("Enter the title of the task\t")
            new_task += ", " + input("Enter a description of the task\t")
            today = date.today()
            new_task += today.strftime(", %d %b %Y")
            new_task += ", " + input("Enter the due date of the task e.g 23 Sep 2022\t") + ", No"
            with open('tasks.txt', 'a') as f:
                f.write(new_task)
            print("TASKS SUCCESSFULLY ADDED\n")
            break
        else:
            print("Username not found")

def task_print(line):
    """Prints out task in an easy to read format"""
    line = line.split(", ")
    print(f"""_______________________________________________________________________
                                                                
    Task:           {line[1]}
    Assigned to:    {line[0]}
    Date Assigned:  {line[3]}
    Due Date:       {line[4]}
    Task Complete?  {line[5]}
    Task Description:
    {line[2]}

______________________________________________________________________\n""")

# View all function that sends each line of tasks.txt to task_print function
def view_all():
    """Sends all tasks from tasks file to task_print function"""
    with open('tasks.txt', 'r') as f:
        for line in f:
            task_print(line)

# View my function sends only tasks associated to logged-in username to task_print
# The tasks are added to 'lines' list
# Each task is printed with a task number above
# If the user wants to change a task, the task user or due date is requested
# These changes are made to 'lines' list and then overwritten to tasks.txt
def view_mine(username):
    """Allows user to see all their assigned tasks and edit them individually"""
    f = open('tasks.txt', 'r+')
    lines = f.readlines()
    f.close()
    task_number = 1
    for line in lines:
        if username == line.split(", ")[0]:
            print(f"TASK NUMBER: {task_number}")
            task_print(line)
        task_number += 1
    task_number = int(input("""Enter task number to edit task or mark as complete
Enter '-1' to return to menu\t"""))
    if task_number != -1:
        task = lines[task_number-1]  # This is the task user wants to edit
        task = task.split(", ")
        choice = input("Enter 'e' to edit task or 'm' to mark as complete\t").lower()
        if choice == "e":
            if task[5] == "No\n":  # Checking task is not complete
                choice = input("Enter 'user' to change who the task is assigned to or 'due' to change due date\t")
                if choice == "user":
                    task[0] = input("Please enter a new username assignment\t")
                    print("Task user assingment succefully changed\n")
                elif choice == "due":
                    task[4] = input("Enter new due date e.g 24 Sep 2020\t")
                    print("Task due date succesfully changed\n")
            else:
                print("Task already complete\n")
        elif choice == "m":
            if input("Would you like to mark this task as complete? 'yes' or 'no'") == "yes":
                task[-1] = "Yes\n"
                print("Task marked as complete\n")
        with open("tasks.txt", 'w') as f:
            lines[task_number-1] = ", ".join(task)  # Replacing old task with edited task
            f.writelines(lines)

def generate():
    """Generates report in text files of user and task statistics"""
    total = 0
    comp = 0
    uncomp = 0
    overdue = 0
    f = open("tasks.txt", 'r')
    tasks = f.readlines()
    for x in range(len(tasks)):
        tasks[x] = tasks[x].split(", ")
    for i in tasks:                    # Looping through tasks and adding to each count depending on task completeness
        if i[-1] == "No\n":
            uncomp += 1
            if datetime.strptime(i[4],'%d %b %Y' ) < datetime.today(): # Using datetime objects to compare dates
                overdue += 1
        else:
            comp += 1
        total += 1
    f.close()
    if uncomp == 0:
        uncomp_percent = 0     # Making sure program does not divide by zero
    else:
        uncomp_percent = round((uncomp / total *100),2)
    if overdue == 0:
        overdue_percent = 0
    else:
        overdue_percent = round((overdue /total *100),2)
    with open("task_overview.txt", 'w') as f:
        f.write(f"""Total tasks: {total}
Completed tasks: {comp}
Uncompleted tasks: {uncomp}
Overdue uncompleted tasks: {overdue}
Percentage uncompleted tasks: {uncomp_percent}%
Percentage overdue tasks: {overdue_percent}%\n""")

        with open("user_overview.txt", 'w') as f:
            f.write(f"Total tasks: {total}\n")
            for user in get_users():                #Looping through users
                user_tasks = 0                      # Declaring varibles in for loop so they reset for each user
                comp = 0 
                uncomp = 0
                overdue = 0
                for task in tasks:                  # Looping through tasks
                    if task[0] == user:             # Checking if task is assigned to user
                        user_tasks += 1             # Adding to count if it is assigned to user in current loop
                        if task[-1] == "Yes\n":
                            comp += 1
                        else:
                            uncomp += 1
                            if datetime.strptime(task[4],'%d %b %Y' ) < datetime.today():
                                overdue += 1
                if user_tasks == 0:
                    p_usertasks = 0
                else:
                    p_usertasks = round((user_tasks/total * 100),2)
                if comp == 0:
                    p_comp = 0
                else:
                    p_comp = round((comp/user_tasks * 100),2)
                if uncomp == 0:
                    p_uncomp = 0
                else:
                    p_uncomp = round((uncomp/ user_tasks * 100),2)
                if overdue == 0:
                    p_overdue = 0
                else:
                    p_overdue = round((overdue/ user_tasks * 100),2)
                f.write(f"""\n{user}
                Total tasks for user: {user_tasks}
                Percentage of total tasks assigned to user: {p_usertasks}%
                Percentage of user tasks completed: {p_comp}%
                Percentage of user tasks uncompleted: {p_uncomp}%
                Percentage of user tasks overdue: {p_overdue}%\n""")
    
#====Login Section====
# Here the username is entered and checked against users dictionary
# If the username is valid, a password is requested and checked
# Only when both are correct is the loop broken
while True:
    username = input("Please enter your username:\t")
    if username in get_users():
        password = input("Please enter your password\t")
        if password == get_users()[username]:
            print("\nLOGIN SUCCESSFUL\n")
            break
        else:
            print(f"Password incorrect for {username}\n")
    else:
        print("Username not found\n")

while True:
# presenting the menu to the user and
# making sure that the user input is coneverted to lower case.
    if username == "admin":
        menu = input('''Select one of the following Options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - View my task
gr - Generate report
ds - Display statistics
e - Exit
    : ''').lower()
    else:
        menu = input('''Select one of the following Options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - view my task
e - Exit
: ''').lower()

    if menu == 'r' and username == "admin":
        reg_user()

    elif menu == 'a':
        add_task()

    elif menu == 'va':
        view_all()

    elif menu == 'vm':
        view_mine(username)

    elif menu == 'gr':
        generate()
        print("Report generated\n")

    elif menu == 'ds':
        generate()
        with open("user_overview.txt", 'r') as f:
            print("USER STATISTCS\n_______________________________________")
            for line in f:
                print(line)
        with open("task_overview.txt", 'r') as f:
            print("TASK STATISTCS\n_______________________________________")
            for line in f:
                print(line)

    elif menu == 'e':
        print('Goodbye!!!')
        exit()

    else:
        print("You have made a wrong choice, Please Try again")
