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

var prepare_page = function () {
    var wait = function (ms) {
	start = (new Date()).getTime();
    
	while ((new Date()).getTime - start <= ms)
	    ;
    };

    // displaying reviews in all languages
    var lang = document.getElementById("taplc_location_review_filter_controls_hotels_0_filterLang_ALL");
    if (!(lang == null) && !lang.checked) {
	   try {
	       lang.click();
	       wait(300);
	   } catch(err) {
	       console.log(err);
	   }
    }

    // remove any automatic translation 
    var transl = document.querySelector("input.submitOnClick.no_cpu");
    if (!(transl == null) && !transl.checked) {
	   try {  
	        transl.click();
	       wait(300);
	   } catch(err) {
	       console.log(err);
	   }
    }
};

prepare_page();
