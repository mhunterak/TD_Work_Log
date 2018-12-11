"""
Python Web Development Techdegree
Project 3 - Work Log application
by Maxwell Hunter
--------------------------------
"""
import datetime
import os
import re
'''
Make sure your script runs without errors. Catch exceptions and report errors
to the user in a meaningful way. As a user of the script, I should be prompted
with a menu to choose whether to add a new entry or lookup previous entries.
As a user of the script, if I choose to enter a new work log, I should be able
to provide a task name, a number of minutes spent working on it, and any
additional notes I want to record. As a user of the script, if I choose to
find a previous entry, I should be presented with four options:

find by date
find by time spent
find by exact search
find by pattern

Note:
When finding by date, I should be presented with a list of dates with entries
and be able to choose one to see entries from.

When finding by time spent, I should be allowed to enter the number of minutes
a task took and be able to choose one to see entries from.

When finding by a pattern, I should be allowed
o enter a regular expression and then be presented with entries matching that
pattern in their task name or notes. When finding by an exact string, I should
be allowed to enter a string and then be presented with entries containing that
string in the task name or notes.
When displaying the entries, the entries should be displayed in a readable
format with the date, task name, time spent, and notes information.

Coding Style
Make sure your coding style complies with PEP 8.

Before you submit your project for review, make sure you can check off all of
the items on the Student Project Submission Checklist. The checklist is
designed to help you make sure you’ve met the grading requirements and that
your project is complete and ready to be submitted!

Extra Credit
To get an "exceeds" rating, you can expand on the project in the following
ways:
-Menu has a “quit” option to exit the program.
-Entries can be deleted and edited, letting user change the date, task name,
time spent, and/or notes.
=Entries can be searched for and found based on a date range. For example
between 01/01/2016 and 12/31/2016.
=Entries are displayed one at a time with the ability to page through records
(previous/next/back).
'''


# function for clearing the terminal console
def clear_screen():
    os.system("clear")


# function for validating user input: date
def validate_date(date):
    try:
        # split date into a list for day, month, and year
        d_list = date.split('/')
        # build a datetime date from the list
        date = datetime.date(
            int(d_list[2]),
            int(d_list[1]),
            int(d_list[0]),
            )
        # date is valid
        return True
    # if we get a ValueError,
    except (ValueError, IndexError):
        # date is invalid
        return False


# function for validating user input: time
def validate_time(minutes):
    # if the submitted input is only digits, it's allowed
    return minutes.isdigit()


# function for standardizing user input: date
def standardize_date(date):
    # split date into a list for day, month, and year
    d_list = date.split('/')
    # create datetime object from the string
    date_obj = datetime.date(
        int(d_list[2]),
        int(d_list[1]),
        int(d_list[0]),
        )
    # return the formatted string
    return date_obj.strftime("%d/%m/%Y")


# function for validating user input: name
def validate_name(name):
    # must not be blank
    return len(name)


# function for sorting the list of dictionaries (entries) by date
def sort_dict_list(dict_list):
    return sorted(
        dict_list,
        key=lambda i: i['date'])


# function for performing search and showing the results
def show_query_results(dict_list, query_type, query_selection):
    # count the number of results form the query
    count = 0
    # if query is blank
    if query_selection == "":
        # return blank
        return ""

    # loop over a sorted list

    for i, entry in enumerate(load_tasks()):

        if query_type == 'all':
            count += 1
            print('{}.) {} - {}'.format(
                entry['id'],
                entry['name'],
                entry['date'],
                )
            )
        if query_type in [
            'name',
            'notes',
            'time',
                ]:
            count += 1
            if dict_list[i][query_type] == query_selection:
                count += 1
                print_entry(dict_list[i])
        elif query_type in ['exact']:
            if (query_selection in entry['name']) or (
                    query_selection in entry['notes']):
                count += 1
                print_entry(entry)

        elif query_type in ['pattern']:
            if re.match(query_selection, entry['name']):
                count += 1
                print_entry(dict_list[i])
            elif re.match(query_selection, entry['notes']):
                count += 1
                print_entry(dict_list[i])
    if count > 0:
        select_by_id = input('Select entry by id to view > ')
        if select_by_id.isdigit():
            return select_by_id
        else:
            clear_screen()
            input("Invalid Selection. ")
            return ""
    else:
        input('No Search Results found.')
        return ""


