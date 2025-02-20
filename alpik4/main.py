'''import psutil
import time
import pandas as pd
from datetime import datetime

data = []
def capture_traffic(interval=1): # interval : it's the interval of time
 old_value = psutil.net_io_counters()
 time.sleep(interval)
 new_value = psutil.net_io_counters()
 download_speed = (new_value.bytes_recv - old_value.bytes_recv) / interval
 upload_speed = (new_value.bytes_sent - old_value.bytes_sent) / interval
 return (download_speed, upload_speed)
while True :
 (download, upload) = capture_traffic()
 print(f"Download: {download/1024:.2f} kB/s, Upload: {upload/1024:.2f} kB/s")
 timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
 data.append({"timestamp": timestamp, "download": download, "upload": upload})
 df = pd.DataFrame(data)
 df.to_csv("logs/traffic_log.csv", index=False)









'''
# OKAY OKAY

import psutil
import time
import csv
from datetime import datetime
import win32gui
import win32process
import pandas as pd
import matplotlib.pyplot as plt
import os
'''

class NetworkMonitor:
 def __init__(self, output_file='network_data.csv'):
  self.output_file = output_file
  self.__init__csv()
  self.last_bytes = self._get_network_bytes()

 def __init__csv(self):
  # Only create the file with headers if it doesn't already exist.
  if not os.path.exists(self.output_file):
   headers = [
    'timestamp',
    'download_bytes',  # Données reçues
    'upload_bytes',  # Données envoyées
    'download_speed',  # Vitesse de réception
    'upload_speed',  # Vitesse d'envoi
    'active_app',  # Application en premier plan
    'active_connections'  # Applications avec connexions réseau actives
   ]
   with open(self.output_file, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(headers)

 def _get_network_bytes(self):
  net = psutil.net_io_counters()
  return {
   'upload': net.bytes_sent,
   'download': net.bytes_recv
  }

 def get_active_window(self):
  try:
   window = win32gui.GetForegroundWindow()
   _, pid = win32process.GetWindowThreadProcessId(window)
   process = psutil.Process(pid)
   return process.name()
  except:
   return "unknown"

 def get_network_connections(self):
  # Obtenir toutes les connexions réseau actives
  connections = []
  for conn in psutil.net_connections():
   try:
    if conn.status == 'ESTABLISHED':
     process = psutil.Process(conn.pid)
     connections.append(process.name())
   except:
    continue
  return list(set(connections))  # Enlever les doublons

 def collect_data(self):
  current_time = datetime.now()
  current_bytes = self._get_network_bytes()

  # Calculer les vitesses
  time_diff = 1  # On suppose une seconde entre les mesures
  download_speed = (current_bytes['download'] - self.last_bytes['download']) / time_diff
  upload_speed = (current_bytes['upload'] - self.last_bytes['upload']) / time_diff

  # Collecter les données contextuelles
  active_app = self.get_active_window()
  active_connections = ','.join(self.get_network_connections())

  # Préparer la ligne de données
  data_row = [
   current_time.strftime('%Y-%m-%d %H:%M:%S'),
   current_bytes['download'],
   current_bytes['upload'],
   download_speed,
   upload_speed,
   active_app,
   active_connections
  ]

  # Sauvegarder dans le CSV
  with open(self.output_file, 'a', newline='') as f:
   writer = csv.writer(f)
   writer.writerow(data_row)

  self.last_bytes = current_bytes
  return data_row

 def start_monitoring(self, duration_seconds=3600, interval=1):
  """
  Démarre le monitoring
  duration_seconds: durée en secondes (défaut: 1 heure)
  interval: intervalle entre mesures en secondes (défaut: 1)
  """
  print(f"Démarrage du monitoring réseau...")
  print(f"Données sauvegardées dans: {self.output_file}")
  print("Appuyez sur Ctrl+C pour arrêter")

  end_time = time.time() + duration_seconds

  try:
   while time.time() < end_time:
    data = self.collect_data()
    print(f"\n\rVitesse actuelle - Download: {data[3]/1024:.2f} kB/s, Upload: {data[4]/1024:.2f} kB/s | App active: {data[5]}",
          end='')
    time.sleep(interval)

  except KeyboardInterrupt:
   print("\nMonitoring arrêté par l'utilisateur")

  print("\nMonitoring terminé")


#if __name__ == "__main__":
monitor = NetworkMonitor()
monitor.start_monitoring()
'''

# Data loading

# Load the csv file into a DataFrame
df =pd.read_csv('network_data.csv')
print(df.head())

# Convert the 'timestamp' to a panda datetime format for easier plotting
df['timestamp'] = pd.to_datetime(df['timestamp'])
# Plotting download an upload speeds over time
plt.figure(figsize=(10,6))

# Plot download speed
plt.plot(df['timestamp'], df['download_speed'], label='Download Speed', color='blue')

# Plot upload speed
plt.plot(df['timestamp'], df['upload_speed'], label = 'Upload speed', color='red')

# Add label and title

plt.xlabel('Time')
plt.ylabel('Speed(kbps)')
plt.title('Download and Upload speeds over time')

# Rotate the x-axis labels for better readability

plt.xticks(rotation=45)

# Show the legend

plt.legend()

# Show the plot

plt.tight_layout()
plt.show()