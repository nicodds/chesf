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
from time import sleep

sys.path.insert(0, os.path.abspath('../..'))
from chesf import CHeSF, MAX_ATTEMPTS


class TripAdvisorScraper(CHeSF):
    def __init__(self):
        # the ChromeDriver is in the same directory as the script,
        # change it appropriately
        super().__init__('chromedriver.exe', debug=True)
        self.reviews        = []
        self.properties     = []
        self.property_urls  = []
        self.requested_urls = []

        self.register_callback('before', self._before_cb)
        self.register_callback('after', self._after_cb)

        self._js_code = {
            'prepare': open('js/prepare.js', 'r').read(),
            'parse_reviews': open('js/parse_reviews.js', 'r').read(),
            'parse_property': open('js/parse_property.js', 'r').read(),
            'cb_before': open('js/cb_before.js').read(),
            'cb_after': open('js/cb_after.js').read()
        }

        self._reviews_file          = 'reviews.csv'
        self._property_file         = 'properties.csv'
        self._unrequested_urls_file = 'unrequested_urls.txt'


    def _property_url_is_first_request(self):
        # This method returns True if the property url under consideration is
        # at its first request, otherwise False
        if (self.current_url() in self.requested_urls):
            return False

        return True


    def _before_cb(self):
        # we set as hidden some divs that can intercept clicks on the
        # pagination links.
        # As a plus, we force ordering for popularity
        self.call_js(self._js_code['cb_before'])

        
    def _after_cb(self):
        # remove some annoying elements
#        self.call_js(self._js_code['cb_after'])
 
        # we add this call to wait for the given #id. If the id is not
        # present, we will wait for 0.4*5 seconds
        self.css('#taplc_trip_planner_breadcrumbs_0', timeout=0.4)

        # check if the page is still loading its results
        loading = self.css('#taplc_hotels_loading_box_0', timeout=0.2)

        if len(loading) > 0:
            while loading[0].is_displayed():
                pass


    def parse(self):
        # this is a fast hack, in the future it will be removed using command line
        # options to instruct the program resume operations
        if self.current_url() == 'http://unrequested':
            links = self.read()
        else:
            script = """
            urls = [];
            a=document.querySelectorAll("a.property_title.prominent");

            for (i = 0; i < a.length; i++)
                urls.push(a[i].href);

            return urls;
            """
            links = self.call_js(script)

        for link in links:
            self.enqueue_url(link, self.parse_hotel)
            self.property_urls.append(link)

        print('Stored %i urls (for a total of %i)' %(len(links), self._url_counter))
        
        next_page = self.css('a.nav.next.taLnk.ui_button.primary', timeout=1)
        #next_page = self.xpath('//a[@class="nav next taLnk ui_button primary"]', timeout=1)

        if len(next_page) > 0:
            self.enqueue_click(next_page[0], self.parse)




    def parse_hotel(self):
        # click on the radio button to select reviews in all available
        # languages and, if needed, disable any automatic translation.
        self.call_js(self._js_code['prepare'])
            
        if (self._property_url_is_first_request()):
            self.requested_urls.append(self.current_url())
            sleep(0.2)
            # 0 property_id
            # 1 property_name
            # 2 property_reviews
            # 3 property_rating
            # 4 property_address
            # 5 property_latitude
            # 6 property_longitude
            # 7 property_url
            #
            property_info = self.call_js(self._js_code['parse_property'])
            self.properties.append(property_info)
            print('****** Processing  property %i out of %i ******' %(len(self.requested_urls), len(self.property_urls)))
            print('****** %s  (%i reviews) ******' %(property_info[1], int(property_info[2])))

        # for some weird reason I'm not able to figure out, performing
        # this click on javascript code doesn't work. So this code is
        # here as a workaround. It's unclean, since I had to write two
        # different scripts (prepare.js and parse.js), but it
        # works. At least for the moment, this ugly code will remain
        # here.
        #
        # In a nutshell, this code expands the reviews that, if too
        # long, get truncated.
        expand_selector = 'div.prw_rup.prw_reviews_text_summary_hsx>div>p>span.taLnk.ulBlueLinks'
        expand = self.css(expand_selector, timeout=1);
        expand_check = 0

        while len(expand) > 0 and (expand_check < 3):
            expand[0].click()
            # I haven't found any way to avoid this sleep call
            sleep(0.5)
            expand = self.css(expand_selector, timeout=1);
            expand_check += 1

        # call the script that parse the page and return all results as a 2D
        # list: the first dimension counts the number of reviews parsed (from
        # 1 up to 5), while the second (length 8) is for the reviews parsed
        # from the page. The information parsed are ordered as follows:
        # 0 review_title
        # 1 review_date
        # 2 review_rating
        # 3 review_text
        # 4 lang_placeholder
        # 5 review_user
        # 6 review_id
        # 7 property_id
        #
        results = self.call_js(self._js_code['parse_reviews'])

        if (len(results) == 0):
            print('O reviews for %s' %(self.current_url()))
            return None

        # detect the language of the reviews
        for review in results:
            review[4] = detect(review[3])
            self.reviews.append(review[0:8])

            if len(self.reviews) % 100 == 0:
                print('Saving results (total: %i)' %(len(self.reviews)))
                self.save()

        print('*** Stored %i reviews' %(len(results)))

        selector = 'span.nav.next.taLnk'
        next_page = self.css(selector, timeout=1)

        if len(next_page) > 0:
            self.enqueue_click(next_page[0], self.parse_hotel)


    def save(self):
        requested = set(self.requested_urls)
        unrequested = [u for u in self.property_urls if u not in requested]

        with open(self._reviews_file, 'w', encoding='utf-8') as revs:
            wr = csv.writer(revs, lineterminator='\n')
            wr.writerow(['review_title', 'review_date', 'review_rating',
                         'review_text', 'review_language', 'review_user',
                         'review_id', 'property_id'])
            wr.writerows(self.reviews)

        with open(self._property_file, 'w', encoding='utf-8') as props:
            wr = csv.writer(props, lineterminator='\n')
            wr.writerow(['property_id', 'property_name', 'property_reviews',
                         'property_rating', 'property_address', 'property_latitude',
                         'property_longitude', 'property_url'])
            wr.writerows(self.properties)

        with open(self._unrequested_urls_file, 'w', encoding='utf-8') as urls:
            for u in unrequested:
                urls.write('%s\n' %(u))

    

    def read(self):
        unrequested = False

        with open(self._reviews_file, 'r', encoding='utf-8') as revs:
            rdr = csv.reader(revs)
            next(rdr, None)
            for row in rdr:
               self.reviews.append(row)

        with open(self._property_file, 'r', encoding='utf-8') as props:
            rdr = csv.reader(props)
            next(rdr, None)
            for row in rdr:
                self.properties.append(row)

        with open(self._unrequested_urls_file, 'r', encoding='utf-8') as urls:
            unrequested = [u.strip() for u in urls.readlines()]

        self.enqueue_url('https://www.tripadvisor.com/Hotels-g187791-c2-Rome_Lazio-Hotels.html', self.parse)

        return unrequested


######################################################################
#start_url='https://www.tripadvisor.com/Hotels-g1024144-Poggiardo_Province_of_Lecce_Puglia-Hotels.html'
start_url = 'https://www.tripadvisor.com/Hotels-g187791-c2-Rome_Lazio-Hotels.html'
# start_url = 'http://unrequested'

scraper = TripAdvisorScraper()

try:
    scraper.start(start_url)
except:
    scraper.quit()
    scraper.save()
    raise
