from __future__ import annotations

# Standard library imports.
from typing import Optional

# Project imports.
import disruptive
import disruptive.logging as dtlog
import disruptive.requests as dtrequests
import disruptive.outputs as dtoutputs
from disruptive.outputs import Metric


class DataConnector(dtoutputs.OutputBase):
    """
    Represents a Data Connector.

    When a Data Connector response is received, the content
    is unpacked and the related attributes are set.

    Attributes
    ----------
    dataconnector_id : str
        Unique Data Connector ID.
    project_id : str
        Unique ID of the project where the Data Connector resides.
    display_name : str
        The provided display name.
    dataconnector_type : str
        Dataconnector type. Currently, only HTTP_PUSH is available.
    status : str
        Whether the dataconnector is
        "ACTIVE", "USER_DISABLED", or "SYSTEM_DISABLED".
    config : HttpPushConfig, None
        An object representing the type-specific configuration.
        If an unknown Data Connector type is receiver, this is None.
    event_Types : list[str]
        List of event types that should be forwarded.
        If empty, all event types are forwarded.
    labels : list[str]
        Device labels are not included by default and will only be forwarded
        with the event if the key is specified in this list.

    """

    # Constants for the various dataconnector configuration types.
    HTTP_PUSH = 'HTTP_PUSH'
    DATACONNECTOR_TYPES = [HTTP_PUSH]

    def __init__(self, dataconnector: dict) -> None:
        """
        Constructs the DataConnector object by unpacking
        the raw dataconnector response.

        Parameters
        ----------
        dataconnector : dict
            Unmodified dataconnector response dictionary.

        """

        # Inherit from OutputBase parent.
        dtoutputs.OutputBase.__init__(self, dataconnector)

        # Unpack attributes from dictionary.
        self.dataconnector_id = dataconnector['name'].split('/')[-1]
        self.project_id = dataconnector['name'].split('/')[1]
        self.status = dataconnector['status']
        self.display_name = dataconnector['displayName']
        self.event_types = dataconnector['events']
        self.labels = dataconnector['labels']
        self.dataconnector_type = dataconnector['type']
        self.config = self._from_dict(dataconnector)

    @classmethod
    def get_dataconnector(cls,
                          dataconnector_id: str,
                          project_id: str,
                          **kwargs,
                          ) -> DataConnector:
        """
        Gets the current state of a single Data Connector.

        Parameters
        ----------
        dataconnector_id : str
            Unique dataconnector ID.
        project_id : str
            Unique project ID.
        auth: Auth, optional
            Authorization object used to authenticate the REST API.
            If provided it will be prioritized over global authentication.
        request_timeout: int, optional
            Seconds before giving up a request without an answer.
        request_retries: int, optional
            Maximum number of times to retry a request before giving up.

        Returns
        -------
        dataconnector : DataConnector
            Object representing the target Data Connector.

        Examples
        --------
        >>> dcon = disruptive.DataConnector.get_dataconnector(
        ...     dataconnector_id='z19m68nlq0bgk84smxng',
        ...     project_id='y14u8p094l37cdv1o0ug',
        ... )

        """

        # Construct URL
        url = '/projects/{}/dataconnectors/{}'
        url = url.format(project_id, dataconnector_id)

        # Return DataConnector object of GET request response.
        return cls(dtrequests.DTRequest.get(
            url=url,
            **kwargs,
        ))

    @classmethod
    def list_dataconnectors(cls,
                            project_id: str,
                            **kwargs,
                            ) -> list[DataConnector]:
        """
        Gets a list of the current state of all dataconnectors in a project.

        Parameters
        ----------
        project_id : str
            Unique project ID.
        auth: Auth, optional
            Authorization object used to authenticate the REST API.
            If provided it will be prioritized over global authentication.
        request_timeout: int, optional
            Seconds before giving up a request without an answer.
        request_retries: int, optional
            Maximum number of times to retry a request before giving up.

        Returns
        -------
        dataconnectors : list[DataConnector]
            List of objects each representing a dataconnector.

        Examples
        --------
        >>> dcons = disruptive.DataConnector.list_dataconnectors(
        ...     project_id='y14u8p094l37cdv1o0ug',
        ... )

        """

        # Return list of DataConnector objects of paginated GET response.
        dataconnectors = dtrequests.DTRequest.paginated_get(
            url='/projects/{}/dataconnectors'.format(project_id),
            pagination_key='dataConnectors',
            **kwargs,
        )
        return [cls(dcon) for dcon in dataconnectors]

    @classmethod
    def create_dataconnector(cls,
                             project_id: str,
                             config: disruptive.DataConnector.HttpPushConfig,
                             display_name: str = '',
                             status: str = 'ACTIVE',
                             events: list[str] = [],
                             labels: list[str] = [],
                             **kwargs,
                             ) -> DataConnector:
        """
        Creates a new dataconnector in the specified project.

        Parameters
        ----------
        project_id : str
            Unique project ID.
        config : HttpPush
            An object representing the type-specific configuration.
        display_name : str, optional
            Sets a display name for the project.
        status : {"ACTIVE", "USER_DISABLED"} strm optional
            Status of the new dataconnector.
        events : list[str], optional
            List of event types the dataconnectors should forward.
        labels : list[str], optional
            List of labels to forward with each event.
        auth: Auth, optional
            Authorization object used to authenticate the REST API.
            If provided it will be prioritized over global authentication.
        request_timeout: int, optional
            Seconds before giving up a request without an answer.
        request_retries: int, optional
            Maximum number of times to retry a request before giving up.

        Returns
        -------
        dataconnector : DataConnector
            Object representing the newly created dataconnector.

        Examples
        --------
        >>> dcon = disruptive.DataConnector.create_dataconnector(
        ...     project_id='y14u8p094l37cdv1o0ug',
        ...     config=disruptive.dataconnector_configs.HttpPush(
        ...         url='https://my-endpoint-url.com',
        ...         signature_secret='very-good-secret',
        ...     ),
        ...     display_name='my-first-dcon',
        ... )

        """

        # Construct request body dictionary.
        body: dict = dict()
        body['status'] = status
        body['events'] = events
        body['labels'] = labels
        if len(display_name) > 0:
            body['displayName'] = display_name

        # Add the appropriate field depending on config.
        body['type'] = config.dataconnector_type
        key, value = config._to_dict()
        body[key] = value

        # Construct URL.
        url = '/projects/{}/dataconnectors'.format(project_id)

        # Return DataConnector object of POST request response.
        return cls(dtrequests.DTRequest.post(
            url=url,
            body=body,
            **kwargs,
        ))

    @classmethod
    def update_dataconnector(
        cls,
        dataconnector_id: str,
        project_id: str,
        config: Optional[disruptive.DataConnector.HttpPushConfig] = None,
        display_name: Optional[str] = None,
        status: Optional[str] = None,
        events: Optional[list[str]] = None,
        labels: Optional[list[str]] = None,
        **kwargs,
    ) -> DataConnector:
        """
        Updates the attributes of a dataconnector.
        All parameters that are provided will be updated.

        Parameters
        ----------
        dataconnector_id : str
            Unique ID of the dataconnector to update.
        project_id : str
            Unique ID of the project that contains the dataconnector.
        config : HttpPush, None
            An object representing the type-specific configuration.
        display_name : str, optional
            Sets a display name for the dataconnector.
        status : {"ACTIVE", "USER_DISABLED"} str, optional
            Status of the dataconnector.
        events : list[str], optional
            List of event types the dataconnectors should forward.
        labels : list[str], optional
            List of labels to forward with each event.
        auth: Auth, optional
            Authorization object used to authenticate the REST API.
            If provided it will be prioritized over global authentication.
        request_timeout: int, optional
            Seconds before giving up a request without an answer.
        request_retries: int, optional
            Maximum number of times to retry a request before giving up.

        Returns
        -------
        dataconnector : DataConnector
            Object representing the updated dataconnector.

        Examples
        --------
        >>> dcon = disruptive.DataConnector.update_dataconnector(
        ...     dataconnector_id='z19m68nlq0bgk84smxng',
        ...     project_id='y14u8p094l37cdv1o0ug',
        ...     display_name='new-name',
        ...     events=['temperature', 'touch'],
        ... )

        """

        # Construct request body dictionary.
        body: dict = dict()
        if display_name is not None:
            body['displayName'] = display_name
        if status is not None:
            body['status'] = status
        if events is not None:
            body['events'] = events
        if labels is not None:
            body['labels'] = labels

        # Add the appropriate field depending on config.
        if config is not None:
            key, value = config._to_dict()
            body[key] = value

        # Construct URL.
        url = '/projects/{}/dataconnectors/{}'
        url = url.format(project_id, dataconnector_id)

        # Return DataConnector object of PATCH request response.
        return cls(dtrequests.DTRequest.patch(
            url=url,
            body=body,
            **kwargs,
        ))

    @classmethod
    def delete_dataconnector(cls,
                             dataconnector_id: str,
                             project_id: str,
                             **kwargs,
                             ) -> None:
        """
        Deletes the specified dataconnector.

        Parameters
        ----------
        dataconnector_id : str
            Unique ID of the dataconnector to delete.
        project_id : str
            Unique ID of the project that contains the dataconnector.
        auth: Auth, optional
            Authorization object used to authenticate the REST API.
            If provided it will be prioritized over global authentication.
        request_timeout: int, optional
            Seconds before giving up a request without an answer.
        request_retries: int, optional
            Maximum number of times to retry a request before giving up.

        Examples
        --------
        >>> disruptive.DataConnector.delete_dataconnector(
        ...     dataconnector_id='z19m68nlq0bgk84smxng',
        ...     project_id='y14u8p094l37cdv1o0ug',
        ... )

        """

        # Construct URL.
        url = '/projects/{}/dataconnectors/{}'
        url = url.format(project_id, dataconnector_id)

        # Send DELETE request, but return nothing.
        dtrequests.DTRequest.delete(
            url=url,
            **kwargs,
        )

    @classmethod
    def get_metrics(cls,
                    dataconnector_id: str,
                    project_id: str,
                    **kwargs,
                    ) -> Metric:
        """
        Get the metrics of the last 3 hours for a dataconnector.

        Parameters
        ----------
        dataconnector_id : str
            Unique ID of the dataconnector to list metrics for.
        project_id : str
            Unique ID of the project that contains the dataconnector.
        auth: Auth, optional
            Authorization object used to authenticate the REST API.
            If provided it will be prioritized over global authentication.
        request_timeout: int, optional
            Seconds before giving up a request without an answer.
        request_retries: int, optional
            Maximum number of times to retry a request before giving up.

        Returns
        -------
        metric : Metric
            Object representing the fetched metrics.

        Examples
        --------
        >>> metrics = disruptive.DataConnector.get_metrics(
        ...     dataconnector_id='z19m68nlq0bgk84smxng',
        ...     project_id='y14u8p094l37cdv1o0ug',
        ... )

        """

        # Construct URL.
        url = '/projects/{}/dataconnectors/{}'
        url = url.format(project_id, dataconnector_id)
        url += ':metrics'

        # Return Metric object of GET request response.
        return Metric(dtrequests.DTRequest.get(
            url=url,
            **kwargs,
        ))

    @classmethod
    def sync_dataconnector(cls,
                           dataconnector_id: str,
                           project_id: str,
                           **kwargs,
                           ) -> None:
        """
        Synchronizes the current dataconnector state.

        This method let's you synchronize your cloud service with the current
        state of the devices in your project. This entails pushing the most
        recent event of each type for all devices in your project.

        Parameters
        ----------
        dataconnector_id : str
            Unique ID of the dataconnector to synchronize.
        project_id : str
            Unique ID of the project that contains the dataconnector.
        auth: Auth, optional
            Authorization object used to authenticate the REST API.
            If provided it will be prioritized over global authentication.
        request_timeout: int, optional
            Seconds before giving up a request without an answer.
        request_retries: int, optional
            Maximum number of times to retry a request before giving up.

        Examples
        --------
        >>> disruptive.DataConnector.sync_dataconnector(
        ...     dataconnector_id='z19m68nlq0bgk84smxng',
        ...     project_id='y14u8p094l37cdv1o0ug',
        ... )

        """

        # Construct URL.
        url = '/projects/{}/dataconnectors/{}'
        url = url.format(project_id, dataconnector_id)
        url += ':sync'

        # Send POST request, but return nothing.
        dtrequests.DTRequest.post(
            url=url,
            **kwargs,
        )

    @classmethod
    def _from_dict(cls, dataconnector: dict):
        # Isolate the dataconnector type.
        dataconnector_type = dataconnector['type']

        # Select the appropriate config depending on type.
        if dataconnector_type == 'HTTP_PUSH':
            # Isolate config field.
            config = dataconnector['httpConfig']

            # Create and return an HttpPush object.
            return cls.HttpPushConfig(
                url=config['url'],
                signature_secret=config['signatureSecret'],
                headers=config['headers'],
            )
        else:
            # If this else statement runs, no config is available for type.
            dtlog.log('No config available for {} dataconnectors.'.format(
                dataconnector_type
            ))
            return None

    class HttpPushConfig():
        """
        Type-specific configurations for the HTTP_PUSH dataconnector.

        Attributes
        ----------
        url : str
            Endpoint URL towards which events are forwarded. Must be HTTPS.
        signature_secret : str
            Secret with which each forwarded event is signed.
        headers : dict[str, str]
            Dictionary of headers to include with each forwarded event.

        """

        dataconnector_type = 'HTTP_PUSH'

        def __init__(self,
                     url: Optional[str] = None,
                     signature_secret: Optional[str] = None,
                     headers: Optional[dict] = None,
                     ) -> None:
            """
            Constructs the HttpPushConfig object.

            Parameters
            ----------
            url : str, optional
                Endpoint URL towards which events are forwarded. Must be HTTPS.
            signature_secret : str, optional
                Secret with which each forwarded event is signed.
            headers : dict[str, str], optional
                Dictionary of headers to include with each forwarded event.

            """

            # Set parameter attributes.
            self.url = url
            self.signature_secret = signature_secret
            self.headers = headers

        def _to_dict(self):
            config: dict = dict()
            if self.url is not None:
                config['url'] = self.url
            if self.signature_secret is not None:
                config['signatureSecret'] = self.signature_secret
            if self.headers is not None:
                config['headers'] = self.headers
            return 'httpConfig', config
