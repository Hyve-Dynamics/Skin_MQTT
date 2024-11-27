
# Real-Time Sensor Data Visualization and Analysis

![Real-Time Heatmap Demo](Assets/demo.gif)

This repository contains Python scripts for managing, visualizing, and testing data from the Haptic Matrix in a 10x10 sensor arrangement. The scripts leverage MQTT for real-time data communication and include functionalities for data collection, visualization, and testing.

---

## **Repository Contents**

1. **`MQTT_Test.py`**  
   - **Description**: A simple script to test MQTT connectivity and verify message reception from the broker. It logs received messages to the console.
   - **Key Features**:
     - Connects to the broker and subscribes to the topic `HYVE/#`.
     - Logs any messages received on subscribed topics.
   - **Usage**:
     1. Run the script: `python MQTT_Test.py`.
     2. Check the console for messages received from the broker.

2. **`Data_Fetch.py`**  
   - **Description**: A script to collect raw sensor data in JSON format via MQTT and print it as a flat array of values.
   - **Key Features**:
     - Connects to the broker and subscribes to `HYVE/#`.
     - Parses incoming JSON messages and converts them into a list of integer values.
     - Logs the extracted data to the console.
   - **Usage**:
     1. Run the script: `python Data_Fetch.py`.
     2. Observe the raw sensor data printed as a flat array in the console.

3. **`Heat_Map.py`**  
   - **Description**: A real-time visualization tool for sensor data. It reshapes the incoming data into a 10x10 matrix and displays it as a heatmap.
   - **Key Features**:
     - Visualizes sensor data dynamically using `matplotlib`.
     - Updates the heatmap in real time as new data is received.
     - Automatically adjusts the color scale based on the incoming data.
   - **Usage**:
     1. Install the required Python libraries: `pip install matplotlib numpy paho-mqtt`.
     2. Run the script: `python Heat_Map.py`.
     3. A heatmap window will appear, updating as new sensor data is received.

4. **`TimeTest.py`**  
   - **Description**: Measures the timing characteristics of incoming MQTT messages, such as time intervals and frequency of messages.
   - **Key Features**:
     - Logs the time interval between consecutive messages.
     - Calculates and displays average time per message and messages per second.
     - Plots a histogram of the time intervals.
   - **Usage**:
     1. Install the required Python libraries: `pip install matplotlib numpy paho-mqtt`.
     2. Run the script: `python TimeTest.py`.
     3. After 1 minute, view the printed statistics and the histogram plot.

---

## **Setup Instructions**
1. Install the required Python libraries:
   ```bash
   pip install paho-mqtt matplotlib numpy
   ```
2. Update the broker and port information in each script if necessary.
3. Ensure your sensor network is correctly publishing data to the MQTT broker.

---

## **Contributions**
Feel free to contribute by opening issues or submitting pull requests.

---

## **License**
This repository is available under the [MIT License](LICENSE).

