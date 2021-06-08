#include <ESP8266WiFi.h>
#include <SoftwareSerial.h>
#include <FirebaseArduino.h>
#include <ArduinoJson.h>
#include <ESP8266HTTPClient.h>
#include "DHT.h"        // including the library of DHT11 temperature and humidity sensor
#define DHTTYPE DHT11   // DHT 11
#include "MQ135.h"
#define ANALOGPIN A0
MQ135 gasSensor = MQ135(ANALOGPIN);
#define dht_dpin 2
DHT dht(D2, DHTTYPE);

 
// Set these to run example.
#define FIREBASE_HOST "iottest1-9eb75-default-rtdb.firebaseio.com"
#define FIREBASE_AUTH "mYyNV35sSv0ersGd0tUPRAgHq8mJBorOF1LGV5UJ"
#define WIFI_SSID "4G" //provide ssid (wifi name)
#define WIFI_PASSWORD "WENUSARA1997" //wifi password

void setup() {
  dht.begin();
  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(D4, OUTPUT);
  Serial.begin(9600);     
  pinMode(D5, INPUT);
  pinMode(D6, INPUT);
  pinMode(D7, INPUT);
  pinMode(D8, INPUT);


  // connect to wifi.
 WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
 Serial.print("connecting");
 while (WiFi.status() != WL_CONNECTED)
 {
 Serial.print(".");
 delay(500);
 }
 Serial.println();
 Serial.print("connected: ");
 Serial.println(WiFi.localIP());
 
 
 Firebase.begin(FIREBASE_HOST, FIREBASE_AUTH);
if(Firebase.failed())
 {
 Serial.print(Firebase.error());
 }
 else{
 Serial.println("Firebase Connected");
 digitalWrite(D5, HIGH);
 Firebase.setInt("temperature",25);
 }
 
}

void loop() {


  int i,y,z,p;
  float rzero = gasSensor.getRZero();
  float ppm = gasSensor.getPPM();
  float h = dht.readHumidity();
  float t = dht.readTemperature();  
  float f1 = digitalRead(D5)+digitalRead(D6)+digitalRead(D7)+digitalRead(D8);
  int f6=(int) f1;
  i = (int) t;
  y = (int) h;
  z = (int) rzero;
  p = (int) ppm;
  Serial.println(f6);
  Firebase.setInt("/FirebaseIOT/f1",f6);
  Firebase.setInt("/FirebaseIOT/temperature",i);
  Firebase.setInt("/FirebaseIOT/humidity",y); 
  Firebase.setInt("FirebaseIOT/smoke",p);
  if(ppm>205 || f6 != 4){ 
  Firebase.setString("/FirebaseIOT/de1","not safe");
  digitalWrite(D4, HIGH);
  delay(500);
    }
  else{
    Firebase.setString("/FirebaseIOT/de1","safe");
    digitalWrite(D4, LOW);
    }
  digitalWrite(LED_BUILTIN, HIGH);
  delay(500);
  digitalWrite(LED_BUILTIN, LOW);
  delay(300);
  
}
