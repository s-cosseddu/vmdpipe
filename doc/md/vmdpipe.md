vmdpipe package[¶](#vmdpipe-package "Permalink to this headline")
=================================================================

vmdpipe module[¶](#module-vmdpipe "Permalink to this headline")
---------------------------------------------------------------

VMDpipe provides a set of api to use vmd from python executing tcl code
and scripts.

In the present version, the module does not provide any class, python
interpreter in VMD is not supported and only a single VMD instance is
allowed.

VMD executable can be set using vmdpipe.Vsetpath(path) and retrieved
using vmdpipe.Vgetpath(path)

vmdpipe.printout (boolean) = True is useful for interactive: vmd stdout
is printed to screen instead of being returned as strings

defaultTimeout specifies the wait time (in seconds) before an error is
raised if VMD does not respond. In this case VMD instance is not closed.
You can wait further using vmdpipe.ping() or kill the instance with
vmdpipe.Vkill()

ioLag defines a default time interval before reading vmd stdout after
sending a command using vmdpipe.send\_string()

Module is implemented using subprocess module and vmd stderr is
accessible via vmdpipe.\_vmdin.stderr (See subprocess manual)

 `vmdpipe.`{.descclassname}`Vclose`{.descname}(*timeout=10*)[¶](#vmdpipe.Vclose "Permalink to this definition")
:   close the vmd instance opened by Vopen() and return the returncode

 `vmdpipe.`{.descclassname}`Vgetpath`{.descname}()[¶](#vmdpipe.Vgetpath "Permalink to this definition")
:   get path of vmd used by the module

 `vmdpipe.`{.descclassname}`Vkill`{.descname}()[¶](#vmdpipe.Vkill "Permalink to this definition")
:   kill the vmd instance opened by Vopen()

 `vmdpipe.`{.descclassname}`Vopen`{.descname}(*gui=True*, *timeout=15*, *returnInitStdout=False*)[¶](#vmdpipe.Vopen "Permalink to this definition")
:   open a vmd instance, use only for interactive/test purposes set text
    to False for interactive use with gui

    An error is raised if VMD does not respond within timeout sectonds.
    In this case VMD instance is not closed. You can wait further,
    observe using ping() or kill the instance with Vkill()

    if returnInitStdout is True, the function return the init stdout of
    VMD as string

    if vmd.printout is True, init stdout is printed to screen (useful
    for interactive use)

 `vmdpipe.`{.descclassname}`Vsetpath`{.descname}(*p*)[¶](#vmdpipe.Vsetpath "Permalink to this definition")
:   set path of vmd, default vmd from bash env

 `vmdpipe.`{.descclassname}`aspylist`{.descname}(*x*)[¶](#vmdpipe.aspylist "Permalink to this definition")
:   convert tcl list in python list

 `vmdpipe.`{.descclassname}`astcllist`{.descname}(*x*)[¶](#vmdpipe.astcllist "Permalink to this definition")
:   convert python list in tcl list

 `vmdpipe.`{.descclassname}`callback`{.descname}(*signal*, *capture\_stdout*)[¶](#vmdpipe.callback "Permalink to this definition")
:   listen vmd for a signal and capture stdout

 `vmdpipe.`{.descclassname}`isVMDopen`{.descname}()[¶](#vmdpipe.isVMDopen "Permalink to this definition")
:   

 `vmdpipe.`{.descclassname}`ping`{.descname}(*timeout=15*, *signal='vmdpipesignal'*)[¶](#vmdpipe.ping "Permalink to this definition")
:   Send signal to vmd and wait timeout seconds for the response.
    Finally return the stdout

 `vmdpipe.`{.descclassname}`runAndReturn`{.descname}(*script*, *addexit=True*)[¶](#vmdpipe.runAndReturn "Permalink to this definition")
:   Execute a vmd script in a independent vmd instance, close and return
    the stdout. Both file paths and strings as accepted as script. If
    script is a string, “exit 0” statement is added at the end. This
    should be generally fine but if, for any reason, you want to change
    this default behavior, use addexit=False.

 `vmdpipe.`{.descclassname}`send_string`{.descname}(*commandString*, *timeout=15*, *returnAll=False*, *latency=0.01*)[¶](#vmdpipe.send_string "Permalink to this definition")
:   send tcl code to vmd instance created with Vopen() - timeout : an
    error is raised if VMD does not respond within timeout seconds. VMD
    process is not killed.

    > You further observe the process using ping() or kill it using
    > Vkill(). Increase timeout for commands that take long time.

    -   if returnAll=False (default), function tries to return only the
        final return value from the tcl interpreter; if returnAll=True,
        function returns all the tcl stdout from the command as string
    -   Increase latency if

    if vmdpipe.printout is true vmd stdout is not retured but printed on
    screen, useful for interactive use.

 `vmdpipe.`{.descclassname}`source`{.descname}(*filename*, *\*\*kwargs*)[¶](#vmdpipe.source "Permalink to this definition")
:   source a file in the vmd instance created with Vopen()

### [Table Of Contents](index.html)

-   [vmdpipe package](#)
    -   [vmdpipe module](#module-vmdpipe)

### Related Topics

-   [Documentation overview](index.html)
    -   Previous: [Welcome to vmdpipe’s
        documentation!](index.html "previous chapter")
    -   Next: [Tutorial](tutorial.html "next chapter")

### This Page

-   [Show Source](_sources/vmdpipe.txt)

### Quick search

©2016, Salvatore M Cosseddu. | Powered by [Sphinx
1.4.1](http://sphinx-doc.org/) & [Alabaster
0.7.8](https://github.com/bitprophet/alabaster) | [Page
source](_sources/vmdpipe.txt)

