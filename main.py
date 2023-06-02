from tkinter import *
from tkinter import ttk, messagebox
from random import choice
import helpers


# basic window configuration
root = Tk()
root.title("Colouring Journal")
root.geometry("1000x800")
root.minsize(1000, 800)
root.resizable(True, True)
style = ttk.Style()
style.theme_use("clam")
style.configure("Tab", focuscolor=style.configure(".")["background"])
base_frm = Frame(root, relief="flat", borderwidth=10, bg="gray")
base_frm.pack(fill="both", expand=True)


# create db if it doesn't exist
helpers.create_db()


# create the tabs
tabs = ttk.Notebook(base_frm)
tab1 = Frame(tabs)
tab2 = Frame(tabs)
tab3 = Frame(tabs)
tab4 = Frame(tabs)
tab5 = Frame(tabs)
tab6 = Frame(tabs)
tabs.add(tab1, text="Home")
tabs.add(tab2, text="Colouring Books")
tabs.add(tab3, text="Completed Pages & WIPs")
tabs.add(tab4, text="Notes")
tabs.add(tab5, text="Bingo")
tabs.add(tab6, text="How To")
tabs.pack(fill="both", expand=True)


def main():
    create_tab_1()
    create_tab_2()
    create_tab_3()
    create_tab_4()
    create_tab_5()
    create_tab_6()
    root.mainloop()


def create_tab_1():
    # create background for tab 1
    helpers.create_bg("bg1.png", tab1)

    # pick random quote from text file
    with open("quotes.txt", "r") as file:
        line = file.readlines()
        quote = choice(line)

    # place widgets
    day_frm = Frame(
        tab1, borderwidth=5, relief="groove", width=300, height=60, background="#e1d5f1"
    )
    day_frm.pack(pady=(60, 0))
    day_lbl = Label(
        day_frm, text="Quote of the Day", font=("default", 24), background="#e1d5f1"
    ).place(relx=0.5, rely=0.5, anchor=CENTER)
    quote_frm = Frame(
        tab1, borderwidth=5, relief="groove", width=300, height=300, bg="#e1d5f1"
    )
    quote_frm.pack()
    quote_lbl = Label(
        quote_frm,
        text=quote,
        font=("default", 18),
        background="#e1d5f1",
        wraplength=280,
    ).place(relx=0.5, rely=0.5, anchor=CENTER)


