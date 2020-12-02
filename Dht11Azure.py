import random
import time

from azure.iot.device import IoTHubDeviceClient, Message

CONNECTION_STRING = "HostName=IOTTest301120.azure-devices.net;DeviceId=mypi;SharedAccessKey=VY2LTAVPWfZkr+TGBqFT2dQDvx4ehL8SLEFcggqExSU="

TEMPERATURE = 20.0
HUMIDITY = 60
MSG_TXT = '{{"temperature": {temperature},"humidity": {humidity}}}'

def iothub_client_init():
    client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
    return client


def iothub_client_telemetry_sample_run():
    try:
        client = iothub_client_init()
        print("IoT Hub device sending periodic messages, press Ctrl-C to exit")
        while True:

            temperature = TEMPERATURE + (random.random() * 15)
            humidity = HUMIDITY + (random.random() * 20)
            msg_txt_formatted = MSG_TXT.format(temperature=temperature, humidity=humidity)
            message = Message(msg_txt_formatted)

            if temperature > 30:
                message.custom_properties["temperatureAlert"] = "true"
            else:
                message.custom_properties["temperatureAlert"] = "false"

            print("Sending message: {}".format(message))
            client.send_message(message)
            print("Message successfully sent")
            time.sleep(3)

    except KeyboardInterrupt:
        print("IoTHubClient sample stopped")


if __name__ == '__main__':
    print("IoT Hub Quickstart #1 - Simulated device")
    print("Press Ctrl-C to exit")
    iothub_client_telemetry_sample_run()

    import RPi.GPIO as GPIO
    import dht11
    import time

    # initialize GPIO
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    #GPIO.cleanup()

    # read data using Pin GPIO21
    instance = dht11.DHT11(pin=17)

    while True:

        result = instance.read()
        if result.is_valid():
            print("Temp: %d C" % result.temperature +' '+"Humid: %d %%" % result.humidity)

        time.sleep(1)


