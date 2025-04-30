import pdfplumber
import pandas as pd
import requests
import os
import sys
import re
from pdf2image import convert_from_path
from PIL import Image


fl_url = ''
id_url = 'https://itd.idaho.gov/wp-content/uploads/2020/08/Airport-Facilities-Directory.pdf'
md_url = 'https://marylandregionalaviation.aero/wp-content/uploads/2023/09/Airport%20Directory%202023-24.pdf'
mn_url = 'https://www.dot.state.mn.us/aero/airportdirectory/documents/2024_Airport_Directory_and_Travel_Guide_23JAN24_lowres.pdf'
nd_url = ''
sd_url = ''
or_url = ''
tx_url = ''
wi_url = 'https://wisconsindot.gov/Documents/travel/air/airport-info/arptdir-all.pdf'
wy_url = 'https://drive.google.com/file/d/1s04nV-sgQ0J5bsz9d9yyxE2I1RP3k0ao/view'

airports_url = 'https://davidmegginson.github.io/ourairports-data/airports.csv'
airports_path = 'data/airports.csv'

def extract_page_info(page, text, state):
    # Initialize dictionary to hold extracted info
    airport_info = {
        "Airport Identifier": "",
        "Airport Name": "",
        "Courtesy Car": "No",
        "Bicycles": "No",
        "Camping": "No",
        "Meals": "No"
    }

    #import pdb
    #pdb.set_trace()

    match state:
        case "ar":
            lines = text.split('\n')
            print(lines)
            if lines:
                    # Assuming one of these lines contains the airport name
                    name = ", ".join(lines[0:2])
                    
                    print(name)
                    identmatch = re.search(r'([0-9A-Z]{3})[, ](.*),?', name)
                    if identmatch:
                        ident = identmatch.group(1)
                        ident = re.sub(r', LAT.*', '', ident)

                    namematch = re.search(r'([0-9A-Z]{3})[, ](.*),?', name)
                    if namematch:
                        nme = namematch.group(2)
                        nme = re.sub(r', LAT.*', '', nme)
                        #nme = (lambda s: (lambda w: next((' '.join(w[:-i]) for i in range(len(w)//2, 0, -1) if w[:i] == w[-i:]), s))(s.split()))(nme)
                        

                    print('name:', nme)
                    print('ident:', ident)

            if len(ident) > 4 or len(ident) < 3:
                print(f"Error parsing page {page} ({name})")
                #return #ignore for now, manually fix
            else:
                text = re.sub(r'^[^A-Za-z]+', '', text)
                airport_info["Airport Identifier"] = ident.strip().replace("Ø","0")
                airport_info["Airport Identifier"] = ident.strip().replace("@","0")
                airport_info["Airport Identifier"] = ident.strip().replace("$","S")
                nme = re.sub(r'^[^A-Za-z]+', '', nme)
                airport_info["Airport Name"] = nme.strip().title()

            for line in lines:
                # Check for amenities
                if "courtesy car" in line.lower() or "crew car" in line.lower() or "transportation" in line.lower():
                    airport_info["Courtesy Car"] = "Yes"
                if "camp" in line.lower() or "cabins" in line.lower():
                    airport_info["Camping"] = "Yes"
                mealmatch = re.search(r'food|restaurant', line.lower()) 
                if mealmatch:
                    airport_info["Meals"] = "Yes"
                if "bicycles" in line.lower() or "bikes" in line.lower():
                    airport_info["Bicycles"] = "Yes"

            return airport_info
        case "co":
                lines = text.split('\n')
                ident, nme = "", ""
                print(lines)
                if lines:
                    # Assuming one of these lines contains the airport name
                    name = lines[0]
                    identmatch = re.search(r'[A-Z-\'. ].*\ ([A-Z0-9Ø]{3})\ (.*)\ [A-Z-\'. ]', name)
                    if identmatch:
                        ident = identmatch.group(1)
                    else:
                        ident = name

                    namematch = re.search(r'[A-Z-\'. ].*\ ([A-Z0-9Ø]{3})\ (.*)\ [A-Z-\'. ]', name)
                    if namematch:
                        nme = namematch.group(2)
                        
                    print(ident)
                    print(nme)

                    if len(ident) > 4 or len(ident) < 3:
                        print(f"Error parsing page {page} ({name})")
                        #return #ignore for now, manually fix
                    else:
                        airport_info["Airport Identifier"] = ident.strip().replace("Ø","0")
                        airport_info["Airport Identifier"] = ident.strip().replace("@","0")
                        airport_info["Airport Name"] = nme.strip()
                
                for line in lines:
                    # Check for amenities
                    if "rental" in line.lower() or "courtesy" in line.lower() or "crew car" in line.lower() or "transportation" in line.lower():
                        airport_info["Courtesy Car"] = "Yes"
                    if "camping" in line.lower() or "campsite" in line.lower():
                        airport_info["Camping"] = "Yes"
                    mealmatch = re.search(r'on airport|\b1 mile', line) 
                    if mealmatch:
                        airport_info["Meals"] = "Yes"
                    if "bicycles" in line.lower() or "bikes" in line.lower():
                        airport_info["Bicycles"] = "Yes"

                return airport_info
        case "de":
                lines = text.split('\n')
                ident, nme = "", ""
                print(lines)
                if lines:
                    for line in lines:
                        # Assuming one of these lines contains the airport name
                        #name = lines[0]
                        identmatch = re.search(r'\(([A-Z0-9]{3})\)', line)
                        if identmatch:
                            ident = identmatch.group(1)

                        #namematch = re.search(r'\b([A-Za-z\s\.]+Airport)\s\(([A-Z0-9]{3})\)', line)
                        #if namematch:
                        #    nme = namematch.group(1)
                        nme = lines[0]
                        
                    print(ident)
                    print(nme)

                    if len(ident) > 4 or len(ident) < 3:
                        print(f"Error parsing page {page} ({lines[0]})")
                        #return #ignore for now, manually fix
                    else:
                        airport_info["Airport Identifier"] = ident.strip().replace("Ø","0")
                        airport_info["Airport Identifier"] = ident.strip().replace("@","0")
                        airport_info["Airport Name"] = nme.strip()
                
                for line in lines:
                    # Check for amenities
                    if "courtesy" in line.lower() or "crew car" in line.lower():
                        airport_info["Courtesy Car"] = "Yes"
                    if "camping" in line.lower() or "campsite" in line.lower():
                        airport_info["Camping"] = "Yes"
                    mealmatch = re.search(r'on airport|\b1 mile', line) 
                    if mealmatch:
                        airport_info["Meals"] = "Yes"
                    if "bicycles" in line.lower() or "bikes" in line.lower():
                        airport_info["Bicycles"] = "Yes"

                return airport_info
        case "id":
            lines = text.split('\n')
            print(lines)
            if lines:
                # Assuming the first line contains the airport name
                name = lines[0]
                ident = name.split(' ')[-1]
                nme = " ".join(name.split(' ')[0:-1])
                print(ident)
                print(nme)

                if len(ident) > 4 or len(ident) < 3:
                    print(f"Error parsing page {page} ({name})")
                    #return #ignore for now, manually fix
                else:
                    airport_info["Airport Identifier"] = ident.replace("Ø","0")
                    airport_info["Airport Identifier"] = ident.replace("1D","ID")
                    airport_info["Airport Name"] = nme
            
            for line in lines:
                # Check for amenities
                if "rental" in line.lower() or "courtesy" in line.lower() or "crew car" in line.lower():
                    airport_info["Courtesy Car"] = "Yes"
                if "camp" in line.lower() or "camping" in line.lower() or "campground" in line.lower():
                    airport_info["Camping"] = "Yes"
                if "meals" in line.lower() or "food" in line.lower():
                    airport_info["Meals"] = "Yes"
                if "bicycles" in line.lower() or "bikes" in line.lower():
                    airport_info["Bicycles"] = "Yes"

            return airport_info
        case "ia":
            lines = re.sub(r'\(cid:..?.?\)','', text)
            lines = lines.split('\n')
            print(lines)
            if lines:
                    # Assuming one of these lines contains the airport name
                    name = ", ".join(lines[0:3])
                    identmatch = re.search(r'^(.*?) \(([0-9A-Z]{3})\)', name)
                    if identmatch:
                        ident = identmatch.group(2)

                    namematch = re.search(r'^(.*?) \(([0-9A-Z]{3})\)', name)
                    if namematch:
                        nme = namematch.group(1)
                        #nme = (lambda s: (lambda w: next((' '.join(w[:-i]) for i in range(len(w)//2, 0, -1) if w[:i] == w[-i:]), s))(s.split()))(nme)
                        

                    print(nme)
                    print(ident)

            if len(ident) > 4 or len(ident) < 3:
                print(f"Error parsing page {page} ({name})")
                #return #ignore for now, manually fix
            else:
                airport_info["Airport Identifier"] = ident.strip().replace("Ø","0")
                airport_info["Airport Identifier"] = ident.strip().replace("@","0")
                airport_info["Airport Identifier"] = ident.strip().replace("$","S")
                airport_info["Airport Name"] = nme.strip()

            for line in lines:
                # Check for amenities
                if "courtesy car" in line.lower() or "crew car" in line.lower() or "transportation" in line.lower():
                    airport_info["Courtesy Car"] = "Yes"
                if "camping" in line.lower() or "cabins" in line.lower():
                    airport_info["Camping"] = "Yes"
                mealmatch = re.search(r'food|restaurant', line.lower()) 
                if mealmatch:
                    airport_info["Meals"] = "Yes"
                if "bicycles" in line.lower() or "bikes" in line.lower():
                    airport_info["Bicycles"] = "Yes"

            return airport_info
        case "fl":
            lines = text.split('\n')
            print(lines)
            if lines:
                # Assuming one of these lines contains the airport name
                identifier = " ".join(lines[0:4])
                identmatch = re.search(r'Identifier\ (....?)\ ', identifier)
                if identmatch:
                    ident = identmatch.group(1)

                nme = lines[1]

                print(nme)
                print(ident)

                if len(ident) > 4 or len(ident) < 3:
                    print(f"Error parsing page {page} ({nme})")
                    #return #ignore for now, manually fix
                else:
                    airport_info["Airport Identifier"] = ident.strip().replace("Ø","0")
                    airport_info["Airport Name"] = nme.strip()
            
            for line in lines:
                # Check for amenities
                if "rental car yes" in line.lower() or "courtesy car yes" in line.lower() or "crew car yes" in line.lower():
                    airport_info["Courtesy Car"] = "Yes"
                if "camping" in line.lower():
                    airport_info["Camping"] = "Yes"
                if "dining yes" in line.lower() or "restaurant" in line.lower():
                    airport_info["Meals"] = "Yes"
                if "bicycles" in line.lower() or "bikes" in line.lower():
                    airport_info["Bicycles"] = "Yes"

            return airport_info
        case "wy":
            lines = text.split('\n')
            print(lines)
            if lines:
                # Assuming one of these lines contains the airport name
                name = lines[-1]+lines[-2]+lines[0]+lines[1]
                identmatch = re.search(r'\((.*?)\)', name)
                if identmatch:
                    ident = identmatch.group(1)

                namematch = re.search(r'[/,]\s*([^/(]+)\s*\(', text)
                if namematch:
                    nme = namematch.group(1)

                print(nme)
                print(ident)

                if len(ident) > 4 or len(ident) < 3:
                    print(f"Error parsing page {page} ({name})")
                    #return #ignore for now, manually fix
                else:
                    airport_info["Airport Identifier"] = ident.strip().replace("Ø","0")
                    airport_info["Airport Name"] = nme.strip()
            
            for line in lines:
                # Check for amenities
                if "rental" in line.lower() or "courtesy car" in line.lower() or "crew car" in line.lower() or "transportation" in line.lower():
                    airport_info["Courtesy Car"] = "Yes"
                if "camping" in line.lower():
                    airport_info["Camping"] = "Yes"
                if "food-lodging(1mi)" in line.lower() or "food(1mi)" in line.lower() or "food(1/2mi)" in line.lower() or "food on field" in line.lower() or "restaurant" in line.lower():
                    airport_info["Meals"] = "Yes"
                if "bicycles" in line.lower() or "bikes" in line.lower():
                    airport_info["Bicycles"] = "Yes"

            return airport_info
        case "ga":
            lines = text.split('\n')
            print(lines)
            if lines:
                ident, nme = "", ""
                if re.findall('\s([A-Z0-9]{3})$', lines[0]) and len(lines[0])>8:
                    ident,name = lines[0],lines[0]
                else:
                    ident,name = lines[-2],lines[-2]

                if "-" in name:
                    identmatch = re.search(r'[A-Z|^].+\s?(\w+)\s?-\s?(\w.*)\s(\w\w\w)', ident)
                    if identmatch:
                        ident = identmatch.group(3)
                        nme = identmatch.group(2)
                else:
                    identmatch = re.search(r'[A-Z]\s(\w.*)\s(\w\w\w)$', ident)
                    if identmatch:
                        ident = identmatch.group(2)
                        nme = identmatch.group(1)

                if len(ident) > 4 or len(ident) < 3:
                    print(f"Error parsing page {page} ({name})")
                    #sys.exit(1)
                    return #ignore for now, manually fix
                else:
                    airport_info["Airport Identifier"] = ident.strip().replace("Ø","0")
                    airport_info["Airport Name"] = nme.strip()
            
                if ident == "LANI":
                    airport_info["Airport Name"] = "Turner County"
                    airport_info["Airport Identifier"] = "75J"
                if ident == "013":
                    airport_info["Airport Name"] = "Jimmy Carter Regional"
                    airport_info["Airport Identifier"] = "ACJ"
                if ident == "217":
                    airport_info["Airport Name"] = "Heart of Georgia Regional"
                    airport_info["Airport Identifier"] = "EZM"
                if ident == "—51—":
                    airport_info["Airport Name"] = "Griffin - Spalding County"
                    airport_info["Airport Identifier"] = "6A2"
                if ident == "ONI":
                    airport_info["Airport Name"] = "Telfair-Wheeler"
                    airport_info["Airport Identifier"] = "MQW"
                if ident == ".R.R":
                    airport_info["Airport Name"] = "Barrow County"
                    airport_info["Airport Identifier"] = "WDR"  

            print(nme)
            print(ident)

            for line in lines:
                carmatch = re.search(r'courtesy car', line.lower()) 
                if carmatch:
                    airport_info["Courtesy Car"] = "Yes"

                campmatch = re.search(r'camping', line.lower()) 
                if campmatch:
                    airport_info["Camping"] = "Yes"
                
                mealmatch = re.search(r'dining::.*(\(on-site\)|on field|\/.\d)', line.lower()) 
                if mealmatch:
                    airport_info["Meals"] = "Yes"
                
                if "bicycles" in line.lower() or "bikes" in line.lower():
                    airport_info["Bicycles"] = "Yes"

            return airport_info
        case "ky":
            lines = text.split('\n')
            print(lines)
            if lines:
                ident, nme = "", ""
                ident = lines[-1]
                name = lines[-1]

                identmatch = re.search(r'\w+ (\w+) \d\d$', ident)
                if identmatch:
                    ident = identmatch.group(1)

                namematch = re.search(r'(^\w.*) \w\w\w \d\d$', name)
                if namematch:
                    nme = namematch.group(1)

                if len(ident) > 4 or len(ident) < 3:
                    print(f"Error parsing page {page} ({name})")
                    return #ignore for now, manually fix
                else:
                    airport_info["Airport Identifier"] = ident.strip().replace("Ø","0")
                    airport_info["Airport Name"] = nme.strip()
            
            print(nme)
            print(ident)

            for line in lines:
                carmatch = re.search(r'ccrreeww ccaarr:: yes', line.lower()) 
                if carmatch:
                    airport_info["Courtesy Car"] = "Yes"

                campmatch = re.search(r'camping', line.lower()) 
                if campmatch:
                    airport_info["Camping"] = "Yes"
                
                mealmatch = re.search(r'ddiinniinngg::.*(\(on-site\)|on field|\/.\d)', line.lower()) 
                if mealmatch:
                    airport_info["Meals"] = "Yes"
                
                if "bicycles" in line.lower() or "bikes" in line.lower():
                    airport_info["Bicycles"] = "Yes"

            return airport_info
        case "ks":
            lines = text.split('\n')
            print(lines)
            if lines:
                    # Assuming one of these lines contains the airport name
                    name = ", ".join(lines[1:3])
                    #identmatch = re.search(r'\((.*?)\)', name)
                    identmatch = re.search(r'^(.*?)\b([0-9A-Z]{3})\b', name)
                    if identmatch:
                        ident = identmatch.group(2)

                    namematch = re.search(r'^(.*?)\b([0-9A-Z]{3})\b', name)
                    if namematch:
                        nme = namematch.group(1)
                        nme = (lambda s: (lambda w: next((' '.join(w[:-i]) for i in range(len(w)//2, 0, -1) if w[:i] == w[-i:]), s))(s.split()))(nme)
                        

                    print(nme)
                    print(ident)

            if len(ident) > 4 or len(ident) < 3:
                print(f"Error parsing page {page} ({name})")
                #return #ignore for now, manually fix
            else:
                airport_info["Airport Identifier"] = ident.strip().replace("Ø","0")
                airport_info["Airport Identifier"] = ident.strip().replace("@","0")
                airport_info["Airport Identifier"] = ident.strip().replace("$","S")
                airport_info["Airport Name"] = nme.strip()
                if "HOLCOMB" in nme:
                        airport_info["Airport Name"] = "Private"
            
            for line in lines:
                # Check for amenities
                if "rental" in line.lower() or "courtesy car" in line.lower() or "crew car" in line.lower() or "transportation" in line.lower():
                    airport_info["Courtesy Car"] = "Yes"
                if "camping" in line.lower() or "cabins" in line.lower():
                    airport_info["Camping"] = "Yes"
                mealmatch = re.search(r'food|restaurant', line.lower()) 
                if mealmatch:
                    airport_info["Meals"] = "Yes"
                if "bicycles" in line.lower() or "bikes" in line.lower():
                    airport_info["Bicycles"] = "Yes"

            return airport_info
        case "md":
            lines = text.split('\n')
            print(lines)
            if lines:
                # Assuming one of these lines contains the airport name
                nme = lines[0]
                if "St. Mary’s" in nme: nme = "St. Mary's" # why
                if "/" in nme: nme = lines[0].split('/')[-1].strip()
                if "-" in nme: nme = lines[0].split('-')[-1].strip()
                identstr = "_"+ "_".join(lines[-15:-1])+"_" # wow
                print(identstr)
                idmatch = re.search(r"[_\/-]{}.*?(\w\w\w)_".format(re.escape(nme)), identstr)
                if idmatch:
                    ident = idmatch.group(1)        
                
                print(nme)
                print(ident)

                if len(ident) > 4 or len(ident) < 3:
                    print(f"Error parsing page {page} ({nme})")
                    #return #ignore for now, manually fix
                else:
                    airport_info["Airport Identifier"] = ident.strip().replace("Ø","0")
                    airport_info["Airport Name"] = nme.strip()
            
            for line in lines:
                # Check for amenities
                if "rental" in line.lower() or "courtesy" in line.lower() or "crew car" in line.lower():
                    airport_info["Courtesy Car"] = "Yes"
                if "camping" in line.lower():
                    airport_info["Camping"] = "Yes"
                if "restaurant" in line.lower():
                    airport_info["Meals"] = "Yes"
                if "bicycles" in line.lower() or "bikes" in line.lower():
                    airport_info["Bicycles"] = "Yes"

            return airport_info
        case "mi":
            lines = text.split('\n')
            print(lines)
            if lines:
                ident, nme = "", ""
                name = lines[0]
                identmatch = re.search(r'[^,](\w+\s?){1,3} _?\((\w+)\)?', name)
                if identmatch:
                    ident = identmatch.group(2)

                namematch = re.search(r'([^,]+(\w\s?){1,3}) \(\w+\)', name)
                if namematch:
                    nme = namematch.group(1)

                if len(ident) > 4 or len(ident) < 3:
                    print(f"Error parsing page {page} ({name})")
                    sys.exit(1)
                    #return #ignore for now, manually fix
                else:
                    airport_info["Airport Identifier"] = ident.strip().replace("Ø","0")
                    airport_info["Airport Name"] = nme.strip()

                if ident == "FNT":
                    airport_info["Airport Name"] = "Bishop Intl" 

                # Y98,GRAND MARAIS,No,No,Yes,No
                # IRS,KIRSCH,No,No,No,No,No
                # LWA,SOUTH HAVEN,No,No,No,No,No
                # MI8,SAULT STE. MARIE,Yes,No,Yes,Yes,Yes
                # MBS,SAGINAW,No,No,No,No,No
                # PTK,OAKLAND COUNTY INT’L,Yes,No,No,No,Yes
                # 1D2,CANTON-PLYMOUTH-METTETAL,Yes,No,No,No,Yes
                # OGM,ONTONAGON,Yes,No,Yes,Yes,Yes
                # 6Y5,TWO HEARTED,No,No,No,Yes,No
                # 2E2,Sharpe's Strip,Yes,No,No,No


            for line in lines:
                # Check for amenities
                # 27 TRANSP (TRANSPORTATION), CC == Courtesy car
                # RON (REMAIN OVER NIGHT)
                # TRNSP: CC, Rntl car
                
                carmatch = re.search(r'trnsp: cc|rntl car|courtesy car]', line.lower()) 
                if carmatch:
                    airport_info["Courtesy Car"] = "Yes"

                campmatch = re.search(r'camping', line.lower()) 
                if campmatch:
                    airport_info["Camping"] = "Yes"
                
                mealmatch = re.search(r'meals: in town, [0.5|0.75|1.0]|meals: adj', line.lower()) 
                if mealmatch:
                    airport_info["Meals"] = "Yes"
                
                if "bicycles" in line.lower() or "bikes" in line.lower():
                    airport_info["Bicycles"] = "Yes"

            return airport_info
        case "mo":
            lines = text.split('\n')
            print(lines)
            if lines:
                # Assuming one of these lines contains the airport name
                nme = lines[1]
                ident = lines[2]
                # identmatch = re.search(r'\w+\s-\s(\w+)', name)
                # if identmatch:
                #     ident = identmatch.group(1)

                # namematch = re.search(r'(\w+)\s-\s\w+', name)
                # if namematch:
                #     nme = namematch.group(1)

                print(nme)
                print(ident)

                if len(ident) > 4 or len(ident) < 3:
                    print(f"Error parsing page {page} ({name})")
                    #return #ignore for now, manually fix
                else:
                    airport_info["Airport Identifier"] = ident.strip().replace("Ø","0")
                    airport_info["Airport Name"] = nme.strip()
            
            for line in lines:
                # Check for amenities
                if "courtesy car: yes" in line.lower() or "car rental: yes" in line.lower():
                    airport_info["Courtesy Car"] = "Yes"
                campmatch = re.search(r'overnight camping.+: yes', line.lower()) 
                if campmatch:
                    airport_info["Camping"] = "Yes"
                
                mealmatch = re.search(r'numerous dining facilities in area|dining:.+\s[½¼1]', line.lower()) 
                if mealmatch:
                    airport_info["Meals"] = "Yes"
                
                if "bicycles" in line.lower() or "bikes" in line.lower():
                    airport_info["Bicycles"] = "Yes"

            return airport_info
        case "mn":
            lines = text.split('\n')
            print(lines)
            if lines:
                # Assuming one of these lines contains the airport name
                name = lines[0]
                identmatch = re.search(r'\w+\s-\s(\w+)', name)
                if identmatch:
                    ident = identmatch.group(1)

                namematch = re.search(r'(\w+)\s-\s\w+', name)
                if namematch:
                    nme = namematch.group(1)

                print(nme)
                print(ident)

                if len(ident) > 4 or len(ident) < 3:
                    print(f"Error parsing page {page} ({name})")
                    #return #ignore for now, manually fix
                else:
                    airport_info["Airport Identifier"] = ident.strip().replace("Ø","0")
                    airport_info["Airport Name"] = nme.strip()
            
            for line in lines:
                # Check for amenities
                if "courtesy car" in line.lower() or "crew car" in line.lower() or "transportation" in line.lower():
                    airport_info["Courtesy Car"] = "Yes"
                campmatch = re.search(r'campgrounds:.+\s[½¼1]|underwing camp: yes', line.lower()) 
                if campmatch:
                    airport_info["Camping"] = "Yes"
                
                mealmatch = re.search(r'dining:.+\s[½¼1]', line.lower()) 
                if mealmatch:
                    airport_info["Meals"] = "Yes"
                
                if "bicycles" in line.lower() or "bikes" in line.lower():
                    airport_info["Bicycles"] = "Yes"

            return airport_info
        case "nc":
                lines = text.split('\n')
                print(lines)
                if lines:
                    # Assuming one of these lines contains the airport name
                    name = lines[0]
                    identmatch = re.search(r'- (\w{3})$', name)
                    if identmatch:
                        ident = identmatch.group(1)

                    namematch = re.search(r'^(.*?) -', name)
                    if namematch:
                        nme = namematch.group(1)

                    print(nme)
                    print(ident)

                    if len(ident) > 4 or len(ident) < 3:
                        print(f"Error parsing page {page} ({name})")
                        #return #ignore for now, manually fix
                    else:
                        airport_info["Airport Identifier"] = ident.strip().replace("Ø","0")
                        airport_info["Airport Name"] = nme.strip()
                
                for line in lines:
                    # Check for amenities
                    if "rental" in line.lower() or "courtesy car" in line.lower() or "crew car" in line.lower() or "transportation" in line.lower():
                        airport_info["Courtesy Car"] = "Yes"
                    if "camping" in line.lower() or "cabins" in line.lower():
                        airport_info["Camping"] = "Yes"
                    mealmatch = re.search(r'restaurant', line) 
                    if mealmatch:
                        airport_info["Meals"] = "Yes"
                    if "bicycles" in line.lower() or "bikes" in line.lower():
                        airport_info["Bicycles"] = "Yes"

                return airport_info
        case "mt":
            lines = text.split('\n')
            print(lines)
            if lines:
                identmatch = re.search(r'IDENT:\s(\w\w\w)', text)
                if identmatch:
                    ident = identmatch.group(1).replace("Ø","0")

                nme = lines[-1]

                print(nme)
                print(ident)

                if len(ident) > 4 or len(ident) < 3:
                    print(f"Error parsing page {i} ({nme})")
                    #return #ignore for now, manually fix
                else:
                    airport_info["Airport Identifier"] = ident.strip().replace("Ø","0")
                    airport_info["Airport Name"] = nme.strip()
            
            for line in lines:
                # Extracting the identifier
                if "IDENT:" in line:
                    parts = line.split()
                    ident_index = parts.index("IDENT:") + 1
                    if ident_index < len(parts):
                        airport_info["Airport Identifier"] = parts[ident_index]
                # Check for amenities
                if "rental" in line.lower() or "courtesy" in line.lower() or "crew car" in line.lower():
                    airport_info["Courtesy Car"] = "Yes"
                if "camping" in line.lower() or "campsite" in line.lower() or "campground" in line.lower() or "cabins" in line.lower():
                    airport_info["Camping"] = "Yes"
                mealmatch = re.search(r'service:.+[A-Za-z]\s[½¼1]|adjacent|on field', line.lower())
                if mealmatch:
                    airport_info["Meals"] = "Yes"
                if "bicycles" in line.lower() or "bikes" in line.lower():
                    airport_info["Bicycles"] = "Yes"
            
            if airport_info["Airport Identifier"] == "8S1":
                airport_info["Courtesy Car"] = "Yes"
            if airport_info["Airport Identifier"] == "DLN":
                airport_info["Courtesy Car"] = "Yes"
            if airport_info["Airport Identifier"] == "8U4":
                airport_info["Camping"] = "Yes"

            return airport_info      
        case "oh":
            lines = text.split('\n')
            print(lines)
            if lines:
                ident, nme = "", ""
                ident = lines[0]
                name = lines[1]

                identmatch = re.search(r'\w+ (\w+)$', ident)
                if identmatch:
                    ident = identmatch.group(1)

                # namematch = re.search(r'[^,]((\w+\s?){1,3}) \(\w+\)', name)
                # if namematch:
                #     nme = namematch.group(1)

                if len(ident) > 4 or len(ident) < 3:
                    print(f"Error parsing page {page} ({name})")
                    return #ignore for now, manually fix
                else:
                    airport_info["Airport Identifier"] = ident.strip().replace("Ø","0")
                    airport_info["Airport Name"] = nme.strip()

            for line in lines:
                
                carmatch = re.search(r'courtesy car|courtesy transportation', line.lower()) 
                if carmatch:
                    airport_info["Courtesy Car"] = "Yes"

                campmatch = re.search(r'camping', line.lower()) 
                if campmatch:
                    airport_info["Camping"] = "Yes"
                
                mealmatch = re.search(r'restaurant within 2 miles', line.lower()) 
                if mealmatch:
                    airport_info["Meals"] = "Yes"
                
                if "bicycles" in line.lower() or "bikes" in line.lower():
                    airport_info["Bicycles"] = "Yes"

            return airport_info
        case "ne":
            lines = text.split('\n')
            print(lines)
            if lines:
                name = lines[0]
                if "(" not in name:
                    name = lines[1] #stupid
                namematch = re.search(r'^([a-zA-Z\'-].*)\(\w+\)', name)
                if namematch:
                    nme = namematch.group(1)
                identmatch = re.search(r'^[a-zA-Z\'-].*\((\w+)\)', name)
                if identmatch:
                    ident = identmatch.group(1)

                print(nme)
                print(ident)

                if len(ident) > 4 or len(ident) < 3:
                    print(f"Error parsing page {page} ({name})")
                    #return #ignore for now, manually fix
                else:
                    airport_info["Airport Identifier"] = ident.strip().replace("Ø","0")
                    airport_info["Airport Name"] = nme.strip()
            
            for line in lines:
                # Check for amenities
                if "courtesy vehicle" in line.lower() or "car rental: yes" in line.lower():
                    airport_info["Courtesy Car"] = "Yes"
                campmatch = re.search(r'overnight camping.+: yes', line.lower()) 
                if campmatch:
                    airport_info["Camping"] = "Yes"
                
                mealmatch = re.search(r'numerous dining facilities in area|dining:.+\s[½¼1]', line.lower()) 
                if mealmatch:
                    airport_info["Meals"] = "Yes"
                
                if "bicycles" in line.lower() or "bikes" in line.lower():
                    airport_info["Bicycles"] = "Yes"

            return airport_info
        case "nj":
            lines = text.split('\n')
            ident, nme = "", ""
            print(lines)
            if lines:
                # Assuming one of these lines contains the airport name
                name = ",".join(lines[0:10])
                identmatch = re.search(r'\((.*?)\)', name)
                if identmatch:
                    ident = identmatch.group(1)
                # else:
                #     ident = name

                namematch = re.search(r'\b([A-Z0-9- ]+)\b', lines[0])
                if namematch:
                    nme = namematch.group(1)
                    
                print(ident)
                print(nme)

                if len(ident) > 4 or len(ident) < 3:
                    print(f"Error parsing page {page} ({name})")
                    #return #ignore for now, manually fix
                else:
                    airport_info["Airport Identifier"] = ident.strip().replace("Ø","0")
                    airport_info["Airport Identifier"] = ident.strip().replace("@","0")
                    airport_info["Airport Name"] = nme.strip()
            
            for line in lines:
                # Check for amenities
                if "rental" in line.lower() or "courtesy" in line.lower() or "crew car" in line.lower() or "transportation" in line.lower():
                    airport_info["Courtesy Car"] = "Yes"
                if "camping" in line.lower() or "cabins" in line.lower():
                    airport_info["Camping"] = "Yes"
                mealmatch = re.search(r'restaurant', line) 
                if mealmatch:
                    airport_info["Meals"] = "Yes"
                if "bicycles" in line.lower() or "bikes" in line.lower():
                    airport_info["Bicycles"] = "Yes"

            return airport_info
        case "nv":
            lines = text.split('\n')
            print(lines)
            # if lines:
            #     name = lines[0]
            #     if "(" not in name:
            #         name = lines[1] #stupid
            #     namematch = re.search(r'^([a-zA-Z\'-].*)\(\w+\)', name)
            #     if namematch:
            #         nme = namematch.group(1)
            #     identmatch = re.search(r'^[a-zA-Z\'-].*\((\w+)\)', name)
            #     if identmatch:
            #         ident = identmatch.group(1)

            #     print(nme)
            #     print(ident)

            #     if len(ident) > 4 or len(ident) < 3:
            #         print(f"Error parsing page {page} ({name})")
            #         #return #ignore for now, manually fix
            #     else:
            #        airport_info["Airport Identifier"] = ident.strip().replace("Ø","0")
            #        airport_info["Airport Name"] = nme.strip()
            
            ident = ""
            for line in lines:
                if len(line) == 3 and ident == "":
                    print(line)
                    ident = line
                    airport_info["Airport Identifier"] = ident.strip().replace("Ø","0")
                    if len(ident) > 4 or len(ident) < 3:
                        print(f"Error parsing page {page} ({name})")
                namematch = re.search(r'^([a-zA-Z\'-].*)\(\w+\)', line)
                if namematch:
                    nme = namematch.group(1)
                    print(nme)
                    airport_info["Airport Name"] = nme.strip()
                if ident == "01U":
                    airport_info["Airport Name"] = "DUCKWATER AIRPORT"
                if ident == "A34":
                    airport_info["Airport Name"] = "Dayton Valley Airpark"
                if ident == "ELY":
                    airport_info["Airport Name"] = "ELY/YELLAND FIELD"
                if ident == "0L4":
                    airport_info["Airport Name"] = "Lida Juncion Airport"
                if ident == "LAS":
                    airport_info["Airport Name"] = "McCarran International"
                if ident == "MEV":
                    airport_info["Airport Name"] = "Minden-Tahoe Airport"
                if ident == "VGT":
                    airport_info["Airport Name"] = "North Las Vegas Airport"
                if ident == "U08":
                    airport_info["Airport Name"] = "Perkins Field"
                if ident == "RTS":
                    airport_info["Airport Name"] = "Reno-Stead Airport"
                if ident == "N59":
                    airport_info["Airport Name"] = "Rosaschi Airpark"
                if ident == "3L2":
                    airport_info["Airport Name"] = "Sky Ranch Estates"
                if ident == "LWL":
                    airport_info["Airport Name"] = "Sky Ranch Estates"

                # Check for amenities
                if "courtesy car" in line.lower() or "car rental" in line.lower():
                    airport_info["Courtesy Car"] = "Yes"
                campmatch = re.search(r'overnight camping.+: fyes', line.lower()) 
                if campmatch:
                    airport_info["Camping"] = "Yes"
                
                mealmatch = re.search(r'restaurants: yes', line.lower()) 
                if mealmatch:
                    airport_info["Meals"] = "Yes"
                
                if "bicycles" in line.lower() or "bikes" in line.lower():
                    airport_info["Bicycles"] = "Yes"

            return airport_info
        case "nd":
            lines = text.split('\n')
            print(lines)
            if lines:
                # Assuming one of these lines contains the airport name
                ident = lines[1]
                nme = lines[2]

                print(nme)
                print(ident)

                if len(ident) > 4 or len(ident) < 3:
                    print(f"Error parsing page {page} ({nme})")
                    #return #ignore for now, manually fix
                else:
                    airport_info["Airport Identifier"] = ident.strip().replace("Ø","0")
                    airport_info["Airport Name"] = nme.strip()
            
            for line in lines:
                if "rental" in line.lower() or "courtesy car" in line.lower() or "transportation" in line.lower():
                    airport_info["Courtesy Car"] = "Yes"
                
                campmatch = re.search(r'campgrounds:.+\s[½¼1]|underwing camp: yes', line.lower()) 
                if campmatch:
                    airport_info["Camping"] = "Yes"
                
                mealmatch = re.search(r'dining:.+\s[½¼1]', line.lower()) 
                if mealmatch:
                    airport_info["Meals"] = "Yes"
                
                if "bicycles" in line.lower() or "bikes" in line.lower():
                    airport_info["Bicycles"] = "Yes"

            return airport_info
        case "ny":
                lines = text.split('\n')
                print(lines)
                if lines:
                    ident = lines[4]
                    #Assuming one of these lines contains the airport name
                    ident = ",".join(lines[0:10])
                    #print("ident ", ident)
                    identmatch = re.search(r'[, ^]([\w$@]{3})[, \n$]', ident)
                    if identmatch:
                        ident = identmatch.group(1)

                    namematch = re.search(r'(.*)', lines[0])
                    #print("name ", lines[0])
                    if namematch:
                        nme = namematch.group(1)
                        nme = (lambda s: (lambda w: next((' '.join(w[:-i]) for i in range(len(w)//2, 0, -1) if w[:i] == w[-i:]), s))(s.split()))(nme)
                        
                    print(ident)
                    print(nme)

                    if len(ident) > 4 or len(ident) < 3:
                        print(f"Error parsing page {page} ({name})")
                        #return #ignore for now, manually fix
                    else:
                        airport_info["Airport Identifier"] = ident.strip().replace("Ø","0")
                        airport_info["Airport Identifier"] = ident.strip().replace("@","0")
                        airport_info["Airport Identifier"] = ident.strip().replace("$","S")
                        airport_info["Airport Name"] = nme.strip()
                        if "HOLCOMB" in nme:
                             airport_info["Airport Name"] = "Private"
                
                for line in lines:
                    # Check for amenities
                    if "rental" in line.lower() or "courtesy car" in line.lower() or "crew car" in line.lower() or "transportation" in line.lower():
                        airport_info["Courtesy Car"] = "Yes"
                    if "camping" in line.lower() or "cabins" in line.lower():
                        airport_info["Camping"] = "Yes"
                    mealmatch = re.search(r'food|on airport', line) 
                    mealmatch = re.search(r'OFF - ?[0.5 MILE|0.25 MILE|1 MILE|ON AIRPORT]', line) 
                    if mealmatch:
                        airport_info["Meals"] = "Yes"
                    if "bicycles" in line.lower() or "bikes" in line.lower():
                        airport_info["Bicycles"] = "Yes"

                return airport_info
        case "or":
            return "not implemented"
        case "sc":
                lines = text.split('\n')
                print(lines)
                if lines:
                    # Assuming one of these lines contains the airport name
                    name = lines[0]
                    identmatch = re.search(r'^([\w$@]{3}) -', name)
                    if identmatch:
                        ident = identmatch.group(1)

                    namematch = re.search(r'^[^-]+ - (.*?)(?: - \d+)?$', name)
                    if namematch:
                        nme = namematch.group(1)
                        nme = (lambda s: (lambda w: next((' '.join(w[:-i]) for i in range(len(w)//2, 0, -1) if w[:i] == w[-i:]), s))(s.split()))(nme)

                    print(nme)
                    print(ident)

                    if len(ident) > 4 or len(ident) < 3:
                        print(f"Error parsing page {page} ({name})")
                        #return #ignore for now, manually fix
                    else:
                        airport_info["Airport Identifier"] = ident.strip().replace("Ø","0")
                        airport_info["Airport Identifier"] = ident.strip().replace("@","0")
                        airport_info["Airport Identifier"] = ident.strip().replace("$","S")
                        airport_info["Airport Name"] = nme.strip()
                        if airport_info["Airport Name"] == "173": airport_info["Airport Name"] = "T73"
                
                for line in lines:
                    # Check for amenities
                    if "rental" in line.lower() or "courtesy car" in line.lower() or "crew car" in line.lower() or "transportation" in line.lower():
                        airport_info["Courtesy Car"] = "Yes"
                    if "camping" in line.lower() or "cabins" in line.lower():
                        airport_info["Camping"] = "Yes"
                    mealmatch = re.search(r'restaurant', line) 
                    if mealmatch:
                        airport_info["Meals"] = "Yes"
                    if "bicycles" in line.lower() or "bikes" in line.lower():
                        airport_info["Bicycles"] = "Yes"

                return airport_info
        case "sd":
            lines = text.split('\n')
            print(lines)
            if lines:
                # Assuming one of these lines contains the airport name
                namestr = lines[0]
                ident = namestr.split(" ")[-1]
                nme = " ".join(namestr.split(" ")[1:-1])

                print(nme)
                print(ident)

                if len(ident) > 4 or len(ident) < 3:
                    print(f"Error parsing page {page} ({nme})")
                    #return #ignore for now, manually fix
                else:
                    airport_info["Airport Identifier"] = ident.strip().replace("Ø","0")
                    airport_info["Airport Name"] = nme.strip()
            
            for line in lines:
                # Check for amenities
                if "rental" in line.lower() or "courtesy" in line.lower() or "crew car" in line.lower():
                    airport_info["Courtesy Car"] = "Yes"
                if "camping" in line.lower():
                    airport_info["Camping"] = "Yes"
                if "dining: " in line.lower():
                    airport_info["Meals"] = "Yes"
                if "bicycles" in line.lower() or "bikes" in line.lower():
                    airport_info["Bicycles"] = "Yes"

            return airport_info
        case "tn":
                lines = text.split('\n')
                ident, nme = "", ""
                print(lines)
                if lines:
                    # Assuming one of these lines contains the airport name
                    name = lines[0]
                    identmatch = re.search(r'^(.*?)\-([A-Z0-9@]{2,3}) .*? \- (\d+)$', name)
                    if identmatch:
                        ident = identmatch.group(2)
                    else:
                        ident = name

                    namematch = re.search(r'^(.*?)\-([A-Z0-9@]{2,3}) .*? \- (\d+)$', name)
                    if namematch:
                        nme = namematch.group(1)
                        
                    print(ident)
                    print(nme)

                    if len(ident) > 4 or len(ident) < 3:
                        print(f"Error parsing page {page} ({name})")
                        #return #ignore for now, manually fix
                    else:
                        airport_info["Airport Identifier"] = ident.strip().replace("Ø","0")
                        airport_info["Airport Identifier"] = ident.strip().replace("@","0")
                        airport_info["Airport Name"] = nme.strip()
                
                for line in lines:
                    # Check for amenities
                    if "rental" in line.lower() or "courtesy" in line.lower() or "crew car" in line.lower() or "transportation" in line.lower():
                        airport_info["Courtesy Car"] = "Yes"
                    if "camping" in line.lower() or "cabins" in line.lower():
                        airport_info["Camping"] = "Yes"
                    mealmatch = re.search(r'restaurant', line) 
                    if mealmatch:
                        airport_info["Meals"] = "Yes"
                    if "bicycles" in line.lower() or "bikes" in line.lower():
                        airport_info["Bicycles"] = "Yes"

                return airport_info
        case "tx":
                lines = text.split('\n')
                print(lines)
                if lines:
                    # Assuming one of these lines contains the airport name
                    name = lines[-1]+lines[-2]+lines[0]+lines[1]
                    identmatch = re.search(r'\((.*?)\)', name)
                    if identmatch:
                        ident = identmatch.group(1)

                    namematch = re.search(r'[/,]\s*([^/(]+)\s*\(', text)
                    if namematch:
                        nme = namematch.group(1)

                    print(nme)
                    print(ident)

                    if len(ident) > 4 or len(ident) < 3:
                        print(f"Error parsing page {page} ({name})")
                        #return #ignore for now, manually fix
                    else:
                        airport_info["Airport Identifier"] = ident.strip().replace("Ø","0")
                        airport_info["Airport Name"] = nme.strip()
                
                for line in lines:
                    # Check for amenities
                    if "rental" in line.lower() or "courtesy car" in line.lower() or "crew car" in line.lower() or "transportation" in line.lower():
                        airport_info["Courtesy Car"] = "Yes"
                    if "camping" in line.lower() or "cabins" in line.lower():
                        airport_info["Camping"] = "Yes"
                    mealmatch = re.search(r'FOOD-LODGING\([½¼1]MI|1\/2MI|1\/4 ?MI|1\/2|ON FIELD\)', line) 
                    if mealmatch:
                        airport_info["Meals"] = "Yes"
                    if "bicycles" in line.lower() or "bikes" in line.lower():
                        airport_info["Bicycles"] = "Yes"

                return airport_info
        case "wi":
            lines = text.split('\n')
            print(lines)
            if lines:
                # Assuming one of these lines contains the airport name
                name = " ".join(lines[0:2])
                print(name)
                identmatch = re.search(r'\((.*?)\)', name)
                if identmatch:
                    ident = identmatch.group(1)

                namematch = re.search(r'\d+\s?\d?\s+(.*?)\s+\(', name)
                if namematch:
                    nme = namematch.group(1)

                if "Airport Diagram" in nme:
                    return
                
                print(nme)
                print(ident)

                if len(ident) > 4 or len(ident) < 3:
                    print(f"Error parsing page {page} ({name})")
                    #return #ignore for now, manually fix
                else:
                    airport_info["Airport Identifier"] = ident.strip().replace("Ø","0")
                    airport_info["Airport Name"] = nme.strip()
            
            for line in lines:
                # Check for amenities
                if "rental" in line.lower() or "courtesy car" in line.lower() or "crew car" in line.lower():
                    airport_info["Courtesy Car"] = "Yes"
                if "camping" in line.lower():
                    airport_info["Camping"] = "Yes"
                if "food" in line.lower() or "restaurant" in line.lower():
                    airport_info["Meals"] = "Yes"
                if "bicycles" in line.lower() or "bikes" in line.lower():
                    airport_info["Bicycles"] = "Yes"

            return airport_info
        case "vt":
                lines = text.split('\n')
                ident, nme = "", ""
                print(lines)
                if lines:
                    for line in lines:
                        # Assuming one of these lines contains the airport name
                        #name = lines[0]
                        identmatch = re.search(r'\b([A-Za-z\s\.]+Airport)\s\(([A-Z0-9]{3})\)', line)
                        if identmatch:
                            ident = identmatch.group(2)

                        namematch = re.search(r'\b([A-Za-z\s\.]+Airport)\s\(([A-Z0-9]{3})\)', line)
                        if namematch:
                            nme = namematch.group(1)
                        
                    print(ident)
                    print(nme)

                    if len(ident) > 4 or len(ident) < 3:
                        print(f"Error parsing page {page} ({lines[1]})")
                        #return #ignore for now, manually fix
                    else:
                        airport_info["Airport Identifier"] = ident.strip().replace("Ø","0")
                        airport_info["Airport Identifier"] = ident.strip().replace("@","0")
                        airport_info["Airport Name"] = nme.strip()
                
                for line in lines:
                    # Check for amenities
                    if "courtesy" in line.lower() or "crew car" in line.lower():
                        airport_info["Courtesy Car"] = "Yes"
                    if "camping" in line.lower() or "campsite" in line.lower():
                        airport_info["Camping"] = "Yes"
                    mealmatch = re.search(r'on airport|\b1 mile', line) 
                    if mealmatch:
                        airport_info["Meals"] = "Yes"
                    if "bicycles" in line.lower() or "bikes" in line.lower():
                        airport_info["Bicycles"] = "Yes"

                return airport_info            
        case _:
            return "Not implemented"  

def parse_state(airport_data, state, directory_url, method, start_page, end_page):
    pdf = f'directories/{state}.pdf'
    out = f'data/airport_info_{state}.csv'
    imgDir = f'images/{state}/'

    # dl if we need 
    if not os.path.exists(pdf):
        download_pdf(directory_url, pdf)

    with pdfplumber.open(pdf) as pdff:
        total_pages = len(pdff.pages)
        print(f"Total pages: {total_pages}")
        if method == "pairs":
            for i in range(start_page - 1, total_pages - (total_pages - end_page) - 1): # pairs of pages
                if (i - start_page + 1) % 2 == 0:  # every other
                    current_page_text = pdff.pages[i].extract_text() if pdff.pages[i] else ""
                    next_page_text = pdff.pages[i + 1].extract_text() if i + 1 < len(pdff.pages) else ""  # Handle the last page case
                    text = current_page_text + " " + next_page_text
                    if text:
                        airport_info = extract_page_info(i, text, state)
                        if airport_info:
                            airport_data.append(airport_info)
                            id = airport_info.get("Airport Identifier")
                            id = id.replace("Ø","0")
                            if id:
                                save_combined_image(pdf, i + 1, i + 2, id, imgDir)  # Adjust indices as necessary
                if i >= (total_pages - (total_pages - end_page) - 1):  # Check if it's time to break after processing pairs
                    break
        else:
            #from PIL import Image
            import pytesseract
            for i, page in enumerate(pdff.pages[start_page-1:], start=start_page):
                
                # True if image recognition needed
                if False:
                    save_image(pdf, i, "tmptesseract", imgDir)
                    img = Image.open(f"{imgDir}tmptesseract.png")
                    text = pytesseract.image_to_string(img)
                else:
                    text = page.extract_text()
                
                if text:
                    airport_info = extract_page_info(i, text, state)
                    if airport_info:
                        airport_data.append(airport_info)
                        id = airport_info.get("Airport Identifier")
                        id = id.replace("Ø","0")
                        if id: save_image(pdf, i, id, imgDir)
                if i > (total_pages - (total_pages-end_page)):
                    break
            
    # Convert the list of dictionaries into a pandas DataFrame
    df = pd.DataFrame(airport_data)
    
    # Print the DataFrame
    print(df.to_string())

    df.to_csv(out, index=False)
    print(f"Data saved to {out}")

def parse_state_custom(airport_data, state, directory_url, page_ranges, individual_pages):
    import os
    import pdfplumber
    from PIL import Image
    import pytesseract

    pdf = f'directories/{state}.pdf'
    out = f'data/airport_info_{state}.csv'
    imgDir = f'images/{state}/'

    # Download PDF if not present
    if not os.path.exists(pdf):
        download_pdf(directory_url, pdf)

    with pdfplumber.open(pdf) as pdff:
        total_pages = len(pdff.pages)
        print(f"Total pages: {total_pages}")

        # Process pairs of pages
        for start_page, end_page in page_ranges:
            for i in range(start_page, end_page, 2):  # step by 2 for pairs
                current_page_text = pdff.pages[i].extract_text() if pdff.pages[i] else ""
                next_page_text = pdff.pages[i + 1].extract_text() if i + 1 < len(pdff.pages) else ""  # Handle the last page case
                text = current_page_text + " " + next_page_text
                
                # if image recognition needed
                page = pdff.pages[i]
                save_image(pdf, i, "tmptesseract", imgDir)
                img = Image.open(f"{imgDir}tmptesseract.png")
                text = pytesseract.image_to_string(img)
                #print(text)
                #text = page.extract_text()  # Comment if you need to use tesseract image extraction

                if text:
                    airport_info = extract_page_info(i, text, state)
                    if airport_info:
                        airport_data.append(airport_info)
                        id = airport_info.get("Airport Identifier")
                        id = id.replace("Ø", "0")
                        if id:
                            save_combined_image(pdf, i + 1, i + 2, id, imgDir)  # Adjust indices as necessary
                if i >= end_page - 1:  # Check if it's time to break after processing pairs
                    break

        # Process individual pages
        if individual_pages:
            for i in individual_pages:
                page = pdff.pages[i - 1]

                # # if image recognition needed
                # save_image(pdf, i, "tmptesseract", imgDir)
                # img = Image.open(f"{imgDir}tmptesseract.png")
                # text = pytesseract.image_to_string(img)
                text = page.extract_text()  # Comment if you need to use tesseract image extraction
                if text:
                    airport_info = extract_page_info(i, text, state)
                    if airport_info:
                        airport_data.append(airport_info)
                        id = airport_info.get("Airport Identifier")
                        id = id.replace("Ø", "0")
                        if id:
                            save_image(pdf, i, id, imgDir)
    
    # Convert the list of dictionaries into a pandas DataFrame
    df = pd.DataFrame(airport_data)
    
    # Print the DataFrame
    print(df.to_string())

    df.to_csv(out, index=False)
    print(f"Data saved to {out}")

def save_combined_image(pdf_path, start_page, end_page, name, imgdir):
    if not os.path.exists(imgdir):
        os.makedirs(imgdir)

    # Convert pages to images
    images = convert_from_path(pdf_path, first_page=start_page, last_page=end_page)
    #to rotate uncomment the following
    #images = [image.rotate(270, expand=True) for image in images] 

    # Assuming images are not empty and have the same width
    total_height = sum(image.height for image in images)
    max_width = max(image.width for image in images)
    
    # Create a new image with the combined height of the two pages
    combined_image = Image.new('RGB', (max_width, total_height))
    
    # Paste the images into the combined image
    y_offset = 0
    for image in images:
        combined_image.paste(image, (0, y_offset))
        y_offset += image.height
    
    # Save the combined image
    combined_image_filename = f"{imgdir}{name}.png"
    combined_image.save(combined_image_filename)

def save_image(pdf_path, pageNum, name, imgdir):
    if not os.path.exists(f'{imgdir}'):
        os.makedirs(imgdir)

    images = convert_from_path(pdf_path, first_page=pageNum, last_page=pageNum) #For Kansas, use_cropbox=True
    for i, image in enumerate(images):
        image.save(f'{imgdir}{name}.png')

def download_pdf(url, save_path):
    print(f"Downloading pdf from {url}")
    try:
        # Send a GET request to the URL
        response = requests.get(url, stream=True)
        
        # Check if the request was successful (HTTP status code 200)
        if response.status_code == 200:
            # Open the file path as a binary file and write the content
            with open(save_path, 'wb') as f:
                f.write(response.content)
            print(f"PDF successfully downloaded and saved as '{save_path}'.")
        else:
            print(f"Failed to download the PDF. HTTP status code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred downloading file: {e}")  

def main():

    airport_data = []
    if not os.path.exists(airports_path):
        download_pdf(airports_url, airports_path)

    parse_state(airport_data, "mt", "nilurl", "single", 35, 155)
    sys.exit(1)

    parse_state(airport_data, "ar", id_url, "single", 1, 93)
    parse_state(airport_data, "ia", id_url, "pairs", 1, 228)
    parse_state(airport_data, "ks", id_url, "single", 5, 142)
    parse_state(airport_data, "ny", id_url, "single", 1, 126)
    parse_state(airport_data, "sc", id_url, "single", 16, 81)
    parse_state(airport_data, "nc", id_url, "single", 13, 120)
    parse_state_custom(airport_data, "de", "nilurl", [(13,14),(17,18),(21,22),(28,29),(32,33),(36,37),(40,41),(44,45),(48,49),(52,53)],None)
    parse_state_custom(airport_data, "vt", "nilurl", [(56, 63), (65, 74),(79,82)], [64,75,76,77,78])
    parse_state(airport_data, "co", "nilurl", "single", 24, 99)
    parse_state(airport_data, "tn", "nilurl", "single", 11, 89)
    parse_state(airport_data, "nj", "nilurl", "single", 18, 58)
    parse_state(airport_data, "mi", "nilurl", "single", 30, 261)
    parse_state(airport_data, "ga", "nilurl", "single", 24, 128)
    parse_state(airport_data, "ky", "nilurl", "pairs", 9, 124)
    parse_state(airport_data, "oh", "nilurl", "pairs", 22, 323)
    parse_state(airport_data, "nv", "nilurl", "pairs", 12, 111)
    parse_state(airport_data, "ne", "nilurl", "single", 8, 86)
    parse_state(airport_data, "mo", "nilurl", "pairs", 17, 258)
    parse_state(airport_data, "id", id_url, "single", 38, 182)
    parse_state(airport_data, "fl", "nilurl", "single", 11, 138)
    parse_state(airport_data, "md", mn_url, "pairs", 11, 78)
    parse_state(airport_data, "mn", mn_url, "pairs", 22, 293)
    parse_state(airport_data, "mt", "nilurl", "single", 36, 157)
    parse_state(airport_data, "or", mn_url, "pairs", 13, 221)
    parse_state(airport_data, "mt", "nilurl", "single", 36, 157)
    parse_state(airport_data, "sd", "nilurl", "pairs", 36, 175)
    parse_state(airport_data, "tx", wy_url, "single", 24, 411)
    parse_state(airport_data, "wa", wy_url, "single", 10, 138)
    parse_state(airport_data, "wi", wy_url, "single", 35, 177)
    parse_state(airport_data, "wy", wy_url, "pairs", 12, 91)

if __name__ == "__main__":
    main()
