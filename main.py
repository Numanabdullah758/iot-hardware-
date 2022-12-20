water_pump = None
alarm = None

# ---------------------intrupt (close alarm)-------------------------------
timer = Timer(0)

def closeAlarm(timer):
    relay2.value(not False)
    
timer.init(period=60000, mode=Timer.PERIODIC, callback=closeAlarm)
# ------------------------------------------------------------------------


# alarm system -------------------------------------------------------
def alarm_sys(water_level):
    global water_pump
    global alarm
    
    if water_level == "error":
        return
    else:
        water_level = int(water_level)
        
       
    if water_level in PUMP_ON_RANGE:
        relay1.value(not True)  # water pump
        water_pump = True
    elif water_level in PUMP_OFF_RANGE:
        relay1.value(not False)  # water pump
        water_pump = False


    if water_level in ALARM_ON_RANGE_LOW:
        relay2.value(not True)  # alarm
        alarm = True
    elif water_level in ALARM_ON_RANGE_FULL:
        relay2.value(not True)  # alarm
        alarm = True
        
# --------------------------------------------------------------------


# water_tank_sensor --------------------------------------------------
def water_tank_sensor():
    output = {}
    total_distance = int(jsn_sensor.distance_cm())
    distance = total_distance - 20
    water_lvl_cm = W_TANK_HEIGHT - distance
    water_lvl_pct = int(100 * (water_lvl_cm / W_TANK_HEIGHT))

    # calculating liters
    water_vol_cm3 = math.pi * pow(W_TANK_RADIUS, 2) * water_lvl_cm
    water_vol_ltr = water_vol_cm3 / 1000

    if water_lvl_cm in range(0, W_TANK_HEIGHT+1):
        output["water_lvl_cm"] = water_lvl_cm
        output["water_lvl_pct"] = water_lvl_pct
        output["water_vol_ltr"] = water_vol_ltr
    else:
        output["water_lvl_cm"] = "error"
        output["water_lvl_pct"] = "error"
        output["water_vol_ltr"] = "error"

    return output
# --------------------------------------------------------------------


# client_socket && server_socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('', 80))
server_socket.listen(5)


while True:
    
    
#     print("_________________________________")
#     print("data : ", data)
    print(PUMP_ON_RANGE)
    print(PUMP_OFF_RANGE)
    print(ALARM_ON_RANGE_FULL)
    print(ALARM_ON_RANGE_LOW)
#     print("_________________________________")

    conn, addr = server_socket.accept()
    
    data = {}
    data["sensor_reading"]= water_tank_sensor()
    print(data["sensor_reading"]["water_lvl_pct"])
#     alarm_sys(data["sensor_reading"]["water_lvl_pct"])
    data["water_pump"] = water_pump
    data["alarm"] = alarm
    
    data_json = json.dumps(data)
    
    
    conn.send(data_json)
    conn.close()


