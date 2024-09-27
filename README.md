# State General Aviation Airport Data

Parse state airport directories for attributes like Courtesy Car, Bicycles, Camping, Meals. Outputs data in a json for use in AirstripMap.com.

Data is as good as the state airport directories. Some notate cars, meals, bikes, and camping. Some do not.

## Instructions

1. Find the state airport directory
2. Copy paste a `parse_directory.py` `parse_state` function and update the state info and pdf location
3. Run the below commands. You'll need to play around with the text extraction (consider tesseract if needed, uncomment in `parse_state` function)
4. Make any adjustments needed (and update at the bottom of the `parse_directory` file for future runs. Replace/update in the `airport_info_state.csv` file.)

```sh
pip install -r requirements.txt
brew install poppler
brew install optipng

python3 parse_directory.py
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

- [x] Alabama (no useful state directory)
- [x] Alaska (no useful state directory)
- [x] [Arizona](https://azdot.gov/planning/airport-development/airports) (no useful state directory)
- [ ] [Arkansas](https://fly.arkansas.gov/airport-info.html) (individual links, needs compiled...)
- [x] [California](https://dot.ca.gov/programs/transportation-planning/division-of-transportation-planning/aeronautics) (no useful state directory)
- [x] [Colorado](https://www.codot.gov/programs/aeronautics/Periodicals/colorado-airport-directory)
- [x] [Connecticut](https://ctairports.org/airports/)  (no useful state directory)
- [x] [Delaware](https://deldot.gov/Programs/airports/pdfs/de_airport_directory_2009_2010.pdf)
- [x] [Florida](https://fdotwww.blob.core.windows.net/sitefinity/docs/default-source/topics/2019_directory.pdf)
- [x] [Georgia](https://www.dot.ga.gov/InvestSmart/Aviation/AirportAid/AirportDirectory.pdf) (imperfect parsing)
- [x] Hawaii (no useful state directory)
- [x] [Idaho](https://itd.idaho.gov/aero/)
- [x] Illinois (no useful state directory)
- [x] [Indiana](https://www.in.gov/indot/multimodal/aviation/indiana-public-use-airports/) (no useful state directory)
- [x] [Iowa](https://iowadot.gov/aviation/airport-information) (no useful state directory)
- [ ] [Kansas](https://www.ksdot.gov/Assets/wwwksdotorg/bureaus/divAviation/pdf/AirportDir.pdf) (doubled pdf)
- [x] [Kentucky](https://transportation.ky.gov/aviation/documents/airport-directory.pdf)
- [x] [Louisiana](https://wwwapps.dotd.la.gov/multimodal/aviation/airportdirectory.aspx) (no useful state directory)
- [x] [Maine](https://www.maine.gov/mdot/aviation/) (no useful state directory)
- [x] [Maryland](https://marylandregionalaviation.aero/publications/)
- [x] [Massachusetts](https://www.mass.gov/public-use-airports/locations) (no useful state directory)
- [x] [Michigan](https://www.michigan.gov/mdot/travel/mobility/aeronautics/airports)
- [x] [Minnesota](https://www.dot.state.mn.us/aero/airportdirectory/index.html)
- [x] Mississippi  (no useful state directory)
- [x] [Missouri](https://www.modot.org/aviation-publications)
- [x] [Montana](https://www.mdt.mt.gov/aviation/airports.aspx)
- [x] [Nebraska](https://govdocs.nebraska.gov/epubs/A4000/D001.html)
- [x] [Nevada](https://www.dot.nv.gov/mobility/aviation/airport-directory)
- [ ] [New Hampshire](https://www.dot.nh.gov/about-nh-dot/divisions-bureaus-districts/aeronautics/airport-directory) (individual links)
- [x] [New Jersey](https://www.nj.gov/transportation/freight/aviation/documents/NJDOTAirportDirectory.pdf)
- [ ] New Mexico [(none published, but kind of)](https://realfilef260a66b364d453e91ff9b3fedd494dc.s3.amazonaws.com/03b30a00-9999-46c6-92b6-8719de594652?AWSAccessKeyId=AKIAJBKPT2UF7EZ6B7YA&Expires=1721493497&Signature=z8VM%2Fhcyv2q1t3UQ4tQOce%2Bf8ak%3D&response-content-disposition=inline%3B%20filename%3D%22New%20Mexico%20Aviation%202022%20Technical%20Report.pdf%22&response-content-type=application%2Fpdf) and [here](https://idea.appliedpavement.com/hosting/newmexico/#path=2)
- [ ] [New York](https://www.dot.ny.gov/divisions/operating/opdm/aviation/repository/air_dir/toc.html) (individual pdf links)
- [x] [North Carolina](https://www.ncdot.gov/divisions/aviation/Documents/nc-airport-guide.pdf)
- [x] [North Dakota](https://aero.nd.gov/publications/)
- [x] [Ohio](https://www.transportation.ohio.gov/programs/aviation/airports/airport-directory)
- [x] [Oklahoma](https://oklahoma.gov/aerospace/airports/find-an-airport.html) (no pdf)
- [x] [Oregon](https://www.oregon.gov/aviation/Pages/Reports.aspx)
- [x] [Pennsylvania](https://www.penndot.pa.gov/TravelInPA/airports-pa/Pages/default.aspx)  (no useful state directory)
- [ ] Rhode Island
- [ ] [South Carolina](https://aeronautics.sc.gov/sites/default/files/2024-02/SC%20Aeronautics%20Pilots%20Book%202024%20%20PROOF3%20%281%29.pdf)
- [x] [South Dakota](https://dot.sd.gov/transportation/aviation/airport-information)
- [x] [Tennessee](https://www.tdot.tn.gov/PublicDocuments/aeronautics/Airport-directory.pdf)
- [x] [Texas](https://ftp.dot.state.tx.us/pub/txdot-info/avn/airport-directory-list.pdf)
- [x] Utah  (no useful state directory)
- [x] [Vermont](https://vtrans.vermont.gov/sites/aot/files/aviation/VASP_FINAL_2021-08-18.pdf)
- [x] [Virginia](https://doav.virginia.gov/airport-directory/) no useful state directory
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
- [Fly2Lunch](http://www.fly2lunch.com/index.php)
- [Pirep.io](https://pirep.io/) ***