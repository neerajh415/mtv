import hmac
import requests
from hashlib import sha1
import base64
import json
import csv
from django.core.cache import cache
from datetime import datetime

BASE_URL = 'http://pre-master.sandman.coverfox.com'
API_AUTHENTICATION_ID = 'YjfFj8O48iZFstqoiE3sfN7iPJPXIsy8ta1oEr9u'
API_AUTHENTICATION_KEY = 'ALBel0kuaEni82lYPSFXPwhC5Lmv6DZAVSoDD8D0NsiZ3IQqHMGVv8z54yV7Hq12i5bjHa2HPdGqQpN0i9HIeztNIJFPzMJ3QroDqOKtIZCgqFTaMBsJMspGvNFJV3tE'

ofile = open('Database2.csv', "wb")
writer = csv.writer(ofile, delimiter='\t', quotechar='"', quoting=csv.QUOTE_ALL)


def get_headers(path):
    request_time = datetime.utcnow()
    string_to_sign = "%s %s" % (
        path, request_time.strftime('%Y-%m-%dT%H:%M:%SZ'))
    h = hmac.HMAC(API_AUTHENTICATION_KEY, string_to_sign, sha1)
    signature = base64.b64encode(h.digest())
    headers = {
        'Authorization': 'CVFX ' + API_AUTHENTICATION_ID + ':' + signature,
        'Date': request_time.strftime('%Y-%m-%dT%H:%M:%SZ'),
    }
    return headers


def doPost(path, parameters=None):
    if parameters:
        response = requests.post(BASE_URL.rstrip(
            '/') + path, headers=get_headers(path), data=parameters)
    else:
        response = requests.post(BASE_URL.rstrip(
            '/') + path, headers=get_headers(path))

    if response.status_code == 200:
        print response.content
        jsonresponse = json.loads(response.content)
        if jsonresponse['success']:
            return True, jsonresponse
        else:
            return False, None
    else:
        return False, None


def doGet(path):
    response = requests.get(BASE_URL.rstrip(
        '/') + path, headers=get_headers(path))

    if response.status_code == 200:
        print response.content
        jsonresponse = json.loads(response.content)
        if jsonresponse['success']:
            return True, jsonresponse
        else:
            return False, None
    else:
        return False, None

EP_RTOS = '/apis/motor/%s/rtos/'
EP_MODEL_LIST = '/apis/motor/%s/vehicles/'
EP_VARIANT_LIST = '/apis/motor/%s/vehicles/%s/variants/'
EP_QUOTES = '/apis/motor/%s/quotes/'
EP_REFRESH_QUOTE = '/apis/motor/%s/quotes/%s/refresh/%s/'
EP_GENERATE_TRANSACTION = '/apis/motor/%s/confirm/%s/'
EP_SUBMIT_TRANSACTION = '/apis/motor/%s/buy/%s/%s/'


def get_rtos(vehicle_type):
    success, response = doPost(EP_RTOS % vehicle_type)
    if success:
        return response['data']['rtos']
    return None


def get_models(vehicle_type):
    success, response = doPost(EP_MODEL_LIST % vehicle_type)
    if success:
        return response['data']['models']
    return None


def get_variants(vehicle_type, model_id):
    success, response = doPost(EP_VARIANT_LIST % (vehicle_type, model_id))
    if success:
        return response['data']['variants']
    return None


def get_quote(vehicle_type, parameters):
    success, response = doPost(EP_QUOTES % vehicle_type, parameters)
    if success:
        return response
    return None

def get_key(*args): 
    return "-".join(args) 

def refresh_quote(vehicle_type, quote_id, insurer, parameters):
    success, response = doPost(EP_REFRESH_QUOTE % (
        vehicle_type, quote_id, insurer), parameters)
    if success:
        return response['data']['activityId']
    return None


def generate_form(vehicle_type, activity_id):
    success, response = doPost(EP_GENERATE_TRANSACTION %
                               (vehicle_type, activity_id))
    if success:
        return response['data']['transactionId']
    return None


