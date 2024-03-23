# State General Aviation Airport Data

Parse state airport directories for attributes like Courtesy Car, Bicycles, Camping, Meals. Outputs data in a json blob for use in SkyPin.

Idaho and Montana directories notate cars, meals, bikes, and camping. Washington does not.

  - [ ] Oregon (good luck with text extraction)

## To Dos

- [ ] Missing a few images for Idaho
- [ ] Automate data fixes
- [ ] Add states

## Instructions

1. Find the state airport directory
2. Copy paste a `get_state_data.py` file and update the state info and pdf location
3. Run the below commands. You'll need to play around with the text extraction probably
4. Make any adjustments needed (and update at the bottom of the get_state_data file for future runs. Replace/update in the airport_info_state.csv file.)

```sh
pip install -r requirements.txt
brew install poppler

python3 get_state_data.py
python3 data_to_json.py
python3 combined_data.py data_id.json data_mt.json data_wa.json
cat combined_data.py | pbcopy
```

5. Then copy `data.json` to `wheretofly/public/data.json`
6. And copy over the images in `images_state` to `wheretofly/public/images/`


Airport data airports.csv from: https://ourairports.com/data/ 


**Dislaimer**: data subject to error, do not use for navigation purposes, etc, etc

----
### Directories

- Montana - https://www.mdt.mt.gov/aviation/airports.aspx
- Idaho - https://itd.idaho.gov/aero/
- Washington -https://wsdot.wa.gov/engineering-standards/all-manuals-and-standards/manuals/airport-guide
- Wyoming - https://www.dot.state.wy.us/home/aeronautics.html
- Oregon - https://www.oregon.gov/aviation/Pages/Reports.aspx