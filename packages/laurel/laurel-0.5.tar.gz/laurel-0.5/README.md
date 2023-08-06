Python control of C by GE Bluetooth lightbulbs
==============================================

A simple Python API for controlling [C by GE](https://www.cbyge.com/) lighting devices.

Example use
-----------

Retrieve authentication data from the remote API and automatically create devices:

```
import laurel

connection = laurel.laurel("username", "password")
devices = connection.devices

# Connect to the mesh - if you have multiple devices in a network you can
# connect to any of them

devices[0].network.connect()
```

Show device information:

```
print(devices[0].name)
print(devices[0].id)
print(devices[0].type)
print(devices[0].brightness)
print(devices[0].temperature)
print(devices[0].red)
print(devices[0].green)
print(devices[0].blue)
```

Set the device brightness to 50%:

```
if devices[0].supports_dimming() == True:
  devices[0].set_brightness(50)
```

If the device supports colour temperature setting:

```
if devices[0].supports_temperature() == True:
  devices[0].set_temperature(50)
```

If the device supports RGB:

```
if devices[0].supports_rgb() == True:
  devices[0].set_rgb(128, 255, 0)
```

Turn the device off:

```
devices[0].set_power(False)
```

Force an update of the device state (note that this is asynchronous):

```
devices[0].update_status()
```
