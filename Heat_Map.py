import paho.mqtt.client as mqtt
import signal
import sys
import time
import json
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# MQTT broker details
BROKER = "broker.mqtt.cool"
PORT = 1883

# Initialize MQTT client
client = mqtt.Client()

# Global variable to hold sensor data
sensor_matrix = np.zeros((10, 10))  # 10x10 matrix initialized with zeros

# Create a figure and axis for the heatmap
fig, ax = plt.subplots()
heatmap = ax.imshow(sensor_matrix, cmap="viridis", interpolation="nearest", aspect="auto")
plt.colorbar(heatmap, ax=ax)
ax.set_title("Real-Time Sensor Heatmap")
ax.set_xlabel("Sensor Column")
ax.set_ylabel("Sensor Row")

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
    global sensor_matrix
    try:
        # Parse the payload as JSON
        data = json.loads(msg.payload.decode())
        
        # Extract values and convert to integers
        values = [int(value) for value in data.values()]
        
        # Reshape the array into a 10x10 matrix
        sensor_matrix = np.array(values).reshape((10, 10))
        
        # Print the reshaped matrix (OPTIONAL)
        #print("Updated Sensor Matrix:")
        #print(sensor_matrix)
    except json.JSONDecodeError:
        print("Failed to decode message payload as JSON.")
    except ValueError:
        print("Error reshaping the array. Ensure there are exactly 100 elements.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Update function for the heatmap
def update_heatmap(*args):
    global sensor_matrix
    heatmap.set_data(sensor_matrix)  # Update heatmap data
    heatmap.set_clim(vmin=np.min(sensor_matrix), vmax=np.max(sensor_matrix))  # Adjust color scale
    return heatmap,

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

# Start the animation for real-time updates
ani = FuncAnimation(fig, update_heatmap, interval=50, blit=True)  # Update every 50 ms

# Keep the script running
print("Press Ctrl+C to stop and send the STOP command...")
plt.show()
