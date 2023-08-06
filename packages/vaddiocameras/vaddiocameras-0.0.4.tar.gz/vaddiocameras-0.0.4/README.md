# vaddiocameras
Connect to Vaddio cameras over Telnet and retreive information.
Telnet must be enabled in the camera's web GUI -> Security.


## CameraConnect():
init with no parameters
### set_cameras(cameras):
List of dicts, with each dict being a separate camera.
Requires 'ip_address':'nnn.nnn.nnn.nnn; in the dict.
Any additional keys will be accepted but are not required.
Including 'room':'room_name' is recommended.
['room'] will also be parsed from the camera's hostname if the
naming convention is room-whatever, eg. ABC123-VADDIO

### config(user_name, password, write_results, output_path):
#### user_name: name used when vaddio security was initially setup
#### password: password to use with user_name
#### output_path: dir to store telnet data is write_results is True.
#### write_results: default True. Write telnet data to 'output_path/Vaddio room telnet.txt'.
If you're going to be using ParseCameraResponse(), you must set write_results to True.

### set_requests(requests):
Accepts a list of ASCII requests to send via telnet.
Requests that are already going to be sent:
'network settings get',
'streaming settings get',
'version',
'camera tilt get',
Any requests you provide will be appended to this list.
Tilt is polled because a reply of '0' probably means the camera has rebooted at some
point and is now sitting in the factory Home position.

### run():
Called by gathering run() to an asyncio queue, or by using
asyncio.run(instance_name.run())
Begins Telnetting into the cameras provided, sending requests, and writing the
results to file if desired. If you're going to be using ParseCameraResponse(), you
must set write_results to True.

## ParseCameraResponse()
#### input_path: dir containing the 'Vaddio room telnet.txt' files created by CameraConnect(). Try using input_path=camera_connect_instance.output_path if you're Telnetting and parsing in the same program.
#### excel_path: default 'camera_rooms.xlsx'. Filename used when exporting camera information.

### run():
Called by gathering run() to an asyncio queue, or by using
asyncio.run(instance_name.run())
Begins parsing information from the files located in input_path, then creates an Excel table with all of the camera data. Also returns the camera data as a list of dicts.

