import asyncio
from logging import debug, info, warning, error


class LogSniffer():

	def __init__(self) -> None:
		pass


	def set_systems(self, systems):
		self.systems = systems


	def config(self,
		output_dir,
		user_name='administrator', password='password',
		log_type='error_log',
		clear_logs=False,
		debug_ftp=0,
		timeout=10
			):
		self.output_dir = output_dir
		self.user_name = user_name
		self.password = password
		self.log = log_type
		self.clear_logs = clear_logs
		self.debug_ftp = debug_ftp
		self.timeout = timeout
		return


	async def _retrieve_logs(self, system):
		from os import mkdir
		import ftplib
		
		# connect ftp
		ftp = ftplib.FTP(
			system['master_ip'],
			user=self.user_name,
			passwd=self.password
			)
		ftp.timeout = 100
		ftp.debugging = self.debug_ftp

		# read top level directory
		try:
			files = ftp.nlst()  # not handling empty dir since we know there's something there
			if len(files) == 0:
				warning(f"files must be manually retrieved from {system['full_name']} (32MB NI-700) ftp://{system['master_ip']}")

			await asyncio.sleep(0)
			# filter
			try:
				for file in files:
					if (self.log == 'error_log' and file.lower().endswith('.log')) or file.endswith(f"{self.log}.txt") or file.endswith(f"{self.log.upper()}.TXT"):
						await asyncio.sleep(0)
						
						filename = f"{self.output_dir}{system['full_name']} {file}"
						try:
							mkdir(f"{self.output_dir}{[self.log]}")
							debug(f"amxlogs.py created {self.output_dir}{[self.log]}")
						except FileExistsError:
							pass
						with open(filename, 'wb+') as f:
							ftp.retrbinary(f"RETR {file}", f.write)
							debug(f"amxlogs.py retrieved {system['full_name']} {file}")
						
						debug(ftp.retrlines('LIST'))

						if self.clear_logs == 'True':
							ftp.delete(file)
							debug(f"amxlogs.py deleted {system['full_name']} {file}")
				ftp.quit()
				return
			except Exception as e:
				error(f"amxlogs.py _retrieve_logs() {self.log} for file in files: {e}")
				ftp.quit()
				return

		except Exception as e:
			error(f"amxlogs.py _retrieve_logs() {system['full_name']} {self.log} {e}")
			return


	async def run(self):
		# filter down to systems with log files
		for system in self.systems:
			if self.log not in system: system[self.log] = False
		filtered_systems = [x for x in self.systems if x[self.log] is True]
		info(f"{self.log} found in {len(filtered_systems)} rooms:")
		for x in filtered_systems:
			info(f"\t{x['full_name']}")

		tasks = []
		for i, _ in enumerate(filtered_systems):
			tasks.append(self._retrieve_logs(filtered_systems[i]))
		await asyncio.gather(*tasks)
		return
