/* Copyright 2018 Domenico Delle Side <nico@delleside.org>
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

// a list of css classes to set as hidden in order to prevent they cover
// page elements that we want to click
css_classes = ['hsx_hd_cross_sell_properties wrap', 'loadingWhiteBox'];

for (i=0; i<css_classes.length; i++) {
    d = document.getElementsByClassName(css_classes[i]);
    if (d.length > 0)
        d[0].style.visibility = 'hidden';
}

try {
    // a click on the breadcrub bar to remove the calendar overlay
    document.getElementById('taplc_trip_planner_breadcrumbs_0').click();
} catch(err) {
    console.log(err);
}