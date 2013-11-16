import string, os

qsub_command = 'cat'

dict = {'COMMAND' : 'echo',
	'NTHREADS' : 1}

max_nthreads = 8

for nthreads in xrange(1, max_nthreads+1):
	dict['NTHREADS'] = nthreads

	infile = open ('pbstemplate', 'r')

	outfilename = 'pbs.sh'
	outfile = open (outfilename, 'w')
	
	for line in infile:
		outfile.write(string.Template(line).substitute(dict))
		
	infile.close()
	outfile.close()

	os.system('%s %s' % (qsub_command, outfilename))

	os.system('sleep 1')