def create_tab_2():
    def show_all():
        book_records = helpers.get_data_from_db("books")
        for child in books.get_children():
            books.delete(child)
        for record in book_records:
            books.insert(
                parent="",
                index="end",
                values=(
                    record[0],
                    record[1],
                    record[2],
                    record[3],
                    record[4],
                    record[5],
                    record[6],
                    str(record[7]) + "%",
                ),
            )

    def collect_data():
        artist = artist_ent.get().strip()
        book = book_ent.get().strip()
        release = release_ent.get().strip()
        publisher = publisher_ent.get().strip()
        pages = pages_ent.get().strip()
        completed = completed_ent.get().strip()
        return (artist, book, release, publisher, pages, completed)

    # function to add new colouring books to treeview and the db
    def add_book():
        try:
            data = helpers.validate_input(collect_data)
            book_id = helpers.add_book_to_db(data)
            books.insert(
                parent="",
                index="end",
                values=(
                    book_id,
                    data[0],
                    data[1],
                    data[2],
                    data[3],
                    data[4],
                    data[5],
                    str(data[6]) + "%",
                ),
            )
            clear_entries()
            total_text.set("Total Number of\n Books: " + str(len(books.get_children())))
        except ValueError:
            pass

    # function to select klicked treeview element
    def select_book(e):
        artist_ent.delete(0, END)
        book_ent.delete(0, END)
        release_ent.delete(0, END)
        publisher_ent.delete(0, END)
        pages_ent.delete(0, END)
        completed_ent.delete(0, END)
        try:
            selected_book = books.selection()[0]
            selected_book_info = books.item(selected_book, "values")
            artist_ent.insert(0, selected_book_info[1])
            book_ent.insert(0, selected_book_info[2])
            release_ent.insert(0, selected_book_info[3])
            publisher_ent.insert(0, selected_book_info[4])
            pages_ent.insert(0, selected_book_info[5])
            completed_ent.insert(0, selected_book_info[6])
        except IndexError:
            pass

    ##function to edit existing colouring books, update treeview and the db
    def edit_book():
        try:
            selected_book = books.selection()[0]
            selected_book_id = books.item(selected_book, "values")[0]
            try:
                data = helpers.validate_input(collect_data)
                books.item(
                    selected_book,
                    text="",
                    values=(
                        selected_book_id,
                        data[0],
                        data[1],
                        data[2],
                        data[3],
                        data[4],
                        data[5],
                        str(data[6]) + "%",
                    ),
                )
                helpers.edit_book_in_db(selected_book_id, data)
                clear_entries()
            except TypeError:
                pass
        except IndexError:
            pass

    # function to delete a book from treeview and the db
    def remove_book():
        try:
            selected_book = books.selection()[0]
            selected_book_id = books.item(selected_book, "values")[0]
            books.delete(selected_book)
            total_text.set("Total Number of\n Books: " + str(len(books.get_children())))
            helpers.remove_item_from_db("books", selected_book_id)
        except IndexError:
            pass

    # function to clear all entry widgets
    def clear_entries():
        artist_ent.delete(0, END)
        book_ent.delete(0, END)
        release_ent.delete(0, END)
        publisher_ent.delete(0, END)
        pages_ent.delete(0, END)
        completed_ent.delete(0, END)
        try:
            books.selection_remove(books.selection()[0])
        except IndexError:
            pass

    # function to search for book by artist
    def search_for():
        find_artist = artist_ent.get()
        if find_artist == "":
            messagebox.showerror(
                "Missing Name", "You're not searching for anything!", icon="question"
            )
        else:
            book_records = helpers.search_for_book(find_artist)
            if book_records == []:
                messagebox.showerror(
                    "No result", "No matching Artist could be found.", icon="question"
                )
            else:
                for child in books.get_children():
                    books.delete(child)
                for record in book_records:
                    books.insert(
                        parent="",
                        index="end",
                        values=(
                            record[0],
                            record[1],
                            record[2],
                            record[3],
                            record[4],
                            record[5],
                            record[6],
                            str(record[7]) + "%",
                        ),
                    )
            clear_entries()

    # create the scrollbar
    scroll = Scrollbar(tab2, orient=VERTICAL)
    scroll.pack(side=RIGHT, fill=Y)

    books = ttk.Treeview(tab2, yscrollcommand=scroll.set)
    scroll.config(command=books.yview)

    # create the treeview widget
    books["columns"] = (
        "ID",
        "Artist",
        "Booktitle",
        "Release Date",
        "Publisher/ Series",
        "Nr. of Pages",
        "Completed Pages",
        "% Completed",
    )
    books.column("#0", width=0, stretch=NO)
    books.column("ID", width=30, min=30)
    books.column("Artist", anchor=W, width=150, min=100)
    books.column("Booktitle", anchor=W, width=220, min=100)
    books.column("Release Date", anchor=W, width=80, min=50)
    books.column("Publisher/ Series", anchor=W, width=150, min=100)
    books.column("Nr. of Pages", anchor=W, width=60, min=50)
    books.column("Completed Pages", anchor=W, width=90, min=50)
    books.column("% Completed", anchor=N, width=70, min=50)

    book_headings = (
        "ID",
        "Artist",
        "Booktitle",
        "Release Date",
        "Publisher/ Series",
        "Nr. of Pages",
        "Completed Pages",
        "% Completed",
    )
    for header in book_headings:
        books.heading(header, text=header, anchor=W)

    books.pack(fill="both", expand=True)

    # create a frame and place entry widgets
    options_frm = Frame(tab2)
    options_frm.pack(fill=X, anchor=S)

    artist_lbl = Label(options_frm, text="Artist").grid(column=0, row=0, sticky=NW)
    book_lbl = Label(options_frm, text="Booktitle").grid(column=1, row=0, sticky=NW)
    release_lbl = Label(options_frm, text="Release Date").grid(
        column=2, row=0, sticky=NW
    )
    publisher_lbl = Label(options_frm, text="Publisher/ Series").grid(
        column=3, row=0, sticky=NW
    )
    pages_lbl = Label(options_frm, text="Nr. of Pages").grid(column=4, row=0, sticky=NW)
    completed_lbl = Label(options_frm, text="Pages completed").grid(
        column=5, row=0, sticky=NW
    )

    artist_options = (
        "Johanna Basford",
        "Lulu Mayo",
        "Kerby Rosanes",
        "Hanna Karlzon",
        "Hannah Lynn",
        "Christine Karron",
        "Rita Berman",
        "Derya Cakirsoy",
        "Teresa Goodridge",
        "Maria Trolle",
        "Kameliya Angelkova",
        "Unknown",
    )
    artist_ent = ttk.Combobox(options_frm, values=artist_options)
    artist_ent.grid(column=0, row=1, sticky=NW)
    book_ent = Entry(options_frm)
    book_ent.grid(column=1, row=1, sticky=NW)
    release_ent = Entry(options_frm)
    release_ent.grid(column=2, row=1, sticky=NW)
    publisher_options = (
        "Amazon",
        "Jade Summer",
        "Creative Haven",
        "Coco Wyo",
        "Coloring Heaven",
        "Mythographic",
    )
    publisher_ent = ttk.Combobox(options_frm, values=publisher_options)
    publisher_ent.grid(column=3, row=1, sticky=NW)
    pages_ent = Entry(options_frm)
    pages_ent.grid(column=4, row=1, sticky=NW)
    completed_ent = Entry(options_frm)
    completed_ent.grid(column=5, row=1, sticky=NW)

    # create buttons and place them on frame
    show_all()
    total_text = StringVar()
    total_text.set("Total Number of\n Books: " + str(len(books.get_children())))
    new_book_btn = Button(options_frm, text="Add Book", command=add_book)
    new_book_btn.grid(column=0, row=2)
    save_edited_book_btn = Button(options_frm, text="Save Changes", command=edit_book)
    save_edited_book_btn.grid(column=1, row=2)
    delete_book_btn = Button(
        options_frm, text="Delete Selected Book", command=remove_book
    )
    delete_book_btn.grid(column=2, row=2)
    clear_btn = Button(options_frm, text="Clear Entry Boxes", command=clear_entries)
    clear_btn.grid(column=3, row=2)
    search_btn = Button(options_frm, text="Search for Artist", command=search_for)
    search_btn.grid(column=4, row=2)
    show_all_btn = Button(options_frm, text="Show all Books", command=show_all)
    show_all_btn.grid(column=5, row=2)
    total_books_lbl = Label(
        options_frm,
        borderwidth=2,
        relief="groove",
        textvariable=total_text,
        font=("", 14),
        anchor=CENTER,
    )
    total_books_lbl.grid(column=8, row=0, rowspan=3, padx=5, ipadx=10, ipady=5)

    books.bind("<ButtonRelease-1>", select_book)
    # change this to "<<TreeviewSelect>>", lambda event: table.selection


