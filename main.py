#hehehehehehehe

water_pump = False
water_pump_state = ""
alarm = False
alarm_state = ""
is_sensor_connected= False


timer = Timer(0)  
 
def closeAlarm(timer):
  relay2.value(not False)
 
timer.init(period=60000, mode=Timer.PERIODIC, callback=closeAlarm)

def states():
    global water_pump_state
    global alarm_state
    
    if water_pump:
        water_pump_state = "ON"
    else:
        water_pump_state = "OFF"
        
    if alarm:
        alarm_state = "ALERT"
    else:
        alarm_state = "SLEEP"
        

def alarm_sys(water_level):
    global water_pump
    global water_pump_state
    global alarm
    global alarm_state
    
    
    
    
    if water_level[1]<20 and water_level[1]>10:
        relay1.value(not True)#water pump
        water_pump = True
    elif water_level[1]<10 and water_level[1]>-1:
        relay2.value(not True)#alarm
        alarm = True
    elif water_level[1]>90 and water_level[1]<95:
        relay1.value(not False)#water pump
        water_pump = False
    elif water_level[1]>95 and water_level[1]<100:
        relay2.value(not True)#alarm
        alarm = False
    else:
        pass
        #relay2.value(not False)#alarm

    
# jsn-sr04t is distance sensor
def read_jsnsr04t_sensor():
    output = []
    distance = int(jsn_sensor.distance_cm())-20
    water_level = (WATER_TANK_HEIGHT)-distance
    water_level_percentage = 100*(water_level/WATER_TANK_HEIGHT)
    
    #calculating liters
    volume = math.pi*pow(WATER_TANK_RADIUS,2)*water_level
    liters_of_water = volume/1000
    
    if water_level==WATER_TANK_HEIGHT+20:
        is_sensor_connected=False
        output.append("disconnected")
        output.append("disconnected")
        output.append("disconnected")
    else:
        is_sensor_connected=True
        output.append(water_level)
        output.append(water_level_percentage)
        output.append(liters_of_water)
        
    print('Water_level :', water_level, 'cm')
    print('Water_level :', water_level_percentage, '%')
    print('Water       :', liters_of_water, 'liter')
    return output


def web_page():
    global water_pump_state
    global alarm_state
    
    distance = read_jsnsr04t_sensor()
    
    if is_sensor_connected:        
        alarm_sys(distance)
        states()
        
    html = """<!DOCTYPE HTML>
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <meta http-equiv="refresh" content="1">
        
        
        <style>
            table, th, td
            {
                border: 1px solid black;
                border-collapse: collapse;
            }
            
            .button
            {
                display: inline-block;
                background-color: #e7bd3b;
                border: none; 
                border-radius: 4px;
                color: white;
                padding: 5px 10px;
                text-decoration: none;
                margin: 2px;
                cursor: pointer;
            }
        
        </style>

    </head>
    <body>
        <div>
                <p><a href="/?led=on"><button class="button">ON</button></a></p>
                <p><a href="/?led=off"><button class="button">OFF</button></a></p>
  
        
            <h2>Synavos IOT</h2>
            <h2>water tank level indicator</h2>
            
            <table style="width: 100%;">
                <caption>Level indicator</caption>
                <tr>
                    <th>Water level</th>
                    <th>Water level</th>
                    <th>Water</th>
                </tr>
                <tr>
                    <td>""" + str(distance[0]) + """ cm</td>
                    <td>""" + str(distance[1]) + """ %</td>
                    <td>""" + str(distance[2]) + """ liter</td>
                </tr>
            </table>
            <br>
            
            <div class="border" style="height:200px;width:100px;border:2px solid red;">
                <div class="" style="background-color:blue;height:100%;width:100px;"></div>
            </div>
            <p style="font-size:13px;margin-top:0px;margin-bottom:0px;">100%</p>
            
            
            <p>Water pump state: <strong>""" + water_pump_state + """</strong></p>
         
                <input class="form-check-input" type="checkbox" role="switch" id="flexSwitchCheckDefault" >
                <label for="flexSwitchCheckDefault">Auto</label>
                
                <input class="form-check-input" type="checkbox" role="switch" id="flexSwitchCheckDefault" >
                <label for="flexSwitchCheckDefault">Auto</label>
    
            <p>Alarm state: <strong>""" + alarm_state + """</strong></p>


        </div>
        
    </body>
    </html>"""
    return html


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

while True:  
    try:
        if gc.mem_free() < 102000:
            gc.collect()
        conn, addr = s.accept()
        conn.settimeout(3.0)
        print('Got a connection from %s' % str(addr))
        request = conn.recv(1024)
        conn.settimeout(None)
        request = str(request)
        #print('Content = %s' % request)
        led_on = request.find('/?led=on')
        led_off = request.find('/?led=off')
        if led_on == 6:
            print('LED ON')
            esp_led.value(1)
            
        if led_off == 6:
            print('LED OFF')
            esp_led.value(0)
            
        response = web_page()
        conn.send('HTTP/1.1 200 OK\n')
        conn.send('Content-Type: text/html\n')
        conn.send('Connection: close\n\n')
        conn.sendall(response)
        conn.close()
    except OSError as e:
        conn.close()
        print('Connection closed')



