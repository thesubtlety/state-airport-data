# State General Aviation Airport Data

Parse state airport directories for attributes like Courtesy Car, Bicycles, Camping, Meals. Outputs data in a json for use in AirstripMap.com.

Data is as good as the state airport directories. Some notate cars, meals, bikes, and camping. Some do not.

## Instructions

1. Find the state airport directory
2. Copy paste a `get_state_data.py` file and update the state info and pdf location
3. Run the below commands. You'll need to play around with the text extraction
4. Make any adjustments needed (and update at the bottom of the `get_state_data` file for future runs. Replace/update in the `airport_info_state.csv` file.)

```sh
pip install -r requirements.txt
brew install poppler
brew install optipng

python3 get_state_data.py
python3 data_to_json.py <statecode e.g. mt>
python3 combined_data.py data/data*.json && cat data/combined_data.json | pbcopy
#For size
magick mogrify -colorspace gray images/*
optipng images/*
```

5. Then copy `combined_data.json` to `airstripmap/public/data.json`
6. And copy over the images in `images/state` to `airstripmap/public/images/`

Airport data airports.csv from: https://ourairports.com/data/ 

**Dislaimer**: data subject to error, do not use for navigation purposes, etc, etc

## To Dos

- [ ] fix duplicates HRF, 32S, 1D8, PUW, RGK, 25u, s60, dls, ono, 

----
### Directories

https://www.faa.gov/airports/resources/state_aviation

- [-] Alabama (no useful state directory)
- [-] Alaska (no useful state directory)
- [-] [Arizona](https://azdot.gov/planning/airport-development/airports) (no useful state directory)
- [ ] [Arkansas](https://fly.arkansas.gov/airport-info.html) (needs compiled...)
- [-] [California](https://dot.ca.gov/programs/transportation-planning/division-of-transportation-planning/aeronautics) (no useful state directory)
- [ ] [Colorado](https://www.codot.gov/programs/aeronautics/Periodicals/colorado-airport-directory) (doubled pdf)
- [-] [Connecticut](https://ctairports.org/airports/)  (no useful state directory)
- [ ] [Delaware](https://deldot.gov/Programs/airports/pdfs/de_airport_directory_2009_2010.pdf)
- [x] [Florida](https://fdotwww.blob.core.windows.net/sitefinity/docs/default-source/topics/2019_directory.pdf)
- [x] [Georgia](https://www.dot.ga.gov/InvestSmart/Aviation/AirportAid/AirportDirectory.pdf) (imperfect parsing)
- [-] Hawaii (no useful state directory)
- [x] [Idaho](https://itd.idaho.gov/aero/)
- [-] Illinois (no useful state directory)
- [-] [Indiana](https://www.in.gov/indot/multimodal/aviation/indiana-public-use-airports/) (no useful state directory)
- [-] [Iowa](https://iowadot.gov/aviation/airport-information) (no useful state directory)
- [ ] [Kansas](https://www.ksdot.gov/Assets/wwwksdotorg/bureaus/divAviation/pdf/AirportDir.pdf) (doubled pdf)
- [x] [Kentucky](https://transportation.ky.gov/aviation/documents/airport-directory.pdf)
- [-] [Louisiana](https://wwwapps.dotd.la.gov/multimodal/aviation/airportdirectory.aspx) (no useful state directory)
- [ ] Maine
- [x] [Maryland](https://marylandregionalaviation.aero/publications/)
- [ ] Massachusetts
- [ ] [Michigan](https://www.michigan.gov/mdot/travel/mobility/aeronautics/airports) (pdf broken - needs image recognized)
- [x] [Minnesota](https://www.dot.state.mn.us/aero/airportdirectory/index.html)
- [ ] Mississippi
- [x] [Missouri](https://www.modot.org/aviation-publications)
- [x] [Montana](https://www.mdt.mt.gov/aviation/airports.aspx)
- [x] [Nebraska](https://govdocs.nebraska.gov/epubs/A4000/D001.html)
- [x] [Nevada](https://www.dot.nv.gov/mobility/aviation/airport-directory)
- [ ] New Hampshire
- [ ] [New Jersey](https://www.nj.gov/transportation/freight/aviation/documents/NJDOTAirportDirectory.pdf)
- [ ] New Mexico
- [ ] New York
- [ ] North Carolina
- [x] [North Dakota](https://aero.nd.gov/publications/)
- [x] [Ohio](https://www.transportation.ohio.gov/programs/aviation/airports/airport-directory)
- [-] [Oklahoma](https://oklahoma.gov/aerospace/airports/find-an-airport.html) (no pdf)
- [x] [Oregon](https://www.oregon.gov/aviation/Pages/Reports.aspx)
- [-] [Pennsylvania](https://www.penndot.pa.gov/TravelInPA/airports-pa/Pages/default.aspx)  (no useful state directory)
- [ ] Rhode Island
- [ ] South Carolina
- [x] [South Dakota](https://dot.sd.gov/transportation/aviation/airport-information)
- [ ] Tennessee
- [x] [Texas](https://ftp.dot.state.tx.us/pub/txdot-info/avn/airport-directory-list.pdf)
- [-] Utah  (no useful state directory)
- [ ] Vermont
- [ ] Virginia
- [x] [Washington](https://wsdot.wa.gov/engineering-standards/all-manuals-and-standards/manuals/airport-guide)
- [ ] West Virginia
- [x] [Wisconsin](https://wisconsindot.gov/Pages/travel/air/airport-info/arptdir-city.aspx)
- [x] [Wyoming](https://www.dot.state.wy.us/home/aeronautics.html)

### Other Resources
- [FAA Chart Supplements](https://www.faa.gov/air_traffic/flight_info/aeronav/digital_products/dafd/)
- [VFR Charts](https://www.faa.gov/air_traffic/flight_info/aeronav/digital_products/vfr/)
- [CSVs, KMLs of US airports](https://hub.arcgis.com/documents/f74df2ed82ba4440a2059e8dc2ec9a5d/explore)
- [SkyVector](https://skyvector.com/)
- [VFR Map](https://vfrmap.com/)