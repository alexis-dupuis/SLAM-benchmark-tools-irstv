#!/usr/bin/python
# -*- coding: utf-8 -*-

write_path = "/media/sf_myShare/rovio/2018-06-18-16-17-12/rovio_result.txt"
csv_path = "/media/sf_myShare/rovio/2018-06-18-16-17-12/rovio_odometry.csv"

my_file = open(write_path, "w")
open_file = open(csv_path, "r")


"""Souvenir emouvant d'une journée perdue pour rien... :

frst_frame_real_ts = 1403636579.7635555  #past here the first image's real timestamp (if changed)
lst_frame_real_ts = 1403636763.813555456

frst_frame_ros_ts = 1529410547.863364461 #past here the first image's ROS timestamp
lst_frame_ros_ts = float(open_file.readlines()[-1].split(',')[0])*1e-9

open_file.close()
open_file = open("/media/sf_myShare/rovio/2018-06-18-16-17-12/result/test_rovio_odometry.csv", "r")

offset_ts = frst_frame_real_ts - frst_frame_ros_ts

D_ts_data = lst_frame_real_ts - frst_frame_real_ts #182
D_ts_res = lst_frame_ros_ts - frst_frame_ros_ts #110

"""

i=0

for line in open_file:
	
	if i>0:
		#Read the current rovio data
		data_read = line.split(',')
		tss, tsns, x, y, z, qx, qy, qz, qw = data_read[4], data_read[5], data_read[11], data_read[12], data_read[13], data_read[15], data_read[16], data_read[17], data_read[18]
		ts = str( tss + "." + tsns )
		###ts = str( D_ts_data/D_ts_res * ts - (D_ts_data - D_ts_res)/D_ts_res * frst_frame_real_ts )

		#Reorganise it
		data_towrite = [ts, x, y, z, qx, qy, qz, qw]

		#Write it
		for i in range(len(data_towrite)):
			my_file.write(data_towrite[i])
			if i<7:
				my_file.write(' ')
		my_file.write("\n")
	i += 1

my_file.close()
open_file.close()

print "File:   ", write_path , "    UPDATED"

