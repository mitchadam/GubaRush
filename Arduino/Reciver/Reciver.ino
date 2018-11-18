#include <RH_ASK.h>
#include <SPI.h> // Not actualy used but needed to compile

RH_ASK driver;

//Data connects to Digital pin 11
//Connect Ground and VCC to Ground, 5V


void setup()
{
    Serial.begin(9600); // Debugging only
    if (!driver.init())
         Serial.println("init failed");
}

void loop()
{
    char buf[12]; // will store raw data read from driver
    uint8_t buflen = sizeof(buf);
    
    int16_t* integers; // will store data converted to int16's

    // read raw data into buf
    if (driver.recv(buf, &buflen)) // Non-blocking
    {
      integers = (int16_t*) buf; // point integers at buf so that the data is read as int16's 
      Serial.println("start");
      Serial.println(integers[0]); // AcX  
      Serial.println(integers[1]); // AcY
      Serial.println(integers[2]); // AcZ
      Serial.println(integers[3]); // GyX
      Serial.println(integers[4]); // GyY
      Serial.println(integers[5]); // GyZ
      Serial.println("end");      
    }
}
