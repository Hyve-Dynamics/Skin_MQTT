import paho.mqtt.client as mqtt
import signal
import sys
import time
import json
import numpy as np
import matplotlib.pyplot as plt

# MQTT broker details
BROKER = "broker.mqtt.cool"
PORT = 1883

# Initialize MQTT client
client = mqtt.Client()

# Callback when the client successfully connects to the broker
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected successfully to the broker!")
        # Subscribe to all topics under HYVE
        client.subscribe("HYVE/#")
        print("Subscribed to HYVE/#")
    else:
        print(f"Failed to connect. Error code: {rc}")

# Callback when a message is received from the broker
def on_message(client, userdata, msg):
    try:
        # Parse the payload as JSON
        data = json.loads(msg.payload.decode())
        
        # Extract values and convert to integers
        values = [int(value) for value in data.values()]
        
        # Ensure there are 100 values to reshape into 10x10
        if len(values) == 100:
            # Reshape into a 10x10 matrix
            sensor_matrix = np.array(values).reshape(10, 10)
            
            # Plot the heatmap
            plot_heatmap(sensor_matrix)
        else:
            print("Received data does not contain exactly 100 values.")
    except json.JSONDecodeError:
        print("Failed to decode message payload as JSON.")
    except Exception as e:
        print(f"An error occurred: {e}")

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

# Function to plot the heatmap
def plot_heatmap(matrix):
    plt.imshow(matrix, cmap='hot', interpolation='nearest')
    plt.colorbar(label='Sensor Value')
    plt.title('Sensor Heatmap')
    plt.xlabel('X Axis (Sensor Columns)')
    plt.ylabel('Y Axis (Sensor Rows)')
    plt.show()

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
