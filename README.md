# State General Aviation Airport Data

Parse state airport directories for attributes like Courtesy Car, Bicycles, Camping, Meals. Outputs data in a json for use in AirstripMap.com.

Data is as good as the state airport directories. Some notate cars, meals, bikes, and camping. Some do not.

States without useful data for this project
- Washington
- Florida

## To Dos

- [ ] Automate data fixes
- [ ] show both pages for wyoming, idaho (see southdakota)
- [ ] re-data mt and tx
- [ ] Oregon (good luck with text extraction)
- [ ] add pilots lounge, fishing

## Instructions

1. Find the state airport directory
2. Copy paste a `get_state_data.py` file and update the state info and pdf location
3. Run the below commands. You'll need to play around with the text extraction probably
4. Make any adjustments needed (and update at the bottom of the get_state_data file for future runs. Replace/update in the airport_info_state.csv file.)

```sh
pip install -r requirements.txt
brew install poppler

python3 get_state_data.py
python3 data_to_json.py <statecode e.g. mt>
python3 combined_data.py data*.json && cat combined_data.json | pbcopy
```

5. Then copy `data.json` to `airstripmap/public/data.json`
6. For size, `magick mogrify -colorspace gray images/*`
7. And copy over the images in `images_state` to `airstripmap/public/images/`


Airport data airports.csv from: https://ourairports.com/data/ 


**Dislaimer**: data subject to error, do not use for navigation purposes, etc, etc

----
### Directories

https://www.faa.gov/airports/resources/state_aviation

- [ ] Alabama
- [ ] Alaska
- [ ] Arizona
- [ ] Arkansas
- [ ] California - https://dot.ca.gov/programs/transportation-planning/division-of-transportation-planning/aeronautics (no state directory?)
- [ ] Colorado
- [ ] Connecticut
- [ ] Delaware
- [x] Florida - https://fdotwww.blob.core.windows.net/sitefinity/docs/default-source/topics/2019_directory.pdf
- [ ] Georgia
- [ ] Hawaii
- [x] Idaho - https://itd.idaho.gov/aero/
- [ ] Illinois
- [ ] Indiana
- [ ] Iowa
- [ ] Kansas
- [ ] Kentucky
- [ ] Louisiana
- [ ] Maine
- [x] Maryland - https://marylandregionalaviation.aero/publications/
- [ ] Massachusetts
- [ ] Michigan
- [ ] Minnesota
- [ ] Mississippi
- [ ] Missouri
- [x] Montana - https://www.mdt.mt.gov/aviation/airports.aspx
- [ ] Nebraska
- [ ] Nevada
- [ ] New Hampshire
- [ ] New Jersey
- [ ] New Mexico
- [ ] New York
- [ ] North Carolina
- [x] North Dakota - https://aero.nd.gov/publications/
- [ ] Ohio
- [ ] Oklahoma
- [ ] Oregon - https://www.oregon.gov/aviation/Pages/Reports.aspx
- [ ] Pennsylvania
- [ ] Rhode Island
- [ ] South Carolina
- [x] South Dakota - https://dot.sd.gov/transportation/aviation/airport-information
- [ ] Tennessee
- [x] Texas - https://ftp.dot.state.tx.us/pub/txdot-info/avn/airport-directory-list.pdf
- [ ] Utah
- [ ] Vermont
- [ ] Virginia
- [x] Washington - https://wsdot.wa.gov/engineering-standards/all-manuals-and-standards/manuals/airport-guide
- [ ] West Virginia
- [x] Wisconsin - https://wisconsindot.gov/Pages/travel/air/airport-info/arptdir-city.aspx
- [x] Wyoming - https://www.dot.state.wy.us/home/aeronautics.html

### Other Resources
- [FAA Chart Supplements](https://www.faa.gov/air_traffic/flight_info/aeronav/digital_products/dafd/)
- [VFR Charts](https://www.faa.gov/air_traffic/flight_info/aeronav/digital_products/vfr/)
- [CSVs, KMLs of US airports](https://hub.arcgis.com/documents/f74df2ed82ba4440a2059e8dc2ec9a5d/explore)
- [SkyVector](https://skyvector.com/)
- [VFR Map](https://vfrmap.com/)