#!/usr/bin/env python
"""
Provide a set of wraps for common vmd command to be used with vmdpipe
"""

from .vmdpipe import *

# --------------------------------------------------
#               Utils

def aspylist(x, outbraces=True):
    """convert tcl list in python list"""
    if x.find("{") == 0:
        lns = {}
        if outbraces:
            code = "l=["+x.replace("}","]").replace("{","[").replace(" ",",")+"]"
        else:
            code = "l="+x.replace("}","]").replace("{","[").replace(" ",",")

        # execute the command
        try :
            exec(code, lns)
        except:
            print("An error as occurred... not helpful but sorry!")
        return lns['l']
    else:
        return x.split()

def astcllist(x):
    """convert python list in tcl list"""
    return str(x).replace("]","}").replace("[","{").replace(", "," ")

def mol(loadOption="new", opts=""):
    """
    Wrap on mol command. 
    For loadOption check vmd manual (default new)
    opts (string) is used to pass options 
    """
    out=send_string('mol {} {}'.format(loadOption, opts), returnAll=True)
    # possible outputs
    if loadOption=="new":
        return [x.strip() for x in out if not x.startswith("Info")][0]
    else:
        return out 

def loadTclPackages(plist):
    """
    load packages from plist (list) and return package versions
    """
    return [send_string('package require {}'.format(x)) for x in plist]
    
def atomselect(molId, selection, frame="now"):
    """
    Create a new atom selection 
    (see http://www.ks.uiuc.edu/Research/vmd/current/ug/node199.html)
    Return name of atomselection for atmdo() 
    """
    return send_string('atomselect {} "{}" frame {}'.format(
        molId, selection, frame))

def atmdo(atmsel, string):
    """Do something with the atom selection 
    arguments are provided using "string"
    e.g.
    atmdo(atmsel, "get name")
    atmdo(atmsel, "delete")
    """
    return send_string(atmsel+" "+string)

def mergemols (mollist, delete=False):
    """
    Merge multiple vmd molecules using topotools return new molID
    Delete original mol if required
    """
    tcllist=astcllist([int(x) for x in mollist])
    mol=send_string('::TopoTools::mergemols '+tcllist)
    if delete:
        # delete original
        map(mol, ["delete"]*len(mollist), mollist)
    return mol

def center(molID):
    """
    center a molecule, require utiltools package to be loaded
    """
    send_string("::utiltools::mod::center {} all".format(molID))

def writesel(molID, file, sel="all", type="pdb"):
    """
    write a selection (default all) to a file of a 
    given type (default pdb)
    """
    all=atomselect(molID, sel)
    atmdo(all, "write"+type+" "+file)
    atmdo(all, "delete")
    return

def saveMols(mollist, outpref, type='pdb', sel='all'):
    """
    Save multiple mols from a list in files <outpref><id>.<type> 
    """   
    for x in range(len(mollist)):
        outfile="output/replica"+str(x)+".gro"
        print('Writing mol {} in {}'.format(mollist[x], outfile))
        writesel(mollist[x], outfile, sel=sel, type="type")

def getCoordNums(molid, refsel, neighsel, distance):
    """
    compute coordination numbers for reference atoms. Require utiltools.
    """

    loadTclPackages(['utiltools'])

    # use ::utiltools::measure::NeighAtms to compute coordination numbers
    # and store in a dictionary
    command=('::utiltools::measure::NeighAtms '
             '{} "{}" "{}" {} now now T'.format(
                 molid, refsel, neighsel, distance))
    
    return aspylist(send_string(command))

if __name__ == "__main__":
    pass
