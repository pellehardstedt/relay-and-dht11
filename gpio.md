### Instructions for Connecting Relay and DHT11 to Raspberry Pi GPIO

#### 1. Connecting the Relay to GPIO

1. **Identify the Relay Pins:**
    - **VCC**: Power supply pin (usually 5V or 3.3V).
    - **GND**: Ground pin.
    - **IN**: Control signal pin.

2. **Connect the Relay to the Raspberry Pi:**
    - **VCC**: Connect to the 5V pin on the Raspberry Pi (Pin 2 or Pin 4).
    - **GND**: Connect to a ground pin on the Raspberry Pi (Pin 6, Pin 9, Pin 14, etc.).
    - **IN**: Connect to a GPIO pin on the Raspberry Pi (e.g., GPIO17, which is Pin 11).

#### 2. Connecting the DHT11 to GPIO

1. **Identify the DHT11 Pins:**
    - **VCC**: Power supply pin (usually 3.3V or 5V).
    - **GND**: Ground pin.
    - **DATA**: Data signal pin.

2. **Connect the DHT11 to the Raspberry Pi:**
    - **VCC**: Connect to the 3.3V pin on the Raspberry Pi (Pin 1 or Pin 17).
    - **GND**: Connect to a ground pin on the Raspberry Pi (Pin 6, Pin 9, Pin 14, etc.).
    - **DATA**: Connect to a GPIO pin on the Raspberry Pi (e.g., GPIO4, which is Pin 7).

#### GPIO Pinout Reference

 3.3V  (1) (2)  5V
 GPIO2 (3) (4)  5V
 GPIO3 (5) (6)  GND
 GPIO4 (7) (8)  GPIO14
   GND (9) (10) GPIO15
 GPIO17(11) (12) GPIO18
 GPIO27(13) (14) GND
 GPIO22(15) (16) GPIO23
 3.3V (17) (18) GPIO24
 GPIO10(19) (20) GND
 GPIO9 (21) (22) GPIO25
 GPIO11(23) (24) GPIO8
   GND (25) (26) GPIO7
   
#### Example Wiring

- **Relay:**
  - VCC to Pin 2 (5V)
  - GND to Pin 6 (GND)
  - IN to Pin 11 (GPIO17)

- **DHT11:**
  - VCC to Pin 1 (3.3V)
  - GND to Pin 9 (GND)
  - DATA to Pin 7 (GPIO4)

By following these instructions, you can connect the relay and DHT11 sensor to the GPIO pins on your Raspberry Pi.