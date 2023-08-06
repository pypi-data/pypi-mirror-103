import asyncio
import aiohttp

BASE_URL = "https://api.tomorrow.io/v4/"


class Tomorrow:
    """Wrapper object for making calls to the tomorrow.io API."""

    def __init__(
        self,
        api_key: str,
        units: str = "imperial",
        latitude: float = 42.028548,
        longitude: float = -93.647507,
    ):
        if units not in ["imperial", "metric"]:
            raise ValueError("Can only provide imperial or metric units")
        self._api_key = api_key
        self.units = units
        self.longitude = longitude
        self.latitude = latitude
        self._session = aiohttp.ClientSession()

    async def get_timeline_async(
        self,
        data_fields=None,
        latitude: float = None,
        longitude: float = None,
        timestep: str = "1h",
        start_time: str = None,
        end_time: str = None,
    ):
        """Gets a timeline, based on the parameters.

        The default behaviour is to get the entirety of the available forecast, in one hour intervals.
        """
        if data_fields is None:
            # Default to the current temperature and general weather condition
            data_fields = ["temperature", "weatherCode"]
        if longitude is None:
            longitude = self.longitude
        if latitude is None:
            latitude = self.latitude
        if timestep not in ["best", "1m", "15m", "30m", "1h", "1d", "current"]:
            raise ValueError(
                'Invalid timestep. Must be one of "best", "1m", "5m", "15m", "30m", "1h", "1d" or "current"'
            )
        params = {
            "location": "{},{}".format(latitude, longitude),
            "fields": data_fields,
            "units": self.units,
            "apikey": self._api_key,
            "startTime": start_time,
            "endTime": end_time,
            "timesteps": timestep,
        }
        async with self._session.get(BASE_URL + "timelines", params=params) as res:
            return await res.json()

    def get_timeline(
        self,
        data_fields=None,
        latitude: float = None,
        longitude: float = None,
        timestep: str = "1h",
        start_time: str = None,
        end_time: str = None,
    ):
        """Synchronous wrapper for async_get_timeline"""
        return asyncio.get_event_loop().run_until_complete(
            (
                self.get_timeline_async(
                    data_fields=data_fields,
                    latitude=latitude,
                    longitude=longitude,
                    timestep=timestep,
                    start_time=start_time,
                    end_time=end_time,
                )
            )
        )

    async def get_current_async(
        self, data_fields=None, latitude: float = None, longitude: float = None
    ):
        """Get the current values."""
        return await self.get_timeline_async(
            data_fields=data_fields,
            latitude=latitude,
            longitude=longitude,
            timestep="current",
        )

    def get_current(
        self, data_fields=None, latitude: float = None, longitude: float = None
    ):
        """Synchronous wrapper for get_current_async"""
        return self.get_timeline(
            data_fields=data_fields,
            latitude=latitude,
            longitude=longitude,
            timestep="current",
        )
