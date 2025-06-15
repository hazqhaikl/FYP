#include <Wire.h>
#include <LiquidCrystal_I2C.h>

// Initialize the LCD.
LiquidCrystal_I2C lcd(0x27, 16, 2);

const int sensorPin = A0; // Analog pin for sensor input

// --- Moving Average Filter Parameters ---
const int FILTER_WINDOW_SIZE = 10; // Number of samples to average (adjust as needed)
int sensorReadings[FILTER_WINDOW_SIZE]; // Array to store raw readings
long runningSum = 0; // Sum of readings in the window
int readIndex = 0; // Index for circular buffer

// --- Variables for voltage conversion and output ---
float rawInputVoltage_mV = 0.0; // Raw input voltage in mV (before MA)
float filteredOutputVoltage_mV = 0.0; // Filtered output voltage in mV (after MA)

void setup() {
  Serial.begin(9600);
  lcd.init();
  lcd.backlight();

  // Initialize the moving average filter's buffer
  for (int i = 0; i < FILTER_WINDOW_SIZE; i++) {
    sensorReadings[i] = 0; // Start with all zeros in the buffer
  }
  runningSum = 0; // Ensure initial sum is zero

  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("System Ready!");
  delay(1500); // Wait a bit to show "System Ready"
}

void loop() {
  // Read the new raw analog value from the sensor
  int newRawReading = analogRead(sensorPin);

  // --- Moving Average Filter Logic ---
  // 1. Subtract the oldest reading from the running sum
  runningSum -= sensorReadings[readIndex];

  // 2. Add the new reading to the running sum
  runningSum += newRawReading;

  // 3. Store the new reading in the array, replacing the oldest one
  sensorReadings[readIndex] = newRawReading;

  // 4. Advance the index for the next iteration, wrapping around
  readIndex = (readIndex + 1) % FILTER_WINDOW_SIZE;

  // Calculate the average of the raw ADC values
  float filteredRawADCValue = (float)runningSum / FILTER_WINDOW_SIZE;

  // Convert the raw (but now filtered) ADC value to voltage in mV
  // (Assuming Arduino's 5V reference and 10-bit ADC)
  filteredOutputVoltage_mV = (filteredRawADCValue * 5.0 / 1023.0) * 1000.0;

  // Optionally, convert the original raw reading to mV as well, if you want to see the raw noise
  rawInputVoltage_mV = (newRawReading * 5.0 / 1023.0) * 1000.0;


  // --- Display on LCD ---
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Voltage Output:");
  lcd.setCursor(4, 1);
  lcd.print(filteredOutputVoltage_mV, 1); // Display filtered voltage with 1 decimal place
  lcd.print(" mV");

  // You can also print the raw voltage to Serial Monitor to compare the effect
  Serial.print("Raw: ");
  Serial.print(rawInputVoltage_mV, 1);
  Serial.print(" mV, Filtered: ");
  Serial.print(filteredOutputVoltage_mV, 1);
  Serial.println(" mV");

  delay(1000); // Delay for reading convenience
}