def submit_form(vehicle_type, insurer, transaction_id, form_parameters):
    success, response = doPost(EP_SUBMIT_TRANSACTION % (
        vehicle_type, insurer, transaction_id), form_parameters)
    return success

quote_parameters = {
    "cngKitValue": "0",
    "extra_paPassenger": "0",
    "extra_isLegalLiability": "0",
    "extra_isAntiTheftFitted": "0",
    "extra_isMemberOfAutoAssociation": "0",
    "extra_isTPPDDiscount": "0",
    "extra_user_occupation": "0",
    "extra_user_dob": "",
    "isNewVehicle": "0",
    "idvNonElectrical": "0",
    "isClaimedLastYear": "0",
    "registrationNumber[]": ["MH", "01", "0", "0"],
    "manufacturingDate": "01-01-2010",
    "registrationDate": "01-01-2010",
    "idvElectrical": "0",
    "voluntaryDeductible": "0",
    "isCNGFitted": "0",
    "vehicleId": "1262",
    "idv": "0",
    "previousNCB": "25",
    "addon_is247RoadsideAssistance": "0",
    "addon_isInvoiceCover": "0",
    "addon_isDriveThroughProtected": "0",
    "addon_isDepreciationWaiver": "0",
    "addon_isEngineProtector": "0",
    "addon_isNcbProtection": "0",
    "addon_isKeyReplacement": "0",
    "newPolicyStartDate": "02-01-2016",
    "pastPolicyExpiryDate": "01-01-2016"
}

vehicle_type = 'fourwheeler'

vehicles = ["1262"]
rtos = [ ("Ahmedabad", "GJ-01"), 
        ("Surat", "GJ-05"), 
        ("Mumbai","MH-01"), 
        ("Gurgaon","DL-15"), 
        ("Kanpur", "UP-77"), 
        ("Lucknow" ,"UP-32"), 
        ("Nagpur" ,"MH-31"), 
        ("Bangalore","KA-01"), 
        ("Delhi", "DL-01"), 
        ("Indore" ,"MP-09"), 
        ("Chennai" ,"TN-07"), 
        ("Hyderabad", "AP-09"), 
        ("Pune", "MH-12"), 
        ("Chandigarh","CH-01"), 
        ("Kolkata", "WB-01"), 
        ("Jaipur", "RJ-14")]

agencb = [(1, "0", "20"), 
            (2, "20", "25"), 
            (3, "25", "35"), 
            (4, "35", "45"), 
            (5, "45", "50"), 
            (6, "50", "50"), 
            (7, "50", "50"), 
            (8, "50", "50"), 
            (9, "50", "50"), 
            (10, "50", "50")]

