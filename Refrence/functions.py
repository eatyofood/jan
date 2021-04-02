import webbrowser
#from Refrence.chatbots.basic_example import ronBot
import pandas as pd
import pretty_errors
#from Janet import typewords
from pynput.keyboard import Key, Controller
import shutil 
from tqdm import trange
import time
import os
from datetime import datetime
import pyttsx3
kb = Controller()
resli = []
TALKMODE = False

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


def iterate_press(COMMAND,p,keys):
    '''
    iterates through a key, or keyboard shortcut howevermany times
    '''

    how_many = 1
    p = p.replace(COMMAND,'').split(' ')
    if len(p) == 2:
        p = p[1]
        if p in numbers.keys():
            how_many = int(numbers[p])


    for i in range(how_many):
        print('COMMAND')
        press(keys)

def open_term():
    press([Key.ctrl,'j'])
    wait(3)




def move_directory(original=None,target=None):
    if original == None:
        original = input('ORIGINAL FILE:')
    if target == None:
        target = input('TARGET FILE-PATH:')

    shutil.move(original,target)


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


def sys(a):
    os.system(a)

       
def typewords(words):
    print('==TYPEING WORDS==')
    kb.type(words)


 


def define_function(p):
    func_name = p.replace('define function ','').replace(' ','_')
    typewords('def {}():'.format(func_name))
    press(Key.enter)


def get_clone(working_dir):

    say('grabbing url in 2 seconds')
    wait(2)
    press([Key.ctrl,'l'])
    press([Key.ctrl,'c'])
    press([Key.esc])
    wait(1)
    press([Key.ctrl,'l'])
    press([Key.ctrl,'x'])
    say('insert the url for the repo')
    url = 'git clone ' + str(input('GITHUB REPO:'))
    dirname = url.split('/')[-1]
    if '.git' not in url:
        url = url+'.git'
    os.system(url)
    #check if there is a requirements folder
    dili = os.listdir(dirname)
    print(pd.DataFrame(dili,columns=['Files']))


    for i in dili:
        if 'req' in i:
            req_file = i
            say('this repo contains a dependencies list')


    
    
        
    #req_file = [f for f in dili if 'requirements' in f][0]
    say('do you want to enter directory from the terminal?')
    yn = str(input('ENTER TERMINAL?:'))
    
    if 'y' in yn.lower():
        say('you have 2 seconds to give me access to the terminal')

        wait(3)
    
        press([Key.ctrl,'j'])#open
        wait(1)
        press([Key.ctrl,'j'])#close
        wait(1)
        press([Key.ctrl,'j'])#open
        wait(1)
        #press([Key.ctrl,'j'])#close

        wait(2)
        #sys('cd {}'.format(dirname))
        typewords('cd {}'.format(dirname))
        wait(1)
        press(Key.enter)
        wait(1)
        typewords('ls')
        wait(1)
        press(Key.enter)
        
        typewords('pip install -r {}'.format(dirname))

def read_me(working_dir):
    CMD = 'ebook-viewer --detach '
    say('opening documentation' )
    dili = os.listdir(working_dir)
    mds  = [f for f in dili if '.md' in dili]
    if len(mds) > 0:
        print('there are {} .md files in: '.format(str(len(mds))),working_dir)
        say(('there are {} .md files in: '.format(str(len(mds))),working_dir))
        print(dili)
        if 'README.md' in dili:
            path = working_dir+'README.md'
            os.system(CMD + path)
    else:
        os.system(CMD + working_dir)

def print_function():
    typewords('print("")')
    press(Key.left)
    press(Key.left)


    

def terminal_directory(directory=None):
        if directory == None:
            say('insert directory path')
            directory = str(input('DIRECTORY:'))
        
        say('you have 2 seconds to give me access to the terminal')
        

        wait(3)
    
        press([Key.ctrl,'j'])#open
        wait(1)
        press([Key.ctrl,'j'])#close
        wait(1)
        press([Key.ctrl,'j'])#open
        wait(1)
        wait(2)
        #sys('cd {}'.format(dirname))
        typewords('cd {}'.format(directory))
        wait(1)
        press(Key.enter)
        wait(1)
        typewords('ls')
        wait(1)
        press(Key.enter)




def system_module(comand='""'):
    typewords("os.system({})".format(comand))
    press(Key.left)
    press(Key.left)


def for_i_in_range():
    typewords("for i in range(len()):")
    press(Key.left)
    press(Key.left)
    press(Key.left)





        

def tractor():
    typewords("""
                        #DOWNSHIFT!!
                        COMMAND = 'downshift'
                        KEYS    = [Key.shift,Key.down]
                        if COMMAND in p :
                            press(KEYS)
                            sp = len(p.replace(COMMAND,'').split(' '))
                            if sp > 0:
                                for i in range(sp):
                                    press(KEYS)    
    """)
