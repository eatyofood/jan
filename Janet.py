#!/usr/bin/env python3
from number_dictionary import number_dictionary
from Refrence.functions import back_end_parsing
import argparse
import os
import queue
import sounddevice as sd
import vosk
import sys
import pandas as pd
from pynput.keyboard import Controller
import pyttsx3
import pretty_errors
import os
import pandas as pd
from pynput.keyboard import Key, Controller
import time
from tqdm import trange
from datetime import datetime
from Refrence import functions as funk
from Refrence.memory import working_directory
from Chatty import ronBot
chat_skip = 0
working_dir = working_directory#'/home/brando/algos/Develop/LaunchPad'
script_name = ''
kb = Controller()

TYPE   = False
SLEEP  = False
NUMBER_MODE = False
RELAX_MODE=False
TALKMODE = False
response = ''
thing_you_said = []
q = queue.Queue()
"""
number_dictionary = {
    'one' : '1',
    'two' : '2',
    'too' : '2',
    'to'  : '2',
    'three' : '3',
    'four' : '4',
    'for'  : '4',
    'five' : '5',
    'six'  : '6',
    'seven' : '7',
    'eight' : '8',
    'nine'  : '9',
    'ten'   : '10',
    'point' : '.',
    'equals' : '='
}
"""
number_dictionary

rpath   = 'Refrence/'
numbers = dict(pd.read_csv(rpath+'numberStrings.csv').set_index('string').T)

def numbers_and_words():
    print('')


def press(key):
    '''
    this lets you press a key or a list of keys in the case of a keyboard shortcut...
    
    '''
    if type(key) != list:
        print('==SINGLE KEY==')
        kb.press(key)
        kb.release(key)
    
    
    else:

        print('==LIST KEYS==')

        if len(key) == 2:
            key1 = key[0]
            key2 = key[1]
        
            kb.press(key1)
            kb.press(key2)
            kb.release(key1)
            kb.release(key2)
        
        else:
                
            for i in key:
                kb.press(i)
            for i in key:
                kb.release(i)



def number_switcher(p):
    p = p.replace('digital input','')
    for i in number_dictionary.keys():
        p = p.replace(i,number_dictionary[i])
    return p 

       
def typewords(words):
    print('==TYPEING WORDS==')
    kb.type(words)


 

eng = pyttsx3.init()
eng.setProperty('rate',150)
eng.setProperty('voice','english+f4')
def say(words):
    
    os.system('figlet {}'.format(words))
    
    eng.say(words)
    eng.runAndWait()


def wait(seconds):
    '''
    start    = datetime.now()
    stoptime = start + pd.Timedelta(seconds=seconds)
    time_yet = False

    if time_yet == False:
    '''
    for i in trange(round(seconds*100)):
        time.sleep(0.01)
        #time_yet = stoptime > datetime.now()



# Open Browser
import webbrowser

browser = False
from word2number import w2n
def iterate_commands(COMMAND,KEYS,p,fig=True):
    if COMMAND in p :
        iterate = 1
        sp = len(p.replace(COMMAND,'').split(' '))
        print(len(p.replace(COMMAND,'').split(' ')))
        if sp > 0:
            try:
                iterate = w2n.word_to_num(p)
                print(iterate)
            except:
                iterate = sp
            for i in range(iterate):
                press(KEYS)   
                print('==KEY PRESS==')
                time.sleep(0.3)
        if fig == True:
            os.system("figlet {}".format(COMMAND))

def open_term():
    press([Key.ctrl,'j'])
    wait(3)


def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text

def callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

parser = argparse.ArgumentParser(add_help=False)
parser.add_argument(
    '-l', '--list-devices', action='store_true',
    help='show list of audio devices and exit')
args, remaining = parser.parse_known_args()
if args.list_devices:
    print(sd.query_devices())
    parser.exit(0)
parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter,
    parents=[parser])
parser.add_argument(
    '-f', '--filename', type=str, metavar='FILENAME',
    help='audio file to store recording to')
parser.add_argument(
    '-m', '--model', type=str, metavar='MODEL_PATH',
    help='Path to the model')
