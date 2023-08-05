import logging
from typing import List, Optional

from requests import Response

from cognite.well_model.client._api_client import APIClient
from cognite.well_model.client.api.api_base import BaseAPI
from cognite.well_model.client.models.resource_list import NPTList
from cognite.well_model.models import NPT, DoubleRangeWithUnit, NPTFilter

logger = logging.getLogger("WellsAPI")


class EventsAPI(BaseAPI):
    def __init__(self, wells_client: APIClient):
        super().__init__(wells_client)

    def list_npt_events(
        self,
        md: Optional[DoubleRangeWithUnit] = None,
        duration: Optional[DoubleRangeWithUnit] = None,
        npt_code: Optional[str] = None,
        npt_code_detail: Optional[str] = None,
    ) -> NPTList:
        npt_filter = NPTFilter(measured_depth=md, duration=duration, npt_code=npt_code, npt_code_detail=npt_code_detail)

        path: str = self._get_path("/events/list")
        response: Response = self.wells_client.post(url_path=path, json=npt_filter.json(), params=None)
        events: List[NPT] = [NPT.parse_obj(x) for x in response.json()]
        return NPTList(events)

    def list_nds_events(self):
        raise NotImplementedError
