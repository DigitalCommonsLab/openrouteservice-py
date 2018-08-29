# Copyright (C) 2018 HeiGIT, University of Heidelberg.
#
# Modifications Copyright (C) 2018 HeiGIT, University of Heidelberg.
#
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy of
# the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.
#

"""Performs requests to the ORS geocode API (direct Pelias clone)."""
from openrouteservice import convert

valid_layers = ['venue',
                 'address',
                 'street',
                 'neighbourhood',
                 'borough',
                 'localadmin',
                 'locality',
                 'county',
                 'macrocounty',
                 'region',
                 'macroregion',
                 'county',
                 'coarse']

valid_sources = ['osm', 'oa', 'wof', 'gn']

def pelias_search(client, text,
            focus_point=None,
            rect_min_x=None,
            rect_min_y=None,
            rect_max_x=None,
            rect_max_y=None,
            circle_point=None,
            circle_radius=None,
            sources=None,
            layers=None,
            country=None,
            size=None,
            dry_run=None):
    """
    Geocoding is the process of converting addresses into geographic
    coordinates.
    
    This endpoint queries directly against a Pelias instance.
    
    :param text: Full-text query against search endpoint. Required.
    :type text: string

    :param focus_point: Focusses the search to be around this point and gives
        results within a 100 km radius higher scores.
    :type query: list or tuple of (Long, Lat)

    :param rect_min_x: Min longitude by which to constrain request geographically.
    :type rect_min_x: float

    :param rect_min_y: Min latitude by which to constrain request geographically.
    :type rect_min_y: float

    :param rect_max_x: Max longitude by which to constrain request geographically.
    :type rect_max_x: float

    :param rect_max_y: Max latitude by which to constrain request geographically.
    :type rect_max_y: float

    :param circle_point: Geographical constraint in form a circle.
    :type circle_point: list or tuple of (Long, Lat)

    :param circle_radius: Radius of circle constraint in km. Default 50.
    :type circle_radius: integer

    :param sources: The originating source of the data. One or more of 
        ['osm', 'oa', 'wof', 'gn']. Currently only 'osm', 'wof' and 'gn' are 
        supported.
    :type sources: list of strings

    :param layers: The administrative hierarchy level for the query. Refer to 
        https://github.com/pelias/documentation/blob/master/search.md#filter-by-data-type
        for details.
    :type layers: list of strings

    :param country: Constrain query by country. Accepts alpha-2 or alpha-3 
        digit ISO-3166 country codes.
    :type country: list of strings

    :param size: The amount of results returned. Default 10.
    :type size: integer
    
    :raises ValueError: When parameter has invalid value(s).
    :raises TypeError: When parameter is of the wrong type.

    :rtype: call to Client.request()
    """

    params = {'text': text}
    
    if focus_point:
        params['focus.point.lon'] = convert._format_float(focus_point[0])
        params['focus.point.lat'] = convert._format_float(focus_point[1])
    
    if rect_min_x:
        params['boundary.rect.min_lon	'] = convert._format_float(rect_min_x)
        
    if rect_min_y:
        params['boundary.rect.min_lat	'] = convert._format_float(rect_min_y)
        
    if rect_max_x:
        params['boundary.rect.max_lon	'] = convert._format_float(rect_max_x)
        
    if rect_max_y:
        params['boundary.rect.max_lon	'] = convert._format_float(rect_max_y)
    
    if circle_point:
        params['boundary.circle.lon'] = convert._format_float(circle_point[0])
        params['boundary.circle.lat'] = convert._format_float(circle_point[1])
        
    if circle_radius:
        params['boundary.circle.radius'] = circle_radius
        
    if sources:
        if not convert._is_list(sources):
            raise TypeError('Data source invalid.')
        if not all((source in valid_sources) for source in sources):
            raise ValueError("Source must be one or more of {}".format(valid_sources))
        params['sources'] = convert._comma_list(sources)

    if layers:
        if not convert._is_list(layers):
            raise TypeError('Invalid layer type for geocoding.')
        if not all((layer in valid_layers) for layer in layers):
            raise ValueError("Source must be one or more of ".format(valid_layers))
        params['layers'] = convert._comma_list(layers)

    if country:
        if not isinstance(country, str):
            raise TypeError('Country must be a string.')
        params['country'] = country

    if size:
        params['size'] = size

    return client.request("/geocode/search", params, dry_run=dry_run)

  