def print_entry(entry):
    print('{}.) {} ({}) - {}'.format(
        entry['id'],
        entry['name'],
        entry['date'],
        entry['time'],
        )
    )


def get_number_of_tasks():
    return len(load_tasks())


# TASK CRUD: create task
def new_task():
    clear_screen()
    valid_date = False
    while valid_date is False:
        date = input("Enter your date for this task now, 'dd/mm/yyyy' > ")
        valid_date = validate_date(date)
        if valid_date:
            date = standardize_date(date)
        else:
            print("Invalid date. please try again.")

    valid_time = False
    while valid_time is False:
        # a number of minutes spent working on it, and any
        time = input("Minutes spent working on it > ")
        valid_time = validate_time(time)
        if not valid_time:
            print("Please enter Minutes spent in whole integers")

    # I should be able to provide a task name,
    name = ""
    while not validate_name(name):
        name = input("New Task Name > ")
        if not len(name):
            print("Name may not be blank.")

    # additional notes I want to record.
    # is not required, so does not require valifation
    notes = input("Enter any additional notes > ")
    if not len(notes):
        notes = " "
    id = 1
    for entry in load_tasks():
        if int(entry['id']) == id:
            id = int(entry['id']) + 1
    db_string = str(id) + "||" + date + '||' + time + '||' + name + '||' + notes + """<|
"""
    with open("worklog.txt", 'a+') as wl:
        wl.write(db_string)


# TASK CRUD: recall task
def load_tasks():
    try:
        with open("worklog.txt", 'r') as wl:
            existing_entries = wl.read()
            entries_list = existing_entries.split("""<|
""")
            entries_list.pop(-1)
            dict_list = []
            for i, entry in enumerate(entries_list):
                entry_dict = {}
                entry_list = entry.split('||')
                entry_dict['id'] = entry_list[0]
                entry_dict['date'] = entry_list[1]
                entry_dict['time'] = entry_list[2]
                entry_dict['name'] = entry_list[3]
                entry_dict['notes'] = entry_list[4]
                dict_list.append(entry_dict)
            return sort_dict_list(dict_list)
    except OSError:
        print("Work log not found. 0 entries available.")
        return []


# TASK CRUD: UPDATE TASKS
# (save list of tasks)
def save_tasks(dict_list):
    dict_list = sort_dict_list(dict_list)
    db_string = ""
    for dictionary in dict_list:
        id = dictionary['id']
        date = dictionary['date']
        time = dictionary['time']
        name = dictionary['name']
        notes = dictionary['notes']
        db_string += id + '||' + date + '||' + time + '||' + name + '||' + notes + """<|
"""
    with open("worklog.txt", 'w') as wl:
        wl.write(db_string)


def edit_task(dict_list, select_by_id):
    for entry in dict_list:
        if entry['id'] == select_by_id:
            date_input = input(
                'Enter new date (currently {}) > '.format(
                    entry['date']
                )
            )
            entry['date'] = standardize_date(date_input)

            time_input = input(
                'Enter new time (currently {} minutes) > '.format(
                    entry['time']))
            if validate_time(time_input):
                entry['time'] = time_input

            name_input = input(
                'Enter new name (currently {}) > '.format(
                    entry['name']))
            if validate_name(name_input):
                entry['name'] = name_input

            entry['notes'] = input(
                'Enter new notes (currently {}) > '.format(
                    entry['notes']))
            break

    print("Post Updated.")
    save_tasks(dict_list)
    return dict_list


# TASK CRUD - DELETE TASK
def delete_task(dict_list, select_by_id):
    for i, dictionary in enumerate(dict_list):
        if dictionary['id'] == select_by_id:
            dict_list.pop(i)
    input('Post #{} deleted.'.format(select_by_id))
    save_tasks(dict_list)
    return dict_list


