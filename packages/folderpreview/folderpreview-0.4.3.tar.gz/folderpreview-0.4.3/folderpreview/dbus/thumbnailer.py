
import itertools

import asyncio

from dbus_next.constants import BusType
from .message_bus import MessageBus

from folderpreview import LogicException

class Thumbnailer():

	BUS = 'org.freedesktop.thumbnails.Thumbnailer1'
	PATH = '/org/freedesktop/thumbnails/Thumbnailer1'
	INTERFACE = 'org.freedesktop.thumbnails.Thumbnailer1'

	SCH_BACKGROUND = 'background'
	SCH_DEFAULT = 'default'

	def __init__(self):
		self._loop = None

		self._bus = None
		self._object = None
		self._interface = None

		self._supported = None
		self._schedulers = None
		self._flavors = None

		self._loop = asyncio.get_event_loop()

	def sync_queue_wait(self, uris, mimes, flavor, timeout):
		return self._loop.run_until_complete(
			self.queue_wait(uris, mimes, flavor, timeout)
		)

	async def queue_wait(self, uris, mimes, flavor, timeout):
		handle = None

		interface = await self._get_interface()
		finished = self._loop.create_future()
		finished_handles = []
		def on_finished(finished_handle):
			finished_handles.append(finished_handle)
			if (handle in finished_handles):
				finished.set_result(True)
				interface.off_finished(on_finished)

		interface.on_finished(on_finished)

		handle = await self.queue(uris, mimes, flavor)

		if (handle not in finished_handles):
			await self._wait(finished, timeout)

	async def queue(self, uris, mimes, flavor):
		interface = await self._get_interface()
		scheduler = await self.get_scheduler()
		result = await interface.call_queue(
			list(uris), list(mimes), flavor, scheduler, 0
		)

		return result

	def sync_get_supported(self):
		return self._loop.run_until_complete(
			self.get_supported()
		)

	async def get_supported(self):
		if (not self._supported):
			interface = await self._get_interface()
			self._supported = set(itertools.chain(*(
				await interface.call_get_supported()
			)))

		return self._supported

	async def get_scheduler(self):
		schedulers = await self.get_schedulers()

		return self.SCH_BACKGROUND in schedulers\
			and self.SCH_BACKGROUND\
			or self.SCH_DEFAULT

	async def get_schedulers(self):
		if (not self._schedulers):
			interface = await self._get_interface()
			self._schedulers = await interface.call_get_schedulers()

		return self._schedulers

	def sync_get_flavors(self):
		return self._loop.run_until_complete(
			self.get_flavors()
		)

	async def get_flavors(self):
		if (not self._flavors):
			interface = await self._get_interface()
			self._flavors = await interface.call_get_flavors()

		return self._flavors

	async def _wait(self, future, timeout):
		scheduler = await self.get_scheduler()
		if (scheduler == self.SCH_BACKGROUND):
			await asyncio.wait(
				[future],
				loop = self._loop,
				timeout = timeout
			)
		else:
			raise LogicException('Wait for child thumbs')

	async def _get_interface(self):
		if (not self._interface):
			obj = await self._get_object()
			self._interface = obj.get_interface(
				self.__class__.INTERFACE
			)

		return self._interface

	async def _get_object(self):
		if (not self._object):
			_bus = await self._get_bus()
			self._object = await _bus.get_proxy_object(
				self.__class__.BUS,
				self.__class__.PATH
			)

		return self._object

	async def _get_bus(self):
		if (not self._bus):
			self._bus = await MessageBus(
				bus_type = BusType.SESSION
			)\
				.connect()

		return self._bus

