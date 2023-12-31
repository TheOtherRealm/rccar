
/*
  This sketch will create a new access point (with no password).
  It will then launch a new server and print out the IP address
  to the Serial monitor. From there, you can open that address in a web browser
  to control the car.
  If the IP address of your board is yourAddress:
    http://yourAddress/#F makes the car go Forward
    http://yourAddress/#L makes the car go Left
    http://yourAddress/#R makes the car go Right
    http://yourAddress/#B makes the car go Backward
    Combining F/B & L/R buttons makes the car do both
 */
#include <SPI.h>
#include <WiFiNINA.h>
#include <mbed.h>
#include "arduino_secrets.h"
#include <SparkFun_TB6612.h>
#define AIN1 8
#define BIN1 5
#define AIN2 9
#define BIN2 4
#define PWMA 10
#define PWMB 3
#define STBY 7
///////Put the WiFi network info in the secret tab (arduino_secrets.h)
char ssid[] = SECRET_SSID;  // The network SSID (name)
int led = LED_BUILTIN;
int status = WL_IDLE_STATUS;
// these constants are used to allow you to make your motor configuration
// line up with function names like forward.  Value can be 1 or -1
const int offsetA = 1;
const int offsetB = 1;
// Initializing motors with the TB6612FNG H-Bridge Motor Driver library
Motor motor1 = Motor(AIN1, AIN2, PWMA, offsetA, STBY);
Motor motor2 = Motor(BIN1, BIN2, PWMB, offsetB, STBY);
int rMotorControl = 9;
int fMotorControl = 10;
int rMotorState = 's';
int fMotorState = 's';
int statusUpdate = 0;
WiFiServer server(80);
void setup() {
  //Initialize serial and wait for port to open:
  Serial.begin(9600);
  Serial.setTimeout(200);
  Serial.print("Access Point Web Server ssid: ");
  Serial.print(ssid);
  Serial.print("and pswrd: ");
  Serial.println(pass);
  pinMode(led, OUTPUT);  // set the LED pin mode
  // make the transistor's pin an output:
  pinMode(rMotorControl, OUTPUT);
  pinMode(fMotorControl, OUTPUT);
  // check for the WiFi module:
  if (WiFi.status() == WL_NO_MODULE) {
    Serial.println("Communication with WiFi module failed!");
    // don't continue
    while (true)
      ;
  }
  String fv = WiFi.firmwareVersion();
  if (fv < WIFI_FIRMWARE_LATEST_VERSION) {
    Serial.println("Please upgrade the firmware");
  }
  // by default the local IP address of will be 192.168.4.1
  Serial.print("Creating access point named: ");
  Serial.println(ssid);
  // Create open network and print some status indicators for debuging
  status = WiFi.beginAP(ssid, 1);
  Serial.println(WL_AP_LISTENING);
  Serial.println(WL_NO_SSID_AVAIL);
  Serial.println(WL_SCAN_COMPLETED);
  Serial.println(WL_AP_FAILED);
  Serial.println(WL_DELAY_START_CONNECTION);
  Serial.println(WL_IDLE_STATUS);
  Serial.println(status);

  while (status == WL_AP_FAILED) {
    Serial.println("Creating access point failed");
    status = WiFi.beginAP(ssid);
    Serial.println(status);
    // Uncoment this to make the code not continue if wifi can't be set up
    // while (true);
  }
  if (status != WL_AP_LISTENING) {
    Serial.println("Creating access point failed");
    // This makes the code not continue if wifi can't be set up
    while (true);
  }
  delay(10000);
  // wait 10 seconds for connection:
  // start the web server on port 80 (http)
  server.begin();
  // you're connected now, so print out the status
  printWiFiStatus();
  statusUpdate = 0;
  Serial.println(status);
}
void loop() {
  // compare the previous WiFi status to the current status
  if (status != WiFi.status()) {
    // it has changed, update the variable
    status = WiFi.status();
    if (status == WL_AP_CONNECTED) {
      // a device has connected to the AP
      Serial.println("Device connected to AP");
    } else {
      // a device has disconnected from the AP, and we are back in listening mode
      Serial.println("Device disconnected from AP");
    }
  }
  WiFiClient client = server.available();  // listen for incoming clients
  if (client) {                            // if you get a client,
    // Serial.println("new client");          // print a message out the serial port
    String currentLine = "";      // make a String to hold incoming data from the client
    while (client.connected()) {  // loop while the client's connected
      if (client.available()) {   // if there's bytes to read from the client,
        char c = client.read();   // read a byte, then
        // Serial.write(c);                   // print it out the serial monitor
        if (c == '\n') {  // if the byte is a newline character
          // if the current line is blank, you got two newline characters in a row.
          // that's the end of the client HTTP request, so send a response:
          if (currentLine.length() == 0) {
            // HTTP headers always start with a response code (e.g. HTTP/1.1 200 OK)
            // and a content-type so the client knows what's coming, then a blank line:
            client.println("HTTP/1.1 200 OK");
            client.println("Content-type:text/html");
            client.println();
            String pageHTML = R"EOF(
<!DOCTYPE html>
<html>
<head>
    <title>Car Controls</title>
</head>
<body>
    <div style='text-align: center;font-size: xx-large;width: auto;'>
        <div>
            <button style='font-size: 3em;' class='dirBut' data-dir='f' id='forward'>Forward</button>
        </div>
        <div style="width: auto;">
            <button style='font-size: 3em;width:30%;' class='dirBut' data-dir='l' id='left'>Left</button>
            <button style='font-size: 3em;width:30%;' class='dirBut' data-dir='s' id='stop'>Stop</button> 
            <button style='font-size: 3em;width:30%;' class='dirBut' data-dir='r' id='right'>Right</button>
        </div>
        <div>
            <button style='font-size: 3em;' class='dirBut' data-dir='b' id='back'>Back</button>
        </div>
    </div>
    <div style='text-align: center;font-size: 3em;'> Direction: <span id='dir_display'></span>
    </div>
    <script>
        function startup() {
            const direct = document.querySelectorAll('.dirBut');
            direct.forEach((but) => {
                but.addEventListener('mousedown', buttonPressed);
                but.addEventListener('touchstart', buttonPressed);
                but.addEventListener('touchend', buttonReleased);
                but.addEventListener('mouseup', buttonReleased);
            });
        }
        document.addEventListener('DOMContentLoaded', startup);
        function buttonPressed(but) {
            but.preventDefault();
            const dirDisplay = document.querySelector('#dir_display');
            if(window.location.hash=='#s'){
                window.location.hash='';
                dirDisplay.innerHTML ='';
            }
            console.log(window.location.hash);
            dirDisplay.innerHTML = dirDisplay.innerHTML + but.target.dataset.dir
            window.location.hash = dirDisplay.innerHTML
            const req = new XMLHttpRequest();
            req.addEventListener("load", reqListener);
            req.open("GET", but.target.dataset.dir);
            req.send(but.target.dataset.dir);
        }
        function buttonReleased(but) {
            but.preventDefault();
            const dirDisplay = document.querySelector('#dir_display');
            window.location.hash = 's';
            // console.log(but);
            dirDisplay.innerHTML = 's';
            const req = new XMLHttpRequest();
            req.addEventListener("load", reqListener);
            req.open("GET", 's');
            req.send('s');
        }
        function reqListener() {
            // console.log(this.responseText);
        }
    </script>
</body>
</html>)EOF";
            // the content of the HTTP in the previus variable:
            client.print(pageHTML);
            // The HTTP response ends with another blank line:
            client.println();
            // break out of the while loop:
            break;
          } else {  // if you got a newline, then clear currentLine:
            currentLine = "";
          }
        } else if (c != '\r') {  // if you got anything else but a carriage return character,
          currentLine += c;      // add it to the end of the currentLine
        }
///////////////////////
//This is where the code for controlling the motors starts!!!
///////////////////////
        // Check to see if the client request was "GET /f" or "GET /b" (f=front; b=back) or "GET /r" or "GET /l" (r=right; l=left):
        if (currentLine.endsWith("GET /f")) {
          rMotorState = 'f';
          Serial.println("Forward");
          digitalWrite(led, HIGH);  // Movement turns the LED on
          //Use of the drive function which takes as arguements the speed
          //and optional duration.  A negative speed will cause it to go
          //backwards.  Speed can be from -255 to 255.  Also use of the
          //brake function which takes no arguements.
          motor1.drive(-255);
        } else if (currentLine.endsWith("GET /b")) {
          rMotorState = 'b';
          Serial.println("Back ");
          digitalWrite(led, HIGH);  // Movement turns the LED on
          //Use of the drive function which takes as arguements the speed
          //and optional duration.  A negative speed will cause it to go
          //backwards.  Speed can be from -255 to 255.  Also use of the
          //brake function which takes no arguements.
          motor1.drive(255);
        } else if (currentLine.endsWith("GET /s")) {
          rMotorState = 's';
          Serial.println("Stop");
          digitalWrite(led, LOW);  // GET /s turns the LED off
          motor1.brake();          // Stops the moter
        }
        if (currentLine.endsWith("GET /l")) {
          fMotorState = 'l';
          Serial.println("left");
          digitalWrite(led, HIGH);  // Movement turns the LED on
          //Use of the drive function which takes as arguements the speed
          //and optional duration.  A negative speed will cause it to go
          //backwards.  Speed can be from -255 to 255.  Also use of the
          //brake function which takes no arguements.
          motor2.drive(255);
        } else if (currentLine.endsWith("GET /r")) {
          fMotorState = 'r';
          Serial.println("right " + rMotorState);
          digitalWrite(led, HIGH);  // Movement turns the LED on
          //Use of the drive function which takes as arguements the speed
          //and optional duration.  A negative speed will cause it to go
          //backwards.  Speed can be from -255 to 255.  Also use of the
          //brake function which takes no arguements.
          motor2.drive(-255);
        } else if (currentLine.endsWith("GET /s")) {
          fMotorState = 's';
          Serial.println("Stop");
          digitalWrite(led, LOW);  // GET /s turns the LED off
          motor2.brake();          // Stops the moter
        }
      }
    }
    // close the connection:
    client.stop();
    Serial.println("client disconnected");
    Serial.println(statusUpdate%50000);
  } else {
    if ((statusUpdate==50000)) {
      Serial.println(status);
      if (rMotorState == 's' || fMotorState == 's') {
        digitalWrite(led, LOW);  // GET /s turns the LED off
        motor1.brake();          // Stops the moter
      }
      statusUpdate = 0;
    } else {
      statusUpdate++;
    }
    if (rMotorState == 'f') {
      digitalWrite(led, HIGH);  // Movement turns the LED on
      //Use of the drive function which takes as arguements the speed
      //and optional duration.  A negative speed will cause it to go
      //backwards.  Speed can be from -255 to 255.  Also use of the
      //brake function which takes no arguements.
      motor1.drive(-255);
    } else if (rMotorState == 'b') {
      digitalWrite(led, HIGH);  // Movement turns the LED on
      //Use of the drive function which takes as arguements the speed
      //and optional duration.  A negative speed will cause it to go
      //backwards.  Speed can be from -255 to 255.  Also use of the
      //brake function which takes no arguements.
      motor1.drive(255);
    } else if (rMotorState == 's') {
      digitalWrite(led, LOW);  // GET /s turns the LED off
      motor1.brake();          // Stops the moter
    }
    if (rMotorState == 'l') {
      Serial.println("left");
      digitalWrite(led, HIGH);  // Movement turns the LED on
      //Use of the drive function which takes as arguements the speed
      //and optional duration.  A negative speed will cause it to go
      //backwards.  Speed can be from -255 to 255.  Also use of the
      //brake function which takes no arguements.
      motor2.drive(255);
    } else if (rMotorState == 'r') {
      Serial.println("right ");
      digitalWrite(led, HIGH);  // Movement turns the LED on
      //Use of the drive function which takes as arguements the speed
      //and optional duration.  A negative speed will cause it to go
      //backwards.  Speed can be from -255 to 255.  Also use of the
      //brake function which takes no arguements.
      motor2.drive(-255);
    } else if (rMotorState == 's') {
      digitalWrite(led, LOW);  // GET /s turns the LED off
      motor2.brake();          // Stops the moter
    }
  }
}
void rMotor(int dir, int state) {
  // for (int x = 0; x <= 255; x++) {
  Serial.println("FFFFFFFFF");
  Serial.println(dir);
  analogWrite(dir, 255);
}
void printWiFiStatus() {
  // print the SSID of the network you're attached to:
  Serial.print("SSID: ");
  Serial.println(WiFi.SSID());
  // print your WiFi shield's IP address:
  IPAddress ip = WiFi.localIP();
  Serial.print("IP Address: ");
  Serial.println(ip);
  // print where to go in a browser:
  Serial.print("To see this page in action, open a browser to http://");
  Serial.println(ip);
}