/* Copyright 2017 Domenico Delle Side <nico@delleside.org>
 *
 *    Licensed under the Apache License, Version 2.0 (the "License");
 *    you may not use this file except in compliance with the License.
 *    You may obtain a copy of the License at
 *
 *        http://www.apache.org/licenses/LICENSE-2.0
 *
 *    Unless required by applicable law or agreed to in writing,
 *    software distributed under the License is distributed on an "AS
 *    IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
 *    express or implied.  See the License for the specific language
 *    governing permissions and limitations under the License.
 */

var map_url_parser = function (img_element) {
    var url = '';

    if (img_element.hasAttribute('src'))
        url = img_element.getAttribute('src');

    if (url.length > 100)
        return url.split('&')[7].split('=')[1].split(',');

    return [null, null]
}

var obj_to_string = function (ob) {
    var address = (ob.streetAddress || '') + ', ';
    address += (ob.postalCode || '') + ', ';
    address += (ob.AddressLocality || '') + ', ';
    address += ob.addressCountry.name || '';

    return address;
}

var get_property_info = function () {
    var property_id      = null;
    var property_name    = null;
    var property_address = null;
    var latitude         = null;
    var longitude        = null;
    var property_reviews = 0;
    var bubbles          = null;
    var property_rating  = 0;
    var property_url     = null;

    try {
        let json_script = '';
        
        do {
            json_script = document.querySelector('script[type="application/ld+json"]').textContent;
        } while (json_script.length <= 0);

        json_data = JSON.parse(json_script);

        if (document.querySelector('div.prv_map.clickable>img'))
            [latitude, longitude] = map_url_parser(document.querySelector('div.prv_map.clickable>img'));
	    property_id      = window.location.pathname.split('-')[2].replace('d', '');
        property_url     = window.location.href;
    	property_name    = json_data.name;
    	property_address = obj_to_string(json_data.address);
        if (json_data.hasOwnProperty('aggregateRating')) {
            property_reviews = json_data.aggregateRating.reviewCount;
            property_rating  = json_data.aggregateRating.ratingValue;
        }
    } catch(err) {
        console.log("++++++++++++++++++ Error parsing property info ++++++++++++++++++");
        console.log(err);
    }

    return [property_id, property_name, property_reviews, property_rating, property_address, latitude, longitude, property_url];
};


return get_property_info();
