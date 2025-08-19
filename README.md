# e-ink-screen

This project uses a Raspberry Pi to drive a Waveshare e-ink screen.

## Getting Started

The first step is to enable both SPI and I2C. I'm not entirely sure why I2C was needed for my device, but it would *not* work without it when using Python.

Open a terminal and enter the following command to bring up the Raspberry Pi config:

```bash
sudo raspi-config
```

From there, go to **Interfacing Options** -> **SPI** -> **Yes**. This will enable SPI.

Next, go to **Interfacing Options** -> **I2C** -> **Yes**. This will enable I2C.

After enabling both of these, it is necessary to reboot the Raspberry Pi:

```bash
sudo reboot now
```

### Python

This project is written in Python. There is also a C library for the Waveshare screen.

We first need to install pip using your method of choice.

I used the [get-pip.py script](https://pip.pypa.io/en/stable/installation/):

```bash
wget https://bootstrap.pypa.io/get-pip.py
python get-pip.py
```

After pip is installed, run the following command to install the required libraries from the root of this repository:

```bash
pip -r requirements.txt
```

### Waveshare e-Paper Library

Once our initial setup is complete, we can download the Waveshare e-Paper Library. This is what actually allows us to interface with the e-ink displays.

Check out the repository from Github:

```bash
git clone https://github.com/waveshareteam/e-Paper/tree/master
```

Alternatively download the files directly from Waveshare:

```bash
wget https://files.waveshare.com/wiki/common/E-Paper_code.zip
unzip E-Paper_code.zip -d e-Paper
```

Now navigate to the `e-Paper/RaspberryPi_JetsonNano/python/examples` directory.

### Hardware Setup

> [!NOTE]
> If your display is a HAT you can disregard most of this section. In that case you can simply make sure you have the correct orientation and plug it directly into the GPIO header.

We're now ready to hook up the e-ink display to the Raspberry Pi. Familiarize yourself with the GPIO pinouts before attempting this. For added safety, you can turn off your Pi before doing this to make sure any accidental pin configuration won't fry your screen, and allow you to double check everything before turning everything back on.

The pin connection should be as follows:

| RPi Pin Name | RPi GPIO (Physical Pin)      | e-Paper Pin | Notes                                          |
| ------------ | ---------------------------- | ----------- | ---------------------------------------------- |
| 3.3V         | 1 or 17                      | VCC         | **Power supply**, 3.3V only (do not use 5V)    |
| GND          | 6, 9, 14, 20, 25, 30, 34, 39 | GND         | Ground                                         |
| MOSI         | GPIO 10 (19)                 | DIN (MOSI)  | SPI data (This PIN is called SDI on my screen) |
| SCLK         | GPIO 11 (23)                 | CLK (SCK)   | SPI clock                                      |
| CS           | GPIO 8  (24)                 | CS          | Chip Select                                    |
| DC           | GPIO 25 (22)                 | DC          | Data/Command                                   |
| RST          | GPIO 17 (11)                 | RST         | Reset pin                                      |
| BUSY         | GPIO 24 (18)                 | BUSY        | Busy status                                    |

### Testing

It is recommended to run the example scripts for your display before attempting to write things yourself.

These examples are found in the python/examples directory in your Waveshare e-Paper Library installation directory. Be sure to check out the README there to familiarize yourself with how the naming convention is used for each example. Some trial and error may be needed to determine exactly which version you need to use.

### Configuration

TODO

