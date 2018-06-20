#!/usr/bin/python
# -*- coding: utf-8 -*-




#res_file_path = "/media/sf_myShare/exp_results/rovio/"
#res_file_path = "/media/sf_myShare/exp_results/Vins_Mono/MH_01_easy/"
#res_file_path = "/media/sf_myShare/exp_results/ORB_SLAM2/"
res_file_path = "/media/sf_myShare/exp_results/lsd_slam/"
#res_file_path = "/media/sf_myShare/exp_results/dso/"

#res_file = "rovio_results_corrected.txt"
#res_file = "vins_result_loop_reworked_corrected.txt"
#res_file = "ORBSLAM2_results_corrected.txt"
#res_file = "dso_results_corrected.txt"
res_file = "lsd_pose_result_corrected.txt"

#ref_path = "/media/sf_myShare/exp_results/data.tum" #For Vins and Rovio, else: 
ref_path = "/media/sf_myShare/exp_results/data_cam0frame.txt" #For ORB-SLAM2, LSD-SLAM, DSO...







#========================#
# Some useful functions...
#========================#


import matplotlib.pyplot as plt
from math import *

def q_mult(q1, q2):
    w1, x1, y1, z1 = q1
    w2, x2, y2, z2 = q2
    w = w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2
    x = w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2
    y = w1 * y2 + y1 * w2 + z1 * x2 - x1 * z2
    z = w1 * z2 + z1 * w2 + x1 * y2 - y1 * x2
    return w, x, y, z

def q_conjugate(q):
    w, x, y, z = q
    return (w, -x, -y, -z)

def qv_mult(q1, v1):
    q2 = (0.0,) + v1
    return q_mult(q_mult(q1, q2), q_conjugate(q1))[1:]

def axisangle_to_q(v, theta):
    v = normalize(v)
    x, y, z = v
    theta /= 2
    w = cos(theta)
    x = x * sin(theta)
    y = y * sin(theta)
    z = z * sin(theta)
    return w, x, y, z

def q_to_axisangle(q):
    w, v = q[0], q[1:]
    theta = acos(w) * 2.0
    return normalize(v), theta

def quaternion_to_euler_angle(w, x, y, z):
	ysqr = y * y
	
	t0 = +2.0 * (w * x + y * z)
	t1 = +1.0 - 2.0 * (x * x + ysqr)
	R = degrees(atan2(t0, t1))
	
	t2 = +2.0 * (w * y - z * x)
	t2 = +1.0 if t2 > +1.0 else t2
	t2 = -1.0 if t2 < -1.0 else t2
	P = degrees(asin(t2))
	
	t3 = +2.0 * (w * z + x * y)
	t4 = +1.0 - 2.0 * (ysqr + z * z)
	H = degrees(atan2(t3, t4))
	
	return R, P, H





#========================================================================#
#Transforming EuRoC's groundtruth from IMU frame to cam0 frame and saving
#Leave in comments except if you want to change the groundtruth files...
#========================================================================#


"""

my_file = open("/media/sf_myShare/exp_results/data_cam0frame.txt", "w")
open_file = open("/media/sf_myShare/exp_results/data.tum", "r")


for line in open_file:

	#Read the groundtruth line
	data_read = line.split(' ')
	ts, x, y, z, qx, qy, qz, qw = data_read[0], float(data_read[1]), float(data_read[2]), float(data_read[3]), float(data_read[4]), float(data_read[5]), float(data_read[6]), float(data_read[7])

	#Do some magic...
	q = [qw, qx, qy, qz]
	dx, dy, dz, dq = [0.0216401454975, 0.064676986768, -0.00981073058949, [0.712301460669, 0.010343836119, 0.0104993233706, -0.701752800292]]
	dq = q_conjugate(dq)
	qsw, qsx, qsy, qsz = q_mult(q, dq)

	data_towrite = [ts, str(x+dx), str(y+dy), str(z+dz), str(qsx), str(qsy), str(qsz), str(qsw)]

	#Write results
	for i in range(len(data_towrite)):
		my_file.write(data_towrite[i])
		if i<7:
			my_file.write(' ')
	my_file.write("\n")

my_file.close()
open_file.close()

print "File:   /media/sf_myShare/exp_results/data_cam0frame.txt    UPDATED,  you must now update ORBSLAM2_result_corrected.txt  with evo."

"""





#==============================================================#
#Transforming SLAM results in errors wrt groundtruth and saving
#==============================================================#


#"""

my_file = open(res_file_path + "result_error.txt", "w")
open_res_file = open(res_file_path + res_file, "r")
open_data_file = open(ref_path, "r") #groundtruth


""" Doesn't work, but problem dodge anyway
#=================

last_res_ts = open_res_file.readlines()[0].split(' ')[0]
last_data_ts = open_data_file.readlines()[0].split(' ')[0]
delta = float(last_data_ts) - float(last_res_ts)

print delta

#=================

open_res_file.close()
open_data_file.close()

open_res_file = open(res_file_path + res_file, "r") 
open_data_file = open(ref_path, "r")

#=================
"""


