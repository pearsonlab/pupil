'''
Code for light/dark test orginally coded in Matlab.
'''
from psychopy import visual, core
import numpy as np
import display

def lightdarktest(mode,outfile): # mode = 0 (dark test) or 1 (light test), outfile is the file that data is saved to
	testWin = visual.Window(size=(640,400), monitor="testMonitor", units="pix") # Create window to display test
	if mode==0: # dark test
		task = 'darktest'
		numtrials = 3 # number of light/dark cycles
		habit_mat = [1,1,1] # set habituation to full brightness
		stim_mat = np.negative(np.ones((numtrials,3))) # set stimulus matrix to darkness
		rec_mat = np.ones((numtrials,3)) # back to full brightness for recovery
		stim_time = 1 # duration of stimulus in seconds
	elif mode ==1: # light test
		task = 'lighttest'
		habit_mat = [-1,-1,-1] # habituation is black
		stim_mat = [[-0.5, -0.5, -0.5], # stimulus is increasing brightness each time
					[0.00, 0.00, 0.00],
					[0.50, 0.50, 0.50],
					[1.00, 1.00, 1.00]]
		numtrials = len(stim_mat) # set numtrials based on number of stimulus conditions
		rec_mat = np.negative(np.ones((numtrials,3))) # recovery goes back to black
		stim_time = 0.2 # length of stimulus time in seconds
	habit_dur = 10 # time for habituation
	recover_dur = 8*np.ones((1,numtrials)) # time for recovery between stimuli
	stim_dur = stim_time*np.ones((1,numtrials)) # duration of each stimulus
	display.countdown(testWin) # display countdown before task

	# habituation
	display.fill_screen(testWin, habit_mat)
	core.wait(habit_dur)

	### Start eye tracking

	for i in range(numtrials):
		core.wait(2.0)

		# display stimulus
		display.fill_screen(testWin, stim_mat[i])

		### record timestamp on tracker for start of stimulus

		# wait for stimulus
		core.wait(stim_dur[0][i])

		# display recovery
		display.fill_screen(testWin, rec_mat[i])

		### record timestamp on tracker for end of stimulus

		# wait for recovery
		core.wait(recover_dur[0][i])

	### End eye tracking

	### Read and save eye data ()


if __name__ == '__main__':
	lightdarktest(0,None)