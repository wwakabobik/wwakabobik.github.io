##########################
Can AI write a fairy tale?
##########################
:date: 2023-07-30 14:22
:author: wwakabobik
:tags: ai, storytelling, openai
:slug: ai_fairy_tale_attempt_1
:category: ai
:status: published
:summary: Are AI ready to tell the stories? At least teenager fairy tale?
:cover: assets/images/bg/ai.png


Problem Statement
=================

So, why bother with a weather station at all? Sure, there are more weather apps and services today than anyone could ever need, complete with local forecasts down to the meter. But apart from checking the outdoor conditions, I need real-time data from temperature and humidity sensors inside my own space. And I’m not just gathering this data for fun. Knowing the indoor and outdoor temperatures means I can control things like the boiler or ventilation system, automating a comfortable indoor climate without lifting a finger—weather-responsive automation at its finest.

On top of that, I want to track weather trends over longer time periods, like one or two years. Meaning, this data needs a place to live—a proper, dedicated storage solution.

From all this, let’s lay down the key requirements:

1. Data Storage: We’ll need a server to hoard all the precious data.
2. Sensor Variety and Modularity: Sensors in different locations, doing different things, so let’s keep it modular (hello, IoT).
3. Cloud Sync: Besides local storage, it’d be nice to throw at least the current readings into the cloud.
4. Data Sharing: We’ll end up with a solid dataset, so why not make it shareable?

Ready? Let's dive into the fun stuff.

Architecture
============

The simplest and most popular setup for a weather station is often Arduino. But getting it to play nice with a home network? That’s going to need additional shields and adapters, meaning extra cash and extra hassle—i.e., wasted time. So instead, I’m going for something with Wi-Fi baked right in: the ESP8266 (NodeMCU) module, paired with various sensors. This little powerhouse works just as well indoors as it does outdoors and can even act as a server if you’re feeling adventurous.

But why stop there? Let’s get some real muscle at the center. Luckily, I’ve got a dust-covered, first-gen Raspberry Pi lying around (though any version would work). The indoor sensors could connect directly to the Pi’s GPIO, but here’s the catch: my Pi and router are conveniently set up in one room, but I need monitoring in another. If you don’t have this setup challenge, congrats—you can cut down on one NodeMCU. For the rest of us, the Pi will receive data from the sensors, store it in a database, and display it on demand. Plus, the Pi can be outfitted with a LoRa receiver, letting it pull data from out-of-range sensors (perfect for those Arduinos). Finally, the Pi will ship all the data to the cloud.

Parts List
----------
Here’s what we’ll need to assemble this dream team:

* Raspberry Pi
* ESP8266 (2 units, +1 optional)
* BME280 (2 units) for temperature, humidity, and pressure
* Real-Time Clock DS1302 (optional)
* 128x64 OLED Display with SH1106 controller (optional)
* Rain Sensor with LM373 comparator (optional)
* UV Sensor GY-VEML6070 (optional)
* Raspberry Pi Camera (optional)
* Arduino Nano (2 units, optional)
* SX1278 LoRa module (3 units, optional)
* Magnetic Compass with QMC5883L or HMC5883L chip (optional)
* Ambient Light Sensor with LM737 comparator (optional)
* Voltage Sensors up to 25V (optional)
* Current Sensors ACS712 (optional)

With all this in hand, we’re ready to construct a networked weather-tracking beast.


Connecting the SX1278 to the Raspberry Pi
=========================================

First, let’s wire up the radio module to the Raspberry Pi.

Pin Connections
---------------

.. list-table::
   :header-rows: 1

   * - Raspberry Pi Pin
     - SX1278 Pin
   * - 3.3V
     - 3.3V
   * - GROUND
     - GROUND
   * - GPIO10
     - MOSI
   * - GPIO9
     - MISO
   * - GPIO11
     - SCK
   * - GPIO8
     - NSS/ENABLE
   * - GPIO4
     - DIO0
   * - GPIO22
     - RST

Connect the pins on your Raspberry Pi to the SX1278 as shown in the diagram.

.. note::
   Different Raspberry Pi revisions can have varying pin layouts, so check the documentation to confirm which pins to use.

A Few Warnings for LoRa Module Setup
------------------------------------