def create_tab_3():
    def show_all_pages():
        completed_records = helpers.get_data_from_db("completed_pages")

        for child in completed.get_children():
            completed.delete(child)

        for record in completed_records:
            completed.insert(
                parent="",
                index="end",
                values=(
                    record[0],
                    record[1],
                    record[2],
                    record[3],
                    record[4],
                    record[5],
                    record[6],
                    record[7],
                    record[8],
                ),
            )

    def clear_entries():
        artist_ent.delete(0, END)
        book_ent.delete(0, END)
        page_ent.delete(0, END)
        materials_ent.delete(0, END)
        used_ent.delete(0, END)
        start_ent.delete(0, END)
        end_ent.delete(0, END)
        try:
            completed.selection_remove(completed.selection()[0])
        except IndexError:
            pass

    def calculate_status():
        finished = 0
        wip = 0
        for child in completed.get_children():
            pages_count = completed.item(child, "values")[7]
            if pages_count:
                finished += 1
            if not pages_count:
                wip += 1
        finished_txt.set("Completed Pages: " + str(finished))
        wip_txt.set("WIPs: " + str(wip))

    def get_status(end_date):
        if end_date:
            return "Done!"
        else:
            return "WIP"

    def collect_pages_data():
        artist = artist_ent.get().strip()
        book = book_ent.get().strip()
        page = page_ent.get().strip()
        material = materials_ent.get().strip()
        used_for = used_ent.get().strip()
        start = start_ent.get().strip()
        end = end_ent.get().strip()
        return (artist, book, page, material, used_for, start, end)

    def add_completed():
        try:
            data = helpers.validate_pages_input(collect_pages_data)
            status = get_status(data[6])
            completed_id = helpers.add_page_to_db(data, status)
            completed.insert(
                parent="",
                index="end",
                values=(
                    completed_id,
                    data[0],
                    data[1],
                    data[2],
                    data[3],
                    data[4],
                    data[5],
                    data[6],
                    status,
                ),
            )
            clear_entries()
            calculate_status()
        except TypeError:
            pass

    def select_page(e):
        artist_ent.delete(0, END)
        book_ent.delete(0, END)
        page_ent.delete(0, END)
        materials_ent.delete(0, END)
        used_ent.delete(0, END)
        start_ent.delete(0, END)
        end_ent.delete(0, END)
        try:
            selected_page = completed.selection()[0]
            selected_page_info = completed.item(selected_page, "values")
            artist_ent.insert(0, selected_page_info[1])
            book_ent.insert(0, selected_page_info[2])
            page_ent.insert(0, selected_page_info[3])
            materials_ent.insert(0, selected_page_info[4])
            used_ent.insert(0, selected_page_info[5])
            start_ent.insert(0, selected_page_info[6])
            end_ent.insert(0, selected_page_info[7])
        except IndexError:
            pass

    def save_changes():
        try:
            selected_page = completed.selection()[0]
            selected_page_id = completed.item(selected_page, "values")[0]
            try:
                data = helpers.validate_pages_input(collect_pages_data)
                status = get_status(data[6])
                completed.item(
                    selected_page,
                    text="",
                    values=(
                        selected_page_id,
                        data[0],
                        data[1],
                        data[2],
                        data[3],
                        data[4],
                        data[5],
                        data[6],
                        status,
                    ),
                )
                helpers.edit_page_in_db(data, status, selected_page_id)
                clear_entries()
                calculate_status()
            except ValueError:
                pass
        except IndexError:
            pass

    def remove_page():
        try:
            selected_page = completed.selection()[0]
            selected_page_id = completed.item(selected_page, "values")[0]
            completed.delete(selected_page)
            calculate_status()
            helpers.remove_item_from_db("completed_pages", selected_page_id)
        except IndexError:
            pass

    def show_wips():
        for child in completed.get_children():
            end_date = completed.item(child, "values")[7]
            if end_date:
                completed.detach(child)

    scroll = Scrollbar(tab3, orient=VERTICAL)
    scroll.pack(side=RIGHT, fill=Y)

    completed = ttk.Treeview(tab3, yscrollcommand=scroll.set)
    scroll.config(command=completed.yview)

    completed.bind("<ButtonRelease-1>", select_page)

    completed["columns"] = (
        "No",
        "Artist",
        "Booktitle",
        "Page Name or Number",
        "Materials Used",
        "Used for",
        "Start Date",
        "End Date",
        "Status",
    )
    completed.column("#0", width=0, stretch=NO)
    completed.column("No", width=30, min=30)
    completed.column("Artist", anchor=W, width=150)
    completed.column("Booktitle", anchor=W, width=150)
    completed.column("Page Name or Number", anchor=W, width=140)
    completed.column("Materials Used", anchor=W, width=150)
    completed.column("Used for", anchor=W, width=150)
    completed.column("Start Date", anchor=W, width=60)
    completed.column("End Date", anchor=W, width=60)
    completed.column("Status", anchor=W, width=60)

    pages_headings = (
        "No",
        "Artist",
        "Booktitle",
        "Page Name or Number",
        "Materials Used",
        "Used for",
        "Start Date",
        "End Date",
        "Status",
    )
    for heading in pages_headings:
        completed.heading(heading, text=heading, anchor=W)

    completed.pack(fill="both", expand=True)

    options_frm = Frame(tab3)
    options_frm.pack(fill=X, anchor=S)
    options_frm.columnconfigure([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], minsize=50)

    artist_lbl = Label(options_frm, text="Artist").grid(column=0, row=0, sticky=NW)
    book_lbl = Label(options_frm, text="Booktitle").grid(column=1, row=0, sticky=NW)
    page_lbl = Label(options_frm, text="Page Name or Number").grid(
        column=2, row=0, sticky=NW
    )
    materials_lbl = Label(options_frm, text="Materials Used").grid(
        column=3, row=0, sticky=NW
    )
    used_lbl = Label(options_frm, text="Used for (#, Tags etc.)").grid(
        column=4, row=0, sticky=NW
    )
    start_lbl = Label(options_frm, text="Start Date").grid(column=5, row=0, sticky=NW)
    end_lbl = Label(options_frm, text="End Date").grid(column=6, row=0, sticky=NW)

    artist_ent = Entry(options_frm)
    artist_ent.grid(column=0, row=1, sticky=NW)
    book_ent = Entry(options_frm)
    book_ent.grid(column=1, row=1, sticky=NW)
    page_ent = Entry(options_frm)
    page_ent.grid(column=2, row=1, sticky=NW)
    materials_ent = Entry(options_frm)
    materials_ent.grid(column=3, row=1, sticky=NW)
    used_ent = Entry(options_frm)
    used_ent.grid(column=4, row=1, sticky=NW)
    start_ent = Entry(options_frm)
    start_ent.grid(column=5, row=1, sticky=NW)
    end_ent = Entry(options_frm)
    end_ent.grid(column=6, row=1, sticky=NW)

    show_all_pages()
    finished_txt = StringVar()
    wip_txt = StringVar()
    calculate_status()
    new_page_btn = Button(options_frm, text="Add Page", command=add_completed)
    new_page_btn.grid(column=0, row=3, sticky=W)
    save_changed_page_btn = Button(
        options_frm, text="Save Changes", command=save_changes
    )
    save_changed_page_btn.grid(column=1, row=3, sticky=W)
    remove_page_btn = Button(
        options_frm, text="Remove Selected Page", command=remove_page
    )
    remove_page_btn.grid(column=2, row=3)
    clear_btn = Button(options_frm, text="Clear Entry Boxes", command=clear_entries)
    clear_btn.grid(column=3, row=3)
    show_wips_btn = Button(options_frm, text="Show only WIPs", command=show_wips)
    show_wips_btn.grid(column=4, row=3)
    show_all_btn = Button(options_frm, text="Show all pages", command=show_all_pages)
    show_all_btn.grid(column=5, row=3)
    sep = ttk.Separator(options_frm, orient="horizontal").grid(
        column=0, row=4, columnspan=10, sticky=EW, pady=5
    )
    nr_of_pages_lbl = Label(
        options_frm, textvariable=finished_txt, font=("default", 16)
    ).grid(column=0, row=5, columnspan=2)
    nr_of_wips_lbl = Label(
        options_frm, textvariable=wip_txt, font=("default", 16)
    ).grid(column=2, row=5)