def pelias_structured(client, text,
                     address=None,
                     neighbourhood=None,
                     borough=None,
                     locality=None,
                     county=None,
                     region=None,
                     postalcode=None,
                     country=None,
                     dry_run=None):
    """
    With structured geocoding, you can search for the individual parts of a location. 
    Structured geocoding is an option on the search endpoint, 
    which allows you to define a query that maintains the individual fields.
    
    This endpoint queries directly against a Pelias instance.
    
    :param text: Full-text query against search endpoint. Required.
    :type text: list of strings
    
    :param address: Can contain a full address with house number or only a street name. 
    :type address: list of strings
    
    :param neighbourhood: Neighbourhoods are vernacular geographic entities that 
        may not necessarily be official administrative divisions but are important nonetheless.
    :type neighbourhood: list of strings
    
    :param borough: Mostly known in the context of New York City, even though they may exist in other cities.
    :type borough: list of strings
    
    :param locality: Localities are equivalent to what are commonly referred to as cities.
    :type locality: list of strings
    
    :param county: Administrative divisions between localities and regions.
        Not as commonly used in geocoding as localities, but useful when attempting to 
        disambiguate between localities. 
    :type county: list of strings
    
    :param region: Normally the first-level administrative divisions within countries, analogous to states 
        and provinces in the United States and Canada. Can be a full name or abbreviation.
    :type region: list of strings
    
    :param postalcode: Dictated by an administrative division, which is almost always countries.
        Postal codes are unique within a country.
    :type postalcode: list of strings
    
    :param country: Highest-level divisions supported in a search. Can be a full name or abbreviation.
    :text county: list of strings
    
    :raises TypeError: When parameter is of the wrong type.

    :rtype: call to Client.request()
    """
    
    params = {'text': text}
    
    if address:
        if not isinstance(address, str):
            raise TypeError('Address must be a string.')
        params['address'] = address

    if neighbourhood:
        if not isinstance(neighbourhood, str):
            raise TypeError('Neighbourhood must be a string.')
        params['neighbourhood'] = neighbourhood

    if borough:
        if not isinstance(borough, str):
            raise TypeError('Borough must be a string.')
        params['borough'] = borough

    if locality:
        if not isinstance(locality, str):
            raise TypeError('Locality must be a string.')
        params['locality'] = locality

    if county:
        if not isinstance(county, str):
            raise TypeError('County must be a string.')
        params['county'] = county

    if region:
        if not isinstance(region, str):
            raise TypeError('Region must be a string.')
        params['region'] = region

    if postalcode:
        if not isinstance(postalcode, str):
            raise TypeError('Postalcode must be a string.')
        params['postalcode'] = postalcode

    if country:
        if not isinstance(country, str):
            raise TypeError('Country must be a string.')
        params['country'] = country
        
    return client.request("/geocode/search/structured", params, dry_run=dry_run)
  
  
def pelias_reverse(client, point,
                    circle_radius=None,
                    sources=None,
                    layers=None,
                    country=None,
                    size=None,
                    dry_run=None):
    """
    Reverse geocoding is the process of converting geographic coordinates into a
    human-readable address.
    
    This endpoint queries directly against a Pelias instance.

    :param point: Coordinate tuple. Required.
    :type point: list or tuple of [Lon, Lat]

    :param circle_radius: Radius around point to limit query in km. Default 1.
    :type circle_radius: integer

    :param sources: The originating source of the data. One or more of 
        ['osm', 'oa', 'wof', 'gn']. Currently only 'osm', 'wof' and 'gn' are 
        supported.
    :type sources: list of strings

    :param layers: The administrative hierarchy level for the query. Refer to 
        https://github.com/pelias/documentation/blob/master/search.md#filter-by-data-type
        for details.
    :type layers: list of strings

    :param country: Constrain query by country. Accepts alpha-2 or alpha-3 
        digit ISO-3166 country codes.
    :type country: list of strings

    :param size: The amount of results returned. Default 10.
    :type size: integer
    
    :raises ValueError: When parameter has invalid value(s).

    :rtype: dict from JSON response
    """
    
    params = dict()

    if not convert._is_list(point):
        raise TypeError('Point must be a list/tuple of coordinates.')
        
    params['point.lon'] = convert._format_float(point[0])
    params['point.lat'] = convert._format_float(point[1])
        
    if circle_radius:
        params['boundary.circle.radius'] = str(circle_radius)
        
    if sources:
        if not convert._is_list(sources):
            raise TypeError('Data source invalid.')
        if not all((source in valid_sources) for source in sources):
            raise ValueError("Source must be one or more of {}".format(valid_sources))
        params['sources'] = convert._comma_list(sources)

    if layers:
        if not convert._is_list(layers):
            raise TypeError('Invalid layer type for geocoding.')
        if not all((layer in valid_layers) for layer in layers):
            raise ValueError("Source must be one or more of ".format(valid_layers))
        params['layers'] = convert._comma_list(layers)

    if country:
        if not isinstance(country, str):
            raise TypeError('Country must be a string.')
        
        params['country'] = country

    if size:
        params['size'] = size

    return client.request("/geocode/reverse", params, dry_run=dry_run)
