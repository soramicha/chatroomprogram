import curses
import threading
import time
import os

class Screen:
    def __init__(self):
        screen = curses.initscr()
        curses.start_color()
        self.num_rows, self.num_cols = screen.getmaxyx()
        
        # create color pairs
        curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)

        # pad will be 1000 lines tall, with 100 columns
        self.pad = curses.newpad(1000, self.num_cols)

        self.startingrowonwindow = self.num_rows - 1
        # 1 = number of lines to make, num_cols is the number of characters you have per line, (self.startingrowonwindow, 0) is where to start (y, x)
        self.my_window = curses.newwin(1, self.num_cols, self.startingrowonwindow, 0)
        
        # calculate where on the pad to print out the results
        self.startingrowonpad = self.startingrowonwindow - 2 # two lines above the startingrowonwindow
        self.numlines = 0
        self.startlinetoshow = 0
        
        # create a lock to prevent race condition
        self.lock = threading.Lock()

    # 1 for don't echo, 2 for echo
    def messageshowstatus(self, value):
        if value == 1:
            # hide user's typing
            curses.noecho()
        else:
            # flush out all input buffer
            curses.flushinp()
            
            # turn back echo to allow user to see what they type
            curses.echo()

    # get input and return it in string
    def getinput(self):
        # get string in windows
        message = self.my_window.getstr()
        
        # erase the string in window
        self.my_window.erase()
        
        return str(message, 'utf-8') # RETURN IN STRING FORM

    # print out the message
    def showmessage(self, message, colorpair): # get message in STRING FORM
        # prevents race conditiion with different threads accessing same functions at the same time
        with self.lock:
            # get window cursor coordinates (y, x)
            windowy, windowx = self.my_window.getyx()
            
            thestring = message
            
            # count number of lines on the pad
            self.numlines += thestring.count('\n')
            
            # print out the string
            self.pad.addstr(thestring, curses.color_pair(colorpair))
            
            # refresh will refresh the entire screen and change all positions of the line
            if (self.startingrowonpad-self.numlines) < 0:
                self.startlinetoshow = self.numlines - self.startingrowonpad
                
            # first line to show, first character to show, where on the screen to start (y, x), max lines showing, max chars showing on one line
            self.pad.refresh(self.startlinetoshow, 0, self.startingrowonpad-self.numlines, 0, self.startingrowonpad, self.num_cols - 1)
            self.numlines += 1
            
            self.pad.addstr("\n")
            
            # move cursor back to window and then refresh the window
            self.my_window.move(windowy, windowx)
            self.my_window.refresh()
    
    # close screen
    def close(self):
        curses.endwin()
    
"""  

# ~ UNIT TESTING ~

def printoutnum(screen):
     count = 0
     while True:
         screen.showmessage(str(count), 1)
         count += 1
         time.sleep(5)
         
def printhi(screen):
    while True:
        screen.showmessage("Hi", 1)
        time.sleep(3)
         
def miniprogram():
    screen = Screen()
    threading.Thread(target=printoutnum, args=[screen]).start()
    while True:
        screen.showmessage(screen.getinput(), 1)
        
# check if this is the only file running, if so, this will run, otherwise it won't because it's imported to somewhere else
if __name__ == "__main__":
    miniprogram()

# ~ MINI PROGRAM TO EXPERIMENT WITH CURSES ~

def miniprogramscreen(username):
    # initialize screen
    screen = curses.initscr()
    curses.start_color()
    num_rows, num_cols = screen.getmaxyx()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_RED)

    # pad will be 1000 lines tall, with 100 columns
    pad = curses.newpad(1000, 100)

    # 2 = number of lines to make, 100 is the number of characters you have per line, 0, 0 is where to start (y, x)
    my_window = curses.newwin(2, 100, (num_rows - 1), 0)

    start = num_rows - 3
    numlines = 0
    linenumber = 0
   
    while True:
        # get string in windows
        c = my_window.getstr()
        
        # add the string in windows it to the pad
        pad.addstr(bytes(username, 'utf-8') + b": " + c + b"\n", curses.color_pair(1))

        # erase the string in windows
        my_window.clear()
        my_window.refresh()

        # first line to start, first character to start, where on the screen to start (y, x), max lines showing, max chars showing on one line
        # refresh will refresh the entire screen and change all positions of the line, allowing scrolling through the pad
        if (start-numlines) < 0:
            linenumber += 1
            
        # post the string
        pad.refresh(linenumber, 0, start-numlines, 0, start, 100)
        numlines += 1
        
        if "bye" in str(c, 'utf-8'):
            curses.napms(1000)
            break

    curses.endwin()
"""