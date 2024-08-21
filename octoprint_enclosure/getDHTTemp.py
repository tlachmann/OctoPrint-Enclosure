import sys
import time
import adafruit_dht
from microcontroller import Pin
import board

# Parse command line parameters.
sensor_args =   {
                    '11': adafruit_dht.DHT11,
                    '22': adafruit_dht.DHT22,
                    '2302': adafruit_dht.DHT22
                }

milliseconds=2400
if len(sys.argv) == 3 and sys.argv[1] in sensor_args:
    sensor = sensor_args[sys.argv[1]]
    pin = sys.argv[2]
else:
    sys.exit(1)

dht_dev = sensor(Pin(pin), use_pulseio=True)
dht_dev._trig_wait = milliseconds

#dht_dev = adafruit_dht.DHT11(board.D4)
#dht_dev._trig_wait = 2400

# DHT sensor read fails quite often, causing enclosure plugin to report value of 0.
# If this happens, retry as suggested in the adafruit_dht docs.
def getHumi(dht_dev):
    max_retries = 20
    retry_count = 0
    while retry_count <= max_retries:
        try:
            humidity = dht_dev.humidity
            if humidity:
                return humidity
        except RuntimeError as e:
            time.sleep(2)
            retry_count += 1
            continue
        except Exception as e:
            #dht_dev.exit()
            raise e
        time.sleep(3)
        retry_count += 1

    return

def getTemp(dht_dev):
    max_retries = 20
    retry_count = 0
    while retry_count <= max_retries:
        try:
            temperature = dht_dev.temperature
            if temperature:
                return temperature
        except RuntimeError as e:
            time.sleep(2)
            retry_count += 1
            continue
        except Exception as e:
            #dht_dev.exit()
            raise e
        time.sleep(2)
        retry_count += 1
    return

def main():
    try:
        temperature = getTemp(dht_dev)
        humidity = getHumi(dht_dev)
        print('{0:0.1f} | {1:0.1f}'.format(temperature, humidity))
    except:
        print('-1 | -1')
    finally:
        dht_dev.exit()

if __name__ == "__main__":
    main()
