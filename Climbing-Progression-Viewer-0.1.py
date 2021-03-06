from tkinter import *
import sqlite3
from tkinter import messagebox

global city_entry
global sector_entry
global route_entry
global ascent_entry
global style_entry
global grade_entry
global comment_entry

global city_entry_edit
global sector_entry_edit
global route_entry_edit
global ascent_entry_edit
global style_entry_edit
global grade_entry_edit
global comment_entry_edit
global input_id_entry
global edit_window
global connection
global cursor

ascents_list_id = []


def formatting_input_data(info_list):
    formatted_info = f"City:{info_list[0]}, " \
                     f"Sector: {info_list[1]}, " \
                     f"Route: {info_list[2]}, " \
                     f"Ascent: {info_list[3]}," \
                     f" Grade: {info_list[5]}, " \
                     f"Comment: {info_list[6]}, " \
                     f"ID: {info_list[7]} \n"
    return formatted_info


# function too see if we have records in our ascent's list
def check_for_records():
    global connection
    global cursor
    # Creating db
    connection = sqlite3.connect("Climbing progression data.db")
    # Creating our cursor
    cursor = connection.cursor()
    cursor.execute("SELECT oid FROM climbing_info")
    # result will give us list. If our records are empty the result list will be empty.
    results = cursor.fetchall()
    connection.commit()
    connection.close()
    # if results list is not empty we can open our view ascents view
    if results:
        return True
    # if result list is empty return false
    return False


# function to make sure that we have such ID in our database
def check_for_element_in_db(number):
    global connection
    global cursor
    # Creating db
    connection = sqlite3.connect("Climbing progression data.db")
    # Creating our cursor
    cursor = connection.cursor()
    cursor.execute("SELECT oid FROM climbing_info")

    results = cursor.fetchall()
    number = int(number)
    for result in results:
        ascents_list_id.append(result[0])
    connection.commit()
    connection.close()

    if number in ascents_list_id:
        ascents_list_id.clear()
        return True
    return False


# function behind our delete ascent button
def delete_ascent():
    global connection
    global cursor
    record_id = input_id_entry.get()
    if record_id:
        if check_for_element_in_db(record_id):
            response = messagebox.askyesno("Warning",
                                           f"You are going to permanently delete\nascent with ID num: "
                                           f"{input_id_entry.get()}.\nAre you sure you want to do this?")
            if response:
                # Creating db
                connection = sqlite3.connect("Climbing progression data.db")
                # Creating our cursor
                cursor = connection.cursor()

                cursor.execute("DELETE from climbing_info WHERE oid = " + input_id_entry.get())

                connection.commit()
                connection.close()

                input_id_entry.delete(0, END)
        else:
            messagebox.showinfo("Error", "There is no such ID in the records!!\nTry with another ID")
    else:
        messagebox.showinfo("Error", "You have to add ascent's ID.\nClick see records to get the ID number.")


# function that save the changes when we hit the save changes button in our edit view
def save_info_from_add_ascent():
    global city_entry_edit
    global sector_entry_edit
    global route_entry_edit
    global ascent_entry_edit
    global style_entry_edit
    global grade_entry_edit
    global comment_entry_edit
    global input_id_entry
    global edit_window
    global connection
    global cursor
    if city_entry_edit.get() and sector_entry_edit.get() and route_entry_edit.get() and \
            ascent_entry_edit.get() and style_entry_edit.get() and grade_entry_edit.get():
        # Creating db
        connection = sqlite3.connect("Climbing progression data.db")
        # Creating our cursor
        cursor = connection.cursor()
        record_id = input_id_entry.get()
        # this is the way to update db in sql3
        cursor.execute("""UPDATE climbing_info SET
                        city = :city,
                        sector = :sector,
                        route = :route,
                        ascent = :ascent,
                        style = :style,
                        grade = :grade,
                        comment = :comment
                        WHERE oid = :oid""",
                       {"city": city_entry_edit.get(),
                        "sector": sector_entry_edit.get(),
                        "route": route_entry_edit.get(),
                        "ascent": ascent_entry_edit.get(),
                        "style": style_entry_edit.get(),
                        "grade": grade_entry_edit.get(),
                        "comment": comment_entry_edit.get(),
                        "oid": record_id
                        })

        connection.commit()
        connection.close()
        close_window(edit_window)
    else:
        messagebox.showinfo("Notification", "You have empty fields!!")


