# 🧪 Robust Analysis of UV-Enhanced Potentiometric Sensor Output Using AI Tools

This repository contains the complete code and documentation for my Final Year Project (FYP) submitted to the Department of Mechatronics Engineering, IIUM.

> **Title:** Robust Analysis of UV-Enhanced Potentiometric Sensor Output Using AI Tools  
> **Author:** Muhammad Haziq Haikal bin Suaib  
> **Supervisor:** Dr. Marmeezee bin Mohd Yusoff  
> **University:** International Islamic University Malaysia  
> **Date:** June 2025

---

## 📌 Project Summary

This project explores a novel approach for classifying the quality of **stingless bee honey** using a **UV-enhanced TiO₂ potentiometric sensor** and **machine learning**.

- A **custom-built measurement system** using Arduino and signal conditioning techniques is used to measure voltage responses of honey samples.
- A **Decision Tree Classifier (DTC)** is trained on the sensor data to classify honey into three categories:
  - **Good**
  - **Medium**
  - **Poor**

This work demonstrates a **low-cost, portable, and robust alternative** to conventional lab-based honey adulteration tests.

---

## 🚀 Features

- 🧪 TiO₂ UV potentiometric sensor fabricated and tested
- 📊 Voltage output correlates with honey adulteration level
- 🔧 Signal conditioning: Analog amplification (LM741) + Digital filtering (SMA)
- 🤖 Accurate ML classification using Decision Tree Classifier (100% test accuracy)
- 💡 Designed for portability and real-time use

---

## 🖥️ Requirements

- UV-enhanced potentiometric sensor
- Arduino Uno
- LM741 Operational Amplifier (non-inverting configuration)
- 2x16 I2C LCD Display
- UV Flashlight (395–410 nm)
- Multimeter
- Breadboard, resistors, jumper wires

---

## 📈 Results Summary

- Sensor output voltage increases with increasing adulteration
- Decision Tree Classifier achieved 100% accuracy on test data
- Clear and interpretable decision rules based on voltage and adulterant type
- System shows strong potential for on-site honey quality testing

---

## 📦 Future Improvements
- Expand dataset with different honey types and real-world samples
- Test with other ML models (Random Forest, SVM, ANN)
- Integrate full system into a compact, battery-powered portable device
- Improve wiring and design an enclosure for field use
