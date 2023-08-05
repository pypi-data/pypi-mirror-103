#!/usr/bin/env python
# Part of TotalDepth: Petrophysical data processing and presentation
# Copyright (C) 1999-2011 Paul Ross
# 
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
# 
# Paul Ross: apaulross@gmail.com
"""
Created on 10 Nov 2010

@author: p2ross
"""
__author__  = 'Paul Ross'
__date__    = '2010-08-02'
__version__ = '0.1.0'
__rights__  = 'Copyright (c) Paul Ross'

import time
import sys
import logging
from optparse import OptionParser
import struct

from TotalDepth.LIS.core import PhysRec
from TotalDepth.util import Histogram

# How much of the logical data to display
LEN_TRUNCATE = 32

def scanFile(fp, isVerbose, keepGoing, dumpTellS, theS=sys.stdout):
#    print(dumpTellS)
    try:
        myPrh = PhysRec.PhysRecRead(fp, fp, keepGoing)
    except PhysRec.ExceptionPhysRec as err:
        print('Can not open file, error: %s' % str(err))
        return
    # Now other stuff generated by this loop
    theS.write('Offset        Length  Type  Logical Data\n')
    myLdSigma = bytes()
    myOffs = myPrh.tellLr()
    # Histogram of lengths and types
    myHistLen = Histogram.Histogram()
    myHistTyp = Histogram.Histogram()
    for myLd, isLdStart in myPrh.genLd():
        if isLdStart:
            if len(myLdSigma) == 0:
                # First time through the loop then don't write anything
                pass
            else:
                # This is not the first time through the loop
                # so write out the trailing LogicalData length
                lrType = -1
                if len(myLdSigma) > 0:
                    lrType = myLdSigma[0]
                    myHistLen.add(len(myLdSigma))
                    myHistTyp.add(lrType)
                theS.write('0x{:08X}  {:8d}  {:4d}'.format(myOffs, len(myLdSigma), lrType))
                if myOffs not in dumpTellS \
                and not isVerbose and len(myLdSigma) > LEN_TRUNCATE:
                    theS.write('  {!r:s}...\n'.format(myLdSigma[0:LEN_TRUNCATE]))
                else:
                    theS.write('  {!r:s}\n'.format(myLdSigma))
                myLdSigma = bytes() 
                myOffs = myPrh.tellLr()
        myLdSigma += myLd
    if len(myLdSigma) > 0:
        theS.write('0x{:08X}  {:8d}  {:4d}'.format(myOffs, len(myLdSigma), lrType))
        if myOffs not in dumpTellS \
        and not isVerbose and len(myLdSigma) > LEN_TRUNCATE:
            theS.write('  {!r:s}...\n'.format(myLdSigma[0:LEN_TRUNCATE]))
        else:
            theS.write('  {:s}\n'.format(myLdSigma))
    theS.write('Histogram of Logical Data lengths:\n')
    theS.write(myHistLen.strRep(100, valTitle='Bytes', inclCount=True))
    theS.write('\n')
    theS.write('Histogram of Logical Record types:\n')
    theS.write(myHistTyp.strRep(100, inclCount=True))
    theS.write('\n')
    

def retIntDumpList(theStr):
    """Splits a string and returns a list of integers from hex/dec."""
    r = []
    for w in theStr.split():
        try:
            if w.startswith('0x'):
                r.append(int(w[2:], 16))
            else:
                r.append(int(w))
        except (TypeError, ValueError) as err:
            logging.error('Can not understand integer {:s}: {:s}'.format(w, err))
    return r

def main():
    usage = """usage: %prog [options] file
Scans a LIS79 file and dumps logical record data."""
    print('Cmd: %s' % ' '.join(sys.argv))
    optParser = OptionParser(usage, version='%prog ' + __version__)
    optParser.add_option("-k", "--keep-going", action="store_true", dest="keepGoing", default=False, 
                      help="Keep going as far as sensible. [default: %default]")
    optParser.add_option(
            "-d", "--dump",
            type="str",
            dest="dump",
            default='',
            help="Dump complete data at these integer positions (ws separated, hex/dec). [default: %default]"
        )      
    optParser.add_option(
            "-l", "--loglevel",
            type="int",
            dest="loglevel",
            default=20,
            help="Log Level (debug=10, info=20, warning=30, error=40, critical=50) [default: %default]"
        )      
    optParser.add_option("-v", "--verbose", action="store_true", dest="verbose", default=False, 
                      help="Verbose Output. [default: %default]")
    opts, args = optParser.parse_args()
    clkStart = time.clock()
    # Initialise logging etc.
    logging.basicConfig(level=opts.loglevel,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    #datefmt='%y-%m-%d % %H:%M:%S',
                    stream=sys.stdout)
    # Your code here
    if len(args) == 1:
        scanFile(args[0], opts.verbose, opts.keepGoing, retIntDumpList(opts.dump))
    else:
        optParser.print_help()
        optParser.error("Wrong number of arguments, I need one only.")
        return 1
    clkExec = time.clock() - clkStart
    print('CPU time = %8.3f (S)' % clkExec)
    print('Bye, bye!')
    return 0

if __name__ == '__main__':
    #multiprocessing.freeze_support()
    sys.exit(main())

    
    
    