
from tkinter import *
import tkinter as tk
#from tk import *
import requests
import xml.sax
import xml.etree.ElementTree as ET
from xml.dom import minidom
from lxml import etree
import copy

global rowid_route
global rowid_Direction
global rowid_stops
global sel_route
global sel_direction
global sel_stop

class BusRoute:


    def __init__(self, speed=0):
        self.query = ""



def clicked(route,dir,stop):
    URL = 'http://svc.metrotransit.org/NexTrip/' + sel_route + '/' + sel_direction + '/' + sel_stop
    print(URL)
    #resp = requests.get('http://svc.metrotransit.org/NexTrip/921/4/KEFO')
    resp = requests.get(URL)
    if resp.status_code != 200:
        # This means something went wrong.
        raise requests.ApiError('GET /tasks/ {}'.format(resp.status_code))

    root = ET.fromstring(resp.content)

    try:
        for child in root[0].iter('*'):
            if child.tag[73:] == 'DepartureText':
                ret_txt = child.text
    except:
        ret_txt = "Last bus already left"

    print(ret_txt)
    # delete previous text in enter1
    enter4.delete(0, 50)
    # now display the selected text
    enter4.insert(0, ret_txt)

    return ret_txt

def get_routes():

    resp = requests.get('http://svc.metrotransit.org/NexTrip/Routes')
    if resp.status_code != 200:
        # This means something went wrong.
        raise requests.ApiError('GET /tasks/ {}'.format(resp.status_code))

    root = ET.fromstring(resp.content)

    for child in root.iter('*'):
        if child.tag[73:] == 'Route':
            rowid_route.append(child.text)

    try:
         for child in root.iter('*'):
            route_id = ""
            if child.tag[73:] == 'Description':
                 listbox1.insert(END, child.text)

    except:
         ret_txt = "No Routes"


def get_direction(route_id):

    listbox2.delete(0,END)
    URL = 'http://svc.metrotransit.org/NexTrip/Directions/' +route_id
    resp = requests.get(URL)
    if resp.status_code != 200:
        # This means something went wrong.
        raise requests.ApiError('GET /tasks/ {}'.format(resp.status_code))

    root = ET.fromstring(resp.content)

    #rowid_Direction = []

    for child in root.iter('*'):
        if child.tag[73:] == 'Value':
            global rowid_Direction
            rowid_Direction.append(child.text)

    try:
         for child in root.iter('*'):
            route_id = ""
            if child.tag[73:] == 'Text':
                 listbox2.insert(END, child.text)

    except:
         ret_txt = "No Routes"
    print(rowid_Direction)
    prev_rowid_Direction = rowid_Direction

def get_stops(route_id,direction_id):
    global rowid_Direction
    global rowid_stops
    rowid_Direction = []
    rowid_stops = []
    listbox3.delete(0,END)
    URL = 'http://svc.metrotransit.org/NexTrip/Stops/' +sel_route + '/' + sel_direction
    #print(URL)
    resp = requests.get(URL)
    if resp.status_code != 200:
        # This means something went wrong.
        raise requests.ApiError('GET /tasks/ {}'.format(resp.status_code))

    root = ET.fromstring(resp.content)

    for child in root.iter('*'):
        if child.tag[73:] == 'Value':
            rowid_stops.append(child.text)

    try:
         for child in root.iter('*'):
            route_id = ""
            if child.tag[73:] == 'Text':
                print("stops are ")
                print(child.text)
                listbox3.insert(END, child.text)

    except:
         ret_txt = "No Routes"

    print(rowid_stops)

def get_list1(event):
    # get selected line index
    index = listbox1.curselection()[0]
    # get the line's text
    seltext = listbox1.get(index)
    # delete previous text in enter1
    #enter1.delete(0, 50)
    # now display the selected text
    #enter1.insert(0, rowid_route[index])
    global sel_route
    sel_route = rowid_route[index]
    #rowid_Direction = []
    get_direction(sel_route)

def get_list2(event):
    #print("begining of list2")
    #print(rowid_Direction)
    # get selected line index
    index = listbox2.curselection()[0]
    # get the line's text
    seltext = listbox2.get(index)
    # delete previous text in enter1
    #enter2.delete(0, 50)
    # now display the selected text
    #enter2.insert(0, index)
    #print("row direction in get_list2 is ")
    #print(rowid_Direction)
    global sel_direction
    global rowid_Direction
    sel_direction = rowid_Direction[index]
    #print(sel_route,sel_direction)
    get_stops(sel_route,sel_direction)


