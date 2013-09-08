#!/usr/bin/python

def getopts(argv):

    opts = {}

    while argv:

        if argv[0][0] == '-':                  # find "-name value" pairs

            opts[argv[0]] = argv[1]            # dict key is "-name" arg

            argv = argv[2:]                    

        else:

            argv = argv[1:]

    return opts

 

if __name__ == '__main__':

    from sys import argv
    import os

    myargs = getopts(argv)

    if myargs.has_key('-i'):                    #get inputfile name

        print "#Job list filename:", myargs['-i']
        jobFileList = file(myargs['-i'],'r')
        iCount = 0
        while True:
            jobScripteName = jobFileList.readline()
            if len(jobScripteName) == 0:        #ZERO indicate EOF, exit
                break
            jobSubCmd = "qsub "+jobScripteName
            print "#",iCount,":",jobSubCmd,
            iCount = iCount + 1
            os.system(jobSubCmd)
        jobFileList.close()
            
