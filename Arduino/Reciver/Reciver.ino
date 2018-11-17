#include <RH_ASK.h>
#include <SPI.h> // Not actualy used but needed to compile

RH_ASK driver;

void setup()
{
    Serial.begin(9600); // Debugging only
    if (!driver.init())
         Serial.println("init failed");
}

void loop()
{
    char buf[6]; // will store raw data read from driver
    uint8_t buflen = sizeof(buf);
    
    int16_t* integers; // will

    // read raw data into buf
    if (driver.recv(buf, &buflen)) // Non-blocking
    {
      integers = (int16_t*) buf; // point integers at buf so that the data is read as int16's 
      Serial.print("Message: ");
      Serial.println(integers[0]);  
      Serial.println(integers[1]);  
      Serial.println(integers[2]);         
    }
}