# function to make sure that we filled all the fields needed to add new ascent.


# We make sure to ask for confirmation to delete
# function behind our clear_history_button. It will clear all of our data.
def clear_all_ascents_from_history(wnd):
    global connection
    global cursor
    response = messagebox.askokcancel("Confirmation", "You are going to permanently delete your history." "\n"
                                                      "Are you sure you want to do this?")
    if response:
        # Creating db
        connection = sqlite3.connect("Climbing progression data.db")
        # Creating our cursor
        cursor = connection.cursor()

        cursor.execute("DELETE from climbing_info")

        # Commit changes to our db
        connection.commit()
        # Closing our db
        connection.close()
        messagebox.showinfo("Notification", "Your history is clear !!")
        close_window(wnd)


# function to use when we want to destroy some window
def close_window(window1):
    window1.destroy()


# function to add the current record to our records when we hit the add button
def adding_record():
    global city_entry
    global sector_entry
    global route_entry
    global ascent_entry
    global style_entry
    global grade_entry
    global comment_entry
    global connection
    global cursor
    # using function to make sure that we filled the all the entry to add ascent
    if city_entry.get() and sector_entry.get() and route_entry.get() \
            and ascent_entry.get() and style_entry.get() and grade_entry.get():
        # Creating db
        connection = sqlite3.connect("Climbing progression data.db")
        # Creating our cursor
        cursor = connection.cursor()

        cursor.execute(
            "INSERT INTO climbing_info VALUES (:city_name, :sector, :route, :ascent, :style, :grade, :comment)",
            {
                "city_name": city_entry.get(),
                "sector": sector_entry.get(),
                "route": route_entry.get(),
                "ascent": ascent_entry.get(),
                "style": style_entry.get(),
                "grade": grade_entry.get(),
                "comment": comment_entry.get()
            })

        # Commit changes to our db
        connection.commit()
        # Closing our db
        connection.close()
        # after we add some record we want to delete the data from our entry_boxes
        city_entry.delete(0, END)
        sector_entry.delete(0, END)
        route_entry.delete(0, END)
        ascent_entry.delete(0, END)
        style_entry.delete(0, END)
        grade_entry.delete(0, END)
        comment_entry.delete(0, END)
        # popup message to tell the user he added new ascent
        messagebox.showinfo("Added ascent", "New ascent added")
    # if some entry is not filled we put popup message to explain to the user what is the problem
    else:
        messagebox.showinfo("Notification", "You have empty fields!!")


# creating function that open new window when we hit the review ascent button.
def render_review_wanted_ascent():
    global connection
    global cursor

    record_id = input_id_entry.get()
    if record_id:
        if check_for_element_in_db(record_id):
            review_ascent = Tk()
            # see_data_window.geometry("500x500")
            review_ascent.title("Review ascent")
            review_ascent.attributes("-topmost", True)
            # Creating db

            connection = sqlite3.connect("Climbing progression data.db")
            # Creating our cursor

            cursor = connection.cursor()
            cursor.execute("SELECT *, oid FROM climbing_info WHERE oid = " + record_id)
            results = cursor.fetchall()

            for result in results:
                label = Label(review_ascent, text=formatting_input_data(result), font=25)

                label.grid(row=0, column=0)

            connection.commit()
            connection.close()
            # if we don't have such ID in our records we put popup message to explain to the user what is wrong
        else:
            messagebox.showinfo("Error", "There is no such ID in the records!!\nTry with another ID")

    # if we don't have filled id_entry from our user we put popup message to inform the user what is happening
    else:
        messagebox.showinfo("Error", "You have to add ascent's ID.\nClick see records to get the ID number.")