def punt():
    press([Key.ctrl,'j'])
    wait(1)
    press([Key.ctrl,'j'])
    wait(1)
    press(Key.up)
    press(Key.enter)


def update_system():
    os.system("./restart_script.sh")

def hop():
    press([])

def back_end_parsing(p,TALKMODE):
    

    if 'test the new thing' in p:
        say('hello this is a new way to do this')
    


    if "kill line" in p:
        press([Key.ctrl,'d'])


    if ("pound" == p) or (p == 'lb'):
        press('#')

    if "micro heading" in p:
        press(Key.enter)
        typewords('### ')
        


    if "meditation" in p:

        os.system('rhythmbox-client --play Holosync\ -\ Awakening\ Prologue/Audio\ Training-Sync\ Meditation\ Centerpointe\ -\ Holosync\ -\ 02\ Of\ 06\ -\ The\ Dive.flac ')


    if "stop music" in p:
        os.system("rhythmbox-client --pause")

    if "establish database connection" in p:
        with open(r'Refrence/Templates/template1.py') as file:
            for line in file.readlines():
                typewords(line)


    if "create template" in p:
        
        say('what we calling this template?')
        #new_template = template_path + str(input('TEMPLATE NAME:'))
        
        # open code
        os.system('code /home/brando/algos/Develop/LaunchPad/Refrence/functions.py')
        wait(2)
        press([Key.ctrl,Key.end])
        press(Key.enter)
        say('what shall the command be?')
        command = str(input('COMMAND'))
        template_path = 'Refrence/Templates/'

        #if len(new_template.split()) < 2:
        num = len(os.listdir(template_path)) + 1
        new_template = template_path + 'template{}.py'.format((command.replalce(' ','')))

        say('please get back in the code editer 3 seconds')
        wait(3)
        
        typewords("""
    if '{}' in p:
    with open(r'{}') as file:
    for line in file.readlines():
    typewords(line)
                """.format(command,new_template))

        
        os.system('>{}'.format(new_template))
        os.system('gedit {}'.format(new_template))

    if 'import libraries' in p:
        with open(r'Refrence/Templates/template2.py') as file:
            for line in file.readlines():
                typewords(line)






    if "open web cam" in p:
        os.system("cheese")

    if "if path doesn't exist" in p:
        with open(r'Refrence/Templates/template4.py') as file:
            for line in file.readlines():
                typewords(line)


                                            


    if "favorite notebook" in p:
        webbrowser.open_new('http://localhost:8888/notebooks/Develop/DataBase/15min%20And%20Daily%20Downloaders.ipynb')

    if "daytime index" in p:
        typewords('df.index = pd.to_datetime(df.index)')


    if 'parsing strings' in p:
        with open(r'Refrence/Templates/template5.py') as file:
            for line in file.readlines():
                typewords(line)

                                        
    if "notebook checkpoint" in p:
        say('here is your notebook checkpoint')
        webbrowser.open_new('http://localhost:8888/notebooks/Develop/DataBase/Twitter%20-%20And%20Grids%20And%20Index%20All%20Right%20Here.ipynb')

    if "project free tv" in p:
        webbrowser.open_new('https://www.projectfreetv.fun/')
        


    if "this is a test" in p:
        say('this is a demonstration hell yeah')
    if "pay respects" in p:
        press('f')

    if 'duration function' in p:
        with open(r'Refrence/Templates/templateiteration.py') as file:
            for line in file.readlines():
                typewords(line)

    
                                        
    if "import pandas" in p:
        typewords('''
        import pandas as pd
        import numpy as np
        import cufflinks as cf
        cf.go_offline(connected=False)
        import os
        from tqdm import trange
        ''')
        kb.press(Key.shift)
        for i in trange(6):
            press(Key.up)
            wait(0.2)
        kb.release(Key.shift)

        for i in trange(8):
            press([Key.ctrl,'['])
            wait(0.2)



    if "for item in range" in p:
        typewords('for i in trange():')
    if "length of data frame" in p:
        typewords('len(df)')
    if "type words" in p:
        typewords('typewords([Key.')
    
    #thing
    COMMAND = 'comment lines'
    if (COMMAND in p) or ("comment out" in p) or ('comments out' in p) :
        iterations = 1
        sp = len(p.replace(COMMAND,'').split(' '))
        if sp > 0:
            try:
                iterations = int(w2n.word_to_num(p))
            except:
                pass
            for i in range(iterations):
                press('#') 
                press(Key.down)  
                press(Key.left) 

    if 'set up back test' in p:
            with open(r'Refrence/Templates/backtest_template8.py') as file:
                for line in file.readlines():
                    typewords(line)

                                    
                
                