VEHICLE_MASTER= [
    #('Maruti', 'Maruti Alto', 'Maruti Alto LXi', 1202),
    #('Maruti', 'Maruti 800', 'Maruti 800 Std', 6009),
    #('Maruti', 'Maruti Wagon R', 'Maruti Wagon R LXI BS IV', 1279),
    ('Maruti', 'Maruti Swift', 'Maruti Swift VDI BS IV', 1260),
    ('Maruti', 'Maruti Alto', 'Maruti Alto LX', 1205),
    #('Maruti', 'Maruti 800', 'Maruti 800 AC', 1196),
    #('Maruti', 'Maruti Swift Dzire', 'Maruti Swift Dzire VDI', 1248),
    #('Maruti', 'Maruti Omni', 'Maruti Omni 8 Seater BSII', 1237),
    #('Hyundai', 'Hyundai Santro Xing', 'Hyundai Santro Xing GLS', 1057),
    #('Maruti', 'Maruti 800', 'Maruti 800 AC BSIII', 1196),
    #('Tata', 'Tata Indica', 'Tata Indica DLS', 1382),
    #('Maruti', 'Maruti Swift', 'Maruti Swift VXI', 1262),
    #('Maruti', 'Maruti 800', 'Maruti 800 Std BSIII', 6009),
    #('Hyundai', 'Hyundai i10', 'Hyundai i10 Magna', 1017),
    #('Honda', 'Honda City ZX', 'Honda City ZX GXi', 7070),
    #('Maruti', 'Maruti Wagon R', 'Maruti Wagon R VXI BS IV', 1285),
    #('Hyundai', 'Hyundai Santro Xing', 'Hyundai Santro Xing XL', 1061),
    #('Maruti', 'Maruti Wagon R', 'Maruti Wagon R LXI BSIII', 1279),
    #('Maruti', 'Maruti Esteem', 'Maruti Esteem Vxi', 1235),
    #('Maruti', 'Maruti Wagon R', 'Maruti Wagon R VXI BSIII', 1285),
    #('Hyundai', 'Hyundai Accent', 'Hyundai Accent GLE', 976),
    #('Hyundai', 'Hyundai i10', 'Hyundai i10 Era', 1019),
    #('Maruti', 'Maruti Alto K10', 'Maruti Alto K10 VXI', 1204),
    #('Hyundai', 'Hyundai Accent', 'Hyundai Accent CRDi', 7258),
    #('Hyundai', 'Hyundai Santro Xing', 'Hyundai Santro Xing XO', 1081),
    #('Maruti', 'Maruti Alto 800', 'Maruti Alto 800 LXI', 1211),
    #('Tata', 'Tata Indigo', 'Tata Indigo LX', 1443),
    #('Tata', 'Tata Indigo', 'Tata Indigo LS', 1441),
    #('Maruti', 'Maruti Wagon R', 'Maruti Wagon R LX BS IV', 1277),
    #('Tata', 'Tata Indica', 'Tata Indica DLE', 1380),
    #('Maruti', 'Maruti Ritz', 'Maruti Ritz VDi', 1240),
    #('Mahindra', 'Mahindra Bolero', 'Mahindra Bolero SLX', 1115),
    #('Maruti', 'Maruti Swift Dzire', 'Maruti Swift Dzire VXI', 1249),
    #('Maruti', 'Maruti Esteem', 'Maruti Esteem Lxi', 1231),
    #('Hyundai', 'Hyundai i10', 'Hyundai i10 Sportz', 1011),
    #('Hyundai', 'Hyundai Santro Xing', 'Hyundai Santro Xing GL', 2415),
    #('Ford', 'Ford Ikon', 'Ford Ikon 1.3L Rocam Flair', 889),
    #('Hyundai', 'Hyundai Accent', 'Hyundai Accent GLS', 978),
    #('Tata', 'Tata New Safari', 'Tata New Safari DICOR 2.2 EX 4x2', 1548),
    #('Hyundai', 'Hyundai Accent', 'Hyundai Accent GLS 1.6', 979),
    #('Maruti', 'Maruti Swift', 'Maruti Swift LDI BSIV', 1256),
    #('Maruti', 'Maruti Swift', 'Maruti Swift LXI', 1245),
    #('Hyundai', 'Hyundai Santro Xing', 'Hyundai Santro Xing XP', 1064),
    #('Maruti', 'Maruti Omni', 'Maruti Omni 5 Seater', 1236),
    #('Maruti', 'Maruti Zen Estilo', 'Maruti Zen Estilo LXI BSIII', 1288),
    #('Maruti', 'Maruti Eeco', 'Maruti Eeco 5 Seater AC', 1219),
    #('Tata', 'Tata Indica V2 Turbo', 'Tata Indica V2 Turbo DLG TC', 7075),
    #('Ford', 'Ford Fiesta 2004-2010', 'Ford Fiesta 2004-2010 1.4 Duratorq ZXI', 6987),
    #('Hyundai', 'Hyundai Santro Xing', 'Hyundai Santro Xing XG', 1059),
    #('Chevrolet', 'Chevrolet Spark', 'Chevrolet Spark 1 LS', 812),
    #('Maruti', 'Maruti Wagon R Duo', 'Maruti Wagon R Duo Lxi', 7034),
    #('Ford', 'Ford Ikon', 'Ford Ikon 1.3 Flair', 890),
    #('Tata', 'Tata Indigo CS 2008-2012', 'Tata Indigo CS 2008-2012 LX (TDI) BS III', 6032),
    #('Mahindra', 'Mahindra Scorpio 2002-2013', 'Mahindra Scorpio 2002-2013 SLX', 1138),
    #('Mahindra', 'Mahindra XUV500', 'Mahindra XUV500 W8 2WD', 1157),
    #('Honda', 'Honda City ZX', 'Honda City ZX EXi', 7139),
    #('Hyundai', 'Hyundai Accent', 'Hyundai Accent Executive', 7003),
    #('Maruti', 'Maruti Alto', 'Maruti Alto Std', 7327),
    #('Maruti', 'Maruti Eeco', 'Maruti Eeco 7 Seater Standard', 1220),
    #('Ford', 'Ford Figo', 'Ford Figo Diesel Titanium', 877),
    #('Maruti', 'Maruti Esteem', 'Maruti Esteem LX', 1229),
    #('Tata', 'Tata New Safari', 'Tata New Safari DICOR 2.2 LX 4x2', 2411),
    #('Ford', 'Ford Figo', 'Ford Figo Diesel ZXI', 879),
    #('Hyundai', 'Hyundai i10', 'Hyundai i10 Magna 1.1L', 1017),
    #('Mahindra', 'Mahindra Scorpio 2002-2013', 'Mahindra Scorpio 2002-2013 VLX', 1129),
    #('Tata', 'Tata Indigo CS 2008-2012', 'Tata Indigo CS 2008-2012 LS (TDI) BS III', 7055),
    #('Maruti', 'Maruti Alto', 'Maruti Alto VXi', 1208),
    #('Hyundai', 'Hyundai Accent', 'Hyundai Accent Gvs', 984),
    #('Tata', 'Tata Indica', 'Tata Indica DLX', 1384),
    #('Maruti', 'Maruti Alto K10', 'Maruti Alto K10 LXI', 1202),
    #('Hyundai', 'Hyundai Getz', 'Hyundai Getz GLS', 995),
    #('Chevrolet', 'Chevrolet Spark', 'Chevrolet Spark 1 LT', 813),
    #('Maruti', 'Maruti Ertiga', 'Maruti Ertiga VDI', 1223),
    #('Maruti', 'Maruti Swift Dzire', 'Maruti Swift Dzire LDI', 1579),
    #('Maruti', 'Maruti Swift Dzire', 'Maruti Swift Dzire ZDI', 1251),
    #('Maruti', 'Maruti Wagon R', 'Maruti Wagon R LXI DUO BSIII', 7033),
    #('Mahindra', 'Mahindra Scorpio 2002-2013', 'Mahindra Scorpio 2002-2013 M2DI', 1146),
    #('Maruti', 'Maruti Zen Estilo', 'Maruti Zen Estilo VXI BSIII', 1290),
    #('Honda', 'Honda City 2008-2011', 'Honda City 2008-2011 1.5 S MT', 930),
    #('Tata', 'Tata Manza', 'Tata Manza Aura Quadrajet', 1416),
    #('Mahindra', 'Mahindra Scorpio 2002-2013', 'Mahindra Scorpio 2002-2013 Sle', 1125),
    #('Maruti', 'Maruti Baleno', 'Maruti Baleno LXI', 1216),
    #('Maruti', 'Maruti SX4 2007-2012', 'Maruti SX4 2007-2012 Zxi BSIII', 1274),
    #('Chevrolet', 'Chevrolet Beat', 'Chevrolet Beat LT', 780),
    #('Chevrolet', 'Chevrolet Aveo', 'Chevrolet Aveo 1.4 LS', 768),
    #('Skoda', 'Skoda Octavia Rider', 'Skoda Octavia Rider 1.9 TDI MT', 1363),
    #('Maruti', 'Maruti Esteem', 'Maruti Esteem VX', 1234),
    #('Maruti', 'Maruti SX4 2007-2012', 'Maruti SX4 2007-2012 Vxi BSIII', 1270),
    #('Maruti', 'Maruti Wagon R', 'Maruti Wagon R LXI CNG', 7033),
    #('Chevrolet', 'Chevrolet Cruze', 'Chevrolet Cruze LTZ', 788),
    #('Tata', 'Tata Nano 2009-2011', 'Tata Nano 2009-2011 Lx', 1449),
    #('Chevrolet', 'Chevrolet Beat', 'Chevrolet Beat Diesel LT', 781),
    #('Maruti', 'Maruti Swift', 'Maruti Swift ZXI', 1265),
    #('Hyundai', 'Hyundai EON', 'Hyundai EON Era Plus', 7179),
    #('Fiat', 'Fiat Palio', 'Fiat Palio 1.2', 847),
    #('Maruti', 'Maruti Alto', 'Maruti Alto LXi BSII', 1202),
    #('Mahindra', 'Mahindra Scorpio 2002-2013', 'Mahindra Scorpio 2002-2013 2.6 DX', 1135),
    #('Honda', 'Honda City ZX', 'Honda City ZX VTEC', 944),
    #('Hyundai', 'Hyundai Verna 2006-2010', 'Hyundai Verna 2006-2010 CRDi', 1093),
    #('Maruti', 'Maruti Swift', 'Maruti Swift ZDi', 1264),
    #('Maruti', 'Maruti Ritz 2009-2011', 'Maruti Ritz 2009-2011 VDi', 1240),
    #('Hyundai', 'Hyundai Santro Xing', 'Hyundai Santro Xing GL Plus', 1699),
    #('Maruti', 'Maruti 800', 'Maruti 800 DX', 1197),
    #('Maruti', 'Maruti Ritz', 'Maruti Ritz VXi', 1241),
    #('Ford', 'Ford Figo', 'Ford Figo Diesel EXI', 873),
    #('Tata', 'Tata New Safari', 'Tata New Safari DICOR 2.2 EX 4x2 BS IV', 1553),
    #('Volkswagen', 'Volkswagen Vento 2010-2013', 'Volkswagen Vento 2010-2013 Diesel Highline', 1509),
    #('Maruti', 'Maruti Ritz', 'Maruti Ritz LDi', 1238),
    #('Hyundai', 'Hyundai i20 2012-2014', 'Hyundai i20 2012-2014 Sportz 1.4 CRDi', 1055),
    #('Hyundai', 'Hyundai i10', 'Hyundai i10 Magna 1.2 iTech SE', 1023),
    #('Chevrolet', 'Chevrolet Tavera', 'Chevrolet Tavera Neo 3 LS 10 Seats BSIII', 1689),
    #('Chevrolet', 'Chevrolet Beat', 'Chevrolet Beat Diesel LS', 777),
    #('Maruti', 'Maruti Estilo', 'Maruti Estilo LXI', 1288),
    #('Hyundai', 'Hyundai Accent', 'Hyundai Accent GLX', 980),
    #('Tata', 'Tata Indica Vista 2008-2013', 'Tata Indica Vista 2008-2013 Aqua 1.4 TDI', 7089),
    #('Chevrolet', 'Chevrolet Spark 2007-2012', 'Chevrolet Spark 2007-2012 1 LS', 812),
    #('Tata', 'Tata New Safari', 'Tata New Safari DICOR 2.2 VX 4x2', 1602),
    #('Hyundai', 'Hyundai Verna 2006-2010', 'Hyundai Verna 2006-2010 CRDi SX', 1092),
    #('Tata', 'Tata Indica Vista 2008-2013', 'Tata Indica Vista 2008-2013 Aura 1.3 Quadrajet', 1379),
    #('Skoda', 'Skoda Octavia 2000-2010', 'Skoda Octavia 2000-2010 Ambiente 1.9 TDI', 1353),
    #('Maruti', 'Maruti 800', 'Maruti 800 Std BSII', 6009),
    #('Mahindra', 'Mahindra Bolero', 'Mahindra Bolero ZLX', 1120),
    #('Mitsubishi', 'Mitsubishi Lancer', 'Mitsubishi Lancer 1.5 GLXi', 6011),
    #('Tata', 'Tata Manza', 'Tata Manza Aqua Quadrajet', 1378),
    #('Mahindra', 'Mahindra Bolero', 'Mahindra Bolero SLE', 1114),
    #('Chevrolet', 'Chevrolet Optra', 'Chevrolet Optra 1.6 LS', 798),
    #('Hyundai', 'Hyundai Santro Xing', 'Hyundai Santro Xing XS', 1065),
    #('Hyundai', 'Hyundai EON', 'Hyundai EON D Lite', 988),
    #('Tata', 'Tata Indica Vista 2008-2013', 'Tata Indica Vista 2008-2013 Terra 1.4 TDI', 1412),
    #('Tata', 'Tata Nano 2012-2015', 'Tata Nano 2012-2015 LX', 1449),
    #('Chevrolet', 'Chevrolet Optra Magnum', 'Chevrolet Optra Magnum 2 LT', 799),
    #('Tata', 'Tata Indica Vista 2008-2013', 'Tata Indica Vista 2008-2013 Aqua 1.3 Quadrajet', 1378),
    #('Tata', 'Tata Nano 2009-2011', 'Tata Nano 2009-2011 Cx', 1448),
    #('Hyundai', 'Hyundai i20 2009-2011', 'Hyundai i20 2009-2011 Magna', 1048),
    #('Chevrolet', 'Chevrolet Beat', 'Chevrolet Beat LS', 778),
    #('Hyundai', 'Hyundai Accent', 'Hyundai Accent VIVA CRDi', 971),
    #('Tata', 'Tata Indica V2 Xeta', 'Tata Indica V2 Xeta GLS', 1391),
    #('Toyota', 'Toyota Innova', 'Toyota Innova 2.5 G (Diesel) 8 Seater', 2433)
    ]

