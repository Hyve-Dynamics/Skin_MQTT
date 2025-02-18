import paho.mqtt.client as mqtt
import signal
import sys
import time

# MQTT broker details
BROKER = "broker.mqtt.cool"
PORT = 1883

# Initialize MQTT client
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

# Callback when the client successfully connects to the broker
def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print("Connected successfully to the broker!")
        client.subscribe("HYVE/#")
        print("Subscribed to HYVE/#")
    else:
        print(f"Failed to connect. Error code: {reason_code}")

# Callback when a message is received from the broker
def on_message(client, userdata, msg):
    print(f"Message received on topic {msg.topic}: {msg.payload.decode()}")

# Function to send a command to the sensor
def send_command(command):
    topic = "HYVE/REQUEST"
    client.publish(topic, command)
    print(f"Sent command: {command} to topic: {topic}")

# Signal handler for graceful shutdown
def signal_handler(sig, frame):
    print("\nCtrl+C pressed. Sending STOP command...")
    send_command('{"REQUEST":"STOP"}')  # Send STOP command
    client.loop_stop()  # Stop the MQTT loop
    client.disconnect()  # Disconnect from the broker
    print("Disconnected from broker. Exiting...")
    sys.exit(0)

# Assign callback functions
client.on_connect = on_connect
client.on_message = on_message

# Connect to the broker
client.connect(BROKER, PORT, keepalive=60)

# Register signal handler for Ctrl+C
signal.signal(signal.SIGINT, signal_handler)

# Start the MQTT client loop
client.loop_start()

# Example: Send a command to start collecting data
send_command('{"REQUEST":"RUN"}')

# Keep the script running
print("Press Ctrl+C to stop and send the STOP command...")
try:
    while True:
        time.sleep(1)  # Keep the script running
except KeyboardInterrupt:
    signal_handler(None, None)
