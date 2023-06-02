from tkinter import *
from tkinter import messagebox
from PIL import ImageTk,Image
import re
import sqlite3


def create_bg(picture, tab):
    bg = ImageTk.PhotoImage(Image.open(picture))
    bg_lbl = Label(tab, image=bg)
    bg_lbl.image = bg
    bg_lbl.place(x=0, y=0)


def create_how_to(tab, frame_txt, lbl_txt):
    how_to_frm = LabelFrame(
        tab, text=frame_txt, borderwidth=2, background="#d2e2fa", padx=10, pady=10)
    how_to_frm.pack(padx=10, pady=10, fill=X)
    how_to_lbl = Label(
        how_to_frm, text=lbl_txt, font=("default", 12), background="#d2e2fa")
    how_to_lbl.pack(fill=X)
    how_to_lbl.bind('<Configure>', lambda _: how_to_lbl.config(wraplength=how_to_lbl.winfo_width()))


def calculate_percentage(pages, completed):
    try:
        percent = round((int(completed)/int(pages)*100),1)
        if str(percent).endswith(".0"):
            percent = str(percent).removesuffix(".0")
    except ZeroDivisionError:
        percent = 0
    return percent


def validate_input(collect_data):
    artist, book, release, publisher, pages, completed = collect_data()
    
    while True:
        if len(artist) > 60 or len(book) > 60:
            messagebox.showerror("Something went wrong!", "The name you entered is too long.", icon="question")
            break
        elif not re.search(r"^[a-zA-Z.]+(,? [a-zA-Z.]+)*?$", artist, re.IGNORECASE):
            messagebox.showerror("Something went wrong!", "Did you forget the artist's name?", icon="question")
            break
        elif book == "":
            messagebox.showerror("Something went wrong!", "Did you forget the book title?", icon="question")
            break
        elif len(release) > 20 or len(publisher) > 30:
            messagebox.showerror("Something went wrong!", "Your Entry is too long.", icon="question")
        elif release == "":
            release = "Unknown"
            continue
        elif publisher == "":
            publisher = "Unknown"
            continue
        elif pages == "":
            pages = "0"
            continue
        elif completed == "":
            completed = "0"
            continue            
        elif not pages.isdigit() or int(pages) > 1001 or int(pages) < int(completed):
            messagebox.showerror("Something went wrong!", "Please insert a (valid) number of pages.")
            break
        elif not completed.isdigit() or int(completed) > 1001 or int(completed) > int(pages):
            messagebox.showerror("Something went wrong!", "Please insert a (valid) number of completed pages.")
            break
        percent = calculate_percentage(pages, completed)

        return (artist, book, release, publisher, pages, completed, percent)


def validate_pages_input(collect_pages_data):
    artist, book, page, material, used_for, start, end = collect_pages_data()
    
    while True:
        if len(artist) > 60 or len(book) > 60:
            messagebox.showerror("Something went wrong!", "The name you entered is too long.", icon="question")
            break
        elif not re.search(r"^[a-zA-Z.]+(,? [a-zA-Z.]+)*?$", artist, re.IGNORECASE):
            messagebox.showerror("Something went wrong!", "Did you forget the artist's name?", icon="question")
            break
        elif book == "":
            messagebox.showerror("Something went wrong!", "Did you forget the book title?", icon="question")
            break

        return (artist, book, page, material, used_for, start, end)


def create_db():
    conn = sqlite3.connect("colouring_books.db")
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE if not exists books (
                artist, booktitle, release_date, publisher, nr_of_pages, completed_pages, percentage)""")
    cursor.execute("""CREATE TABLE if not exists completed_pages (
                artist, booktitle, page, materials, used_for, start_date, end_date, status)""")
    conn.commit()
    conn.close()


def get_data_from_db(table):
    conn = sqlite3.connect("colouring_books.db")
    cursor = conn.cursor()
    cursor.execute("SELECT oid, * FROM {}".format(table))
    book_records = cursor.fetchall()
    conn.commit()
    conn.close()
    return book_records


def add_book_to_db(data):
    conn = sqlite3.connect("colouring_books.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO books VALUES (?, ?, ?, ?, ?, ?, ?)", data)
    cursor.execute("SELECT oid FROM books")
    book_ids = cursor.fetchall()
    book_id = list(book_ids[-1])
    conn.commit()
    conn.close()
    return book_id


def edit_book_in_db(book_id, data):
    conn = sqlite3.connect("colouring_books.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE books SET artist=?, booktitle=?, release_date=?, publisher=?, nr_of_pages=?, completed_pages=?, percentage=? WHERE oid=?", (*data, book_id))
    conn.commit()
    conn.close()


def remove_item_from_db(table, book_id):
    conn = sqlite3.connect("colouring_books.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM {} WHERE oid=?".format(table), (book_id))
    conn.commit()
    conn.close()


def search_for_book(artist):
    conn = sqlite3.connect("colouring_books.db")
    cursor = conn.cursor()
    cursor.execute("SELECT rowid, * FROM books WHERE artist LIKE ?", ('%'+artist+'%',))
    book_records = cursor.fetchall()
    conn.commit()
    conn.close()
    return book_records


def add_page_to_db(data, status):
    conn = sqlite3.connect("colouring_books.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO completed_pages VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (*data, status))
    cursor.execute("SELECT oid FROM completed_pages")
    completed_ids = cursor.fetchall()
    completed_id = list(completed_ids[-1])
    conn.commit()
    conn.close()
    return completed_id


def edit_page_in_db(data, status, page_id):
    conn = sqlite3.connect("colouring_books.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE completed_pages SET artist=?, booktitle=?, page=?, materials=?, used_for=?, start_date=?, end_date=?, status=? WHERE oid=?", (*data, status, page_id))
    conn.commit()
    conn.close()