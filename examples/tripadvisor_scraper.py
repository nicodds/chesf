# Copyright 2017 Domenico Delle Side <nico@delleside.org>
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing,
#    software distributed under the License is distributed on an "AS
#    IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
#    express or implied.  See the License for the specific language
#    governing permissions and limitations under the License.

import os
import sys
# this module is used to detect the language of the review
from langdetect import detect
import csv

sys.path.insert(0, os.path.abspath('..'))
from chesf import CHeSF, MAX_ATTEMPTS




class TripAdvisorScraper(CHeSF):
    def __init__(self):
        # the ChromeDriver is in the same directory as the script,
        # change it appropriately
        super().__init__('chromedriver.exe')
        self.results = []
        self.register_callback('before', self._before_cb)
        self.register_callback('after', self._after_cb)


    def _before_cb(self):
        # we set as hidden some divs that can intercept clicks on the
        # pagination links
        script = """
        selectors = ['div[class="prw_rup prw_vr_listings_cross_sell_properties_hsx"]', 'div[class="vr_cross_sell_wrap"]'];

        for (i=0; i<selectors.length; i++) {
           d = document.querySelectorAll(selectors[i]);

           if (d.length > 0)
               d[0].style.visibility = 'hidden';
        }
        """
        self.call_js(script)

        
    def _after_cb(self):
        # remove some annoying elements
        script = """
        // a list of css classes to set as hidden in order to prevent they cover
        // page elements that we want to click
        css_classes = ['hsx_hd_cross_sell_properties wrap', 'loadingWhiteBox'];

        for (i=0; i<css_classes.length; i++) {
            d = document.getElementsByClassName(css_classes[i]);
            if (d.length > 0)
                d[0].style.visibility = 'hidden';
        }

        // a click on the breadcrub bar to remove the calendar overlay
        document.getElementById('taplc_trip_planner_breadcrumbs_0').click();
        """

        self.call_js(script)
 
        # we add this call to wait for the given #id. If the id is not
        # present, we will wait for 1*5 seconds
        self.css('#taplc_trip_planner_breadcrumbs_0', 1)
       
        loading = self.css('#taplc_hotels_loading_box_0', 0.2)

        if len(loading) > 0:
            while loading[0].is_displayed():
                pass


    def parse(self):
        script = """
        urls = [];
        a=document.getElementsByClassName("property_title");

        for (i = 0; i < a.length; i++)
            urls.push(a[i].href);

        return urls;
        """
        links = self.call_js(script)

        for i in range(len(links)):
            self.enqueue_url(links[i], self.parse_hotel)
            
        next_page = self.xpath('//a[@class="nav next taLnk ui_button primary"]', 1)

        if len(next_page) > 0:
            self.enqueue_click(next_page[0], self.parse)



    def parse_hotel(self):
        # let's write to separate javascript to allow some time after click
        script_expand = """
        d = document.getElementsByClassName('taLnk ulBlueLinks');

        if (d.length > 0)
            d[0].click();

        box = document.querySelector('span.updating_text');

        while (box.isVisible())
           ;

        """
        self.call_js(script_expand)

        script_ratings = """
        ratings = [];
        d = document.querySelectorAll('div[class="rating reviewItemInline"]>span[class^=ui_bubble_rating]');

        if (d.length >0)
            for (i=0; i<d.length; i++)
                ratings.push(d[i].attributes.class.value.split("_")[3]/10);

        return ratings;
        """

        script_reviews = """
        reviews = [];
        d = document.querySelectorAll('div.wrap > div.prw_rup.prw_reviews_text_summary_hsx > div > p');

         if (d.length >0)
            for (i=0; i<d.length; i++)
                reviews.push(d[i].textContent);

        return reviews;
        """  

        ratings = self.call_js(script_ratings)
        reviews = self.call_js(script_reviews)
       
        for i in range(len(reviews)):
            rev_content = reviews[i]
            rev_lang    = detect(rev_content)
            rev_rating  = ratings[i]

            self.results.append([rev_lang, rev_rating, rev_content])

        selector = '#taplc_location_reviews_list_hotels_0>div>div.prw_rup.prw_common_north_star_pagination>div>span.nav.next.taLnk'
        next_page = self.css(selector, 1)

        if len(next_page) > 0:
            self.enqueue_click(next_page[0], self.parse_hotel)


    def save(self, file):
        f = open(file, 'w', encoding='utf-8')
        wr = csv.writer(f)
        for item in self.results:
            wr.writerow(item)

        f.close


######################################################################

start_url = 'https://www.tripadvisor.it/Hotels-g187791-c2-Rome_Lazio-Hotels.html'
scraper = TripAdvisorScraper()

try:
    scraper.start(start_url)
except:
    scraper.quit()
    scraper.save('results.csv')
    raise