# functionality behind our show all ascents button
def render_show_all_records():
    global connection
    global cursor

    # crating our sll records view
    all_results_window = Tk()
    all_results_window.title("All records")
    all_results_window.attributes("-topmost", True)

    # creating scrollbar so that we can scroll in our window if we need to
    scrollbar = Scrollbar(all_results_window)
    # I don't know why but with grid is not working?
    scrollbar.pack(side=RIGHT, fill=Y)
    # Creating listbox that will contain all the records we have, yscrollcommand is like command and
    # .set is the method that we use to attach the scrollbar to the listbox
    all_results_listbox = Listbox(all_results_window, font=20, yscrollcommand=scrollbar.set)

    # Creating db
    connection = sqlite3.connect("Climbing progression data.db")

    # Creating our cursor
    cursor = connection.cursor()

    # we select everything from climbing_info table and oid
    cursor.execute("SELECT *, oid FROM climbing_info")

    # record is list that contains all our records info
    # this loop is mainly for formatting
    records = cursor.fetchall()
    for record in records:
        record = f" ID num: {record[7]} " \
                 f"Route: {record[2]}," \
                 f" Date: {record[3]}," \
                 f" Style: {record[4]}," \
                 f" Grade: {record[5]}"

        all_results_listbox.insert(END, record)

    # i don't know why but with grid is not working?
    all_results_listbox.pack(side=LEFT, fill=BOTH, expand=True, ipadx=200)

    # config method to give functionality to our scrollbar
    scrollbar.config(command=all_results_listbox.yview)
    all_results_window.mainloop()

    connection.commit()
    connection.close()


# function behind our top_point_info_button.
def render_get_top_rope_info():
    global connection
    global cursor

    # this is list that will be full of RP ascents(tuples)
    list_with_top_ropes = []
    top_rope_info_window = Tk()
    # see_data_window.geometry("500x500")
    top_rope_info_window.title("Red Point info")
    top_rope_info_window.attributes("-topmost", True)

    # creating scrollbar so that we can scroll in our window if we need to
    scrollbar = Scrollbar(top_rope_info_window)
    # I don't know why but with grid is not working?
    scrollbar.pack(side=RIGHT, fill=Y)
    # Creating listbox that will contain all the records we have, yscrollcommand is like command and
    # .set is the method that we use to attach the scrollbar to the listbox
    all_results_listbox = Listbox(top_rope_info_window, font=20, yscrollcommand=scrollbar.set)

    # Creating db
    connection = sqlite3.connect("Climbing progression data.db")
    # Creating our cursor
    cursor = connection.cursor()

    # we select all from our table
    cursor.execute("SELECT *, oid FROM climbing_info")
    results = cursor.fetchall()

    # for loop to go thru each one RP ascent that we found
    for result in results:
        # We search for "TR" or "tr" in our tuples. If we find it in some tuple we add it to our list with tuples
        if 'TR' in result or "tr" in result:
            list_with_top_ropes.append(result)

    label_for_rp_count = Label(top_rope_info_window, text=f"You have {len(list_with_top_ropes)} top rope ascents:")
    label_for_rp_count.pack()

    for top_rope in list_with_top_ropes:
        # this is our formatting. That's how the user will see the RP ascents
        all_results_listbox.insert(END, formatting_input_data(top_rope))
        print(formatting_input_data(top_rope))

    # i don't know why but with grid is not working?
    all_results_listbox.pack(side=LEFT, fill=BOTH, expand=True, ipadx=200)

    # config method to give functionality to our scrollbar
    scrollbar.config(command=all_results_listbox.yview)



    connection.commit()
    connection.close()
    top_rope_info_window.mainloop()


# function behind our red_point_info_button.
def render_get_red_point_info():
    global connection
    global cursor

    # this is list that will be full of RP ascents(tuples)
    list_with_red_points = []
    red_point_info_window = Tk()
    # see_data_window.geometry("500x500")
    red_point_info_window.title("Red Point info")
    red_point_info_window.attributes("-topmost", True)

    # creating scrollbar so that we can scroll in our window if we need to
    scrollbar = Scrollbar(red_point_info_window)
    # I don't know why but with grid is not working?
    scrollbar.pack(side=RIGHT, fill=Y)
    # Creating listbox that will contain all the records we have, yscrollcommand is like command and
    # .set is the method that we use to attach the scrollbar to the listbox
    all_results_listbox = Listbox(red_point_info_window, font=20, yscrollcommand=scrollbar.set)

    # Creating db
    connection = sqlite3.connect("Climbing progression data.db")

    # Creating our cursor
    cursor = connection.cursor()

    # we select all from our table
    cursor.execute("SELECT *, oid FROM climbing_info")
    results = cursor.fetchall()

    # for loop to go thru each one RP ascent that we found
    for result in results:
        # We search for "RP" in our tuples. If we find "RP" in some tuple we add it to our list with tuples
        if 'RP' in result or "rp" in result:
            list_with_red_points.append(result)

    label_for_rp_count = Label(red_point_info_window, text=f"You have {len(list_with_red_points)} red point ascents:")
    label_for_rp_count.pack()

    # list to be filled with our formatted info about RP ascents

    for red_point in list_with_red_points:
        # this is our formatting. That's how the user will see the RP ascents
        all_results_listbox.insert(END, formatting_input_data(red_point))

    # i don't know why but with grid is not working?
    all_results_listbox.pack(side=LEFT, fill=BOTH, expand=True, ipadx=200)

    # config method to give functionality to our scrollbar
    scrollbar.config(command=all_results_listbox.yview)

    connection.commit()
    connection.close()
    red_point_info_window.mainloop()


