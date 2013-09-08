#!/usr/bin/env python2

test_file = open('test_file','a')
max_iter = 100
for i in range(max_iter):
    for j in range(max_iter):
        test_file.write('a[i][j] = a[%i][%i] \n' % (i,j))

