#include <RH_ASK.h>
#include <SPI.h> // Not actually used but needed to compile

RH_ASK driver;

//Connect Data to Digital Pin 12
//Connect Ground and VCC to Ground, 5V
void setup()
{
    Serial.begin(9600);   // Debugging only
    if (!driver.init())
         Serial.println("init failed");
    
}

void loop()
{
    int16_t inputVariable[3];

    inputVariable[0] = 1;
    inputVariable[1] = 3;
    inputVariable[2] = 4;

    Serial.println(inputVariable[0]);
    Serial.println(inputVariable[1]);
    Serial.println(inputVariable[2]);

    // Send 6 chars (same size as 3 int16's)
    driver.send((char*)inputVariable, 6);
    driver.waitPacketSent();
    delay(1000);
}
