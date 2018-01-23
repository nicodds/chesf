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
selectors_list = ['div.vr_cross_sell_wrap'];

for (let selector of selectors_list) {
	d = document.querySelectorAll(selector);

    if (d.length > 0)
        d[0].style.visibility = 'hidden';
}

tabs_list = document.querySelectorAll('ul.ui_tabs>li.ui_tab');

// to avoid empty pages due to results filtering
for (var tab of tabs_list) {
	if (tab.dataset.sortorder == 'popularity')
		if (tab.classList.length < 3)
			tab.click();
}