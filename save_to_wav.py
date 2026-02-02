import serial
import wave

PORT = "COM5"          # ON Linux: /dev/ttyACM0
BAUD = 921600

RATE = 44100
CHANNELS = 1
SAMPLE_WIDTH = 2       # int16
FRAME_SAMPLES = 256
FRAME_BYTES = FRAME_SAMPLES * SAMPLE_WIDTH

ser = serial.Serial(PORT, BAUD, timeout=1)

wf = wave.open("mic.wav", "wb")
wf.setnchannels(CHANNELS)
wf.setsampwidth(SAMPLE_WIDTH)
wf.setframerate(RATE)

print("Recording... Ctrl+C to stop")

try:
    while True:
        data = ser.read(FRAME_BYTES)
        if len(data) == FRAME_BYTES:
            wf.writeframes(data)
except KeyboardInterrupt:
    pass

wf.close()
ser.close()