row = ["Brand", "Model", "Variants", "Coverfox Id", "RTO", "NCB", "City", "Vehicle_age"]
writer.writerow(row)
for vehid in VEHICLE_MASTER:
    for rto in rtos:
        for age, ncb, ncb_actual in agencb:
	    key = get_key(str(vehid[3]), str(rto[1][0:2]), str(rto[1][3:]), str(ncb), "01-01-"+str(2016-age), "01-01-"+str(2016-age))
	    row = cache.get(key)
	    if row:
                print 'cache'
                print row
	        writer.writerow(row) 
	    else:
		row = []
		quote_parameters["vehicleId"] = vehid[3]
		quote_parameters["registrationNumber[]"] = [rto[1][0:2], rto[1][3:],"0","0"]
                quote_parameters["previousNCB"] = ncb
                quote_parameters["registrationDate"] = "01-01-"+str(2016-age)
                quote_parameters["manufacturingDate"] = "01-01-"+str(2016-age)
                #print vehid, rto, ncb, quote_parameters["registrationDate"], quote_parameters["manufacturingDate"], min_premium
                #print quote_parameters
                quote_response = get_quote(vehicle_type, quote_parameters)
                try:
                    if quote_response:
                        premiums = quote_response["data"]["premiums"]
                        min_premium = min([p["final_premium"] for p in premiums])
                        print min_premium
                except:
                    pass
                row.append(vehid[0])
                row.append(vehid[1])
                row.append(vehid[2])
                row.append(vehid[3])
                row.append(quote_parameters["registrationNumber[]"][0] + "-" + quote_parameters["registrationNumber[]"][1])
                row.append(ncb_actual)
                row.append(rto[0])
                row.append(age)
                row.append(min_premium)
                writer.writerow(row)
                cache.set(key, row)
                print row


   

ofile.close()
