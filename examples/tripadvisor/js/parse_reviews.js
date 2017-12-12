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

var parse_review = function (review_div) {
    var review_id = null;
    var user      = null;
    var title     = null;
    var date      = null;
    var text      = null;
    var bubbles   = null;
    var rating    = null; 

    var lang_placeholder = null;

    var property_id = null
	
    try {
    	review_id = review_div.getAttribute("data-reviewid");
    	user      = review_div.querySelector("span.expand_inline.scrname").textContent;
    	title     = review_div.querySelector("span.noQuotes").textContent;
    	date      = review_div.querySelector("span.ratingDate.relativeDate").getAttribute("title");    
    	text      = review_div.querySelector("div.wrap > div.prw_rup.prw_reviews_text_summary_hsx > div > p").textContent.replace(/(\r\n|\n|\r)/gm," ");

    	bubbles = review_div.querySelector("div.rating.reviewItemInline>span[class^=ui_bubble_rating]");
    	rating  = bubbles.getAttribute("class").split("_")[3]/10;

	property_id = window.location.pathname.split('-')[2].replace('d', '');

    } catch(err) {
	   console.log(err);
    }

    return [title, date, rating, text, lang_placeholder, user, review_id, property_id];
};

var reviews    = document.querySelectorAll("div.review-container");
var processed  = [];

for (var i=0; i<reviews.length; i++) {
    processed.push(parse_review(reviews[i]));
}

return processed;
