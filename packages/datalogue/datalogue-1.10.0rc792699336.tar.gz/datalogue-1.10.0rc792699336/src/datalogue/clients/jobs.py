from typing import List, Optional, Union
from datalogue.clients.http import _HttpClient, HttpMethod
from datalogue.models.job import Job, _job_from_payload
from datalogue.dtl_utils import _parse_list
from datalogue.errors import DtlError
from uuid import UUID


class _JobsClient:
    """
    Client to interact with the Scheduled pipelines
    """

    def __init__(self, http_client: _HttpClient):
        self.http_client = http_client
        self.service_uri = "/scout"

    def list(
        self, page: int = 1, item_per_page: int = 25, pipeline_id: Optional[UUID] = None
    ) -> Union[DtlError, List[Job]]:
        """
        List jobs

        :param page: page to be retrieved
        :param item_per_page: number of jobs to be put in a page
        :param pipeline_id: optional pipeline id used to retrieve related jobs.
        :return: Returns a List of all the available Jobs or an error message as a string
        """

        if pipeline_id:
            endpoint = f"/jobs?page={page}&size={item_per_page}&stream-id={str(pipeline_id)}"
        else:
            endpoint = f"/jobs?page={page}&size={item_per_page}"

        res = self.http_client.make_authed_request(self.service_uri + endpoint, HttpMethod.GET)

        if isinstance(res, DtlError):
            return res

        return _parse_list(_job_from_payload)(res)

    def cancel(self, job_id: UUID) -> Union[DtlError, Job]:
        """"
        Cancel a Job given job_id.

        :param job_id:
        :return: Returns the Job object canceled or an error
        """

        res = self.http_client.make_authed_request(self.service_uri + f"/jobs/{str(job_id)}/cancel", HttpMethod.POST)

        if isinstance(res, DtlError):
            return res

        return _job_from_payload(res)

    def get(self, job_id: UUID) -> Union[DtlError, Job]:
        """"
        Get a Job given job_id.

        :param job_id:
        :return: Returns the Job object or an error
        """

        res = self.http_client.make_authed_request(self.service_uri + f"/jobs/{str(job_id)}/status", HttpMethod.GET)

        if isinstance(res, DtlError):
            return res

        return _job_from_payload(res)
