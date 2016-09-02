#!/usr/bin/env python
"""
VMDpipe provides a set of api to use vmd from python executing tcl code and scripts.

In the present version, the module does not provide any class,
python interpreter in VMD is not supported and only a single VMD
instance is allowed.

VMD executable can be set using vmdpipe.Vsetpath(path) and retrieved using vmdpipe.Vgetpath(path)

vmdpipe.printout (boolean) = True is useful for interactive: vmd stdout is
printed to screen instead of being returned as strings

defaultTimeout specifies the wait time (in seconds) before an error is raised 
if VMD does not respond. In this case VMD instance is not closed. 
You can wait further using vmdpipe.ping() or kill the instance with vmdpipe.Vkill()

ioLag defines a default time interval before reading vmd stdout after sending a command 
using vmdpipe.send_string()

Module is implemented using subprocess module and vmd stderr is accessible via vmdpipe._vmdin.stderr 
(See subprocess manual)
""" 

import os
import sys
import threading
from subprocess import Popen, PIPE, STDOUT, check_output, run
from time import sleep

__author__ = "Salvatore M Cosseddu"
__copyright__ = "Copyright 2016, SMCosseddu"
__credits__ = ["Salvatore M Cosseddu"]
__license__ = "GPL"
__version__ = "0.0.1"
__maintainer__ = "Salvatore M Cosseddu"
__status__ = "Development"


# --------------------------------------------------
#               Common variables
printout=True
defaultTimeout=15
ioLag=0.01
_vmdexec='vmd'
_vmdin=None
_listener=None

# set/get
def Vsetpath (p):
    """set path of vmd, default vmd from bash env"""
    global _vmdexec
    _vmdexec=p

def Vgetpath():
    """get path of vmd used by the module"""
    return(_vmdexec)

# --------------------------------------------------
#                Opening/closing 
def Vopen(gui=True, timeout=defaultTimeout, returnInitStdout=False):
    """
    open a vmd instance, use only for interactive/test purposes
    set text to False for interactive use with gui

    An error is raised if VMD does not respond within timeout sectonds. In this case VMD instance is not closed. 
    You can wait further, observe using ping() or kill the instance with Vkill()

    if returnInitStdout is True, the function return the init stdout of VMD as string  

    if vmd.printout is True, init stdout is printed to screen (useful for interactive use)
    """
    global _vmdin

    # check if a vmd instance exists
    if isVMDopen():
        raise "VMD instance already exists, terminate it before starting a new one"
    
    if gui:
        # interactive with gui
        command=[_vmdexec, "-nt"]
    else:
        # dispdev text 
        command=[_vmdexec, "-dispdev", "text"]

    _vmdin=Popen(command, stdout=PIPE, stdin=PIPE, stderr=PIPE, bufsize=1, universal_newlines=True)

    # test if vmd has started 
    initStdout=ping(timeout)
    if printout:
        sys.stdout.write("".join(out))
        print("(vmdpipe) started")
    
    if returnInitStdout:
        return(initStdout)
    else:
        return
   

def Vclose(timeout=10):
    """close the vmd instance opened by Vopen() and return the returncode"""
    global _vmdin
    send_string("\nexit 0\n")
    try:
        return _vmdin.wait(timeout)
    except:
        print("VMD took more than timeout to exit, will be terminated")
        _vmdin.terminate()
        return _vmdin.poll()

def Vkill():
    """kill the vmd instance opened by Vopen()"""
    _vmdin.kill()


def isVMDopen():
    if _vmdin is None:
        # never opened
        return False
    if _vmdin.poll() == None:
        return True
    else:
        # closed
        return False
# --------------------------------------------------
#                  Check VMD
def callback(signal, capture_stdout):
    """listen vmd for a signal and capture stdout"""
    for reply in iter(_vmdin.stdout.readline, ''):
        if reply.strip() == signal:
            return(capture_stdout)
        else:
            capture_stdout.append(reply)