def get_list3(event):
    # get selected line index
    index = listbox3.curselection()[0]
    # get the line's text
    seltext = listbox3.get(index)
    # delete previous text in enter1
    #enter3.delete(0, 50)
    # now display the selected text
    #enter3.insert(0, rowid_stops[index])
    global sel_stop
    sel_stop = rowid_stops[index]
    clicked(sel_route, sel_direction,sel_stop)

def close_window (root):
    root.destroy()

if __name__ == '__main__':
    rowid_route = []
    rowid_Direction = []
    rowid_stops = []
    sel_route = ''
    sel_direction = ''
    sel_stop = ''
    window = tk.Tk()
    window.title("Welcome to BusRoute App!!!")

    # Add a grid
    mainframe = Frame(window)
    mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
    mainframe.columnconfigure(0, weight=1)
    mainframe.rowconfigure(0, weight=1)
    mainframe.pack(pady=100, padx=100)

    #lbl.grid(column=0, row=0)

    # Create a Tkinter variable
    tkvar = StringVar(window)

    # Create a Tkinter variable
    tkvar2 = StringVar(window)

    #Screen header
    enter5 = Entry(mainframe, width=40, bg='white',font=("Courier", 44),justify="center")
    enter5.insert(0, 'Welcome to Bus route App!!')
    enter5.grid(row=1, column=0)

    # Label
    enter1 = Entry(mainframe, width=50, bg='yellow')
    enter1.insert(0, 'Click the Route')
    enter1.grid(row=2, column=0)

    # create the listbox1 (note that size is in characters)
    listbox1 = Listbox(mainframe, width=50, height=6)
    listbox1.grid(row=100, column=0)
    # create a vertical scrollbar to the right of the listbox
    yscroll = Scrollbar(command=listbox1.yview, orient=VERTICAL)
    #yscroll.grid(row=0, column=1, sticky=N + S)
    listbox1.configure(yscrollcommand=yscroll.set)

    #load routes
    get_routes()

    # left mouse click on a list item to display selection
    listbox1.bind('<ButtonRelease-1>', get_list1)

    # Label
    enter2 = Entry(mainframe, width=50, bg='yellow')
    enter2.insert(0, 'Click the direction')
    enter2.grid(row=500, column=0)

    # create the listbox2 (note that size is in characters)
    listbox2 = Listbox(mainframe, width=50, height=6)
    listbox2.grid(row=600, column=0)
    # create a vertical scrollbar to the right of the listbox
    yscroll2 = Scrollbar(command=listbox2.yview, orient=VERTICAL)
    # yscroll.grid(row=0, column=1, sticky=N + S)
    listbox2.configure(yscrollcommand=yscroll2.set)

    # Label
    enter3 = Entry(mainframe, width=50, bg='yellow')
    enter3.insert(0, 'Click the stops')
    enter3.grid(row=1200, column=0)


    # create the listbox3 (note that size is in characters)
    listbox3 = Listbox(mainframe, width=50, height=6)
    listbox3.grid(row=1300, column=0)
    # create a vertical scrollbar to the right of the listbox
    yscroll3 = Scrollbar(command=listbox3.yview, orient=VERTICAL)
    # yscroll.grid(row=0, column=1, sticky=N + S)
    listbox3.configure(yscrollcommand=yscroll2.set)


    print("row direction in main")
    print(rowid_Direction)

    #get_stops("901", "4")

    # left mouse click on a list item to display selection
    listbox2.bind('<ButtonRelease-1>', get_list2)

    # left mouse click on a list item to display selection
    listbox3.bind('<ButtonRelease-1>', get_list3)

    #Display
    enter4 = Entry(mainframe, width=50, bg='grey')
    enter4.insert(0, 'Next bus is after : ')
    enter4.grid(row=500, column=1)


    #Sub_button = Button(mainframe, text="Check Route time", command=clicked).grid(row=100, column=20)
    close_button = Button(mainframe, text="Close", command=lambda: close_window(window),width=50,height=5,bg='green').grid(row=100, column=1)


    window.mainloop()

