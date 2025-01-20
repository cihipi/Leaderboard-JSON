# Leaderboard-JSON
Contains all the JSON files used by https://leaderboard.cihipi.com and allows people to submit updates. However, it's now a little out of date with a shift away from the basic rectangles into more complex and accurate polygons.
## Greetings
If you are reading this, hopefully it means you want to make an update or help better define the regions of parkrun.
## How to update
- An account on https://jsfiddle.net will allow you to return to your updates
- If you are not strong on JSON, I suggest using a JSON editor such as https://jsoneditoronline.org/ This will help you find typos
### Detailed steps
1. Find the country that you want to update. For example Japan is regions.*jp*.json
2. Open the fiddle https://jsfiddle.net/leaderboard/tdLu1504/ 
![JSFiddler main screen](./images/fiddler.png)
You should see three windows
- HTML
- CSS
- JavaScript
3. You can change this to tabs by editing your settings in the top right hand corner.
![Edit the settings by choosing tabs](./images/tabs.png)
4. Select the javascript tab or window.
5. Towards the top of the JavaScript page you should see a similar looking JSON file in red.
![Existing JSON as an example](./images/json.png)
6. Copy the JSON text from github over the top of the existing text.
![Remove the existing JSON](./images/edithere.png)
7. Change the line var targetregion = 0 to match the idx number in the JSON file.
8. Click run or press CTRL + Enter. The google map should update.
9. Editing the **n**orth, **s**outh, **e**ast or **w**est values will move the red rectangle. Events located inside the any of the rectangles will turn green. There isn't a known limit on the number of rectangles.
## File format
* idx = index (non binding)
* name
* description
* one of the following
	* bounds - defining a rectangle to use
	* polygon - the name of a polygon to reference
* events = if a polygon is defined, we use google maps to decide whether a point is inside it or not. saves me a lot of messing around
* excludeRegion = references the idx of any nested regions. Eg ACT is inside NSW in Australia
* zoom = deprecated but a zoom to use for the region
* center = deprecated but where to center the region

## Useful links
- https://hanshack.com/geotools/gimmegeodata/
- https://mapshaper.org/
- https://www.abs.gov.au/websitedbs/censushome.nsf/home/factsheetsgeography/$file/Greater%20Capital%20City%20Statistical%20Area%20-%20Fact%20Sheet.pdf

## Other stats
- https://mostevents.parq.run/
- https://regionnaire.net/
- http://www.elliottline.com/parkrun
- https://parkrace.net
- https://newparkruns.tiiny.site/

## Nodejs
- npm init (you need the git repo URL)
- npm i puppeteer --save

## Update
- worldevents -> polygon
- leaderboard (optional) -> switch do dev
- nodejs
- worldevents -> polygon and region definitions
- leadboard -> generate list of runners
- check

