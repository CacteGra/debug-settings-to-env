import pexpect
import sys
import os
import glob

def spawning():
    child = pexpect.spawn('python settings_to_env.py',timeout=None)
    child.logfile = sys.stdout.buffer
    return child

def answering(child,right_answer,right_path):
    answer = False
    path_answer = False
    while True:
        which_expect = child.expect(["will be set as value for all keys","Enter path to",'Enter value for','Did not find decouple',pexpect.EOF])
        if which_expect == 0:
            if not answer:
                answer = True
                child.sendline('l')
            elif answer and right_answer == 'n':
                child.sendline('n')
            elif answer and right_answer == 'y':
                child.sendline('y')
        elif which_expect == 1:
            if not path_answer:
                path_answer = True
                child.sendline('hello')
            elif right_path == '':
                child.sendline('')
            else:
                child.sendline(right_path)
        elif which_expect == 2:
            child.sendline('pexpecting_test')
        elif which_expect == 3 or which_expect == 4:
            break

def main():
    project_folder = ''
    while not project_folder:
        project_folder = input('Please provide project folder path to settings to env script\n(leave blank if the file is in the root folder of your Django application): ')
        if project_folder and not os.path.exists(os.path.dirname(project_folder)):
            while not os.path.exists(os.path.dirname(project_folder)):
                project_folder = input('Please provide valid project path or leave blank :')
        elif not project_folder:
            for filename in glob.iglob('./**/settings.py', recursive=True):
                project_folder = filename

    child = spawning()
    answering(child,'n','')
    child = spawning()
    answering(child,'y',project_folder)
    child = spawning()
    answering(child,'n',project_folder)
    child = spawning()
    answering(child,'y','')


if __name__ == '__main__':
    main()
