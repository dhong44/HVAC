#include <SimbleeBLE.h>

//setup the connected pins
int light_sensor = 6;
int temp_sensor = 5;

//indicate the output voltage
float voltage = 3.3;

struct information_structure
{
  int light;
  float temp;
  float tempSimblee;
  signed char rssi;
} __attribute__((packed));

information_structure sensorInfo;
int delay_time = 10;

void setup() {

  Serial.begin(9600);

  //setup Bluetooth communications
  SimbleeBLE.advertisementInterval = 10000;
  SimbleeBLE.deviceName = "Sensor 2";
  SimbleeBLE.customUUID = "2220";
  SimbleeBLE.begin();
}

void loop() {

  sensorInfo.light = analogRead(light_sensor);
  sensorInfo.temp = (((voltage / 1024) * analogRead(temp_sensor)) - 0.5) * 100;
  sensorInfo.tempSimblee = Simblee_temperature(CELSIUS);

  SimbleeBLE.send((char*) &sensorInfo, sizeof(sensorInfo));

  
  Simblee_ULPDelay(SECONDS(delay_time));

}

void SimbleeBLE_onRSSI(int rssi)
{
  //Save the RSSI whenever it changes
  sensorInfo.rssi = rssi;
}

void SimbleeBLE_onReceive(char *data, int len)
{
  delay_time = *(int *)data;
  Serial.println(delay_time);
}

  
