.. vmdpipe documentation master file, created by
   sphinx-quickstart on Thu Sep  1 17:22:25 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to vmdpipe's documentation!
===================================

Description:
----------------------

VMDpipe provides a set of api to use vmd from python executing tcl code and scripts.

Notes:
----------------------

In the present version, the module does not provide any class,
python interpreter in VMD is not supported and only a single VMD
instance is allowed.

VMD executable can be set using vmdpipe.Vsetpath(path) and retrieved using vmdpipe.Vgetpath(path)

vmdpipe.printout (boolean) = True is useful for interactive: vmd stdout is
printed to screen instead of being returned as strings

defaultTimeout specifies the wait time (in seconds) before an error is raised 
if VMD does not respond. In this case VMD instance is not closed. 
You can wait further using vmdpipe.ping() or kill the instance with vmdpipe.Vkill()

ioLag defines a default time interval for reading vmd stdout after sending a command 
using vmdpipe.send_string()

Module is implemented using subprocess module and vmd stderr is accessible via vmdpipe._vmdin.stderr 
(See subprocess manual)

Contents:

.. toctree::
   :maxdepth: 1

   vmdpipe
   tutorial