for line in open_res_file:
	
	#Read the result line
	res_read = line.split(' ')
	ts, x, y, z, qx, qy, qz, qw = float(res_read[0]), float(res_read[1]), float(res_read[2]), float(res_read[3]), float(res_read[4]), float(res_read[5]), float(res_read[6]), float(res_read[7])
	
	#Match it with gt according to timestamp
	data_line_vect = [0.0]	
	current_ts = 0.0

	while (ts - current_ts > 0):

		prev_data_line_vect = data_line_vect

		data_line = open_data_file.readline()
		data_line_vect = data_line.split(' ')

		current_ts = float(data_line_vect[0])

	prev_ts = float(prev_data_line_vect[0])

	if abs(ts - prev_ts) < abs(ts - current_ts): #previous line was the best
		data_read = prev_data_line_vect

	else: #current line is the best
		data_read = data_line_vect

	#Do the math...
	gt_ts, gt_x, gt_y, gt_z, gt_qx, gt_qy, gt_qz, gt_qw = data_read[0], float(data_read[1]), float(data_read[2]), float(data_read[3]), float(data_read[4]), float(data_read[5]), float(data_read[6]), float(data_read[7])
	q = [qw, qx, qy, qz]
	gt_q = [gt_qw, gt_qx, gt_qy, gt_qz]
	gt_q = q_conjugate(gt_q)
	qsw, qsx, qsy, qsz = q_mult(q, gt_q)

	data_towrite = [str(ts), str(abs(x-gt_x)), str(abs(y-gt_y)), str(abs(z-gt_z)), str(qsx), str(qsy), str(qsz), str(qsw)]

	#Write the result
	for i in range(len(data_towrite)):
		my_file.write(data_towrite[i])
		if i<7:
			my_file.write(' ')
	my_file.write("\n")




my_file.close()
open_res_file.close()
open_data_file.close()

print "File:   ", res_file_path + "result_error.txt", "    UPDATED"

#"""




#=====================================================#
#Transforming errors to cumulative errors and plotting
#=====================================================#


#"""

open_file = open(res_file_path + "result_error.txt", "r")

N = 500
sequence = "ypr"
max_x, max_y, max_z, max_r, max_p, max_h = 0, 0, 0, 0, 0, 0

cumulative_counter_x = [0]*N
cumulative_counter_y = [0]*N
cumulative_counter_z = [0]*N
cumulative_counter_r = [0]*N
cumulative_counter_p = [0]*N
cumulative_counter_h = [0]*N

fic_stock = []


#Find the maximal errors

#==============

for line in open_file:
	error_read = line.split(' ')
	ts, ex, ey, ez, eqx, eqy, eqz, eqw = error_read[0], float(error_read[1]), float(error_read[2]), float(error_read[3]), float(error_read[4]), float(error_read[5]), float(error_read[6]), float(error_read[7])
	er, ep, eh = quaternion_to_euler_angle(eqw, eqx, eqy, eqz)
	er, ep, eh = abs(er), abs(ep), abs(eh)
	
	fic_stock.append([ex, ey, ez, er, ep, eh])

	if ex > max_x:
		max_x = ex
	if ey > max_y:
		max_y = ey
	if ez > max_z:
		max_z = ez
	if er > max_r:
		max_r = er
	if ep > max_p:
		max_p = ep
	if eh > max_h:
		max_h = eh

print "Max. translation errors:   ", max_x, max_y, max_z

open_file.close()

#Proceed

#==============

for line in fic_stock:

	#Read the errors
	ex, ey, ez, er, ep, eh = line

	#Do the math...
	cumulative_counter_x[ int( ex / max_x * (N-1) ) ] += 1
	cumulative_counter_y[ int( ey / max_y * (N-1) ) ] += 1
	cumulative_counter_z[ int( ez / max_z * (N-1) ) ] += 1
	cumulative_counter_r[ int( er / max_r * (N-1) ) ] += 1
	cumulative_counter_p[ int( ep / max_p * (N-1) ) ] += 1
	cumulative_counter_h[ int( eh / max_h * (N-1) ) ] += 1

for i in range(1, N):
	cumulative_counter_x[i] += cumulative_counter_x[i-1]
	cumulative_counter_y[i] += cumulative_counter_y[i-1]
	cumulative_counter_z[i] += cumulative_counter_z[i-1]
	cumulative_counter_r[i] += cumulative_counter_r[i-1]
	cumulative_counter_p[i] += cumulative_counter_p[i-1]
	cumulative_counter_h[i] += cumulative_counter_h[i-1]

for i in range(0, N):
	tot = len(fic_stock)
	
	cumulative_counter_x[i] = float(cumulative_counter_x[i]) / tot
	cumulative_counter_y[i] = float(cumulative_counter_y[i]) / tot
	cumulative_counter_z[i] = float(cumulative_counter_z[i]) / tot
	cumulative_counter_r[i] = float(cumulative_counter_r[i]) / tot
	cumulative_counter_p[i] = float(cumulative_counter_p[i]) / tot
	cumulative_counter_h[i] = float(cumulative_counter_h[i]) / tot


#Plot results

#==============

Xx = [max_x * i/(N-1) for i in range(N)]
Xy = [max_y * i/(N-1) for i in range(N)]
Xz = [max_z * i/(N-1) for i in range(N)]

fig1 = plt.figure()
fig1.suptitle("XYZ errors distribution", size = 16)

plt.subplot(311)
plt.plot(Xx, cumulative_counter_x, 'r')
plt.legend(["x error distribution"])

plt.subplot(312)
plt.plot(Xy, cumulative_counter_y, 'b')
plt.legend(["y error distribution"])

plt.subplot(313)
plt.plot(Xz, cumulative_counter_z ,'g')
plt.legend(["z error distribution"])

plt.show()

Xr = [max_r * i/(N-1) for i in range(N)]
Xp = [max_p * i/(N-1) for i in range(N)]
Xh = [max_h * i/(N-1) for i in range(N)]

fig2 = plt.figure()
fig2.suptitle("RPY errors distribution", size = 16)

plt.subplot(311)
plt.plot(Xr, cumulative_counter_r, 'm')
plt.legend(["roll error distribution"])

plt.subplot(312)
plt.plot(Xp, cumulative_counter_p, 'c')
plt.legend(["pitch error distribution"])

plt.subplot(313)
plt.plot(Xh, cumulative_counter_h ,'y')
plt.legend(["yaw error distribution"])

plt.show()

#"""

#########################