def create_tab_4():
    # create background for tab 4
    helpers.create_bg("bg2.png", tab4)

    # define functions for the listbox
    def delete_note():
        notes.delete(ANCHOR)

    def add_note():
        notes.insert(END, new_note_ent.get())
        new_note_ent.delete(0, END)

    def save_notes():
        with open("notes.txt", "w") as file:
            for note in notes.get(0, END):
                file.writelines(note.rstrip() + "\n")

    # create the listbox and it's buttons
    notes = Listbox(
        tab4,
        font=("default", 14),
        width=70,
        height=27,
        background="#b7eadf",
        activestyle="none",
        highlightthickness=0,
        selectbackground="#38b299",
    )
    notes.pack(pady=20)

    options_frm = Frame(tab4, background="#b7eadf")
    options_frm.pack()
    new_note_ent = Entry(
        options_frm, font=("default", 14), width=70, background="#b7eadf"
    )
    new_note_ent.pack(side="top")
    add_btn = Button(options_frm, text="Add Note", command=add_note).pack(side="left")
    delete_btn = Button(options_frm, text="Delete Note", command=delete_note).pack(
        side="left"
    )
    save_btn = Button(options_frm, text="Save Notes", command=save_notes).pack(
        side="right"
    )

    # open file and load notes
    with open("notes.txt") as file:
        for line in file:
            notes.insert(END, line)


