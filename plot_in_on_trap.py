import json
import matplotlib.pyplot as plt
import numpy as np
import pdb
import sys


#ask user input
trap=input("Enter a trap letter to analyze: ")


f=open('/home/flyranch/field_data_and_analysis_scripts/2021lab/all_traps_final_analysis_json_files/trap_'+trap+'/master_trap_'+trap+'.json')
data=json.load(f)


release=input("What time flies were released? (e.g. 093425) :")
if (len(release)==6 and type(int(release))==int):
	pass
else:
	print("please enter 6 numbers (000000-235959)")
	sys.exit()

released_time=release[0:2]+':'+release[2:4]+':'+release[4:6]

#create lists
on_trap_list=[]
in_trap_list=[]
sec_since_release_list=[]
actual_timestamp_list=[]

for i in data['trap_'+trap]:
	for k in data['trap_'+trap][i]:
		if i=="flies on trap over time:":
			on_trap_list.append(k)
		elif i=="flies in trap over time:":
			in_trap_list.append(k)
		elif i=="actual timestamp:":
			if len(str(int(k)))==5:
				str_time='0'+str(int(k))[0:1]+':'+str(int(k))[1:3]+':'+str(int(k))[3:5]
				actual_timestamp_list.append(str_time)
			elif len(str(int(k)))==6:
				str_time=str(int(k))[0:2]+':'+str(int(k))[2:4]+':'+str(int(k))[4:6]
				actual_timestamp_list.append(str_time)

f.close()

def calc_sec_since_release(standard,time_stamp):
	zero=int(standard[0:2])*3600+int(standard[3:5])*60+int(standard[6:8])+1
	sec=int(time_stamp[0:2])*3600+int(time_stamp[3:5])*60+int(time_stamp[6:8])
	sec_since_release=sec-zero
	return sec_since_release

#to plot 1 min before release
for i in actual_timestamp_list:
	s=calc_sec_since_release(released_time,i)
	if s>=-60:
		sec_since_release_list.append(s)

# remove first 4min
on_trap_list=on_trap_list[120:]

# to name output file
ind=0

fig=plt.figure()

# to set range xlim, ylim
plt.xlim(-60,500)
plt.ylim(0,16)
plt.xlabel('time since release (sec)')
plt.ylabel('flies at trap')


#in advance, plot data till 360 sec
plt.plot(sec_since_release_list[:55], on_trap_list[:55], '-',markersize=6,color="r",label="on trap")
plt.savefig('/home/flyranch/field_data_and_analysis_scripts/2021lab/plots_for_2021_10_30_trap_G/trap_'+trap+'_'+str(0)+'.png',dpi=600)
#pdb.set_trace()

# 360 sec to 760 sec
for i in range(len(sec_since_release_list[:280])):
	plt.plot(sec_since_release_list[55:i], on_trap_list[55:i], '-',markersize=6,color="r",label="on trap")
	plt.savefig('/home/flyranch/field_data_and_analysis_scripts/2021lab/plots_for_2021_10_30_trap_G/trap_'+trap+'_'+str(ind)+'.png',dpi=600)
	ind+=1

# remove first 4min
in_trap_list=in_trap_list[120:]

plt.plot(sec_since_release_list[:280], in_trap_list[:280], '-',markersize=6,color="b",label="in trap")
plt.savefig('/home/flyranch/field_data_and_analysis_scripts/2021lab/plots_for_2021_10_30_trap_G/trap_'+trap+'_'+'RB'+'.png',dpi=600)




