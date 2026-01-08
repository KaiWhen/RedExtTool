import os
import json
import time
from PIL import Image, ImageFont, ImageDraw
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Screenshot import Screenshot

ROUTE2_BASE_P2 = "https://gunnermaniac.com/pokeworld?local=13#8/48/"
GATE_BASE = "https://gunnermaniac.com/pokeworld?local=50#4/7/"
FOREST_BASE = "https://gunnermaniac.com/pokeworld?local=51#17/47/"
CAN_BASE = "https://gunnermaniac.com/pokeworld?local=92#7/17/"
SURGE_BASE = "https://gunnermaniac.com/pokeworld?local=92#7/12/"

ROUTE2_COORDS = (0, 393, 175, 488)
FOREST_COORDS = (50, 68, 593, 835)
SURGE_COORDS = (50, 68, 205, 375)
NPC1_COORDS = (184, 820)
NPC2_COORDS = (250, 663)
NPC3_COORDS = (455, 620)

driver = webdriver.Chrome()


def load_json(filename):
    try:
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                return json.load(f)
    except Exception as e:
        print(f"Error loading {filename}: {e}")
    return {}


def get_image_cropped(path_type: str, path_base: str, path: str, coords: tuple):
    driver.get(path_base + path)
    if path_type == "forest" or path_type == "surge": 
        ss = Screenshot(driver)
        ss.capture_full_page(output_path=f"{path_type}.png")
    else:
        map_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "submap"))
        )
        time.sleep(0.3)
        map_element.screenshot(f"{path_type}.png")

    im = Image.open(f"{path_type}.png")
    if path_type != "gate":
        im = im.crop(coords)
    return im


def create_images(file: str, path: int):
    path_data = load_json(file)
    for stat in path_data:
        stats = [int(x) for x in stat.strip("()").split(",")]
        stats_str = f"{stats[0]}_{stats[1]}_{stats[2]}_{stats[3]}"
        img_path = f"path_data/forest/p{path_data[stat]['path']}/path_images/{stats_str}.png"
        # if os.path.exists(img_path): continue
        # if stats != [20,22,12,12]: continue
        route2 = path_data[stat]["route2"]
        gate = path_data[stat]["gate"]
        postFight = path_data[stat]["postFight"]
        forest = path_data[stat]["forest"] + postFight
        npcs = path_data[stat]["npcs"]
        npcs_split = [npc.split(",") for npc in npcs.split(" or ")]

        # route2_base = ""
        # if path == 2 or path == 3:
        route2_base = ROUTE2_BASE_P2
        route2_image = get_image_cropped("route2", route2_base, route2, ROUTE2_COORDS)
        gate_image = get_image_cropped("gate", GATE_BASE, gate, ())
        forest_image = get_image_cropped("forest", FOREST_BASE, forest, FOREST_COORDS)

        image_height = forest_image.height + gate_image.height + route2_image.height
        path_image = Image.new('RGBA', (forest_image.width, image_height))
        path_image.paste(forest_image, (0,0))
        path_image.paste(gate_image, (192, 767))
        path_image.paste(route2_image, (208, 767 + gate_image.height))

        draw = ImageDraw.Draw(path_image)
        font = ImageFont.truetype("calibrib.ttf", size=50)
        y_offset = 20
        x_offset = 25
        if len(npcs_split) == 1:
            draw.text((NPC1_COORDS[0] - (x_offset * len(npcs_split[0][0])), NPC1_COORDS[1]), npcs_split[0][0], fill=(255, 0, 0), font=font)
            draw.text((NPC2_COORDS[0] - (x_offset * len(npcs_split[0][1])), NPC2_COORDS[1]), npcs_split[0][1], fill=(255, 0, 0), font=font)
            draw.text(NPC3_COORDS, npcs_split[0][2], fill=(255, 0, 0), font=font)
        elif len(npcs_split) == 2:
            draw.text((NPC1_COORDS[0] - (x_offset * len(npcs_split[0][0])), NPC1_COORDS[1] - (y_offset if npcs_split[0][0] != npcs_split[1][0] else 0)), npcs_split[0][0], fill=(255, 0, 0), font=font)
            if npcs_split[0][0] != npcs_split[1][0]:
                draw.text((NPC1_COORDS[0] - (x_offset * len(npcs_split[1][0])), NPC1_COORDS[1] + y_offset), npcs_split[1][0], fill=(255, 0, 0), font=font)
            draw.text((NPC2_COORDS[0] - (x_offset * len(npcs_split[0][1])), NPC2_COORDS[1] - (y_offset if npcs_split[0][1] != npcs_split[1][1] else 0)), npcs_split[0][1], fill=(255, 0, 0), font=font)
            if npcs_split[0][1] != npcs_split[1][1]:
                draw.text((NPC2_COORDS[0] - (x_offset * len(npcs_split[1][1])), NPC2_COORDS[1] + y_offset), npcs_split[1][1], fill=(255, 0, 0), font=font)
            draw.text((NPC3_COORDS[0], NPC3_COORDS[1] - (y_offset if npcs_split[0][2] != npcs_split[1][2] else 0)), npcs_split[0][2], fill=(255, 0, 0), font=font)
            if npcs_split[0][2] != npcs_split[1][2]:
                draw.text((NPC3_COORDS[0], NPC3_COORDS[1] + y_offset), npcs_split[1][2], fill=(255, 0, 0), font=font)

        path_image.save(img_path)


def create_surge_images(file: str):
    path_data = load_json(file)
    for stat in path_data:
        hp = int(stat)
        cans = path_data[stat]["cans"]
        surge = path_data[stat]["surge"]
        #frames = path_data[stat].get("frames", [])
        #igtsecs = path_data[stat].get("igtSecs", [])
        #logs = path_data[stat].get("logs", {})
        cans_image = get_image_cropped("surge", CAN_BASE, cans, SURGE_COORDS)
        surge_image = get_image_cropped("surge", SURGE_BASE, surge, SURGE_COORDS)
        path_image = Image.new('RGBA', (cans_image.width+surge_image.width, cans_image.height))
        path_image.paste(cans_image, (0,0))
        path_image.paste(surge_image, (cans_image.width,0))
        path_image.save(f"path_data/surge/path_images/{hp}.png")


# create_images("path_data/forest/p2a/p2a.json", 2)
# create_images("path_data/p3b/p3b.json", 3)
# create_surge_images("path_data/surge/surge.json")
# create_images("path_data/p2b/p2bf18g2g3.json", 2)
