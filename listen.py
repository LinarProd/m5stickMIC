import serial
import sounddevice as sd

# SERIAL PARAMETRS
PORT = "COM5"
BAUD = 921600

# AUDIO PARAMETRS
RATE = 44100
CHANNELS = 1
SAMPLE_WIDTH = 2        # int16 (2 byte)
FRAME_SAMPLES = 256     
FRAME_BYTES = FRAME_SAMPLES * SAMPLE_WIDTH

# Serial init
ser = serial.Serial(PORT, BAUD, timeout=1)

print(f"Opening audio stream: {RATE}Hz, {CHANNELS} channel(s), int16")
print("Playing... Ctrl+C to stop")

try:
    # Открываем Raw поток для вывода.
    with sd.RawOutputStream(samplerate=RATE, 
                            channels=CHANNELS, 
                            dtype='int16',
                            blocksize=FRAME_SAMPLES) as stream:
        while True:
            # Читаем сырые байты из COM-порта
            data = ser.read(FRAME_BYTES)
            
            # Если пакет полный, пишем его сразу в аудио-поток
            if len(data) == FRAME_BYTES:
                stream.write(data)

except KeyboardInterrupt:
    print("\nStopping...")

finally:
    ser.close()
