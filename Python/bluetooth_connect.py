import bluetooth, subprocess

# nearby_devices = bluetooth.discover_devices(lookup_names = True, flush_cache = True)
# [print(device) for device in nearby_devices]

print(bluetooth.RFCOMM)
# for address in nearby_devices:
#     print(address, bluetooth.lookup_name(address))

addr = '80:01:84:88:98:3B'      # Device Address
port = 1         # RFCOMM port

# Now, connect in the same way as always with PyBlueZ
s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
s.connect((addr,port))