# creating function to open edit_view window.
def render_edit_ascent_view():
    global city_entry_edit
    global sector_entry_edit
    global route_entry_edit
    global ascent_entry_edit
    global style_entry_edit
    global grade_entry_edit
    global comment_entry_edit
    global input_id_entry
    global edit_window
    global connection
    global cursor
    record_id = input_id_entry.get()
    # we make if statement to see if we have smt in our add_id_entry

    if record_id:
        # if the user added some number to the add_id_entry we check if the current id exist in our records

        if check_for_element_in_db(input_id_entry.get()):
            # if the id number from our user input is valid we create our edit view

            edit_window = Tk()
            edit_window.title("Edit ascent")
            edit_window.geometry("400x400")
            edit_window.attributes("-topmost", True)

            # Creating db

            connection = sqlite3.connect("Climbing progression data.db")
            # Creating our cursor

            cursor = connection.cursor()
            cursor.execute("SELECT * FROM climbing_info WHERE oid = " + record_id)

            # labels for our entry boxes in edit view
            city_label_edit = Label(edit_window, text="City:")
            city_label_edit.grid(row=0, column=0, padx=7, pady=4, sticky=W)
            sector_label_edit = Label(edit_window, text="Sector:")
            sector_label_edit.grid(row=1, column=0, padx=7, pady=4, sticky=W)
            route_label_edit = Label(edit_window, text="Route:")
            route_label_edit.grid(row=2, column=0, padx=7, pady=4, sticky=W)
            ascent_label_edit = Label(edit_window, text="Ascent:")
            ascent_label_edit.grid(row=3, column=0, padx=7, pady=4, sticky=W)
            style_label_edit = Label(edit_window, text="Style:")
            style_label_edit.grid(row=4, column=0, padx=7, pady=4, sticky=W)
            grade_label_edit = Label(edit_window, text="Grade:")
            grade_label_edit.grid(row=5, column=0, padx=7, pady=4, sticky=W)
            comment_label_edit = Label(edit_window, text="Comment:")
            comment_label_edit.grid(row=6, column=0, padx=7, pady=4, sticky=W)

            # creating our entry boxes in edit view
            city_entry_edit = Entry(edit_window, width=40, borderwidth=2)
            city_entry_edit.grid(row=0, column=1, pady=10, padx=10)
            sector_entry_edit = Entry(edit_window, width=40, borderwidth=2)
            sector_entry_edit.grid(row=1, column=1, pady=10)
            route_entry_edit = Entry(edit_window, width=40, borderwidth=2)
            route_entry_edit.grid(row=2, column=1, pady=10)
            ascent_entry_edit = Entry(edit_window, width=40, borderwidth=2)
            ascent_entry_edit.grid(row=3, column=1, pady=10)
            style_entry_edit = Entry(edit_window, width=40, borderwidth=2)
            style_entry_edit.grid(row=4, column=1, pady=10)
            grade_entry_edit = Entry(edit_window, width=40, borderwidth=2)
            grade_entry_edit.grid(row=5, column=1, pady=10)
            comment_entry_edit = Entry(edit_window, width=40, borderwidth=2)
            comment_entry_edit.grid(row=6, column=1, pady=10)

            # we create button to save the changes that we've made
            save_changes_button = Button(edit_window, text="Save changes", borderwidth=4,
                                         command=save_info_from_add_ascent)
            save_changes_button.grid(row=7, column=1, pady=10, padx=10, ipadx=80, columnspan=2)

            # creating button to cancel edit_process
            cancel_edit_button = Button(edit_window, text="Cancel", borderwidth=4,
                                        command=lambda: close_window(edit_window))
            cancel_edit_button.grid(row=8, column=1, pady=10, padx=10, ipadx=99, columnspan=2)

            # that's how we import the existing info for the ascent in our entry boxes in edit view
            records = cursor.fetchall()
            for record in records:
                city_entry_edit.insert(0, record[0])
                sector_entry_edit.insert(0, record[1])
                route_entry_edit.insert(0, record[2])
                ascent_entry_edit.insert(0, record[3])
                style_entry_edit.insert(0, record[4])
                grade_entry_edit.insert(0, record[5])
                comment_entry_edit.insert(0, record[6])
            connection.commit()
            connection.close()

        # if we don't have such ID in our records we put popup message to explain to the user what is wrong
        else:
            messagebox.showinfo("Error", "There is no such ID in the records!!\nTry with another ID")

    # if we don't have filled id_entry from our user we put popup message to inform the user what is happening
    else:
        messagebox.showinfo("Error", "You have to add ascent's ID.\nClick see records to get the ID number.")