Before powering up the LoRa module, *make sure an antenna is attached*. Neglect this and you could end up with a nice, expensive paperweight if the module burns out.

Signal quality depends not just on the antenna but on correct configurations. Pay attention to matching the frequencies of the transmitter and receiver and keep the frequency range clear of noise (think of it like avoiding the traffic jam caused by kids’ RC cars on the same band).


Setting up the Server
======================

Load **Raspberry Pi OS Lite** onto your Raspberry Pi.

Next, let’s set a static IP address:

.. code-block:: bash

   sudo nano /etc/dhcpcd.conf

Add or edit the lines to set your desired IP address and router IP:

.. code-block:: bash

   interface eth0  # or wlan0 if you’re connecting via Wi-Fi
   static ip_address=192.168.0.4/24
   static routers=192.168.0.1
   static domain_name_servers=192.168.0.1 8.8.8.8

Now, let’s enable remote access options via SSH, SPI (for LoRa), and the Camera module if we’ll be using it:

.. code-block:: bash

   sudo raspi-config

Enable:

- **SSH** (for remote access, unless you’re working with a keyboard attached)
- **SPI** (if using LoRa)
- **Camera** (if using the camera)

Make sure auto-login is set:

- Navigate to `Boot Options -> Console Autologin`

Exit `raspi-config`, then reboot:

.. code-block:: bash

   sudo shutdown -r now

With remote access ready, we can connect to the Pi via SSH or keep working with the keyboard.

Since all server logic is written in Python3, install it:

.. code-block:: bash

   sudo apt-get install python3.7

Now download the project H.O.M.E.:

.. code-block:: bash

   cd ~
   git clone https://github.com/wwakabobik/home.git

I’ve chosen **Flask** as the web server—there’s an excellent series on this on Habr, so I won’t go into the details.

Copy the server content to a new directory:

.. code-block:: bash

   mkdir web-server
   cp -r home/home_server/* /home/pi/web-server/

Install dependencies:

.. code-block:: bash

   cd web-server
   sudo python3.7 -m pip install -r requirements.txt

Create the database from the schema template:

.. code-block:: bash

   cat db/schema.sql | sqlite3 flask_db

Everything’s ready! Launch the server:

.. code-block:: bash

   cd /home/pi/web-server && sudo python3.7 app.py

If you want the server to start on boot, add a script call to **/etc/rc.local** just before `exit 0`:

.. code-block:: bash

   /home/pi/flask_startup.sh &

Copy this startup script into place:

.. code-block:: bash

   cd ~
   cp ~/home/bash/flask_startup.sh .

For added reliability, set up a watchdog script to monitor the server’s status and restart it if it’s down. Copy the health check script:

.. code-block:: bash

   cp ~/home/bash/check_health.sh .

Add it to cron:

.. code-block:: bash

   sudo crontab -e

with the following task:

.. code-block:: bash

   1-59/5 * * * * /home/pi/check_health.sh

Server Software Overview
------------------------

The main server file is **app.py**:

.. code-block:: python

   #!/usr/bin/env python3.7

   from multiprocessing.pool import ThreadPool
   from flask import Flask
   from db.db import init_app
   from lora_receiver import run_lora

   app = Flask(__name__, template_folder='templates')

   # import all routes
   import routes.api
   import routes.pages
   import routes.single_page

   if __name__ == '__main__':
       # Start LoRa receiver as subprocess
       pool = ThreadPool(processes=1)
       pool.apply_async(run_lora)
       # Start Flask server
       init_app(app)
       app.run(debug=True, host='0.0.0.0', port='80')
       # Teardown
       pool.terminate()
       pool.join()

In addition to launching the server, this script starts the LoRa receiver as a subprocess to gather sensor data and forward it to the server.

The rest of the architecture is classic Flask. All routes are organized into separate files, static content (like images) is in **static**, templates are in **templates**, and database logic is stored in **db**. Any camera images will be stored in **camera**.

Finally, current readings can be viewed on the dashboard pages, while graphs and data (rendered with Plotly) are available on separate pages.

LoRa Receiver Software
======================

The LoRa receiver's logic is implemented in **home_server/lora_receiver.py**.

