# Mark Hoemmen <mhoemmen AT cs DOT berkeley DOT edu>
# 22 Sep 2007
#
# Python script for generating parametrized PBS scripts and submitting
# them.
#
# Here's how this script works:
# 
# 1. You write a template file (which I'm calling "pbstemplate").
#    It's a plain text file which contains the PBS script, except that
#    you replace the parameters with "$PARAMETERNAME" (in which
#    PARAMETERNAME should be replaced with the name of the parameter).
#    Also, any time you want a literal dollar sign to appear, you MUST
#    replace it with two dollar signs.  This is very important for
#    environment variables such as PBS_WORKDIR.
#  
# 2. Edit this script.  Set template_filename to the name and path of
#    the template file, and set the parameter names (which are strings)
#    and their values in the "dict" variable.  Also change qsub_command
#    from 'cat' (which is handy for debugging, incidentally) to 'qsub'.
#
# 3. Run the script and check for error messages.
########################################################################

# This brings in the very useful string.Template class, which has
# methods for doing string substitution.
import string

# This brings in a generic operating system interface, which includes
# os.system() (which we use to invoke qsub).
import os


########################################################################
# Script body 
########################################################################


# FIXME: change this to 'qsub' when you're done debugging.
qsub_command = 'cat'

# Here is the dictionary (set of (key,value) pairs) which is used for
# substituting $key with value.  We start NTHREADS with the value 1,
# and will later change this.
dict = {'COMMAND' : 'echo',
	'NTHREADS' : 1}

# Here is the maximum number of threads to use.
max_nthreads = 8

# Loop from 1 to max_nthreads, inclusive.  Generate a PBS script file
# for each value of nthreads, and submit it to the job queue.
for nthreads in xrange(1, max_nthreads+1):
	# Set the value of NTHREADS in the current PBS script.
	dict['NTHREADS'] = nthreads

	# Open the template file (for reading).  We don't have to
	# check the return value because Python throws an exception if
	# the open() function fails.
	infile = open ('pbstemplate', 'r')

	# Open the PBS script file (for writing, and delete any
	# existing file of this name first).  We can use the same file
	# each time, because PBS makes a copy when we submit the job,
	# and Python's system() function doesn't return until the
	# system call is complete.  See:
	#
	# http://docs.python.org/lib/os-process.html
	outfilename = 'pbs.sh'
	outfile = open (outfilename, 'w')
	
	# Iterate through the lines of the template file
	for line in infile:
		# Substitute keys for values in the template line,
		# and output the result.
		outfile.write(string.Template(line).substitute(dict))
		
	infile.close()
	outfile.close()

	# Now that we've closed the output file, we can submit the PBS
	# script.
	os.system('%s %s' % (qsub_command, outfilename))

	# Sleep a little while to make sure that PBS has time to copy
	# the script, and also so as not to overload qsub.
	os.system('sleep 1')

########################################################################
# We're done!
########################################################################
