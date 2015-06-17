'''
Functions to display certain recurring instances throughout the different tests
(e.g. countdowns, menu, etc.)
'''
from psychopy import visual, core, event

def countdown(win, time):
	count_time = time  # countdown time in seconds
	countdown_text = visual.TextStim(win, text=str(count_time), 
        font='Helvetica', alignHoriz='center', alignVert='center', units='norm', 
        pos=(0, 0), height=0.2, color=[178, 34, 34], colorSpace='rgb255', 
        wrapWidth=2)
	for i in range(4):
		countdown_text.text = str(count_time)
		countdown_text.draw()
		win.flip()
		core.wait(1.0)
		count_time -= 1
	win.flip(clearBuffer=True) # clears countdown off of the screen

def fill_screen(win, window_color):
	rect = visual.Rect(win,2, 2, units='norm', fillColor=window_color) # set rect to fill window with color
	rect.draw()
	win.flip()

def text_keypress(win, text):
	display_text = visual.TextStim(win, text=text, 
        font='Helvetica', alignHoriz='center', alignVert='center', units='norm', 
        pos=(0, 0), height=0.1, color=[255, 255, 255], colorSpace='rgb255', 
        wrapWidth=2)
	display_text.draw()
	win.flip()
	event.waitKeys()

def cross(win):
	cross= visual.TextStim(win, text='+', 
        font='Helvetica', alignHoriz='center', alignVert='center', units='norm', 
        pos=(0, 0), height=0.3, color=[255, 255, 255], colorSpace='rgb255', 
        wrapWidth=2)
	cross.draw()
	win.flip()

