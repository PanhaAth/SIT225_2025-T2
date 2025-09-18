import threading
from collections import deque
from datetime import datetime, timezone
from arduino_iot_cloud import ArduinoCloudClient

class SmoothArduinoCloudClient:
    def __init__(self, device_id, secret_key, window_size=200):
        self.device_id = device_id
        self.secret_key = secret_key
        self.window_size = window_size
        
        # Data buffers for smooth plotting
        self.time_buffer = deque(maxlen=window_size)
        self.x_buffer = deque(maxlen=window_size)
        self.y_buffer = deque(maxlen=window_size)
        self.z_buffer = deque(maxlen=window_size)
        
        # Latest values
        self.latest_values = {"x": 0.0, "y": 0.0, "z": 0.0}
        self.lock = threading.Lock()
        
        # Client initialization
        self.client = None
        
    def _on_x_changed(self, client, value):
        with self.lock:
            timestamp = datetime.now(timezone.utc).astimezone()
            self.time_buffer.append(timestamp)
            self.x_buffer.append(float(value))
            self.latest_values["x"] = float(value)
    def _on_y_changed(self, client, value):
        with self.lock:
            self.y_buffer.append(float(value))
            self.latest_values["y"] = float(value)
            
    def _on_z_changed(self, client, value):
        with self.lock:
            self.z_buffer.append(float(value))
            self.latest_values["z"] = float(value)
    
    def get_buffers(self):
        """Get a thread-safe copy of all buffers"""
        with self.lock:
            return {
                "time": list(self.time_buffer),
                "x": list(self.x_buffer),
                "y": list(self.y_buffer),
                "z": list(self.z_buffer)
            }
            
    def get_latest(self):
        """Get the latest values"""
        with self.lock:
            return self.latest_values.copy()
    
    def start_client(self):
        """Start the Arduino Cloud client in a background thread"""
        def run_client():
            try:
                self.client = ArduinoCloudClient(
                    device_id=self.device_id,
                    username=self.device_id,
                    password=self.secret_key
                )
                
                # Register variables with callbacks
                self.client.register("py_x", value=None, on_write=self._on_x_changed)
                self.client.register("py_y", value=None, on_write=self._on_y_changed)
                self.client.register("py_z", value=None, on_write=self._on_z_changed)
                
                print("[Smooth Cloud Client] Starting...")
                self.client.start()
            except Exception as e:
                print(f"[Smooth Cloud Client] Error: {e}")
                import traceback
                traceback.print_exc()
        
        # Start client in a daemon thread
        client_thread = threading.Thread(target=run_client, daemon=True)
        client_thread.start()