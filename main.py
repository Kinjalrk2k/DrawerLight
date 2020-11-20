from boltiot import Bolt
import cred
import alerts
import json
import time

api_key = cred.api_key
device_id = cred.device_id

mybolt = Bolt(api_key, device_id)

ir_pin = '4'
led_pin = '0'


def get_sensor(pin):
    try:
        data = json.loads(mybolt.digitalRead(pin))
        if data['success'] != 1:
            print('Request Unsuccessful')
            print('Response data ->', data)
            return None
        sensor_value = int(data['value'])
        return sensor_value

    except Exception as e:
        print('An expection occured while returning the sensor value! Details below:')
        print(e)
        return None


prev_sensor = None
while True:
    sensor_value = get_sensor(ir_pin)
    print(sensor_value)

    if sensor_value == 1 and prev_sensor != 1:
        response = mybolt.digitalWrite(led_pin, 'HIGH')
        alerts.send_sms(
            f'Your drawer was opened on {time.ctime(time.time())}! Ignore, if it was you!')
        prev_sensor = sensor_value

    elif sensor_value == 0 and prev_sensor != 0:
        response = mybolt.digitalWrite(led_pin, 'LOW')
        prev_sensor = sensor_value

    time.sleep(10)
