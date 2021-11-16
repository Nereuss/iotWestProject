from machine import UART
from micropyGPS import MicropyGPS

def numberOfSatallites():
    gpsSat = MicropyGPS()
    return gpsSat.satellites_in_use

def main():
    uart = UART(2, baudrate=9600, bits=8, parity=None, stop=1, timeout=5000, rxbuf=1024)
    gps = MicropyGPS()
    while True:
        buf = uart.readline()
        print("gps start, trying to get gps data")
        print(buf)
        for char in buf:
            gps.update(chr(char)) # Note the conversion to to chr, UART outputs ints normally

        #print('UTC Timestamp:', gps.timestamp)
        #print('Date:', gps.date_string('long'))
        #print('Satellites: ', gps.satellites_in_use)
        #print('Altitude:', gps.altitude)
        #print('Latitude:', gps.latitude_string())
        #print('Longitude:', gps.longitude_string())
        #print('Horizontal Dilution of Precision:', gps.hdop)
        
        formattedLat = gps.latitude_string()
        formattedLat = formattedLat[:-3]
        formattedLon = gps.longitude_string()
        formattedLon = formattedLon[:-3]
        formattedAlt = str(gps.altitude)
        formattedSpd = gps.speed_string()
        formattedSpd = formattedSpd[:-5]
        

        
        gps_ada = formattedSpd+","+formattedLat+","+formattedLon+","+formattedAlt
        # print(gps_ada)
        # def startGPSthread():
        # _thread.start_new_thread(main, ())
        if formattedLat != "0.0":
            print("gps_ada: ",gps_ada)
            return gps_ada
if __name__ == "__main__":
    print('...running main, GPS testing')
    main()