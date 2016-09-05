Tutorial[¶](#tutorial "Permalink to this headline")
===================================================

Vmdpipe provides useful functions to use VMD either iteractively or in a
python script. Few example of it usage are here listed.

Interactive mode:[¶](#interactive-mode "Permalink to this headline")
--------------------------------------------------------------------

Open an interactive session with GUI:

    import vmdpipe as vmd
    vmd.Vopen()

that correspond to:

    import vmdpipe as vmd
    vmd.printout=True       # default, VMD output will be printed on screen
    vmd.Vopen(text=False)   # default, open vmd

Now you can send some command: vmdpipe will try to capture the return
value:

    molID=vmd.send_string('mol pdbload 1k4c')   # load a molecule and store molID
    print("mol {} loaded".format(molID))

By default vmdpipe wait 15s before raising an error:

    molID=send_string('sleep 20')   # an error is raised

Vmd is not killed, but output to that point is lost. This is made to
prevent issues to underlying vmd process to block your script or
workflow. You can check if VMD is still alive, send a signal to check if
it is responsive, or kill it:

    if isVMDopen():
        print("I'm still alive!")

    try:
        vmd.ping(10)
    except:
        vmd.Vkill()

If you know your command will take longer than 15s, increase the timeout
(in seconds):

    t=vmd.send_string('set t test; sleep 20', timeout=100)  # now it is ok!
    print(t)

As you can see, no return value was captured. Because, by default,
send\_string will capture return value of the very last command. If you
prefere otherwise, you can save all the stdout printed as a result of
your command:

    t=vmd.send_string("""
    set t test
    set g {2 3}
    set h [list $t $g]
    """, returnAll=True)  # now everything is stored
    print(t)

As seen, send\_string() accepts very complex list of commands. Simpler way to do so is using::
:   “””...”“”

Alternatively you can store your commands in a file, and source them:

    t=vmd.source("test.tcl")

source() accepts same options of send\_string().

Vmdpipe provides a function to convert tcl lists in python lists:

    # tcl --> python
    t=vmd.aspylist(vmd.send_string("set h [list [list 2 3] [list 4 5] [list 6 7]]))

and back:

    # python --> tcl
    t=vmd.aspylist(vmd.send_string("set h [list [list 2 3] [list 4 5] [list 6 7]]))

To close the vmd instance use:

    vmd.Vclose()                                 # close vmd

Text mode:[¶](#text-mode "Permalink to this headline")
------------------------------------------------------

Text mode is useful for scripting purposes. In a script, it is safest to
run the script opening and closing each time a vmd instance. This is
done using:

    runAndReturn(script)

However, many times you want to maintain the vmd instance opened and
communicate with it. In these cases you can open the session with:

    import vmdpipe as vmd
    vmd.printout=False               # nothing will be printed to screen
    vmd.Vopen(text=True)            # open vmd in text mode

and use all functions above described. It is important to have proper
communications with the underlying vmd instance. Option “latency” in
vmdpipe.send\_string() set time interval before reading vmd stdout after
sending a command. It can be changed globally by setting:

    vmd.ioLag=0.001

Default (0.01) should be fine in most cases, however you can play a bit
reducing it to improve performance or increasing it if you notice vmd
hanging.

### [Table Of Contents](index.html)

-   [Tutorial](#)
    -   [Interactive mode:](#interactive-mode)
    -   [Text mode:](#text-mode)

### Related Topics

-   [Documentation overview](index.html)
    -   Previous: [vmdpipe package](vmdpipe.html "previous chapter")

### This Page

-   [Show Source](_sources/tutorial.txt)

### Quick search

©2016, Salvatore M Cosseddu. | Powered by [Sphinx
1.4.1](http://sphinx-doc.org/) & [Alabaster
0.7.8](https://github.com/bitprophet/alabaster) | [Page
source](_sources/tutorial.txt)