def create_tab_5():
    # create background for tab 5
    helpers.create_bg("bg3.png", tab5)

    def generate_prompts():
        # create the bingo prompts and place them
        prompts = set()

        while len(prompts) < 9:
            with open("bingo.txt", "r") as file:
                line = file.readlines()
                prompt = choice(line)
                prompts.add(prompt)

        prompt_list = list(prompts)

        for i in range(3):
            for j in range(3):
                count = 0
                prompt_frm = Frame(
                    bingo_frm,
                    borderwidth=2,
                    relief="groove",
                    width=200,
                    height=200,
                    bg="LavenderBlush",
                )
                prompt_frm.grid(row=i, column=j)
                prompt_lbl = Label(
                    prompt_frm,
                    text=prompt_list[count].capitalize(),
                    font=("default", 14),
                    background="LavenderBlush",
                    wraplength=180,
                ).place(relx=0.5, rely=0.5, anchor=CENTER)
                prompt_list.pop(count)
                count += 1

    # create the bingo field
    bingo_main_frm = Frame(
        tab5,
        borderwidth=5,
        relief="groove",
        width=600,
        height=60,
        background="LavenderBlush",
    )
    bingo_main_frm.pack(pady=(20, 0))
    bingo_main_lbl = Label(
        bingo_main_frm,
        text="Colouring Bingo",
        font=("default", 24),
        background="LavenderBlush",
    ).place(relx=0.5, rely=0.5, anchor=CENTER)

    bingo_frm = Frame(tab5, width=600, height=600, bg="LavenderBlush")
    bingo_frm.pack()
    refresh_bingo_btn = Button(
        tab5,
        text="Refresh Prompts",
        font=("default", 14),
        borderwidth=5,
        relief="groove",
        width=53,
        background="LavenderBlush",
        takefocus=False,
        command=generate_prompts,
    ).pack()

    generate_prompts()