def ping(timeout=defaultTimeout, signal='vmdpipesignal'):
    """
    Send signal to vmd and wait timeout seconds for the response. Finally return the stdout 
    """
    # variable to capture the stdout

    global _listener
    global _commandStdout

    # if listener still alive simply go on listening
    if _listener != None and _listener.isAlive():
        return _testCallback(timeout)

    # otherwise start a new listener
    _commandStdout=[]
    
    # send signal
    _vmdin.stdin.write("set VMDPIPESIGNAL "+signal+"\n")

    # start a deamon that listen to vmd 
    _listener = threading.Thread(target=callback, args=(signal,_commandStdout))
    # _listener.daemon = True
    _listener.start()

    return _testCallback(timeout)


def _testCallback(timeout):
    # check if deamon alive within timeout
    _listener.join(timeout)

    if _listener.isAlive():
        raise Exception('VMD has not responded within timeout ('+str(timeout)+'s)') 
    else:
        return _commandStdout

# --------------------------------------------------
#                  Control VMD
def send_string(commandString, timeout=defaultTimeout, returnAll=False, latency=ioLag):
    """
    send tcl code to vmd instance created with Vopen()
    - timeout : an error is raised if VMD does not respond within timeout seconds. VMD process is not killed. 
      You further observe the process using ping() or kill it using Vkill(). Increase timeout for commands that take long time.
    - if returnAll=False (default), function tries to return only the final return value from the tcl interpreter;
      if returnAll=True, function returns all the tcl stdout from the command as string
    - Increase latency if 

    if vmdpipe.printout is true vmd stdout is not retured but printed on screen, 
    useful for interactive use. 
    """

    if not isVMDopen():
        raise Exception("VMD instance not found. Open one using Vopen()")
    
    # send command
    _vmdin.stdin.writelines(commandString+"\n")
    # avoid deadlock(?)
    sleep(latency) 
    # wait for output and return
    out=ping(timeout)
    if printout:
        sys.stdout.write("".join(out))

    if returnAll:
        return out
    else:
        return out[-1].strip()

def source(filename, **kwargs):
    """source a file in the vmd instance created with Vopen()"""
    if os.path.isfile(filename):
        return send_string("source "+filename, **kwargs)
    else:
        raise ("filename does not exist")
        
def runAndReturn(script, addexit=True):
    """
    Execute a vmd script in a independent vmd instance, close and return the stdout. 
    Both file paths and strings as accepted as script. If script is a string, "exit 0" statement
    is added at the end. This should be generally fine but if, for any reason, you want to
    change this default behavior, use addexit=False.
    """

    if os.path.isfile(script):
        command=[_vmdexec, "-dispdev", "text", "-eofexit", "-e", script]
        out=check_output(command, stderr=STDOUT, universal_newlines=True)
    else:
        command=[_vmdexec, "-dispdev", "text",]

        # add exit to list of command
        if addexit:
            script += "\nexit 0\n"

        out=run(command, input=script, stdout=PIPE, stderr=STDOUT, universal_newlines=True).stdout
            
    if printout:
        sys.stdout.write("".join(out))
        return
    else:
        return out
            

# --------------------------------------------------
#               Utils

def aspylist(x):
    """convert tcl list in python list"""
    if x.find("{") == 0:
        exec("l=["+x.replace("}","]").replace("{","[").replace(" ",",")+"]")
        return l
    else:
        return x.split()

def astcllist(x):
    """convert python list in tcl list"""
    return str(x).replace("]","}").replace("[","{").replace(", "," ")
    
if __name__ == "__main__":

    # few examples of usage
    Vopen()
    print(send_string('set h "(vmdpipe) This string is a return value from VMD"'))
    Vclose()

    printout=True                            # VMD output will be printed on screen
    Vopen(text=False)                        # open vmd
    molID=send_string('mol pdbload 1k4c')
    print("mol {} loaded".format(molID))

    # timeout
    send_string('set t test; sleep 20')  # will fail, default timeout=15
    isVMDopen()

    send_string('set t test; sleep 20', 30)  # will fail, default timeout=15

    t=send_string("set h [list 2 3]", latency=0.01)
    aspylist(t)
    t=aspylist(send_string("set h [list [list 2 3] [list 4 5] [list 6 7]]"))
    Vclose()
