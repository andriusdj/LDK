#!/bin/python3

import mss
import tesserocr as ocr
from PIL import Image
from PIL import ImageEnhance 

import json

import pyautogui
import time

import sys
import os
from dotenv import load_dotenv
import requests

import xmlrpc.client

load_dotenv()

pyautogui.FAILSAFE = False

url = os.env['HOST'] or 'http://localhost:8069'
db = 'ldk'
username = 'admin'
password = 'admin'

common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
print(f"Connecting to Odoo server... OK {common.version()['server_version']}")

uid = common.authenticate(db, username, password, {})
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

def get_castles(result):
    castles = []
    for line in result:
        if line['player'] not in castles:
            castles.append(line['player'])
    return castles

def create_castle(name):
    id = models.execute_kw(db, uid, password, 'ldk.castle', 'create',[{'name': name}])
    print(f"Created castle for {name} with id {id}")
    return id

def create_castles(result):
    for castle in get_castles(result):
        res = models.execute_kw(db, uid, password, 'ldk.castle', 'search',[[['name', '=', castle]]])
        if not res:
            create_castle(name=castle)            
            print(f"Created castle for {name}: {id}")

def get_castle_id(name):
    res = models.execute_kw(db, uid, password, 'ldk.castle', 'search',[[['name', '=', name]]], {'limit': 1})
    if res:
        return res[0]
    
    return False

def update_chest_values(line):
    res = models.execute_kw(db, uid, password, 'ldk.chest.value', 'search',[[['chest_name', '=', line['chest_name']], ['chest_type', '=', line['chest_type']]]], {'limit': 1})
    if not res:
        res = models.execute_kw(db, uid, password, 'ldk.chest.value', 'create',[{
            'chest_name': line['chest_name'],
            'chest_type': line['chest_type'],
            'value': 0,
        }])
        print(f"Updated chest_value records: {res}")
        return res

def record_chest(line):
    res = models.execute_kw(db, uid, password, 'ldk.chest', 'create',[{
        'castle_id': get_castle_id(name=line['player']) or create_castle(name=line['player']),
        'chest_name': line['chest_name'],
        'chest_type': line['chest_type'],
        'recorded': line['recorded'],
        'expiring_in': line['expiring_in'],
    }])
    print(f"Created chest record: {res}")
    update_chest_values(line)
    return res

def region_grabber(region):
    x1 = region[0]
    y1 = region[1]
    width = region[2]
    height = region[3]

    region = x1, y1, width, height
    with mss.mss() as sct:
        return sct.grab(region)

def get_tmp_filename():
    if len(sys.argv) > 1:
        filename = "save_" + sys.argv[1] + ".json"
    else:
        filename = "save_LDK.json"

    return filename

def save_result(result):
    filename = get_tmp_filename()
    json.dump(result, open(filename, 'w'))

def cleanup():
    filename = get_tmp_filename()
    if os.path.isfile(filename):
        os.remove(filename)

def upload_result(result):
    save_result(result)
    for line in result:
        record_chest(line=line)
    cleanup()

def get_previous_result():
    result = []
    previous_filename = get_tmp_filename()
    if os.path.isfile(previous_filename):
        result = json.load(open(previous_filename))

    return result

def rec_chest(previous_result):
    recording = time.time()

    time.sleep(0.200)
    chest_im = region_grabber(region=(790, 425, 1100, 500))
    chest_img = Image.frombytes("RGB", chest_im.size, chest_im.bgra, "raw", "BGRX")
    chest_img = chest_img.convert('L')    
    width, height = chest_img.size
    chest_img = chest_img.resize((width*5, height*5))

    time_im = region_grabber(region=(1310, 450, 1395, 470))
    time_img = Image.frombytes("RGB", time_im.size, time_im.bgra, "raw", "BGRX")
    time_img = time_img.convert('L')    
    width, height = time_img.size
    time_img = time_img.resize((width*5, height*5))  

    # chest_img.save("./chest_" + str(recording) + ".png") # debug
    # time_img.save("./time_" + str(recording) + ".png") # debug

    chest_text = ocr.image_to_text(chest_img)
    lines = list(filter(None, chest_text.split("\n")))

    time_text = ocr.image_to_text(time_img)
    exp = list(filter(None, time_text.split(" ")))
    if (len(exp) < 2):
        exp = list(filter(None, time_text.split(":")))
    
    for key, val in enumerate(exp):
        exp[key] = val.strip("\n ;:")

    try:
        cname = lines[0].strip("., ")
        player = lines[1].replace(";", ":").split(":")[1].strip("., ")
        chest = lines[2].replace(";", ":").split(":")[1].strip("., ")
        
        print(player + " - " + chest + " (" + cname + ")")
        
        previous_result.append({
            "player": player,
            "chest_name": cname,
            "chest_type": chest,
            "recorded": recording,
            "expiring_in": exp,
        })

    except IndexError:
        upload_result(previous_result)
        sys.exit("No more chests")
    except: 
        upload_result(previous_result)
        sys.exit("Error - save & exit")
        
    pyautogui.mouseDown(1330, 490, 'left')
    pyautogui.mouseUp(1330, 490, 'left')
    time.sleep(0.200)


result = get_previous_result()

while True:
    rec_chest(result)