parser.add_argument(
    '-d', '--device', type=int_or_str,
    help='input device (numeric ID or substring)')
parser.add_argument(
    '-r', '--samplerate', type=int, help='sampling rate')
args = parser.parse_args(remaining)

try:
    if args.model is None:
        args.model = "model"
    if not os.path.exists(args.model):
        print ("Please download a model for your language from https://alphacephei.com/vosk/models")
        print ("and unpack as 'model' in the current folder.")
        parser.exit(0)
    if args.samplerate is None:
        device_info = sd.query_devices(args.device, 'input')
        # soundfile expects an int, sounddevice provides a float:
        args.samplerate = int(device_info['default_samplerate'])

    model = vosk.Model(args.model)

    if args.filename:
        dump_fn = open(args.filename, "wb")
    else:
        dump_fn = None
    li = []
    with sd.RawInputStream(samplerate=args.samplerate, blocksize = 8000, device=args.device, dtype='int16',
                            channels=1, callback=callback):
            print('#' * 80)
            print('Press Ctrl+C to stop the recording')
            print('#' * 80)

            rec = vosk.KaldiRecognizer(model, args.samplerate)
            while True:
                data = q.get()
                if rec.AcceptWaveform(data):
                    p = rec.Result().split('"text" : ')[1].replace('\n}','').replace('"','').replace('huh','') 
                    
                    if TALKMODE == True:
                        
                        if 'shut up' in p:
                            TALKMODE = False
                        
                        # IF ITS BROKEN ITS THIS ONE!
                        if chat_skip == 1:
                            p = ''
                        
                        if chat_skip == 0:
                            if p != response :
                                print('USER INPUT:',p)
                                response = ronBot(p)
                                
                                if (p not in thing_you_said) and (response not in thing_you_said) :
                                    thing_you_said.append(response)
                                    if len(p) > 0:
                                        say(response)
                                        chat_skip = 1
                                        wait(5)
                                    else:
                                        wait(1)
                                else:
                                    wait(2)
                        else:
                            chat_skip = 0
                            wait(3)



                    elif (SLEEP == False) or ('janet' in p) :
                        if 'speak your mind' in p:
                            TALKMODE = True

                            
                    
                        print(p)
                        if "number mode on" in p:
                            NUMBER_MODE = True
                            say('number lock')
                        if "number mode off" in p:
                            NUMBER_MODE = False
                            say('numbers off')


                        if "go to line " in p:
                            press([Key.ctrl,'g'])
                            wait(1)
                            res = w2n.word_to_num(test_str)
                            typewords(str(res))
                            wait(1)
                            press(Key.enter)
                                
                        if (NUMBER_MODE == True) or ('digit input' in p):
                            p = p.replace('digital input','')
                            for i in number_dictionary.keys():
                                p = p.replace(i,number_dictionary[i])
                            

                            
                        #ALL THE FUNCTIONS IN functions.py
                        back_end_parsing(p,TALKMODE)

                        
                        if "proper" in p:
                            p = ' '.join([''.join([w[0].upper(),w[1:]]) for w in p.split(' ')]).replace('Proper ','')
                            typewords(p)

                        
                        if 'typing mode on' in p:
                            TYPE = True
                        if 'typing mode off' in p:
                            TYPE = False
                        if TYPE == True:
                            kb.type(p.replace('typing mode'))

                        '''
                        ACTIVE FUNCTIONS : 
                        '''
                        # delete - TURN THIS INTO A FUNCTION. and combined with the 




                        if 'scratch' in p:
                            how_many = 1
                            p = p.replace('scratch','').split(' ')
                            if len(p) == 2:
                                p = p[1]
                                if p in numbers.keys():
                                    how_many = int(numbers[p])


                            for i in range(how_many):
                                print('COMMAND')
                                press([Key.shift,Key.ctrl,Key.left])
                                press(Key.backspace)

                        
                        if "zebra" in p:
                            press([Key.ctrl,'z'])
                            p_len = p.split(' ')
                            #if len(p_len)> 1:

                                

                                        
                        #ENTER
                        if 'slap' in p:
                            press(Key.enter)
                        #ENTER
                        if 'flat' in p:
                            press(Key.enter)


                        if "snack" in p:
                            press(Key.enter)


                            #say('FIRE!!')
                        #ESC
                        if 'escape' in p:
                            say('escaping')
                            press(Key.esc)
                        if 'bale' in p:
                            say('escaping')
                            press(Key.esc)
                        if 'hail' in p:
                            say('escaping')
                            press(Key.esc)
                        if 'mail' in p:
                            say('escaping')
                            press(Key.esc)
                        if "right" in p :
                            press(Key.right)
                        # LEFT-ARROW
                        if "'left'" in p :
                            press(Key.left)
                        # UP ARROW
                        if 'newyork' in p:
                            press(Key.up)
                        

                        #BACK 
                        if 'go back' in p:
                            press([Key.alt,Key.left]) 
                        # DOWN 
                        if 'tickle' in p:
                            say('he he he he')
                            press(Key.down)
                            wait(1)
                            press(Key.down)
                            wait(1)
                            press(Key.down)
                        

                        '''
                        FUNCTION READY ITERATION [PARSE]
                        '''
                        COMMAND = 'step forward'
                        KEYS    = [Key.ctrl,Key.right]
                        iterate_commands(COMMAND,KEYS,p)
                        COMMAND = 'stepped forward'
                        KEYS    = [Key.ctrl,Key.right]
                        iterate_commands(COMMAND,KEYS,p)
                        

                        COMMAND = 'step back'
                        KEYS    = [Key.ctrl,Key.left]
                        iterate_commands(COMMAND,KEYS,p)

                        # UP
                        COMMAND = 'go up'
                        KEYS    = Key.up
                        iterate_commands(COMMAND,KEYS,p)
                        COMMAND = 'new york'
                        iterate_commands(COMMAND,KEYS,p)


                        #
                        COMMAND = 'go down'
                        KEYS    = Key.down
                        iterate_commands(COMMAND,KEYS,p)
                        COMMAND = 'florida'
                        iterate_commands(COMMAND,KEYS,p)
                            
                        COMMAND = 'oops'
                        KEYS    = [Key.ctrl,'z']
                        iterate_commands(COMMAND,KEYS,p)
                        
                        COMMAND = 'smack'
                        KEYS    = Key.enter
                        iterate_commands(COMMAND,KEYS,p)

                        






                        COMMAND = 'texas'
                        KEYS    = [Key.ctrl,Key.tab]
                        iterate_commands(COMMAND,KEYS,p)


                        if 'para' in p:
                            press('(')                    

                        COM = 'find me '
                        if (COM in p) and (' find' not in p):
                            press([Key.ctrl,'f'])
                            wait(1)
                            p = p.replace(COM,'')
                            typewords(p)


                        if 'replace it with' in p:
                            press([Key.ctrl,'h'])
                            
                        if 'window left' in p:
                            press([Key.ctrl_r,'`'])
                        if 'window right' in p:
                            press([Key.ctrl,'2'])
                        if 'window up' in p:
                            press([Key.ctrl,'1'])
                        if 'window down' in p:
                            press([Key.ctrl,'q'])
                        if 'moniter up' in p:
                            press([Key.alt,'1'])
                        if 'moniter down' in p:
                            press([Key.alt,'2'])
                        

                        if 'firefox' in p:
                            webbrowser.open_new(p.replace('firefox',''))

                        


                        #CLOSE WINDOW
                        if 'close window' in p:
                            press([Key.ctrl,'w'])
                        #SAVE
                        if 'save' in p:
                            press([Key.ctrl,'s'])
                        if 'saber' in p:
                            press([Key.ctrl,'s'])


                        # ALT + TAB
                        if 'altering' in p:
                            press([Key.alt_l,Key.tab])
                        
                        #scroll up OR SCRUB?
                        #if 'job' in p:
                        #    press(Key.page_up)

                        #nebraska
                        if 'nebraska' in p:
                            press([Key.ctrl,'n'])
                        
                        # typeing function
                        if 'insert' in p:
                            typewords(p.replace('insert ',''))
                            #typewords(p)
                        

                        
                        if "tractor" in p:
                            funk.tractor()
                        #DOWNSHIFT!!
                        COMMAND = 'downshift'
                        KEYS    = [Key.shift,Key.down]
                        iterate_commands(COMMAND,KEYS,p)

                        

                        # LAUNCH BROWSER
                        if 'browser' in p:
                            press([Key.ctrl,Key.shift,'b'])
                        if 'search ' in p:
                            page = p.replace('search ','')
                            if len(page) > 0:
                                webbrowser.open_new(page)
                                wait(2)
                                press([Key.ctrl,'l'])
                                typewords(page)

                            else:
                                webbrowser.open_new()
                            
                            #press([Key.ctrl,Key.shift,'b'])
                            #wait(2)
                            #press([Key.ctrl,'l'])
                            #wait(1)
                            typewords(p.replace('search',''))
                        # UNDO
                        if 'undo' == p:
                            press([Key.ctrl,'z'])
                        # REDO
                        if 'redo' in p:
                            press([Key.ctrl,Key.shift,'z'])
                        # SHIFT LEFT
                        if 'shit' == p:
                            press([Key.shift,'z'])
                        #  CTRL SHIFT LEFT
                        if 'cow shit' in p:
                            press([Key.ctrl,Key.shift,Key.left]) 
                        # ALT + O --> ENTER 
                        if 'okay' in p:
                            press([Key.alt,'o'])
                            press(Key.enter)
                        # CTRL SHIFT
                        if 'chris' in p:
                            press([Key.ctrl,Key.right,Key.shift])
                        # BRACKETS
                        if 'barracuda' in p:
                            press('[')
                        # PARENTASIS - 
                        if 'pay' in p:
                            press('(')
                        # HOT KEY ONE
                        #if 'guitar' in p:
                        #    hot_key_one()
                        # REDO!
                        if 'yes' in p:
                            press([Key.ctrl,Key.shift,'z'])
                        # PASTE
                        if 'paste' in p:
                            press([Key.ctrl,'v'])
                        if 'vampire' in p:
                            press([Key.ctrl,'v'])
                        if 'alligator' in p:
                            press([Key.ctrl,'x'])
                        # COPY 
                        if 'copy' in p:
                            press([Key.ctrl,'c'])
                        if 'crocodile' in p:
                            press([Key.ctrl,'c'])
                        # PASTE
                        if 'cut' in p:
                            press([Key.ctrl,'x'])
                        # CTRL + L 
                        if 'address' in p:
                            press([Key.ctrl,'l'])
                        # INDENT
                        if 'to the right' in p :
                            press([Key.ctrl,']'])
                            sp = len(p.replace('to the right','').split(' '))
                            if sp > 0:
                                for i in range(sp):
                                    press([Key.ctrl,']'])
                        COMMAND = 'bank right'
                        if COMMAND in p :
                            press([Key.ctrl,']'])
                            sp = len(p.replace(COMMAND,'').split(' '))
                            if sp > 0:
                                for i in range(sp):
                                    press([Key.ctrl,']'])

                                        
                        # UN-INDENT
                        if 'to the left' in p :
                            press([Key.ctrl,'['])
                        # TRAVEL NORTH
                        if "scroll up" in p :
                            press(Key.page_up)
                        # TRAVEL SOUTH
                        if "scroll down" in p :
                            press(Key.page_down)
                        # QUOTE
                        if "quote" in p :
                            press("'")
                        # DELETE
                        if "destroy" in p :
                            press(Key.backspace)
                        
                        if 'update script' in p:
                            os.system('python3 Janet.py')
                        # DOWN
                        #if "down" in p :
                        #    press(Key.down)
                        
                        #print()
                        # GO TO (')
                        
                        
                        if 'go to sleep' in p:
                            say('eye yum sleepy')
                            #sleep = input('zzZZZZzzzzZZZZzz:') # this could also trigger a pocket spinx function that intentialy hangs up
                            SLEEP = True
                        if "restart colonel" in p:
                            press('9')    
                            press('9')    

                        # #INSERT PREV LINE
    #                    if "answer" in p :
    #                        typewords(prev_word)
    #                    if "insert" in p :
    #                        typewords(prev_word)
                            
                        if 'you tube' in p:
                            webbrowser.open_new('youtube.com')
                            browswer = False
                            say('launching youtube brandon')
        
                        if 'open messenger' in p:
                            webbrowser.open_new('https://www.facebook.com/messages/t/549866038')
                            browswer = False
                            say('opening messenger')

                        if 'system reboot' in p:
                            os.system('reboot')

                        # OPEN YOUTUBE: 
                        if 'open work enviroment' in p:
                            os.system('./launchLaunchPad.sh')

                        if 'full screen' in p:
                            press(Key.f11)
                        
                        if "proper" in p:
                            print('type stuff with caps on the first letter of things')


                        #if 'you tube' in p:
                        #    webbrowser.open_new('youtube.com')
                        #    browswer = False
                        #    say('launching youtube brandon')
                        
                        #
                        if 'khan academy' in p:
                            webbrowser.open_new('https://www.khanacademy.org/computing/computer-programming/sql/more-advanced-sql-queries/pc/challenge-the-wordiest-author')
                            browswer = False
                            say('launching khan academy brandon')
            
                        if 'rolling review' in p:
                            page = 'http://localhost:8888/notebooks/opmem/Review.ipynb'
                            webbrowser.open_new(page)
                            browswer = False
                            say('launching review')
                            

                        if 'rolling journal' in p:
                            page = 'http://localhost:8888/notebooks/Research/ProjectReports/RollingJornal.ipynb'
                            webbrowser.open_new(page)
                            browswer = False
                            say('launching jornal')
                            press([Key.ctrl,'l'])
                            wait(1)
                            typewords(page)
                            #webbrowser.open_new(page,)
                            #webbrowser.Mozilla(page)

                        if 'open virtual code'in p:
                            os.system('code')
                        if 'statement if'in p:
                            typewords('    if in p:')
                            it = 5
                            for i in range(it):
                                press(Key.left)
                            press(Key.space)
                            press(Key.left)
                            press('"')
                        if "explore files" in p:
                            press([Key.ctrl,Key.shift,'@'])

                        if 'try terminal' in p:
                            press([Key.ctrl,'j'])
                            wait(3)
                            #typewords('echo hello there angle from my nightmare')
                            wait(1)
                            #press(Key.enter)
                        
                        if ('set working directory' in p) or ('change working directory' in p):
                            say('paste the directory you are working in')
                            working_dir = str(input('DIRECTORY:'))
                            
                            # SAVE DIRECTORY IN MEMTORY 
                            memory_path = 'Refrence/memory.py'
                            a_file = open(memory_path, "r")
                            list_of_lines = a_file.readlines()
                            new_line = ( '"' + working_dir + '"' )
                            list_of_lines[0] = "working_directory = {}\n".format(new_line)
                            a_file = open(memory_path, "w")
                            a_file.writelines(list_of_lines)
                            a_file.close()

                        


                            say('you are now working in {}'.format(working_dir.split('/')[-1]))
                            #now you can insert this var to do anything...
                        
                        if 'create python script' in p:
                            
                            print('CREATE')
                            say('by what name shall this holy script be known')
                            script_name = str(input('SCRIPT NAME:'))
                            say('and thoust script shall be known as {}'.format(script_name.replace('.py','')))
                            script_name = working_dir +'/' +script_name

                            wait(5)
                            open_term()
    #                        typewords('echo import pandas as pd >{}'.format(working_dir))
                            os.system('echo import pandas as pd >{}'.format(working_dir))
                            wait(1)
                            #press(Key.enter)
                            say('the maker hasts maked another sctipt')
                            wait(1)
                            say('and it was good')

                            wait(1)
    #                        typewords('code {}'.format(script_name))
                            os.system('code {}'.format(script_name))

                            #press(Key.enter)
                            #print('obviously it makes more sense to do this with os but typing is cool ')
                            
                        if "define function" in p:
                            funk.define_function(p)
                        
                        if "score" in p:
                            p = p.replace('score ','').replace(' ','_')
                            typewords(p)
                        
                        if 'open janet' in p:
                            os.system('code /home/brando/algos/Develop/LaunchPad/Janet.py')

                        if 'executive exit' in p:
                            press([Key.alt,Key.f4])

                        if 'create function' in p:
                            os.system('code /home/brando/algos/Develop/LaunchPad/Refrence/functions.py')
                            wait(2)
                            press([Key.ctrl,Key.end])
                            press(Key.enter)

                            typewords('    if in p:')
                            it = 5
                            for i in range(it):
                                press(Key.left)
                            press(Key.space)
                            press(Key.left)
                            typewords('""')
                            press(Key.left)

                        
                        if "rhthym box" in p:
                            os.system('rhythmdb-file ')


                        if 'git clone' in p:
                            funk.get_clone(working_dir)
                        if 'get clone' in p:
                            funk.get_clone(working_dir)
                    
                        if 'terminal directory' in p:
                            say('do you want to transfer to your working directory')
                            print('------------CURRENT DIRECTORY-----------------')
                            print(working_dir)
                            yn = input('USE THIS DIRECTORY?:')
                            d = None
                            if 'y' in yn.lower():
                                d = working_dir
                            funk.terminal_directory(d)

                        if "read me" in p:
                            funk.read_me(working_dir)

                        if "armageddon" in p:
                            press([Key.ctrl,Key.end])
                        if "olympus" in p:
                            press([Key.ctrl,Key.home])
                            #kb.press(Key.alt_l)
                            #wait(1)
                            #kb.press(Key.esc)
                            #wait(1)
                            #kb.release(Key.alt_l)zt
                            #kb.release(Key.esc)
                        if "for i in range" in p:
                            funk.for_i_in_range()

    
                            #press([Key.alt,Key.esc])
                            
                        if "system module" in p:
                            funk.system_module()

                        if "print function" in p:
                            funk.print_function()

                        if 'update system' in p :
                            funk.update_system()

                        if ('punt' in p) or ('hunt' in p):
                            funk.punt()
                        if "enlarge" in p:
                            press([Key.ctrl,'='])
                        if "it's too big" in p:
                            press([Key.ctrl,'-'])
                        if "karma" in p:
                            press(',')

                        if "shit kick" in p:
                            press([Key.shift,Key.enter])

                        if "key library" in p:
                            typewords('press(Key.')

                        if "jump" in p:
                            press([Key.ctrl,Key.right])
                            press([Key.ctrl,Key.right])
                            press([Key.ctrl,Key.right])
                            press([Key.ctrl,Key.right])
                            press(Key.enter)

                        if "bullet point" in p:
                            press(Key.enter)
                            typewords('- ')
                        

                        
                        if "cellular" in p:
                            press(Key.esc)
                            press('b')

                        if "kick" in p:
                            press(Key.enter)
                    
                        if "notation so" in p:
                            press([Key.esc,'1'])


                                        # -- make a note taking function that uses markdown notation 
                    #
                    #--config file that saves working direcory
                    #--a hotkey and hot directorys menue
                    #
                    else:
                        #print('zzzzZZZzzz')
                        
                        if 'wake up' in p:
                            SLEEP = False
                            #if RELAX_MODE == False: # sleep mode is just going to keep turning sleep mode back on 
                            say('good morning')
                        else:
                            zs = []
                            for i in range(len(p.split())):
                                zs.append('z'+'Z')
                            z = ''.join(zs)
                            #print(z)

                            

                    #if 'routine' in p:
                    #    os.system('python3 /home/brando/routine.py')

                    
                    #print(rec.PartialResult())
                if dump_fn is not None:
                    dump_fn.write(data)

                


except KeyboardInterrupt:
    print('\nDone')
    parser.exit(0)
#except Exception as e:
#    parser.exit(type(e).__name__ + ': ' + str(e))


