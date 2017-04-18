"""Classes to handle API queries/searches"""
from ticketpy.model import Venue, Event, Attraction, Classification, Genre, \
    Subgenre, Segment, attr_map


class BaseQuery:
    """Base query/parent class for specific serach types."""
    resource = None
    model = None

    def __init__(self, api_client):
        """
        :param api_client: Instance of ``ticketpy.client.ApiClient``
        """
        self.api_client = api_client

    def __get(self, **kwargs):
        """Sends final request to ``ApiClient``"""
        return self.api_client._search(self.resource, **kwargs)

    def _get(self, keyword=None, entity_id=None, sort=None, include_test=None,
             page=None, size=None, locale=None, **kwargs):
        """Basic API search request, with only the parameters common to all 
        search functions. Specific searches pass theirs through **kwargs.
        
        :param keyword: Keyword to search on
        :param entity_id: ID of the object type (such as an event ID...)
        :param sort: Sort method
        :param include_test: ['yes', 'no', 'only'] to include test objects in 
            results. Default: *no*
        :param page: Page to return (default: 0)
        :param size: Page size (default: 20)
        :param locale: Locale (default: *en*)
        :param kwargs: Additional search parameters
        :return: 
        """
        # Combine universal parameters and supplied kwargs into single dict,
        # then map our parameter names to the ones expected by the API and
        # make the final request
        search_args = kwargs
        search_args.update({
            'keyword': keyword,
            'id': entity_id,
            'sort': sort,
            'include_test': include_test,
            'page': page,
            'size': size,
            'locale': locale
        })
        params = self._search_params(**search_args)
        return self.__get(**params)

    def by_id(self, entity_id):
        """Get a specific object by its ID"""
        resp = self.api_client._get_id(self.resource, entity_id)
        return self.model.from_json(resp)

    @staticmethod
    def _search_params(**kwargs):
        """Update keywords to be API-friendly"""
        # Ex: If 'venue_id' is passed, change to 'venueId
        for k, v in attr_map.items():
            if k in kwargs and k != v:
                kwargs[v] = kwargs[k]
                del kwargs[k]
        return {k: v for (k, v) in kwargs.items() if v is not None}

    @staticmethod
    def from_json(json_obj):
        return json_obj


class AttractionQuery(BaseQuery):
    """Query class for Attractions"""
    resource = 'attractions'
    model = Attraction

    def __init__(self, api_client):
        super().__init__(api_client)

    def find(self, sort=None, keyword=None, attraction_id=None,
             source=None, include_test=None, page=None, size=None,
             locale=None, **kwargs):
        """
        :param sort: Response sort type (API default: *name,asc*)
        :param keyword: 
        :param attraction_id: 
        :param source: 
        :param include_test: Include test attractions (['yes', 'no', 'only'])
        :param page: 
        :param size: 
        :param locale: API default: *en*
        :param kwargs: 
        :return: 
        """
        return self._get(keyword, attraction_id, sort, include_test,
                         page, size, locale, source=source, **kwargs)


class ClassificationQuery(BaseQuery):
    """Classification search/query class"""
    resource = 'classifications'
    model = Classification

    def __init__(self, api_client):
        super().__init__(api_client)

    def find(self, sort=None, keyword=None, classification_id=None,
             source=None, include_test=None, page=None, size=None,
             locale=None, **kwargs):
        """Search classifications

        :param sort: Response sort type (API default: *name,asc*)
        :param keyword: 
        :param classification_id: 
        :param source: 
        :param include_test: Include test classifications 
            (['yes', 'no', 'only'])
        :param page: 
        :param size: 
        :param locale: API default: *en*
        :param kwargs: 
        :return: 
        """
        return self._get(keyword, classification_id, sort, include_test,
                         page, size, locale, source=source, **kwargs)


class SegmentQuery(BaseQuery):
    resource = 'classifications/segments'
    model = Segment

    def __init__(self, api_client):
        super().__init__(api_client)


class GenreQuery(BaseQuery):
    resource = 'classifications/genres'
    model = Genre

    def __init__(self, api_client):
        super().__init__(api_client)


class SubGenreQuery(BaseQuery):
    resource = 'classifications/subgenres'
    model = Subgenre

    def __init__(self, api_client):
        super().__init__(api_client)


