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

var get_property_info = function () {
    var property_id      = null;
    var property_name    = null;
    var property_address = null;
    var latitude         = null;
    var longitude        = null;
    var property_reviews = null;
    var bubbles          = null;
    var property_rating  = null;

    try {
    	property_name    = document.getElementById("HEADING").textContent;
    	property_address = document.querySelector('div.blEntry.address.clickable>div.content.hidden').textContent
    	property_reviews = document.querySelector("span[property=\"v:count\"]").textContent.replace(".", "");
    	
    	bubbles = document.querySelector("div.prw_rup.prw_common_bubble_rating.bubble_rating>span[class^=ui_bubble_rating]");
    	property_rating  = bubbles.getAttribute("class").split("_")[3]/10;

        if (!(map0Div == null)) {
            latitude  = map0Div.lat;
            longitude = map0Div.lng;
        }

        property_id = window.location.pathname.split('-')[2].replace('d', '');
	
    } catch(err) {
	   console.log(err);
    }

    return [property_id, property_name, property_reviews, property_rating, property_address, latitude, longitude];
};


return get_property_info();
