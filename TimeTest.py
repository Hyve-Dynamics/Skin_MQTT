import paho.mqtt.client as mqtt
import numpy as np
import sys
import time
from datetime import datetime
import matplotlib.pyplot as plt

# MQTT broker details
BROKER = "broker.mqtt.cool"
PORT = 1883

# Initialize MQTT client
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

# Variables to track time intervals and total packages
time_intervals = []
previous_timestamp = None
total_packages = 0
start_time = None

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
    global previous_timestamp, time_intervals, total_packages

    # Record the current timestamp
    current_timestamp = datetime.now()

    # Calculate the time difference if there was a previous message
    if previous_timestamp is not None:
        time_diff = (current_timestamp - previous_timestamp).total_seconds()
        time_intervals.append(time_diff)

    # Update the previous timestamp to the current one
    previous_timestamp = current_timestamp

    # Increment the total packages count
    total_packages += 1

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

# Print metrics and plot histogram of time intervals
def print_metrics_and_plot(time_intervals, total_packages):
    # Calculate metrics
    if time_intervals:
        avg_time_per_package = np.mean(time_intervals)
        packages_per_second = total_packages / 60  # 1 minute = 60 seconds
    else:
        avg_time_per_package = 0
        packages_per_second = 0

    # Print metrics
    print("\n===== Metrics =====")
    print(f"Total packages received: {total_packages}")
    print(f"Average time per package: {avg_time_per_package:.6f} seconds")
    print(f"Packages per second: {packages_per_second:.2f} packages/second")

    # Plot histogram
    plt.hist(time_intervals, bins=20, edgecolor='black', alpha=0.75)
    plt.title("Histogram of Time Intervals Between Messages")
    plt.xlabel("Time Interval (seconds)")
    plt.ylabel("Frequency")
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.figtext(0.15, 0.85, f"Total Packages: {total_packages}", fontsize=10)
    plt.show()

# Assign callback functions
client.on_connect = on_connect
client.on_message = on_message

# Connect to the broker
client.connect(BROKER, PORT, keepalive=60)

# Start the MQTT client loop
client.loop_start()

# Start data collection
send_command('{"REQUEST":"RUN"}')
print("Collecting data for 1 minute...")

# Record the start time
start_time = datetime.now()

try:
    # Run for 1 minute
    while (datetime.now() - start_time).total_seconds() < 60:
        time.sleep(0.1)

    # Stop data collection
    print("\n1 minute is up! Sending STOP command...")
    send_command('{"REQUEST":"STOP"}')

    # Stop the MQTT client loop
    client.loop_stop()
    client.disconnect()

    # Print results and metrics
    print_metrics_and_plot(time_intervals, total_packages)

except KeyboardInterrupt:
    signal_handler(None, None)