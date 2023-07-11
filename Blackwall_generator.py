import pandas as pd
import numpy as np
route_data_pd = pd.read_excel('Blackwall_route_2.xlsx', header=None)
route_data = np.array(route_data_pd)
speed_limit_temp = pd.read_excel("Blackwall_speed_limit_real.xlsx", header=None)
speed_limit = np.array(speed_limit_temp)
shape = route_data.shape
sim_time = 20 #in minutes
minute_flow = 0
for i in range(1, shape[0]):
    for j in range(1, shape[1]):
        minute_flow += route_data[i][j]
total_flow = minute_flow * sim_time
total_flow = int(total_flow)
#print(total_flow)
veh_data_temp = np.array([['a'*14]*8]*total_flow)
veh_data = np.array([['a'*14]*8]*total_flow) #0: id, 1: type, 2: depart time, 3: depart lane, 4: depart speed, 5: from, 6: to 7: via
outStr = np.array(["a"*200]*total_flow)
sim_seq = 0
via_grp_1 = ['E000', 'E1000_0', 'E2001_1']
via_grp_2 = ['E3000', 'E2100', 'E2121_0', 'E2110_0']
via_grp_3 = ['E2200_1', 'E3101_0', 'E2221_0', 'E2230_0', 'E2240_0']
via_grp_4 = ['E1301', 'E4206', 'E2370_0', 'E2360_0']
via_grp_5 = ['E2001_0', 'E4005', 'E1000_1']
#'''
for i in range(sim_time):
    for j in range(1, shape[0]):
        for k in range(1, shape[1]):
            if route_data[j][k] >= 1:
                for m in range(route_data[j][k]):
                    seed1 = np.random.rand()
                    veh_data_temp[sim_seq][2] = np.random.randint(0, 60) + i * 60
                    speed_limit_start = speed_limit[j][1]
                    if seed1 <=0.70:
                        veh_data_temp[sim_seq][1] = 'veh_passenger'
                        veh_data_temp[sim_seq][3] = 'best'
                        veh_data_temp[sim_seq][4] = round((np.random.randn() * speed_limit_start * 0.1 + speed_limit_start), 2)
                    elif seed1 > 0.70 and seed1 <= 0.85: 
                        veh_data_temp[sim_seq][1] = 'veh_delivery'
                        veh_data_temp[sim_seq][3] = 'best'
                        veh_data_temp[sim_seq][4] = round((np.random.randn() * speed_limit_start * 0.1 + speed_limit_start*0.95), 2)
                    elif seed1 > 0.85 and seed1 <= 0.90:
                        veh_data_temp[sim_seq][1] = 'veh_lorry'
                        veh_data_temp[sim_seq][3] = '0'
                        veh_data_temp[sim_seq][4] = round((np.random.randn() * speed_limit_start * 0.1 + speed_limit_start*0.85), 2)
                    elif seed1 > 0.90:
                        veh_data_temp[sim_seq][1] = 'veh_motorcycle'
                        veh_data_temp[sim_seq][3] = 'best'
                        veh_data_temp[sim_seq][4] = round((np.random.randn() * speed_limit_start * 0.1 + speed_limit_start), 2)
                    veh_data_temp[sim_seq][5] = route_data[j][0]
                    veh_data_temp[sim_seq][6] = route_data[0][k]
                    if veh_data_temp[sim_seq][5] in via_grp_1:
                        if veh_data_temp[sim_seq][6] in via_grp_2:
                            veh_data_temp[sim_seq][7] = 0
                        elif veh_data_temp[sim_seq][6] in via_grp_3:
                            veh_data_temp[sim_seq][7] = 'E003'
                        elif veh_data_temp[sim_seq][6] not in via_grp_5:
                            veh_data_temp[sim_seq][7] = 'E003 E005'
                    elif veh_data_temp[sim_seq][5] == 'E4210':
                        if veh_data_temp[sim_seq][6] not in via_grp_4:
                            veh_data_temp[sim_seq][7] = 'E4212'
                    sim_seq += 1
            elif route_data[j][k] >= 0.1 and route_data[j][k] < 1:
                flag = 0
                if route_data[j][k] == 0.5:
                    if i % 2 == 1:
                        flag = 1
                elif route_data[j][k] == 0.25:
                    if i % 4 == 2:
                        flag = 1
                elif route_data[j][k] == 0.1:
                    if i % 10 == 5:
                        flag = 1      
                if flag == 1:
                    veh_data_temp[sim_seq][1] = 'veh_passenger'
                    veh_data_temp[sim_seq][2] = np.random.randint(0, 60) + i * 60
                    veh_data_temp[sim_seq][3] = 'best'
                    veh_data_temp[sim_seq][4] = round((np.random.randn() * speed_limit_start * 0.1 + speed_limit_start), 2)
                    veh_data_temp[sim_seq][5] = route_data[j][0]
                    veh_data_temp[sim_seq][6] = route_data[0][k]
                    if veh_data_temp[sim_seq][5] in via_grp_1:
                        if veh_data_temp[sim_seq][6] in via_grp_2:
                            veh_data_temp[sim_seq][7] = 0
                        elif veh_data_temp[sim_seq][6] in via_grp_3:
                            veh_data_temp[sim_seq][7] = 'E003'
                        else:
                            veh_data_temp[sim_seq][7] = 'E003 E005'
                    elif veh_data_temp[sim_seq][5] == 'E4210':
                        if veh_data_temp[sim_seq][6] not in via_grp_4:
                            veh_data_temp[sim_seq][7] = 'E4212'
                    sim_seq += 1
#'''
id_seq = 0
for i in range(sim_time*60):
    for j in range(total_flow):
        if veh_data_temp[j][2] == str(i):
            veh_data[id_seq] = veh_data_temp[j]
            veh_data[id_seq][0] = "veh" + str(id_seq)
            id_seq += 1
for i in range(total_flow):
    tempStr = '    <trip id="'
    tempStr += veh_data[i][0] + '"'
    tempStr += ' type="' + veh_data[i][1] + '"'
    tempStr += ' depart="' + veh_data[i][2] + '"'
    tempStr += ' departLane="' + veh_data[i][3] + '"'
    tempStr += ' departSpeed="' + veh_data[i][4] + '"'
    tempStr += ' from="' + veh_data[i][5] + '"'
    tempStr += ' to="' + veh_data[i][6] + '"'
    if veh_data[i][7] != "aaaaaaaaaaaaaa" and veh_data[i][7] != "0":
        tempStr += ' via="' + veh_data[i][7] + '"'
    tempStr = tempStr + ' />'
    outStr[i] = tempStr

# Open a file in write mode
f = open('Blackwall_demand3.txt', 'w')
for item in outStr:
    f.write("%s\n" % item)
# Close opend file
f.close()