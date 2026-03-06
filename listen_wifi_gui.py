import socket
import sounddevice as sd
import threading
import tkinter as tk
from tkinter import ttk, messagebox

# Параметры аудио
RATE = 44100
CHANNELS = 1
FRAME_SAMPLES = 256
UDP_PORT = 12345

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("M5Stick WiFi Mic")
        self.root.geometry("400x300")
        
        self.is_running = False
        self.thread = None

        # Ввод IP
        tk.Label(root, text="IP адрес M5Stick:").pack(pady=(10, 0))
        self.ip_entry = tk.Entry(root, justify='center')
        self.ip_entry.insert(0, "192.168.1.XX")
        self.ip_entry.pack(pady=5)

        # Выбор динамиков
        tk.Label(root, text="Выберите аудио устройство:").pack(pady=(10, 0))
        
        # Список аудио устройств
        self.devices = sd.query_devices()
        self.device_names = [f"{i}: {d['name']}" for i, d in enumerate(self.devices) if d['max_output_channels'] > 0]
        
        self.device_box = ttk.Combobox(root, values=self.device_names, width=50, state="readonly")
        self.device_box.pack(pady=5)
        if self.device_names:
            self.device_box.current(0) # Выбираем первое по умолчанию

        # Кнопка запуска
        self.btn_start = tk.Button(root, text="Запуск", 
                                   command=self.toggle_stream, 
                                   bg="white", fg="black", font=('Arial', 10, 'bold'))
        self.btn_start.pack(pady=30)

    def audio_worker(self, m5_ip, device_id):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(1.0)
        
        try:
            # Отправляем пакет "Старт" на M5Stick
            sock.sendto(b"start", (m5_ip, UDP_PORT))
            
            with sd.RawOutputStream(samplerate=RATE, channels=CHANNELS, 
                                    dtype='int16', blocksize=FRAME_SAMPLES, 
                                    device=device_id) as stream:
                while self.is_running:
                    try:
                        data, addr = sock.recvfrom(2048)
                        if data:
                            stream.write(data)
                    except socket.timeout:
                        continue
        except Exception as e:
            print(f"Ошибка в потоке: {e}")
        finally:
            sock.close()
            print("Поток закрыт")

    def toggle_stream(self):
        if not self.is_running:
            # Запуск потока
            m5_ip = self.ip_entry.get()
            selected_idx = self.device_box.current()
            
            if selected_idx == -1:
                messagebox.showwarning("Внимание", "Выберите аудио устройство!")
                return
            
            # ID устройства из списка
            real_device_id = int(self.device_names[selected_idx].split(":")[0])
            
            self.is_running = True
            self.btn_start.config(text="ОСТАНОВИТЬ", bg="red")
            
            self.thread = threading.Thread(target=self.audio_worker, 
                                           args=(m5_ip, real_device_id), 
                                           daemon=True)
            self.thread.start()
        else:
            # Остановка
            self.is_running = False
            self.btn_start.config(text="ЗАПУСТИТЬ МИКРОФОН", bg="green")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
