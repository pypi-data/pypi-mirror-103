from amxtelnet import Telnet
from datetime import datetime
import asyncio
from logging import basicConfig, critical, debug, info, warning, error, INFO, DEBUG, WARNING, ERROR, CRITICAL
import re
from amxtoexcel import create_xlsx


class CameraConnect:

	def __init__(self) -> None:
		self.scanned_cameras = []
		self.response_log = []
		self.requests = [
			'network settings get',
			'streaming settings get',
			'version',
			'camera tilt get',
		]


	def set_cameras(self, cameras):
		self.cameras = cameras
		info(f"added {len(self.cameras)} cameras")


	def config(self,
		user_name, password,
		write_results=True, output_path='./output_path/',
		log_replies=True,
			):
		self.user_name = user_name
		self.password = password
		self.write_results = write_results
		self.output_path = output_path
		return


	def set_requests(self, *requests):
		"""
		Requests already being sent:
			'network settings get',
			'streaming settings get',
			'version',
			'camera tilt get',
		"""
		for request in requests:
			self.requests.append(request)
		info(f"requests = {requests}")
		return


	def _write_to_file(self, camera, telnet_text):
		from os import mkdir, path
		# write each telnet rx to individual .txt file
		try:
			mkdir(self.output_path)
			info(f'pingcameras.py created {self.output_path}')
		except Exception as e:
			debug(f"{self.output_path} already exists")

		header = f"{datetime.now()}\n{camera['room']}\nip_address={camera['ip_address']}\nfailed_attempts={camera['failed_attempts']}\nlogin_failure={camera['login_failure']}\n"

		file_path = f"{self.output_path}Vaddio {camera['room']} telnet.txt"
		with open(file_path, 'w+') as f:
			debug(f'pingcameras.py created {file_path}')
			f.write(header + telnet_text)


	async def _poll_camera(self, tn):
		for request in self.requests:
			tn.write(f"{request}\r\n".encode())
			await asyncio.sleep(0)
		return tn


	async def _telnet_camera_login(self, tn, camera):
		if not self.user_name:
			error('user_name was not provided')
			camera['login_failure'] = 'user_name not provided'
			return camera

		if not self.password:
			error('password was not provided')
			camera['login_failure'] = 'password not provided'
			return camera

		camera['camera_user'] = self.user_name
		camera['camera_password'] = self.password
		# create ['failed_attempts'] if it doesn't exist
		try:
			camera['failed_attempts']
		except KeyError:
			camera['failed_attempts'] = 0

		# attempt to login
		tn.write(f"{self.user_name}\r\n".encode())
		tn.read_until(b'\r\nPassword: ')
		tn.write(f"{self.password}\r\n".encode())
		login_result = tn.read_until(b'Welcome admin\r\n> ', timeout=2)

		# login successful, throw back to _telnet_scan_camera() to send commands
		if 'Welcome admin' in login_result.decode():
			camera['login_failure'] = None
			debug(f"{camera['ip_address']} login success")
			return camera

		# login failed, throw back to _telnet_scan_camera() to try the default login
		elif 'Login incorrect' in login_result.decode():
			camera['camera_failed_credentials'] = f"{camera['camera_user']} {camera['camera_password']}"
			camera['login_failure'] = 'invalid login'
			camera['failed_attempts'] += 1
			return camera


	async def _telnet_scan_camera(self, camera):
		try:
			camera['room']
		except KeyError:
			camera['room'] = 'room unknown'
		debug(f"connecting to {camera['room']} - {camera['ip_address']}")

		# avoid key errors later on
		camera['camera_telnet_failure'] = None
		camera['login_failure'] = None

		try:
			with Telnet(camera['ip_address'], timeout=5) as tn:
				telnet_text = ""

				# keep attempting login until success, unknown login, or timeout
				tn.read_until(b'login:')
				camera = await self._telnet_camera_login(tn, camera)

				# check login results
				while True:
					# success
					if camera['login_failure'] is None:
						tn = await self._poll_camera(tn)

						# send 'exit'
						tn.write(b"exit\r\n")
						telnet_text = tn.read_all().decode('ascii')
						break

					# move on to the next camera
					else:
						error(f"""Unable to login to {camera['ip_address']}
								after {camera['failed_attempts']} failed attempts""")
						tn.close()
						telnet_text = ''
						break
				
				if self.write_results: self._write_to_file(camera, telnet_text)
				debug(f"**** {camera['ip_address']} ****\n{telnet_text}\n")

		except Exception as e:
			if camera is not None:
				warning(f"{camera['room']} - {camera['ip_address']} {e}")
				camera['failed_attempts'] = 1
				camera['login_failure'] = e
				telnet_text = ''
				if self.write_results: self._write_to_file(camera, telnet_text)
			else: error(f"pingcameras.py: _telnet_scan_camera() no camera: {camera} {e}")

		self.scanned_cameras.append(camera)
		return


	async def _gather_connections(self, cameras, simultaneous=65535):
		tasks = []
		skip_remainder = True
		camera_count = len(cameras)
		if camera_count <= simultaneous: simultaneous = camera_count
		else: skip_remainder = False
		camera_chunks = int(camera_count / simultaneous)
		camera_remainder = camera_count % simultaneous

		for i in range(camera_chunks):
			tasks = []
			scan_start = (i * simultaneous)
			scan_end = (scan_start + simultaneous)
			for x in range(scan_start, scan_start + simultaneous):
				tasks.append(self._telnet_scan_camera(cameras[x]))
			await asyncio.gather(*tasks)

		# remainder
		if not skip_remainder:
			tasks = []
			scan_start = camera_chunks * simultaneous
			scan_end = camera_chunks * simultaneous + camera_remainder
			for i in range(scan_start, scan_end):
				tasks.append(self._telnet_scan_camera(cameras[i]))
			await asyncio.gather(*tasks)
		return


	async def run(self):
		import time
		# scan time begins to increase when simultaneous is set to 50 or lower
		start = time.perf_counter()
		await(self._gather_connections(self.cameras))
		elapsed = time.perf_counter() - start
		info(f"pingcameras.py CameraConnect() complete in {elapsed:0.2f} seconds\n")
		# 'Vaddio ~ip_address',~ telnet.txt' was created for every room
		return