class EventQuery(BaseQuery):
    """Abstraction to search API for events"""
    resource = 'events'
    model = Event

    def __init__(self, api_client):
        super().__init__(api_client)

    def find(self, sort='date,asc', latlong=None, radius=None, unit=None,
             start_date_time=None, end_date_time=None,
             onsale_start_date_time=None, onsale_end_date_time=None,
             country_code=None, state_code=None, venue_id=None,
             attraction_id=None, segment_id=None, segment_name=None,
             classification_name=None, classification_id=None,
             market_id=None, promoter_id=None, dma_id=None,
             include_tba=None, include_tbd=None, client_visibility=None,
             keyword=None, event_id=None, source=None, include_test=None,
             page=None, size=None, locale=None, **kwargs):
        """Search for events matching given criteria.

        :param sort: Sorting order of _search result 
            (default: *'relevance,desc'*)
        :param latlong: Latitude/longitude filter
        :param radius: Radius of area to _search
        :param unit: Unit of radius, 'miles' or 'km' (default: miles)
        :param start_date_time: Filter by start date/time.
            Timestamp format: *YYYY-MM-DDTHH:MM:SSZ*
        :param end_date_time: Filter by end date/time.
            Timestamp format: *YYYY-MM-DDTHH:MM:SSZ*
        :param onsale_start_date_time: 
        :param onsale_end_date_time: 
        :param country_code: 
        :param state_code: State code (ex: 'GA' not 'Georgia')
        :param venue_id: Find events for provided venue ID
        :param attraction_id: 
        :param segment_id: 
        :param segment_name: 
        :param classification_name: Filter events by a list of 
            classification name(s) (genre/subgenre/type/subtype/segment)
        :param classification_id: 
        :param market_id: 
        :param promoter_id: 
        :param dma_id: 
        :param include_tba: True to include events with a to-be-announced 
            date (['yes', 'no', 'only'])
        :param include_tbd: True to include an event with a date to be 
            defined (['yes', 'no', 'only'])
        :param client_visibility: 
        :param keyword: 
        :param event_id: Event ID to _search 
        :param source: Filter entities by source name: ['ticketmaster', 
            'universe', 'frontgate', 'tmr']
        :param include_test: 'yes' to include test entities in the 
            response. False or 'no' to exclude. 'only' to return ONLY test 
            entities. (['yes', 'no', 'only'])
        :param page: Page number to get (default: 0)
        :param size: Size of page (default: 20)
        :param locale: Locale (default: 'en')
        :return: 
        """
        return self._get(keyword, event_id, sort, include_test, page,
                         size, locale, latlong=latlong, radius=radius,
                         unit=unit, start_date_time=start_date_time,
                         end_date_time=end_date_time,
                         onsale_start_date_time=onsale_start_date_time,
                         onsale_end_date_time=onsale_end_date_time,
                         country_code=country_code, state_code=state_code,
                         venue_id=venue_id, attraction_id=attraction_id,
                         segment_id=segment_id, segment_name=segment_name,
                         classification_name=classification_name,
                         classification_id=classification_id,
                         market_id=market_id, promoter_id=promoter_id,
                         dma_id=dma_id, include_tba=include_tba,
                         include_tbd=include_tbd, source=source,
                         client_visibility=client_visibility, **kwargs)

    def by_location(self, latitude, longitude, radius='10', unit='miles',
                    sort='relevance,desc', **kwargs):
        """Search events within a radius of a latitude/longitude coordinate.

        :param latitude: Latitude of radius center
        :param longitude: Longitude of radius center
        :param radius: Radius to search outside given latitude/longitude
        :param unit: Unit of radius ('miles' or 'km'),
        :param sort: Sort method. (Default: *relevance, desc*). If changed, 
            you may get wonky results (*date, asc* returns far-away events)
        :return: List of events within that area
        """
        # Cast with str() in case an integer/float was passed
        latlong = "{lat},{long}".format(lat=str(latitude), long=str(longitude))
        return self.find(latlong=latlong, radius=str(radius), unit=unit,
                         sort=sort, **kwargs)


class VenueQuery(BaseQuery):
    """Queries for venues"""
    resource = 'venues'
    model = Venue

    def __init__(self, api_client):
        super().__init__(api_client)

    def find(self, keyword=None, venue_id=None, sort=None, state_code=None,
             country_code=None, source=None, include_test=None,
             page=None, size=None, locale=None, **kwargs):
        """Search for venues matching provided parameters
        
        :param keyword: Keyword to search on (such as part of the venue name)
        :param venue_id: Venue ID 
        :param sort: Sort method for response (API default: 'name,asc')
        :param state_code: Filter by state code (ex: 'GA' not 'Georgia')
        :param country_code: Filter by country code
        :param source: Filter entities by source (['ticketmaster', 'universe', 
            'frontgate', 'tmr'])
        :param include_test: ['yes', 'no', 'only'], whether to include 
            entities flagged as test in the response (default: 'no')
        :param page: Page number (default: 0)
        :param size: Page size of the response (default: 20)
        :param locale: Locale (default: 'en')
        :return: Venues found matching criteria 
        :rtype: ``ticketpy.PagedResponse``
        """
        return self._get(keyword, venue_id, sort, include_test, page,
                         size, locale, state_code=state_code,
                         country_code=country_code, source=source, **kwargs)

    def by_name(self, venue_name, state_code=None, **kwargs):
        """Search for a venue by name.

        :param venue_name: Venue name to search
        :param state_code: Two-letter state code to narrow results (ex 'GA')
            (default: None)
        :return: List of venues found matching search criteria
        """
        return self.find(keyword=venue_name, state_code=state_code, **kwargs)