# function for rendering option window
def render_view_ascents_options_view():
    global input_id_entry
    if check_for_records():
        see_data_window = Tk()
        see_data_window.title("Climbing data")
        see_data_window.attributes("-topmost", True)

        # all ascents button
        # TODO CHECK WHAT YOU HAVE DONE HERE !!!
        show_all_ascents_button = Button(see_data_window, text="All ascents", width=11, borderwidth=4,
                                         command=render_show_all_records)
        show_all_ascents_button.grid(row=0, column=0, pady=10, padx=10)

        # we create button to review what we pick from the dropdown menu. The value is in our StringVar variable
        button_for_review = Button(see_data_window, text="Review ascent", borderwidth=4,
                                   command=render_review_wanted_ascent)
        button_for_review.grid(row=0, column=1, pady=10, padx=10)

        # creating button to close the window
        close_window_button = Button(see_data_window, text="Close window", borderwidth=4,
                                     command=lambda: close_window(see_data_window))
        close_window_button.grid(row=4, column=1, pady=10, padx=10)
        # creating buttons for info
        check_info_for_rp_btn = Button(see_data_window, text="Red Point info", width=10, borderwidth=4,
                                       command=render_get_red_point_info)
        check_info_for_rp_btn.grid(row=3, column=0, pady=10, padx=10, ipadx=3)

        check_info_for_tp_btn = Button(see_data_window, text="Top Rope info", width=10, borderwidth=4,
                                       command=render_get_top_rope_info)
        check_info_for_tp_btn.grid(row=3, column=1, pady=10, padx=10, ipadx=3)

        # creating edit button
        button_for_edit = Button(see_data_window, text="Edit ascent", width=11, borderwidth=4,
                                 command=render_edit_ascent_view)
        button_for_edit.grid(row=2, column=0, pady=10, padx=10)

        # creating label for ascent's id
        input_id_label = Label(see_data_window, text="Enter ID:", width=10, borderwidth=4)
        input_id_label.grid(row=1, column=0, pady=10, padx=10)

        # creating entry field to get the input id that the user will want to work with
        input_id_entry = Entry(see_data_window, width=13, borderwidth=4)
        input_id_entry.grid(row=1, column=1, pady=10, padx=10)

        # creating button for deleting ascent
        delete_ascent_button = Button(see_data_window, text="Delete ascent", width=11, borderwidth=4,
                                      command=delete_ascent)
        delete_ascent_button.grid(row=2, column=1, pady=10, padx=10)

        # creating button to delete all history
        clear_all_ascents_btn = Button(see_data_window, text="Delete history", width=11, borderwidth=4, bg="#ff5c5c",
                                       command=lambda: clear_all_ascents_from_history(see_data_window))
        clear_all_ascents_btn.grid(row=4, column=0, pady=10, padx=10)

        see_data_window.mainloop()
    else:
        messagebox.showinfo("Error", "There is no ascents to be shown.")


