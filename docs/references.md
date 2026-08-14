# References

## Research Papers & Resources

### IoT & Edge Computing
- "Fog Computing vs Edge Computing - Comprehensive Overview" (IJCTT)
- "Machine Learning on the Edge: A Survey" (IEEE IoT Journal)
- TensorFlow Lite Microcontrollers: https://www.tensorflow.org/lite/microcontrollers

### Anomaly Detection
- "Isolation Forest for Anomaly Detection" (Liu et al., 2008)
- "Online Anomaly Detection with Concept Drift" (IEEE IoT)
- Scikit-learn Anomaly Detection Algorithms

### Security & Authentication
- MQTT Security Best Practices: https://mqtt.org/mqtt-security
- "A Study of Authentication for IoT Systems" (ACM)
- JWT (JSON Web Tokens): https://jwt.io/

### Electric Fence Technology
- IEEE Standards for Electrical Fencing: IEEE 1048-2003
- "Safety Standards for Livestock Electric Fencing" (ASAE)
- Electromagnetic Compatibility in Agricultural Equipment

---

## Technical Documentation

### Hardware
- **ESP32 Datasheet**: https://www.espressif.com/sites/default/files/documentation/esp32_datasheet_en.pdf
- **INA219 Datasheet**: https://www.ti.com/lit/ds/symlink/ina219.pdf
- **DS18B20 Temperature Sensor**: https://datasheets.maximintegrated.com/en/ds/DS18B20.pdf

### Firmware Development
- Arduino IDE: https://www.arduino.cc/en/software
- ESP-IDF (Espressif IoT Development Framework): https://docs.espressif.com/projects/esp-idf/
- FreeRTOS Documentation: https://www.freertos.org/

### Machine Learning
- TensorFlow Lite: https://www.tensorflow.org/lite
- Scikit-learn User Guide: https://scikit-learn.org/stable/user_guide.html
- Python for IoT: "Making Things Smart" by Hafiz (Packt)

### Backend & Database
- MongoDB Official Documentation: https://docs.mongodb.com/
- Express.js Guide: https://expressjs.com/
- MQTT Protocol Specification: https://mqtt.org/mqtt-specification

### Frontend
- React Official Documentation: https://react.dev/
- Socket.io Documentation: https://socket.io/docs/
- Chart.js Guide: https://www.chartjs.org/docs/latest/

---

## Tools & Software

### Open Source
- **Arduino IDE**: Free, IDE for microcontroller programming
- **VS Code**: Free, lightweight code editor
- **Python**: Free, interpreted language for ML/scripts
- **Git/GitHub**: Free, version control and collaboration
- **MongoDB Community**: Free, document database

### Paid/Subscription (Optional)
- **GitHub Copilot**: $10/month (AI-assisted coding)
- **MongoDB Atlas Premium**: Based on usage (cloud database)
- **AWS/DigitalOcean**: Pay-as-you-go hosting

---

## Learning Resources

### YouTube Channels
- "Edureka IoT Tutorial": Comprehensive IoT fundamentals
- "Andreas Spiess IoT": Practical ESP32 projects
- "Tech Explorations": Arduino & embedded systems
- "Paul McWhorter IoT": ML and Arduino integration

### Online Courses
- Coursera: "IoT Specialization" (UC San Diego)
- Udemy: "The Complete Hands-On Introduction to Apache Kafka"
- edX: "Introduction to Internet of Things (IoT)" (Curtin)

### Documentation Sites
- **GitHub Docs**: https://docs.github.com/
- **Medium.com**: Technical articles and tutorials
- **Stack Overflow**: Q&A for coding issues
- **Hackster.io**: IoT project inspiration

---

## Community & Support

### Forums
- **Arduino Forum**: https://forum.arduino.cc/
- **ESP32 Forum**: https://www.esp32.com/
- **Stack Overflow**: Search with tags [esp32], [tensorflow-lite], [iot]

### GitHub
- **Awesome IoT**: https://github.com/topics/iot
- **Awesome Machine Learning**: https://github.com/topics/machine-learning
- **Open Source Projects**: Search for similar implementations

### Social Media
- **Twitter/X**: Follow @espressif, @Arduino, @TensorFlow
- **LinkedIn**: Join IoT, Embedded Systems, ML communities
- **Discord Servers**: Tech communities for quick questions

---

## Regulatory & Standards

### Electrical Safety
- **IEC 61010-1**: Safety requirements for measuring equipment
- **IEC 60950-1**: Safety of information technology equipment
- **National Electrical Code (NEC)**: US electrical standards

### Data Protection
- **GDPR**: General Data Protection Regulation (EU)
- **CCPA**: California Consumer Privacy Act (USA)
- **ISO 27001**: Information security management

### IoT Certifications
- **CE Mark**: European conformity
- **FCC Certification**: USA electromagnetic compliance
- **RoHS**: Restriction of Hazardous Substances (EU)

---

## Benchmarks & Comparisons

### Performance Metrics
- ESP32 Performance: 240 MHz dual-core, ~80mW average
- INA219 Accuracy: ±0.5% at calibration, ±1% range
- TensorFlow Lite Latency: <50ms for 100K model inference
- MQTT Publish Latency: <100ms (LAN), <500ms (WAN)

### Similar Projects
- "IoT-based Perimeter Security System" (Hackster.io)
- "Smart Fence Monitoring with Arduino" (GitHub)
- "Real-time Anomaly Detection on Edge" (Research paper)

---

## Legal & Compliance

### Intellectual Property
- Open-source licensing: MIT, Apache 2.0, GPL
- Patent search: https://patents.google.com/
- Trademark: https://www.wipo.int/ (WIPO)

### Competitions & Funding
- **Smart India Hackathon (SIH)**: https://www.sih.gov.in/
- **AWS Startup Grant**: Cloud credits for startups
- **GitHub Student Developer Pack**: Free tools for students

---

## Version Control

### Git Workflow
```
Main branch: Production-ready code
├─ Develop branch: Integration branch
│  ├─ feature/esp32-calibration
│  ├─ feature/ml-model-v2
│  ├─ bugfix/relay-timing
│  └─ docs/system-architecture
└─ Release branch: Pre-production testing
```

### Commit Message Standard
```
format: <type>(<scope>): <subject>
<body>
<footer>

Example:
feat(firmware): implement INA219 current reading
- Added I2C initialization
- Calibrated INA219 for ±3.2A range
Fixes #42
```

---

## Glossary

| Term | Definition |
|------|-----------|
| **ADC** | Analog-to-Digital Converter |
| **BLE** | Bluetooth Low Energy |
| **MQTT** | Message Queuing Telemetry Transport |
| **OTA** | Over-The-Air (firmware updates) |
| **RMS** | Root Mean Square (AC current) |
| **TLS** | Transport Layer Security |
| **WiFi** | Wireless Fidelity (802.11) |
| **JSON** | JavaScript Object Notation |
| **REST** | Representational State Transfer |
| **ML** | Machine Learning |

---

## Acknowledgments

This project was developed as part of:
- **Smart India Hackathon 2026**
- **Supported by**: Ministry of Education, National Mission on Education through ICT

---

## Contact & Support

- **GitHub Issues**: Report bugs and feature requests
- **Discussions**: Ask questions and share ideas
- **Email**: [Team contact]
- **LinkedIn**: [Team profiles]

---

**Last Updated**: 14 August 2026
**Status**: Documentation v1.0
**Contributors**: FENCEGUARD-X Team
