#!/usr/bin/python
# -*- coding: utf-8 -*-

my_file = open("/media/sf_myShare/MH_01_easy/mav0/cam0/data_dso.txt", "w")
open_file = open("/media/sf_myShare/MH_01_easy/mav0/cam0/data.csv", "r")
i = -1
for line in open_file:
	if i>=0:
		i_char = str(i)
		my_file.write(i_char)
		my_file.write(" ")
		line_to_copy = line.split(',')
		my_file.write(line_to_copy[0])
		my_file.write("\n")
	i += 1
my_file.close()
open_file.close()
