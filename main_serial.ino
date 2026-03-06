#include <M5StickCPlus2.h>

/* ===================== AUDIO PARAMETRS ===================== */
static constexpr uint32_t AUDIO_SAMPLE_RATE   = 44100;
static constexpr uint16_t AUDIO_BITS_PER_SAMPLE = 16;
static constexpr uint8_t  AUDIO_CHANNELS      = 1;
static constexpr size_t   AUDIO_FRAME_SAMPLES = 256;

/* ===================== SERIAL PARAMETRS ==================== */
static constexpr uint32_t SERIAL_BAUDRATE = 921600;

/* ===================== INDICATOR COLOR =========================== */
static constexpr uint16_t LED_COLOR = GREEN;

/* ===================== BUFFER =============================== */
static int16_t audio_buffer[AUDIO_FRAME_SAMPLES];

void setup() {
    auto cfg = M5.config();
    StickCP2.begin(cfg);

    /* Serial */
    Serial.begin(SERIAL_BAUDRATE);
    while (!Serial) {
        delay(10);
    }

    /* Display indicator */
    StickCP2.Display.clear();
    StickCP2.Display.drawPixel(
        StickCP2.Display.width()  / 2,
        StickCP2.Display.height() / 2,
        LED_COLOR
    );

    /* Audio */
    StickCP2.Speaker.end();
    StickCP2.Mic.begin();
}

void loop() {
    if (StickCP2.Mic.record(
            audio_buffer,
            AUDIO_FRAME_SAMPLES,
            AUDIO_SAMPLE_RATE)) {

        Serial.write(
            reinterpret_cast<uint8_t*>(audio_buffer),
            AUDIO_FRAME_SAMPLES * sizeof(int16_t)
        );
    }
}

