#define R1_RED     27
#define R1_YELLOW  14
#define R1_GREEN   12

#define R2_RED     33
#define R2_YELLOW  25
#define R2_GREEN   26

#define R3_RED     5     
#define R3_YELLOW  18    
#define R3_GREEN   19

String inputString = "";
unsigned long yellowDuration = 2000; // 2 seconds yellow before green

void setup() {
  Serial.begin(9600);

  pinMode(R1_RED, OUTPUT);
  pinMode(R1_YELLOW, OUTPUT);
  pinMode(R1_GREEN, OUTPUT);

  pinMode(R2_RED, OUTPUT);
  pinMode(R2_YELLOW, OUTPUT);
  pinMode(R2_GREEN, OUTPUT);

  pinMode(R3_RED, OUTPUT);
  pinMode(R3_YELLOW, OUTPUT);
  pinMode(R3_GREEN, OUTPUT);

  allRed();
}

void loop() {
  if (Serial.available()) {
    inputString = Serial.readStringUntil('\n');
    inputString.trim();

    if (inputString.length() >= 2) {
      int road = inputString.substring(0, 1).toInt();
      int duration = inputString.substring(1).toInt() * 1000;  // seconds to ms

      switch (road) {
        case 1:
          signalRoad(R1_RED, R1_YELLOW, R1_GREEN, duration);
          break;
        case 2:
          signalRoad(R2_RED, R2_YELLOW, R2_GREEN, duration);
          break;
        case 3:
          signalRoad(R3_RED, R3_YELLOW, R3_GREEN, duration);
          break;
      }
    }
  }
}

void allRed() {
  digitalWrite(R1_RED, HIGH); digitalWrite(R1_YELLOW, LOW); digitalWrite(R1_GREEN, LOW);
  digitalWrite(R2_RED, HIGH); digitalWrite(R2_YELLOW, LOW); digitalWrite(R2_GREEN, LOW);
  digitalWrite(R3_RED, HIGH); digitalWrite(R3_YELLOW, LOW); digitalWrite(R3_GREEN, LOW);
}

void signalRoad(int redPin, int yellowPin, int greenPin, unsigned long greenTime) {
  allRed();  // Reset all to red

  // Yellow ON for 2 seconds
  digitalWrite(redPin, LOW);
  digitalWrite(yellowPin, HIGH);
  delay(yellowDuration);
  digitalWrite(yellowPin, LOW);

  // Green ON
  digitalWrite(greenPin, HIGH);
  delay(greenTime);
  digitalWrite(greenPin, LOW);

  // Back to red
  digitalWrite(redPin, HIGH);
}
