#include <M5StickCPlus2.h>
#include <WiFi.h>
#include <WiFiUdp.h>

const char* WIFI_SSID     = "TP-Link_67C4";
const char* WIFI_PASSWORD = "40349145";
const uint16_t UDP_PORT    = 12345;

static constexpr uint32_t AUDIO_SAMPLE_RATE   = 44100;
static constexpr size_t   AUDIO_FRAME_SAMPLES = 256;
static int16_t audio_buffer[AUDIO_FRAME_SAMPLES];

WiFiUDP udp;
IPAddress remoteIP;
uint16_t remotePort;
bool clientConnected = false;

void setup() {
    auto cfg = M5.config();
    StickCP2.begin(cfg);

    WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
    while (WiFi.status() != WL_CONNECTED) { delay(500); }

    StickCP2.Display.clear();
    StickCP2.Display.printf("IP: %s", WiFi.localIP().toString().c_str());

    StickCP2.Speaker.end();
    StickCP2.Mic.begin();
    udp.begin(UDP_PORT);
}

void loop() {
    // Проверяем, пришел ли запрос от ПК
    int packetSize = udp.parsePacket();
    if (packetSize) {
        remoteIP = udp.remoteIP();
        remotePort = udp.remotePort();
        clientConnected = true;
        // Очищаем буфер входящего пакета
        while(udp.available()) udp.read();
        
        StickCP2.Display.print("Client updated/connected");
    }

    if (clientConnected) {
        if (StickCP2.Mic.record(audio_buffer, AUDIO_FRAME_SAMPLES, AUDIO_SAMPLE_RATE)) {
            udp.beginPacket(remoteIP, remotePort);
            udp.write(reinterpret_cast<uint8_t*>(audio_buffer), AUDIO_FRAME_SAMPLES * sizeof(int16_t));
            udp.endPacket();
        }
    }
}