def render_add_ascent_window():
    # creating our add ascent window
    add_data_window = Tk()
    add_data_window.geometry("400x400")
    add_data_window.title("Add data")
    # we make sure its pinned to the top of the screen
    add_data_window.attributes("-topmost", True)
    # function where we add all the widgets that we need to our add ascent window
    global city_entry
    global sector_entry
    global route_entry
    global ascent_entry
    global style_entry
    global grade_entry
    global comment_entry

    # labels for our entry boxes in add ascent view
    city_label = Label(add_data_window, text="City:")
    city_label.grid(row=0, column=0, padx=7, pady=4, sticky=W)
    sector_label = Label(add_data_window, text="Sector:")
    sector_label.grid(row=1, column=0, padx=7, pady=4, sticky=W)
    route_label = Label(add_data_window, text="Route:")
    route_label.grid(row=2, column=0, padx=7, pady=4, sticky=W)
    ascent_label = Label(add_data_window, text="Ascent:")
    ascent_label.grid(row=3, column=0, padx=7, pady=4, sticky=W)
    style_label = Label(add_data_window, text="Style:")
    style_label.grid(row=4, column=0, padx=7, pady=4, sticky=W)
    grade_label = Label(add_data_window, text="Grade:")
    grade_label.grid(row=5, column=0, padx=7, pady=4, sticky=W)
    comment_label = Label(add_data_window, text="Comment:")
    comment_label.grid(row=6, column=0, padx=7, pady=4, sticky=W)

    # creating our entry boxes for our add ascent view
    city_entry = Entry(add_data_window, width=40, borderwidth=2)
    city_entry.grid(row=0, column=1, pady=10)
    sector_entry = Entry(add_data_window, width=40, borderwidth=2)
    sector_entry.grid(row=1, column=1, pady=10)
    route_entry = Entry(add_data_window, width=40, borderwidth=2)
    route_entry.grid(row=2, column=1, pady=10)
    ascent_entry = Entry(add_data_window, width=40, borderwidth=2)
    ascent_entry.grid(row=3, column=1, pady=10)
    style_entry = Entry(add_data_window, width=40, borderwidth=2)
    style_entry.grid(row=4, column=1, pady=10)
    grade_entry = Entry(add_data_window, width=40, borderwidth=2)
    grade_entry.grid(row=5, column=1, pady=10)
    comment_entry = Entry(add_data_window, width=40, borderwidth=2)
    comment_entry.grid(row=6, column=1, pady=10)

    # creating buttons for our add ascent view
    add_record_button = Button(add_data_window, text="Save ascent", width=30, borderwidth=4, command=adding_record)
    add_record_button.grid(row=7, column=1, ipadx=12, pady=10)
    back_button = Button(add_data_window, text="Close window", width=34, borderwidth=4,
                         command=lambda: close_window(add_data_window))
    back_button.grid(row=8, column=1)
    add_data_window.mainloop()


# Function to render main view. Good if we want to go back to the main view
def render_main_view():
    # creating labels for main view
    welcome_label = Label(main_window, text="Climb smart or die trying" + "\n" + "beta 0.1", font=25)
    welcome_label.grid(row=0, column=0, columnspan=2, padx=125)

    # creating buttons for our main view
    add_ascent_button = Button(main_window, text="Add ascent", borderwidth=4, command=render_add_ascent_window)
    add_ascent_button.grid(row=1, column=1, pady=10, padx=10, ipadx=50)
    view_records_button = Button(main_window, text="See ascents", borderwidth=4,
                                 command=render_view_ascents_options_view)
    view_records_button.grid(row=1, column=0, pady=10, padx=10, ipadx=50)
    workout_button = Button(main_window, text="Training", borderwidth=4)
    workout_button.grid(row=2, column=1, pady=10, padx=10, ipadx=58)
    projects_button = Button(main_window, text="Projects", borderwidth=4)
    projects_button.grid(row=2, column=0, pady=10, padx=10, ipadx=58)


# From here our program start
if __name__ == '__main__':
    main_window = Tk()
    # main_window.geometry("500x500")
    main_window.title("Climbing progression")
    # calling our main view function
    render_main_view()
    # Creating db
    connection = sqlite3.connect("Climbing progression data.db")
    # Creating our cursor
    cursor = connection.cursor()
    # Creating table (climbing_info) in our database with named columns(city, sector..)(all from string type).
    '''cursor.execute("""CREATE TABLE climbing_info
                (city text,
                sector text,
                route text,
                ascent text,
                style text,
                grade text,
             comment text)""")
    '''
    # Commit changes to our db
    connection.commit()
    # Closing our db
    connection.close()
    main_window.mainloop()
