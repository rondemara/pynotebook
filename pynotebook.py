#!/usr/bin/python

import sqlite3
import json
import sys
import readline 
import curses
from curses.textpad import Textbox, rectangle

#config stuff
database = "data/data.db"

#------------------------------------------------
#Setup:
def setup_database():
   con = sqlite3.connect(database)
   with con:
      c = con.cursor()
      c.execute('CREATE TABLE IF NOT EXISTS NOTEBOOKS(id INTEGER PRIMARY KEY, name TEXT)')
      c.execute('CREATE TABLE IF NOT EXISTS NOTES(id INTEGER PRIMARY KEY, title TEXT, date TEXT, data TEXT, notebook_id INTEGER, FOREIGN KEY(notebook_id) references NOTEBOOKS(id))')

#------------------------------------------------
#Notebook Functions
def get_notebooks():
   con = sqlite3.connect(database)
   with con:
      c = con.cursor()
      return c.execute('SELECT name FROM NOTEBOOKS ORDER BY name').fetchall()

def add_notebook(name):
   con = sqlite3.connect(database)
   with con:
      c = con.cursor()
      c.execute('INSERT INTO NOTEBOOKS (name) values("%s")' % name)
      if con.total_changes == 1:
         print "Added: %s" % name
      else:
         print "Failed to add: %s" % name

def delete_notebook(name):
   con = sqlite3.connect(database)
   with con:
      c = con.cursor()
      c.execute('DELETE FROM NOTEBOOKS WHERE (name="%s")' % name)
      if con.total_changes == 1:
         print "Deleted: %s" % name
      else:
         print "Failed to delete: %s" % name

#------------------------------------------------
def list_notebooks():
   notebooks = get_notebooks()
   print "   ------------------"
   print "   Notebooks (%d): " % len(notebooks)
   for notebook in notebooks:
      print "\t" + notebook[0]
   print "   ------------------"

def delete_notebook_menu(name = ""):
   if name == "":
      notebooks = get_notebooks()
      print "Choose a notebook below:"
      for i in xrange(len(notebooks)):
         print "\t(%d) %s" % (i+1, notebooks[i][0])
      id = raw_input("ID: ")
      delete_notebook(notebooks[int(id)-1][0])
   else:
      delete_notebook(name)

def open_notebook():
   notebooks = get_notebooks()

   if len(notebooks) >0:
      print "Choose a notebook below:"
      for i in xrange(len(notebooks)):
         print "\t(%d) %s" % (i+1, notebooks[i][0])
      id = raw_input("ID: ")
      note_menu(notebooks[int(id)-1][0])
   else:
      print "No notebooks to select from."
#------------------------------------------------
#Note Functions
def text_edit(text_to_display):
   stdscr = curses.initscr()
   curses.noecho()
   stdscr.addstr(0, 0, "%s: (hit Ctrl-G when finished)" % text_to_display)

   editwin = curses.newwin(20, 100, 2,1)
   rectangle(stdscr, 1,0, 1+20+1, 1+100+1)
   stdscr.refresh()

   box = Textbox(editwin)

   # Let the user edit until Ctrl-G is struck.
   box.edit()

   # Get resulting contents
   data =  box.gather()
   curses.endwin()
   return data   

def add_note(name):
   title = raw_input("Title: ")
   print "Enter Data: (Ctrl-D to finish)"
   #data = sys.stdin.readline()
   data = text_edit("Enter Note")

   con = sqlite3.connect(database)
   with con:
      c = con.cursor()
      c.execute('INSERT INTO NOTES (title, date, data, notebook_id) VALUES("%s", DATE(), "%s", (SELECT id FROM NOTEBOOKS WHERE name="%s"))' %(title, data, name))
      if con.total_changes == 1:
         print "Added: %s" % title
      else:
         print "Failed to add: %s" % title


def get_notes(name):
   con = sqlite3.connect(database)
   with con:
      c = con.cursor()
      return c.execute('SELECT title FROM NOTES WHERE notebook_id = (SELECT id FROM NOTEBOOKS WHERE name="%s") ORDER BY title' % name).fetchall()

def list_notes(name):
   notes = get_notes(name)
   print "   ------------------"
   print "   Notes (%d): " % len(notes)
   for note in notes:
      print "\t" + note[0]
   print "   ------------------"

#------------------------------------------------
#Menus
def note_menu(name):
   loop =1
   while loop ==1:
      print "\nNotes Menu:"
      list_notes(name)
      print "   (1) List Notes"
      print "   (2) Add Note"
      print "   (3) Open Note"
      print "   (4) Delete Note by Name"
      print "   (5) Delete Note by ID"
      print "   (6) Back to Notebooks"
      option = raw_input("Enter an option: ")

      if option == "1":
         list_notes(name)
      elif option == "2":
         add_note(name)
      elif option == "3":
         open_note(name)
      elif option == "4":
         delete_note(raw_input("Note Name: "), name)
      elif option == "5":
         delete_note_menu(name)
      else:
         loop = 0

def notebook_menu():
   loop =1
   while loop ==1:
      print "\nNotebook Menu: "
      list_notebooks()
      print "   (1) List Notebooks"
      print "   (2) Add Notebook"
      print "   (3) Select Notebook"
      print "   (4) Delete Notebook by Name"
      print "   (5) Delete Notebook by ID"
      print "   (6) Exit"

      option = raw_input("Pick an option: ")

      if option == "1":
         list_notebooks()
      elif option == "2":
         add_notebook(raw_input("Notebook Name: "))
      elif option == "3":
         open_notebook()
      elif option == "4":
         delete_notebook(raw_input("Notebook Name: "))
      elif option == "5":
         delete_notebook_menu()
      else:
         loop = 0

#Entry points:
setup_database()
notebook_menu()
