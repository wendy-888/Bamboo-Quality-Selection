import serial
import time

ser = serial.Serial(
    port='/dev/cu.usbmodem101',
    baudrate=9600,
    timeout=1
)
time.sleep(1)

def read():
    RGB = []
    dummy = []
    timeout_counter = 0
    health_col = []

    while True:
        if ser.in_waiting > 0:
            data = ser.readline()
            data = data.decode().strip()

            if data[0] == 'R' or data[0] == 'G':
                RGB.append(int(data[1:]))
            elif data[0] == 'B':
                RGB.append(int(data[1:]))
                hel = colour(RGB)
                health_col.append(hel)
                RGB = []
            elif data[0] == 'D':
                dummy.append(float(data[1:]))
                timeout_counter += 1
                if timeout_counter == 21: 
                    return health_col, dummy

def colour(data):
    error = [0, 0, 0]
    sum = 0
    sum_prev = 1000
    colour = None
    RGBlist = {"healthy1": [151, 176, 125], "healthy2": [173, 197, 135],  
               "healthy3": [123, 140, 86], "healthy4": [91, 110, 68],  
               "healthy5": [117, 166, 99], "healthy6": [97, 141, 68],  
               "healthy7": [91, 117, 66], "healthy8": [136, 152, 103], 
               "healthy9": [118, 121, 114], "healthy10": [119, 121, 106], 
               "healthy11": [89, 170, 63], "healthy12": [89, 251, 98], 
               "healthy13": [81, 213, 53], "healthy14": [177, 221, 100], 
               "healthy15": [54, 144, 81], 
               "unhealthy1": [158, 162, 136], 
               "unhealthy2": [176, 186, 139], "unhealthy3": [153, 172, 131], 
               "unhealthy4": [151, 172, 127]}
    for key, value in RGBlist.items():
        sum = 0
        for i in range(len(value)):
            error[i] = abs(data[i] - value[i])
            sum += error[i]
        if sum < sum_prev:
            colour = key
            sum_prev = sum
        if sum_prev >= 60:
            colour = "unhealthy!"
    return colour

def distance(dummylist):
    distance_list = []
    heal_dis = []
    for i in range(len(dummylist) - 1):
        distance_list.append(dummylist[i + 1] - dummylist[i])
    for i in range(len(distance_list)):
        if distance_list[i] >= 5:
            heal_dis.append("healthy")
        else:
            heal_dis.append("unhealthy")
    healthy_distance = 0
    unhealthy_distance = 0
    overall_health = ""
    for i in range(len(heal_dis)):
        if heal_dis[i] == "healthy":
            healthy_distance += 1
        elif heal_dis[i] == "unhealthy":
            unhealthy_distance += 1
    if healthy_distance >= unhealthy_distance:
        overall_health = "Healthy"
    else:
        overall_health = "Unhealthy"
    return distance_list, heal_dis, overall_health

if __name__ == "__main__":
    health_col, dummy = read()
    dist, heal_list, overall_health_dist = distance(dummy)
    overall = ""
    print("Distance list: ", dist)
    print("Health distance list: ", heal_list)
    print("Result from distance: ", overall_health_dist)
    healthy_col = 0
    unhealthy_col = 0
    overall_health_col = ""
    for i in range(len(health_col)):
        if health_col[i] == "unhealthy1" or health_col[i] == "unhealthy2" or health_col[i] == "unhealthy3" or health_col[i] == "unhealthy4" or health_col[i] == "unhealthy!":
            unhealthy_col += 1
        else:
            healthy_col += 1
    if healthy_col >= unhealthy_col:
        overall_health_col = "Healthy"
    else:
        overall_health_col = "Unhealthy"
    if overall_health_col == "Healthy" and overall_health_dist == "Healthy":
        overall = "Healthy Bamboo"
    else:
        overall = "Unhealthy Bamboo"
    print("Health colour list: ", health_col)
    print("Result from colour:", overall_health_col)
    print("Overall health condition for bamboo: ", overall)