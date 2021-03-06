#! /usr/bin/env python
# -*- coding: utf8 -*-

import sys
import os

statusfile = sys.argv[1]
inputdir = sys.argv[2]
outputdir = sys.argv[3]
parameters = ' '.join(sys.argv[4:])

import glob

trainfile = None
for inputfile in glob.glob(inputdir + '/*.train'):
    trainfile = inputfile
    
if not trainfile:
    print >>sys.stderr, "No trainfile found"

for testfile in glob.glob(inputdir + '/*.test'):
    outfile = outputdir + '/' + os.path.basename(testfile).split('.')[0] + '.timblout'
    cmd = 'timbl -f ' + trainfile + ' ' + parameters + ' -t ' + testfile + ' -o ' + outfile
    print >>sys.stderr, "Processing " + testfile + ": " + cmd
    os.system(cmd)
    
if parameters.find('-t leave_one_out') != -1:
    print >>sys.stderr, "Testing with leave-one-out"
    os.system('timbl -f ' + trainfile + ' ' + parameters + ' -o ' + outfile)  

    
    
    
