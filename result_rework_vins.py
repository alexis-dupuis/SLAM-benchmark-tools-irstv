#!/usr/bin/python
# -*- coding: utf-8 -*-

my_file = open("/media/sf_myShare/exp_results/Vins_Mono/MH_01_easy/vins_result_loop_reworked.txt", "w")
open_file = open("/media/sf_myShare/exp_results/Vins_Mono/MH_01_easy/vins_result_loop.txt", "r")


for line in open_file:

	#Read the current vins data
	data_read = line.split(' ')
	ts, x, y, z, qw, qx, qy, qz = data_read
	qz = str(float(qz))

	#Reorganise it
	data_towrite = [ts, x, y, z, qx, qy, qz, qw]

	#Write it
	for i in range(len(data_towrite)):
		my_file.write(data_towrite[i])
		if i<7:
			my_file.write(' ')
	my_file.write("\n")

my_file.close()
open_file.close()

print "File:   /media/sf_myShare/exp_results/Vins_Mono/MH_01_easy/vins_result_loop_reworked.txt    UPDATED"