# MVC View - main menu
def main_menu():
    menu_selection = ""
    # I should be prompted
    # with a menu to choose whether to add a new entry or lookup
    # previous entries. As a user of the script,
    clear_screen()
    print("--------")
    print("MAIN MENU")
    print("--------")
    number_of_tasks = get_number_of_tasks()
    print("[N]ew Entry")
    if number_of_tasks:
        print("[L]ookup previous entry")
    print("[Q]uit")
    print("At any time, enter blank input to go back one menu level")

    print()
    menu_selection = input("Enter your selection now > ")

    if menu_selection not in ['n', 'l', 'q']:
        clear_screen()
        input("invalid selection.")

    # if I choose to enter a new work log,
    elif menu_selection.lower() == 'n':
        new_task()
    # As a user of the script, if I choose to find a previous entry,
    if menu_selection.lower() == 'l':
        if get_number_of_tasks():
            lookup_menu(load_tasks())
    # EXTRA CREDIT: quit program
    if menu_selection.lower() == 'q':
        print("Thanks, bye!")
        quit()


# submenu under main_menu
def lookup_menu(dict_list):
    while True:
        query_selection = ""
        clear_screen()
        print("--------")
        print("LOOKUP MENU")
        print("--------")
        print("{} available entries.".format(get_number_of_tasks()))
        print()
        # I should be presented with four options:

        # find by date
        print("Find old entry by [D]ate")
        # find by time spent
        print("Find old entry by [T]ime Spent")
        # find by exact search
        print("Find old entry by [E]xact Search")
        # find by pattern
        print("Find old entry by regex [P]attern")

        print()
        # back to main menu
        menu_selection = input("Enter your selection now > ")
        clear_screen()

        # return to the previous menu
        if menu_selection == '':
            break

        if menu_selection not in ['d', 't', 'e', 'p']:
            input("invalid selection.")
            continue

        elif menu_selection[0].lower() == 'd':
            select_by_id = show_query_results(
                dict_list, 'all', 'd')

        elif menu_selection[0].lower() == 't':
            # ask for time spent
            query_selection = input(
                "Enter your time spent query in number of minutes > ")
            select_by_id = show_query_results(
                dict_list, 'time', query_selection)

        elif menu_selection[0].lower() == 'e':
            # ask for exact search
            query_selection = input(
                "Enter your exact search now > ")
            select_by_id = show_query_results(
                dict_list, 'exact', query_selection)

        elif menu_selection[0].lower() == 'p':
            # ask for pattern
            query_selection = input("Enter your regex pattern now > ")
            select_by_id = show_query_results(
                dict_list, 'pattern', query_selection)
        if not select_by_id.isdigit():
            continue
        if int(select_by_id) > (get_number_of_tasks()):
            clear_screen()
            input("Invalid task id.")
            continue
        if select_by_id != "":
            clear_screen()
            count = 0
            for entry in dict_list:
                if entry['id'] == select_by_id:
                    count += 1
                    print("{}.) {}".format(
                        entry['id'],
                        entry['name'],
                        ))
                    print('Date: {}'.format(
                        entry['date']
                        )
                    )
                    print('{} minutes spent'.format(
                        entry['time']
                        )
                    )
                    print('notes: {}'.format(
                        entry['notes']
                        )
                    )
            if count > 0:
                edit_delete_input = input(
                    'Would you like to [E]dit or [D]elete this post? > ')
                if edit_delete_input.lower() == 'd':
                    dict_list = delete_task(dict_list, select_by_id)
                    break
                elif edit_delete_input.lower() == 'e':
                    dict_list = edit_task(dict_list, select_by_id)
                    break
                elif edit_delete_input == "":
                    continue
                else:
                    clear_screen()
                    input('Invalid Selection. ')
                    continue
            query_selection = ''
        else:
            continue
    return True


if __name__ == "__main__":
    while True:
        main_menu()