class ParseCameraResponse:
	def __init__(self, input_path, excel_path='camera_rooms.xlsx'):
		self.excel_path = excel_path
		if input_path:
			self.input_path = input_path
		else:
			critical('pingcameras.py ParseCameraResponse must be initialized with input_path')
			assert FileNotFoundError


	def __repr__(self) -> str:
		asyncio.run(self.run())


	async def _parse_telnet(self, data_in, telnet_camera):
		re_list = [
			# the order used here will be the order of excel columns later...
			r'(?<=Hostname        )(?P<room>[\w]+)',
			r'(?<=Hostname        )(?P<hostname>[\w-]+)',
			r'(?<=IP Address      )(?P<ip_address>[\d.]+)',
			r'(?<=Netmask         )(?P<subnet>[\d.]+)',
			r'(?<=Gateway         )(?P<gateway>[\d.]+)',
			r'(?<=VLAN            )(?P<vlan>[\w.]+)',
			r'(?<=MAC Address     )(?P<mac_address>[\w:-]+)',
			r'(?<=System Version      )(?P<firmware>[\w\s.]+)',
			r'(?<=0m)(?P<tilt_angle>[\d.-]+)',
			r'(?<=IP Enabled            )(?P<stream_enabled>[\w]+)',
			r'(?<=IP Protocol           )(?P<stream_protocol>[\w]+)',
			r'(?<=IP URL                )(?P<stream_url>[\w-]+)',
			r'(?<=IP Video_Mode         )(?P<stream_mode>[\w]+)',
			r'(?<=IP Preset_Resolution  )(?P<stream_preset_res>[\w]+)',
			r'(?<=IP Preset_Quality     )(?P<stream_preset_quality>[\w]+)',
			r'(?<=IP Custom_Resolution  )(?P<stream_custom_res>[\w]+)',
			r'(?<=IP Custom_Frame_Rate  )(?P<stream_custom_frames>[\w]+)',
		]

		for item in re_list:
			telnet_camera = await self._re_search(item, data_in, telnet_camera)
		
		try:
			telnet_camera['firmware'] = telnet_camera['firmware'].split('\n')[0]

			if telnet_camera['stream_enabled'].lower() == 'true':

				if telnet_camera['stream_mode'] == 'preset':
					telnet_camera['stream_resolution'] = telnet_camera['stream_preset_res']
					telnet_camera['stream_quality'] = telnet_camera['stream_preset_quality']
				else:
					telnet_camera['stream_resolution'] = telnet_camera['stream_custom_res']
					telnet_camera['stream_quality'] = telnet_camera['stream_custom_frames']

				telnet_camera['stream_address'] = f"{telnet_camera['stream_protocol'].lower()}://{telnet_camera['ip_address']}/{telnet_camera['stream_url']}"
			
			else: telnet_camera['stream_address'] = 'disabled'

			del telnet_camera['stream_enabled']
			del telnet_camera['stream_protocol']
			del telnet_camera['stream_url']
			del telnet_camera['stream_mode']
			del telnet_camera['stream_preset_res']
			del telnet_camera['stream_preset_quality']
			del telnet_camera['stream_custom_res']
			del telnet_camera['stream_custom_frames']

		except KeyError as e:
			# unresponsive camera
			warning(f"Camera {telnet_camera['full_name']} {e}. Check for Telnet communication errors.")
			pass

		return telnet_camera


	async def _re_search(self, _re, data_in, telnet_camera):
		if re.search(_re, data_in) is not None:
			telnet_camera = {**telnet_camera, **re.search(_re, data_in).groupdict()}
		return telnet_camera


	async def run(self) -> list:
		from os import scandir
		telnet_info = []

		with scandir(self.input_path) as file_list:
			for file in file_list:
				telnet_camera = {'room':file.name.split(' ')[1]}
				with open(file, 'r') as f:
					file_text = f.read()
					telnet_camera = await self._parse_telnet(file_text, telnet_camera)
				telnet_info.append(telnet_camera)
				debug(f"ParseCameraResponse parsed :\n{telnet_camera}\n")
		
		create_xlsx(telnet_info,path='camera_rooms.xlsx',primary_column_name='room')
		
		return telnet_info


def __test__():
	basicConfig(
		level=INFO,
		filename=f'{datetime.now().replace(microsecond=0)} cameras.log',
		# encoding='utf-8',
		filemode='w',
		format='%(levelname)s %(asctime)s: %(message)s'
		)

	camera_list = [
		{'ip_address':'192.168.1.1', 'room':'BLDG123'},
		{'ip_address':'192.168.1.2'},
		]

	cameras = CameraConnect()
	cameras.set_cameras(camera_list)
	cameras.config(user_name='username',password='password')
	asyncio.run(cameras.run())

	camera_parse = ParseCameraResponse(input_path=cameras.output_path)
	asyncio.run(camera_parse.run())
	

if __name__ == '__main__':
	__test__()
