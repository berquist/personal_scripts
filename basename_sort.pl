#!/usr/bin/env perl

# https://stackoverflow.com/a/4255942

use strict;

my @lines = <STDIN>;
@lines = sort basename_sort @lines;
foreach( @lines ) {
   print $_;
}

sub basename_sort() {
   my @data1 = split('/', $a);
   my @data2 = split('/', $b);
   my $name1 = $data1[@data1 - 1];
   my $name2 = $data2[@data2 - 1];
   return lc($name1) cmp lc($name2);
}
