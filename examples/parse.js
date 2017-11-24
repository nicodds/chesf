var parse_review = function (review_div, hotel_info) {
    var review_id = review_div.getAttribute("data-reviewid");
    var user      = review_div.querySelector("span.expand_inline.scrname").textContent;
    var title     = review_div.querySelector("span.noQuotes").textContent;
    var date      = review_div.querySelector("span.ratingDate.relativeDate").getAttribute("title");
    var text      = review_div.querySelector("div.wrap > div.prw_rup.prw_reviews_text_summary_hsx > div > p").textContent.replace(/(\r\n|\n|\r)/gm," ");

    var bubbles = review_div.querySelector("div.rating.reviewItemInline>span[class^=ui_bubble_rating]");
    var rating  = bubbles.getAttribute("class").split("_")[3]/10;

    var lang_placeholder = null;

    return [title, date, rating, text, lang_placeholder, review_id, user].concat(hotel_info);
};

var get_hotel_info = function () {
    var hotel_name     = document.getElementById("HEADING").textContent;
    var hotel_street   = document.querySelector("span.street-address").textContent;
    var hotel_locality = document.querySelector("span.locality").textContent;
    var hotel_reviews  = document.querySelector("span[property=\"v:count\"]").textContent.replace(".", "");
    var latitude       = null;
    var longitude      = null;

    var bubbles = document.querySelector("div.prw_rup.prw_common_bubble_rating.bubble_rating>span[class^=ui_bubble_rating]");
    var hotel_rating  = bubbles.getAttribute("class").split("_")[3]/10;
    var hotel_address = hotel_street + " " + hotel_locality;

    if (map0Div) {
	latitude  = map0Div.lat;
	longitude = map0Div.lng;
    }

    return [hotel_name, hotel_reviews, hotel_rating, hotel_address, latitude, longitude];
};


var prepare_page = function () {
    var wait = function () {
	var box = document.querySelector("div.loadingBox");
	var containers = document.querySelectorAll("div.review-container");
	var container_ok = null;
	
	for (var i=0; i<containers.length; i++) {
	    if (containers[i].querySelector("span.taLnk.ulBlueLinks")) {
		container_ok = containers[i];
		break;
	    }
	}
	
	while ((box.style.top == "105px") || (container_ok.classList.length > 1) ) {
	    console.log(box.style.top + '-----------------' + container_ok.classList.length);
	}
    };

    var lang = document.getElementById("taplc_location_review_filter_controls_hotels_0_filterLang_ALL");
    if (lang && !lang.checked) {
	lang.click();
	console.log('lang');
	wait();
    }

    var transl = document.querySelector("input.submitOnClick.no_cpu");
    if (transl && !transl.checked) {
	transl.click();
	console.log(transl);
	wait();
    }

    var more = document.querySelector("span.taLnk.ulBlueLinks");
    if (more) {
	more.click();
	console.log('more')
	wait();
    }

};


prepare_page();
var more = document.querySelector('span[class="taLnk ulBlueLinks"]');
//var more = document.querySelector("span.taLnk.ulBlueLinks");
if (more) {
    more.click();
}
var more = document.querySelector('span[class="taLnk ulBlueLinks"]');
//var more = document.querySelector("span.taLnk.ulBlueLinks");
if (more) {
    more.click();
}

var hotel_info = get_hotel_info();
var processed  = [];
var reviews    = document.querySelectorAll("div.review-container");

for (var i=0; i<reviews.length; i++)
    processed.push(parse_review(reviews[i], hotel_info));


return processed;
