import numpy as np
from psychopy import prefs
prefs.general['audioLib'] = ['pyo']
from psychopy import visual, core, sound, event
import display

def oddball(outfile,flag,*args):
	# create new oddball file
	if flag==0:
		numswitches=args[0]
		minbetween=args[1]
		maxbetween=args[2]
		trialvec = makeoddballs(numswitches,minbetween,maxbetween,np.random.randint(1,9999))
	# loads from previously created oddball file
	elif flag==1:
		trialvec = np.genfromtxt('OddballVectors.csv', delimiter=',')

	# set up window
	testWin = visual.Window(size=(640,400), monitor="testMonitor", units="pix") # Create window to display test
	# load sounds
	resource_path = '../task/'
	lowsnd = sound.Sound(resource_path+'500.wav')
	highsnd = sound.Sound(resource_path+'1000.wav')
	# parameters for task
	iti_mean = 3
	iti_range = 2
	# display instructions
	display.text_keypress(testWin, 'In this task, you will listen to some sounds. \n Press any key to continue')
	# play sound samples
	lowsnd.play()
	display.text_keypress(testWin, 'Some sounds are low... \n Press any key to continue')
	highsnd.play()
	display.text_keypress(testWin, '...and some are high. \n Press any key to continue')

	display.text_keypress(testWin, 'When you hear a sound, press the space bar.\n\nPress any key when ready.')
	display.countdown(testWin,4)

	### start eye tracking

	core.wait(2.0) # give small wait time before starting trial

	for isHigh in trialvec:
		### record timestamp for sound play

		if isHigh:
			highsnd.play() # play high sound if oddball
		else:
			lowsnd.play() # otherwise play low sound

		# wait for space bar
		keypress = event.waitKeys(keyList=['space','q'])
		if keypress[0] == 'q':
			break
		elif keypress[0] == 'space':
			### record timestamp for key press
			1+1

		iti = iti_mean + iti_range*(2*np.random.random()-1)

		core.wait(iti)

		### save data for each trial (i.e. timestamps and task and parameters)

	### stop eye tracking

	### read eye data and save


def makeoddballs(noddballs,minrun,maxrun,seed):
	# set the seed
	np.random.seed(seed)

	# run lengths (between min and max) surround each oddball
	lens = np.random.random_integers(minrun,maxrun,noddballs+1)
	#calculate oddballs
	oddtrials = np.cumsum(lens)
	isodd = np.zeros((1,oddtrials[-1]))[0]
	isodd[oddtrials[:-1]] = 1
	np.savetxt('OddballVectors.csv',isodd,delimiter=",")
	return isodd

if __name__ == '__main__':
	# oddball(None,0,5,3,7)
	oddball(None,1)