def create_tab_6():
    # create background for tab 6
    helpers.create_bg("bg4.png", tab6)

    # create explanations for every tab
    how_tos = {
        "Home": "The 'Home' Tab picks a random quote from the quotes.txt file every time the program runs. Most of these were sourced from coloringqueen.net. You can add your own quotes to the quotes.txt file!",
        "Colouring Books": "Add new books to your list by filling the entry boxes below and klicking 'add book'. You don't have to fill all the spaces if you don't have the info. Some artists and publishers can be selected from the dropdown list. To edit or delete an entry, select the book and use the menu below. Search your collection by typing in an artist and click 'search by artist'. The program will automatically calculate the '% completed' of each book.",
        "Completed Pages & WIPs": "Fill in the entry boxes below to add a page to the list. You don't have to fill in all the boxes. Pages without an end date will be considered a WIP and won't be counted into the total completed pages.",
        "Notes": "Add and delete things you want to keep track of, like colour combinations, colouring tags, buddycolours, etc. Don't forget to save your changes!",
        "Bingo": "The Colouring Bingo displays 9 random prompts as inspiration if you don't know what to colour. You can add your own prompts to the bingo.txt file!",
        "Disclaimer": "Background image is from Pixabay.com.\nThis programm was created by Sonja Ruth. Happy Colouring!",
    }

    for element in how_tos:
        helpers.create_how_to(tab6, element, how_tos[element])


if __name__ == "__main__":
    main()
