pip install obd numpy scikit-leary
### 🚗 **Python Code for OBD-II Cybersecurity Monitoring**
```python
import obd
import time
import numpy as np
from sklearn.ensemble import IsolationForest

# Connect to OBD-II adapter
connection = obd.OBD() # Auto-connect to available OBD-II port

# Define PIDs to monitor (e.g., speed, RPM, throttle position)
PIDS = ["RPM", "SPEED", "THROTTLE_POS"]

# Store data for anomaly detection
data_log = []

# Machine Learning Model for Anomaly Detection
def train_anomaly_detector(data):
"""Train Isolation Forest model to detect anomalies."""
model = IsolationForest(contamination=0.05) # 5% anomaly threshold
model.fit(data)
return model

# Function to detect hacking attempts
def detect_hacking(model, new_data):
"""Detect anomalies in OBD-II data."""
prediction = model.predict([new_data])
return prediction[0] == -1 # -1 indicates anomaly

# Main monitoring loop
print("🚗 OBD-II Cybersecurity Monitoring Started...")
while True:
try:
# Read OBD-II data
current_data = []
for pid in PIDS:
response = connection.query(obd.commands[pid])
if response.value is not None:
current_data.append(float(response.value))
else:
current_data.append(0) # Default value if no response

# Log data
data_log.append(current_data)

# Train anomaly detector after collecting enough data
if len(data_log) > 50: # Minimum data points for training
model = train_anomaly_detector(np.array(data_log))
if detect_hacking(model, current_data):
print("⚠️ Possible Auto Hacking Detected! 🚨")
with open("hacking_log.txt", "a") as log_file:
log_file.write(f"Suspicious OBD-II activity detected: {current_data}\n")

time.sleep(1) # Adjust sampling rate

except KeyboardInterrupt:
print("\n🚗 Monitoring Stopped.")
break