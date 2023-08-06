#!/usr/bin/env python3

import argparse
import datetime
import json
import logging
import pickle
import sqlite3
from collections import Counter
from html.parser import HTMLParser
from tkinter import *
from tkinter import messagebox

import requests
import yaml

# variables
name_logfile = "tags_log_file"
name_db = "tags.db"
name_aliases = "synonims.yaml"
current_time = str(datetime.datetime.now())[:-7]


def get_url_site(sitename):
    return "https://{}/".format(sitename)


def define_site_name(sn, file=name_aliases):
    with open(file, 'r') as stream:
        try:
            aliases = yaml.safe_load(stream)
            return aliases.get(sn, sn)
        except yaml.YAMLError as exc:
            print(exc)


def get_page_from_site(url):
    req = requests.get(url)
    if req.status_code in [200]:
        html = req.text
    else:
        print('Can\'t download page')
        html = None
    return html


def get_dict_tags(input_html_date):
    class MyHTMLParser(HTMLParser):
        def __init__(self):
            self.tags = []
            super().__init__()

        def handle_starttag(self, tag, attrs):
            self.tags.append(tag)

    parser = MyHTMLParser()
    parser.feed(input_html_date)
    parser.close()
    return dict(Counter(parser.tags))


def write_to_logfile(url_site):
    logging.info(url_site)


def create_table():
    conn = sqlite3.connect(name_db)
    c = conn.cursor()
    try:
        c.execute("""CREATE TABLE tags_table (
                    sitename text,
                    url text,
                    date_check text,
                    tags blob
                    )""")
    except:
        print("Db already created")
    conn.close()


def tags_to_blob(data):
    return pickle.dumps(data)


def write_to_db(sitename, urlsite, date_check, tags_records):
    conn = sqlite3.connect(name_db)
    c = conn.cursor()
    with conn:
        c.execute("INSERT INTO tags_table VALUES (:sitename, :url, :date_check, :tags_records)",
                  {'sitename': sitename, 'url': urlsite, 'date_check': date_check, 'tags_records': tags_records})
        print("Data inserted into table.")

    conn.close()


def read_from_db(sitename):
    conn = sqlite3.connect(name_db)
    c = conn.cursor()
    with conn:
        c.execute("SELECT tags FROM tags_table WHERE sitename=:sitename", {'sitename': sitename})
        return [pickle.loads(i[0]) for i in c.fetchall()]


def get_info(sn):
    site_name = define_site_name(sn)
    url = get_url_site(site_name)
    write_to_logfile(site_name)
    datapage = get_page_from_site(url)
    tags_blob = tags_to_blob(get_dict_tags(datapage))
    write_to_db(site_name, url, current_time, tags_blob)


def main():
    parser = argparse.ArgumentParser(description="Get info about tags on site")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--get", help="Get tags for specific site (or alias)")
    group.add_argument("--show", help="Get tags from DATABASE for specific site (or alias)")
    group.add_argument("--createdb", action="store_true", help="Create DB to store results")
    args = parser.parse_args()

    logging.basicConfig(filename=name_logfile, level=logging.INFO,
                        format='%(asctime)s:%(message)s')

    if args.createdb:
        create_table()
    elif args.get is not None:
        get_info(args.get)
    elif args.show is not None:
        site_name = define_site_name(args.show)
        for d in read_from_db(site_name):
            print("=============================================")
            print(json.dumps(d, sort_keys=False, indent=4))
    else:
        def click_load():
            if input_site_name.get() != '':
                try:
                    get_info(input_site_name.get())
                    messagebox.showinfo(title="info", message="Info from site successfully loaded")
                except:
                    messagebox.showinfo(title="info", message="Something goes wrong...")
            else:
                messagebox.showinfo(title="info", message="Enter site name")

        def click_view():
            if input_site_name.get() != '':
                site_name = define_site_name(input_site_name.get())
                text.delete(1.0, END)
                for d in read_from_db(site_name):
                    pretty = json.dumps(d, sort_keys=False, indent=4)
                    text.insert(1.0, "\n====================================\n")
                    text.insert(1.0, pretty)
            else:
                messagebox.showinfo(title="info", message="Enter site name")

        def changeOnHover(button, hover_text):
            button.bind("<Enter>", func=lambda e: statusbar.config(
                text=hover_text))
            button.bind("<Leave>", func=lambda e: statusbar.config(
                text="Status"))

        root = Tk()
        root.title("tags info")
        root.geometry('400x400')
        root.resizable(width=False, height=False)
        canvas = Canvas(root, width=400, height=400)
        canvas.pack()

        frame_top = Frame(root, bg='#aaaaaa', bd=5)
        frame_top.place(relx=0, rely=0, relwidth=1, relheight=0.2)

        frame_bottom = Frame(root, bg='#ffffff', bd=5)
        frame_bottom.place(relx=0, rely=0.2, relwidth=1, relheight=0.8)

        input_site_name = Entry(frame_top, bg='white', justify="center", width=30)
        input_site_name.pack()

        btn_load = Button(frame_top, text='Load site\'s info', width=12, command=click_load)
        btn_load.place(relx=0, rely=0.5)
        changeOnHover(btn_load, "Load tags from your favorite website into DB!")

        btn_view = Button(frame_top, text='View site\'s info', width=12, command=click_view)
        btn_view.place(relx=0.67, rely=0.5)
        changeOnHover(btn_view, "View tags from DB")

        scrollbar = Scrollbar(frame_bottom)

        text = Text(frame_bottom, yscrollcommand=scrollbar.set)
        text.place(relwidth=0.95, relheight=0.9)
        scrollbar.config(command=frame_bottom)
        scrollbar.pack(side=RIGHT, fill=Y)

        statusbar = Label(frame_bottom, bg='#FFFFFF', text="Status", bd=1, relief=SUNKEN, anchor=W)
        statusbar.pack(side=BOTTOM, fill=X, ipady=2)
        root.mainloop()


if __name__ == '__main__':
    main()