.. code-block:: python

   from time import sleep
   import requests
   from SX127x.LoRa import *
   from SX127x.board_config import BOARD

   endpoint = "http://0.0.0.0:80/api/v1"

   class LoRaRcvCont(LoRa):
       def __init__(self, verbose=False):
           super(LoRaRcvCont, self).__init__(verbose)
           self.set_mode(MODE.SLEEP)
           self.set_dio_mapping([0] * 6)

       def start(self):
           self.reset_ptr_rx()
           self.set_mode(MODE.RXCONT)
           while True:
               sleep(.5)
               rssi_value = self.get_rssi_value()
               status = self.get_modem_status()
               sys.stdout.flush()

       def on_rx_done(self):
           self.clear_irq_flags(RxDone=1)
           payload = self.read_payload(nocheck=True)
           formatted_payload = bytes(payload).decode("utf-8", 'ignore')
           status = self.send_to_home(formatted_payload)
           if status:
               sleep(1)  # got data, let’s nap to skip repeats
           self.set_mode(MODE.SLEEP)
           self.reset_ptr_rx()
           self.set_mode(MODE.RXCONT)

       def send_to_home(self, payload):
           if str(payload[:2]) == '0,':
               requests.post(url=f'{endpoint}/add_wind_data', json={'data': payload})
           elif str(payload[:2]) == '1,':
               requests.post(url=f'{endpoint}/add_power_data', json={'data': payload})
           else:
               print("Garbage collected, ignoring")  # debug
               status = 1
           return status

   def run_lora():
       BOARD.setup()
       lora = LoRaRcvCont(verbose=False)
       lora.set_mode(MODE.STDBY)
       lora.set_pa_config(pa_select=1)
       assert (lora.get_agc_auto_on() == 1)

       try:
           lora.start()
       finally:
           lora.set_mode(MODE.SLEEP)
           BOARD.teardown()

Here, the main event is in `on_rx_done`, where we receive and decode packets. In `send_to_home`, if the first two characters of `payload` match our sensor code (`"0,"` for wind data or `"1,"` for power data), it’s sent to the server, and we sleep to skip repeated packets.

API
---

The server spends 99% of its time just idling, but for that precious 1%, it handles incoming and outgoing data via an API.

Using Flask’s REST API, we’ll receive and send data from sensors.

**home_server/routes/api.py**

.. code-block:: python

   @app.route('/api/v1/send_data')
   def send_weather_data():
       return send_data()

   @app.route('/api/v1/add_weather_data', methods=['POST'])
   def store_weather_data():
       if not request.json:
           abort(400)
       timestamp = str(datetime.now())
       unix_timestamp = int(time())
       data = request.json.get('data', "")
       db_data = f'"{timestamp}", {unix_timestamp}, {data}'
       store_weather_data(db_data)
       return jsonify({'data': db_data}), 201

In our case, receiving sensor data involves handling a POST request containing JSON, which we then store in the database. On a GET request (via `send_data`), we send data to the cloud.

**home_server/pages/weather_station/send_data.py**

.. code-block:: python

   def send_data():
       data = get_last_measurement_pack('0', '1')
       image = take_photo()
       wu_data = prepare_wu_format(data=data)
       response = str(send_data_to_wu(wu_data))
       response += str(send_data_to_pwsw(wu_data))
       response += str(send_data_to_ow(data))
       response += str(send_data_to_nardmon(data))
       send_image_to_wu(image)
       copyfile(image, f'{getcwd()}/camera/image.jpg')
       return response

Ah yes, the camera. If we have a camera attached to the Raspberry Pi, we can also send or save images of the weather outside. The function below handles that.

**home_server/pages/shared/tools.py**

.. code-block:: python

   from picamera import PiCamera
   <...>
   camera = PiCamera()
   <...>

   def take_photo():
       camera.resolution = (1280, 720)  # lower resolution to fit in limits
       camera.start_preview()
       sleep(5)
       image = f'{getcwd()}/camera/image_{int(time())}.jpg'
       camera.capture(image)
       camera.stop_preview()
       return image

In this setup, current readings are viewable on the dashboard, and historical data is available in graph form (courtesy of Plotly).


.. image:: /assets/images/articles/ai/fairy_tale_attempt_1/instructions_1.png
   :alt: initial ChatGPT instructions



.. pull-quote::
  Epilogue: The Tragic Separation

