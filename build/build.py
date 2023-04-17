import os
import shutil
import gzip
import zlib
import subprocess
import hashlib
import requests
import zipfile

# DONKEY KONG 64 BUILDER
# AKA "CRANKY'S LAB"
# Built by Isotarge
# https://twitter.com/isotarge

# Measure how long this takes
import time
start_time = time.time()

print("Cranky's Lab Build System")
print()

if not os.path.exists("build/n64chain"):
    print("Downloading N64Chain from GitHub. This may take a while...")
    url = "https://github.com/tj90241/n64chain/releases/download/9.1.0/n64chain-windows.zip"
    r = requests.get(url, allow_redirects=True)
    open("n64chain.zip", "wb").write(r.content)
    with zipfile.ZipFile("n64chain.zip", "r") as zip_ref:
        zip_ref.extractall("build/n64chain/")
cwd = os.path.dirname(os.path.abspath(__file__))

print("[1 / 8] - Compiling C Code")
if os.path.exists("obj"):
	shutil.rmtree('obj')
os.mkdir("obj")
with open('./asm/objects.asm', 'w') as obj_asm:
	for root, dirs, files in os.walk(r'src'):
		for file in files:
			if file.endswith('.c'):
				_o = os.path.join(root, file).replace("/", "_").replace("\\", "_").replace(".c", ".o")
				print(os.path.join(root, file))
				obj_asm.write(".importobj \"obj/" + _o + "\"\n")
				subprocess.run([f"{cwd}\\n64chain\\tools\\bin\\mips64-elf-gcc", "-w", "-Wall", "-O1", "-mtune=vr4300", "-march=vr4300", "-mabi=32", "-fomit-frame-pointer", "-fno-toplevel-reorder", "-G0", "-c", "-nostdinc", "-I.", "-Iinclude2", "-Iinclude2/libc", "-DTARGET_N64", "-DF3DEX2_GBI", os.path.join(root, file)])
				shutil.move("./" + file.replace(".c", ".o"), "obj/" + _o)
print()

# Infrastructure for recomputing DK64 global pointer tables
from recompute_pointer_table import pointer_tables, dumpPointerTableDetails, replaceROMFile, writeModifiedPointerTablesToROM, parsePointerTables, getFileInfo, make_safe_filename
from recompute_overlays import isROMAddressOverlay, readOverlayOriginalData, replaceOverlayData, writeModifiedOverlaysToROM

# Patcher functions for the extracted files
from staticcode import patchStaticCode

ROMName = "./rom/dk64.z64"
newROMName = "./rom/dk64-newhack-dev.z64"

if os.path.exists(newROMName):
	os.remove(newROMName)
shutil.copyfile(ROMName, newROMName)

file_dict = [
	{
		"name": "Static ASM Code",
		"start": 0x113F0,
		"compressed_size": 0xB15E4,
		"source_file": "bin/StaticCode.bin",
		"use_external_gzip": True,
		"patcher": patchStaticCode,
	},
	{
		"name": "Nintendo Logo",
		"pointer_table_index": 14,
		"file_index": 94,
		"source_file": "bin/bkong.png",
		"texture_format": "rgba5551"
	},
	{
		"name": "DK Coin Image",
		"pointer_table_index": 14,
		"file_index": 119,
		"source_file": "bin/dk_coin.png",
		"texture_format": "rgba5551"
	},
	{
		"name": "Multicolored Bunch Image",
		"pointer_table_index": 14,
		"file_index": 120,
		"source_file": "bin/multicolored_bunch.png",
		"texture_format": "rgba5551"
	},
	{
		"name": "light_skybox",
		"pointer_table_index": 14,
		"file_index": 46,
		"source_file": "bin/skybox/light_skybox.png",
		"texture_format": "rgba5551",
	},
	{
		"name": "green_skybox",
		"pointer_table_index": 14,
		"file_index": 47,
		"source_file": "bin/skybox/green_skybox.png",
		"texture_format": "rgba5551",
	},
	{
		"name": "sunset_skybox",
		"pointer_table_index": 14,
		"file_index": 48,
		"source_file": "bin/skybox/sunset_skybox.png",
		"texture_format": "rgba5551",
	},
	{
		"name": "black_skybox",
		"pointer_table_index": 14,
		"file_index": 49,
		"source_file": "bin/skybox/black_skybox.png",
		"texture_format": "rgba5551",
	},
	{
		"name": "jiggy_menu_texture",
		"pointer_table_index": 25,
		"file_index": 1215,
		"source_file": "bin/menu/menu_silver.png",
		"texture_format": "rgba5551",
	},
	{
		"name": "jiggy_menu_texture",
		"pointer_table_index": 25,
		"file_index": 1216,
		"source_file": "bin/menu/menu_silver.png",
		"texture_format": "rgba5551",
	},
	{
		"name": "jiggy_menu_texture",
		"pointer_table_index": 25,
		"file_index": 1217,
		"source_file": "bin/menu/menu_silver.png",
		"texture_format": "rgba5551",
	},
	{
		"name": "jiggy_menu_texture",
		"pointer_table_index": 25,
		"file_index": 1218,
		"source_file": "bin/menu/menu_silver.png",
		"texture_format": "rgba5551",
	},
	{
		"name": "jiggy_menu_texture",
		"pointer_table_index": 25,
		"file_index": 1219,
		"source_file": "bin/menu/menu_silver.png",
		"texture_format": "rgba5551",
	},
	{
		"name": "jiggy_menu_texture",
		"pointer_table_index": 25,
		"file_index": 1220,
		"source_file": "bin/menu/menu_silver.png",
		"texture_format": "rgba5551",
	},
	{
		"name": "jiggy_menu_texture",
		"pointer_table_index": 25,
		"file_index": 1221,
		"source_file": "bin/menu/menu_silver.png",
		"texture_format": "rgba5551",
	},
	{
		"name": "Jiggy Sprite",
		"pointer_table_index": 25,
		"file_index": 5468,
		"source_file": "bin/menu/Jiggy_0011_Layer-3.png",
		"texture_format": "rgba5551",
	},
	{
		"name": "Jiggy Sprite",
		"pointer_table_index": 25,
		"file_index": 5469,
		"source_file": "bin/menu/Jiggy_0010_Layer-6.png",
		"texture_format": "rgba5551",
	},
	{
		"name": "Jiggy Sprite",
		"pointer_table_index": 25,
		"file_index": 5470,
		"source_file": "bin/menu/Jiggy_0009_Layer-9.png",
		"texture_format": "rgba5551",
	},
	{
		"name": "Jiggy Sprite",
		"pointer_table_index": 25,
		"file_index": 5471,
		"source_file": "bin/menu/Jiggy_0008_Layer-12.png",
		"texture_format": "rgba5551",
	},
	{
		"name": "Jiggy Sprite",
		"pointer_table_index": 25,
		"file_index": 5472,
		"source_file": "bin/menu/Jiggy_0007_Layer-15.png",
		"texture_format": "rgba5551",
	},
	{
		"name": "Jiggy Sprite",
		"pointer_table_index": 25,
		"file_index": 5473,
		"source_file": "bin/menu/Jiggy_0006_Layer-18.png",
		"texture_format": "rgba5551",
	},
	{
		"name": "Jiggy Sprite",
		"pointer_table_index": 25,
		"file_index": 5474,
		"source_file": "bin/menu/Jiggy_0005_Layer-21.png",
		"texture_format": "rgba5551",
	},
	{
		"name": "Jiggy Sprite",
		"pointer_table_index": 25,
		"file_index": 5475,
		"source_file": "bin/menu/Jiggy_0004_Layer-24.png",
		"texture_format": "rgba5551",
	},
	{
		"name": "Jiggy Sprite",
		"pointer_table_index": 25,
		"file_index": 5476,
		"source_file": "bin/menu/Jiggy_0003_Layer-27.png",
		"texture_format": "rgba5551",
	},
	{
		"name": "Jiggy Sprite",
		"pointer_table_index": 25,
		"file_index": 5477,
		"source_file": "bin/menu/Jiggy_0002_Layer-30.png",
		"texture_format": "rgba5551",
	},
	{
		"name": "Jiggy Sprite",
		"pointer_table_index": 25,
		"file_index": 5478,
		"source_file": "bin/menu/Jiggy_0001_Layer-33.png",
		"texture_format": "rgba5551",
	},
	{
		"name": "Jiggy Sprite",
		"pointer_table_index": 25,
		"file_index": 5479,
		"source_file": "bin/menu/Jiggy_0000_Layer-36.png",
		"texture_format": "rgba5551",
	},
	{
		"name": "jiggy_menu_texture",
		"pointer_table_index": 25,
		"file_index": 1222,
		"source_file": "bin/menu/menu_silver.png",
		"texture_format": "rgba5551",
	},
	{
		"name": "Jiggy Texture",
		"pointer_table_index": 25,
		"file_index": 2939,
		"source_file": "bin/jiggy/image_0000.bin",
		"do_not_extract": True
	},
	{
		"name": "Jiggy Model",
		"pointer_table_index": 4,
		"file_index": 0x74,
		"source_file": "bin/jiggy_model.bin",
		"do_not_delete_source": True
	},
	{
		"name": "Square Platform",
		"pointer_table_index": 4,
		"file_index": 0x5D,
		"source_file": "bin/m2_platform.bin",
		"do_not_delete_source": True
	},
	{
		"name": "Level Text",
		"pointer_table_index": 12,
		"file_index": 0,
		"source_file": "bin/text/level_text.bin",
		"do_not_delete_source": True,
	},
	{
		"name": "SM Midi",
		"pointer_table_index": 0,
		"file_index": 49,
		"source_file": "bin/BK_Spiral_Mountain.bin",
		"use_external_gzip": True,
		"do_not_delete": True,
		"do_not_extract": True
	},
	{
		"name": "Furnace Fun Midi",
		"pointer_table_index": 0,
		"file_index": 77,
		"source_file": "bin/BK_Furnace_Fun.bin",
		"use_external_gzip": True,
		"do_not_delete": True,
		"do_not_extract": True
	},
	{
		"name": "Lair Midi",
		"pointer_table_index": 0,
		"file_index": 105,
		"source_file": "bin/BK_Gruntys_Lair.bin",
		"use_external_gzip": True,
		"do_not_delete": True,
		"do_not_extract": True
	},
	{
		"name": "Menu Midi",
		"pointer_table_index": 0,
		"file_index": 106,
		"source_file": "bin/BK_Banjos_House.bin",
		"use_external_gzip": True,
		"do_not_delete": True,
		"do_not_extract": True
	},
	{
		"name": "Tickers Tower",
		"pointer_table_index": 0,
		"file_index": 28,
		"source_file": "bin/BK Inside Ticker's Tower.bin",
		"use_external_gzip": True,
		"do_not_delete": True,
		"do_not_extract": True
	},
	{
		"name": "Jiggy Collection",
		"pointer_table_index": 0,
		"file_index": 18,
		"source_file": "bin/BK Jiggy collection.bin",
		"use_external_gzip": True,
		"do_not_delete": True,
		"do_not_extract": True
	},
	{
		"name": "Mumbos Hut",
		"pointer_table_index": 0,
		"file_index": 53,
		"source_file": "bin/BK Mumbo's Hut.bin",
		"use_external_gzip": True,
		"do_not_delete": True,
		"do_not_extract": True
	},
	{
		"name": "Mumbos Mountain",
		"pointer_table_index": 0,
		"file_index": 56,
		"source_file": "bin/BK Mumbo's Mountain.bin",
		"use_external_gzip": True,
		"do_not_delete": True,
		"do_not_extract": True
	},
	{
		"name": "Treasure Trove Cove",
		"pointer_table_index": 0,
		"file_index": 68,
		"source_file": "bin/BK Treasure Trove Cove.bin",
		"use_external_gzip": True,
		"do_not_delete": True,
		"do_not_extract": True
	},
	{
		"name": "Inside Nipper",
		"pointer_table_index": 0,
		"file_index": 70,
		"source_file": "bin/BK TTC Inside Nipper.bin",
		"use_external_gzip": True,
		"do_not_delete": True,
		"do_not_extract": True
	},
	{
		"name": "image_0056",
		"pointer_table_index": 25,
		"file_index": 6013,
		"source_file": "bin/spiral_mountain/image_0056.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0056_pal",
		"pointer_table_index": 25,
		"file_index": 6014,
		"source_file": "bin/spiral_mountain/image_0056_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0012",
		"pointer_table_index": 25,
		"file_index": 6015,
		"source_file": "bin/spiral_mountain/image_0012.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0035",
		"pointer_table_index": 25,
		"file_index": 6016,
		"source_file": "bin/spiral_mountain/image_0035.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0035_pal",
		"pointer_table_index": 25,
		"file_index": 6017,
		"source_file": "bin/spiral_mountain/image_0035_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0013",
		"pointer_table_index": 25,
		"file_index": 6018,
		"source_file": "bin/spiral_mountain/image_0013.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0013_pal",
		"pointer_table_index": 25,
		"file_index": 6019,
		"source_file": "bin/spiral_mountain/image_0013_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0002",
		"pointer_table_index": 25,
		"file_index": 6020,
		"source_file": "bin/spiral_mountain/image_0002.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0002_pal",
		"pointer_table_index": 25,
		"file_index": 6021,
		"source_file": "bin/spiral_mountain/image_0002_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0018",
		"pointer_table_index": 25,
		"file_index": 6022,
		"source_file": "bin/spiral_mountain/image_0018.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0018_pal",
		"pointer_table_index": 25,
		"file_index": 6023,
		"source_file": "bin/spiral_mountain/image_0018_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0020",
		"pointer_table_index": 25,
		"file_index": 6024,
		"source_file": "bin/spiral_mountain/image_0020.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0020_pal",
		"pointer_table_index": 25,
		"file_index": 6025,
		"source_file": "bin/spiral_mountain/image_0020_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0003",
		"pointer_table_index": 25,
		"file_index": 6026,
		"source_file": "bin/spiral_mountain/image_0003.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0003_pal",
		"pointer_table_index": 25,
		"file_index": 6027,
		"source_file": "bin/spiral_mountain/image_0003_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0005",
		"pointer_table_index": 25,
		"file_index": 6028,
		"source_file": "bin/spiral_mountain/image_0005.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0005_pal",
		"pointer_table_index": 25,
		"file_index": 6029,
		"source_file": "bin/spiral_mountain/image_0005_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0019",
		"pointer_table_index": 25,
		"file_index": 6030,
		"source_file": "bin/spiral_mountain/image_0019.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0019_pal",
		"pointer_table_index": 25,
		"file_index": 6031,
		"source_file": "bin/spiral_mountain/image_0019_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0041",
		"pointer_table_index": 25,
		"file_index": 6032,
		"source_file": "bin/spiral_mountain/image_0041.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0041_pal",
		"pointer_table_index": 25,
		"file_index": 6033,
		"source_file": "bin/spiral_mountain/image_0041_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0017",
		"pointer_table_index": 25,
		"file_index": 6034,
		"source_file": "bin/spiral_mountain/image_0017.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0017_pal",
		"pointer_table_index": 25,
		"file_index": 6035,
		"source_file": "bin/spiral_mountain/image_0017_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0022",
		"pointer_table_index": 25,
		"file_index": 6036,
		"source_file": "bin/spiral_mountain/image_0022.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0022_pal",
		"pointer_table_index": 25,
		"file_index": 6037,
		"source_file": "bin/spiral_mountain/image_0022_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0023",
		"pointer_table_index": 25,
		"file_index": 6038,
		"source_file": "bin/spiral_mountain/image_0023.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0023_pal",
		"pointer_table_index": 25,
		"file_index": 6039,
		"source_file": "bin/spiral_mountain/image_0023_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0037",
		"pointer_table_index": 25,
		"file_index": 6040,
		"source_file": "bin/spiral_mountain/image_0037.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0037_pal",
		"pointer_table_index": 25,
		"file_index": 6041,
		"source_file": "bin/spiral_mountain/image_0037_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0036",
		"pointer_table_index": 25,
		"file_index": 6042,
		"source_file": "bin/spiral_mountain/image_0036.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0036_pal",
		"pointer_table_index": 25,
		"file_index": 6043,
		"source_file": "bin/spiral_mountain/image_0036_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0000",
		"pointer_table_index": 25,
		"file_index": 6044,
		"source_file": "bin/spiral_mountain/image_0000.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0040",
		"pointer_table_index": 25,
		"file_index": 6045,
		"source_file": "bin/spiral_mountain/image_0040.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0040_pal",
		"pointer_table_index": 25,
		"file_index": 6046,
		"source_file": "bin/spiral_mountain/image_0040_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0060",
		"pointer_table_index": 25,
		"file_index": 6047,
		"source_file": "bin/spiral_mountain/image_0060.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0060_pal",
		"pointer_table_index": 25,
		"file_index": 6048,
		"source_file": "bin/spiral_mountain/image_0060_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0008",
		"pointer_table_index": 25,
		"file_index": 6049,
		"source_file": "bin/spiral_mountain/image_0008.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0008_pal",
		"pointer_table_index": 25,
		"file_index": 6050,
		"source_file": "bin/spiral_mountain/image_0008_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0007",
		"pointer_table_index": 25,
		"file_index": 6051,
		"source_file": "bin/spiral_mountain/image_0007.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0007_pal",
		"pointer_table_index": 25,
		"file_index": 6052,
		"source_file": "bin/spiral_mountain/image_0007_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0006",
		"pointer_table_index": 25,
		"file_index": 6053,
		"source_file": "bin/spiral_mountain/image_0006.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0006_pal",
		"pointer_table_index": 25,
		"file_index": 6054,
		"source_file": "bin/spiral_mountain/image_0006_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0021",
		"pointer_table_index": 25,
		"file_index": 6055,
		"source_file": "bin/spiral_mountain/image_0021.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0021_pal",
		"pointer_table_index": 25,
		"file_index": 6056,
		"source_file": "bin/spiral_mountain/image_0021_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0016",
		"pointer_table_index": 25,
		"file_index": 6057,
		"source_file": "bin/spiral_mountain/image_0016.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0016_pal",
		"pointer_table_index": 25,
		"file_index": 6058,
		"source_file": "bin/spiral_mountain/image_0016_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0015",
		"pointer_table_index": 25,
		"file_index": 6059,
		"source_file": "bin/spiral_mountain/image_0015.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0015_pal",
		"pointer_table_index": 25,
		"file_index": 6060,
		"source_file": "bin/spiral_mountain/image_0015_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0026",
		"pointer_table_index": 25,
		"file_index": 6061,
		"source_file": "bin/spiral_mountain/image_0026.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0026_pal",
		"pointer_table_index": 25,
		"file_index": 6062,
		"source_file": "bin/spiral_mountain/image_0026_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0064",
		"pointer_table_index": 25,
		"file_index": 6063,
		"source_file": "bin/spiral_mountain/image_0064.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0068",
		"pointer_table_index": 25,
		"file_index": 6064,
		"source_file": "bin/spiral_mountain/image_0068.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0068_pal",
		"pointer_table_index": 25,
		"file_index": 6065,
		"source_file": "bin/spiral_mountain/image_0068_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0058",
		"pointer_table_index": 25,
		"file_index": 6066,
		"source_file": "bin/spiral_mountain/image_0058.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0058_pal",
		"pointer_table_index": 25,
		"file_index": 6067,
		"source_file": "bin/spiral_mountain/image_0058_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0076",
		"pointer_table_index": 25,
		"file_index": 6068,
		"source_file": "bin/spiral_mountain/image_0076.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0076_pal",
		"pointer_table_index": 25,
		"file_index": 6069,
		"source_file": "bin/spiral_mountain/image_0076_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0075",
		"pointer_table_index": 25,
		"file_index": 6070,
		"source_file": "bin/spiral_mountain/image_0075.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0069",
		"pointer_table_index": 25,
		"file_index": 6071,
		"source_file": "bin/spiral_mountain/image_0069.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0069_pal",
		"pointer_table_index": 25,
		"file_index": 6072,
		"source_file": "bin/spiral_mountain/image_0069_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0027",
		"pointer_table_index": 25,
		"file_index": 6073,
		"source_file": "bin/spiral_mountain/image_0027.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0027_pal",
		"pointer_table_index": 25,
		"file_index": 6074,
		"source_file": "bin/spiral_mountain/image_0027_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0065",
		"pointer_table_index": 25,
		"file_index": 6075,
		"source_file": "bin/spiral_mountain/image_0065.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0066",
		"pointer_table_index": 25,
		"file_index": 6076,
		"source_file": "bin/spiral_mountain/image_0066.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0067",
		"pointer_table_index": 25,
		"file_index": 6077,
		"source_file": "bin/spiral_mountain/image_0067.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0030",
		"pointer_table_index": 25,
		"file_index": 6078,
		"source_file": "bin/spiral_mountain/image_0030.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0030_pal",
		"pointer_table_index": 25,
		"file_index": 6079,
		"source_file": "bin/spiral_mountain/image_0030_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0014",
		"pointer_table_index": 25,
		"file_index": 6080,
		"source_file": "bin/spiral_mountain/image_0014.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0014_pal",
		"pointer_table_index": 25,
		"file_index": 6081,
		"source_file": "bin/spiral_mountain/image_0014_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0024",
		"pointer_table_index": 25,
		"file_index": 6082,
		"source_file": "bin/spiral_mountain/image_0024.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0024_pal",
		"pointer_table_index": 25,
		"file_index": 6083,
		"source_file": "bin/spiral_mountain/image_0024_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0025",
		"pointer_table_index": 25,
		"file_index": 6084,
		"source_file": "bin/spiral_mountain/image_0025.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0025_pal",
		"pointer_table_index": 25,
		"file_index": 6085,
		"source_file": "bin/spiral_mountain/image_0025_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0010",
		"pointer_table_index": 25,
		"file_index": 6086,
		"source_file": "bin/spiral_mountain/image_0010.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0010_pal",
		"pointer_table_index": 25,
		"file_index": 6087,
		"source_file": "bin/spiral_mountain/image_0010_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0009",
		"pointer_table_index": 25,
		"file_index": 6088,
		"source_file": "bin/spiral_mountain/image_0009.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0009_pal",
		"pointer_table_index": 25,
		"file_index": 6089,
		"source_file": "bin/spiral_mountain/image_0009_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0055",
		"pointer_table_index": 25,
		"file_index": 6090,
		"source_file": "bin/spiral_mountain/image_0055.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0001",
		"pointer_table_index": 25,
		"file_index": 6091,
		"source_file": "bin/spiral_mountain/image_0001.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0031",
		"pointer_table_index": 25,
		"file_index": 6092,
		"source_file": "bin/spiral_mountain/image_0031.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0031_pal",
		"pointer_table_index": 25,
		"file_index": 6093,
		"source_file": "bin/spiral_mountain/image_0031_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0033",
		"pointer_table_index": 25,
		"file_index": 6094,
		"source_file": "bin/spiral_mountain/image_0033.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0033_pal",
		"pointer_table_index": 25,
		"file_index": 6095,
		"source_file": "bin/spiral_mountain/image_0033_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0028",
		"pointer_table_index": 25,
		"file_index": 6096,
		"source_file": "bin/spiral_mountain/image_0028.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0028_pal",
		"pointer_table_index": 25,
		"file_index": 6097,
		"source_file": "bin/spiral_mountain/image_0028_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0029",
		"pointer_table_index": 25,
		"file_index": 6098,
		"source_file": "bin/spiral_mountain/image_0029.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0029_pal",
		"pointer_table_index": 25,
		"file_index": 6099,
		"source_file": "bin/spiral_mountain/image_0029_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0034",
		"pointer_table_index": 25,
		"file_index": 6100,
		"source_file": "bin/spiral_mountain/image_0034.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0034_pal",
		"pointer_table_index": 25,
		"file_index": 6101,
		"source_file": "bin/spiral_mountain/image_0034_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0032",
		"pointer_table_index": 25,
		"file_index": 6102,
		"source_file": "bin/spiral_mountain/image_0032.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0063",
		"pointer_table_index": 25,
		"file_index": 6103,
		"source_file": "bin/spiral_mountain/image_0063.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0059",
		"pointer_table_index": 25,
		"file_index": 6104,
		"source_file": "bin/spiral_mountain/image_0059.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0059_pal",
		"pointer_table_index": 25,
		"file_index": 6105,
		"source_file": "bin/spiral_mountain/image_0059_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0038",
		"pointer_table_index": 25,
		"file_index": 6106,
		"source_file": "bin/spiral_mountain/image_0038.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0039",
		"pointer_table_index": 25,
		"file_index": 6107,
		"source_file": "bin/spiral_mountain/image_0039.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0039_pal",
		"pointer_table_index": 25,
		"file_index": 6108,
		"source_file": "bin/spiral_mountain/image_0039_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0048",
		"pointer_table_index": 25,
		"file_index": 6109,
		"source_file": "bin/spiral_mountain/image_0048.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0048_pal",
		"pointer_table_index": 25,
		"file_index": 6110,
		"source_file": "bin/spiral_mountain/image_0048_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0046",
		"pointer_table_index": 25,
		"file_index": 6111,
		"source_file": "bin/spiral_mountain/image_0046.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0046_pal",
		"pointer_table_index": 25,
		"file_index": 6112,
		"source_file": "bin/spiral_mountain/image_0046_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0047",
		"pointer_table_index": 25,
		"file_index": 6113,
		"source_file": "bin/spiral_mountain/image_0047.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0047_pal",
		"pointer_table_index": 25,
		"file_index": 6114,
		"source_file": "bin/spiral_mountain/image_0047_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0061",
		"pointer_table_index": 25,
		"file_index": 6115,
		"source_file": "bin/spiral_mountain/image_0061.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0061_pal",
		"pointer_table_index": 25,
		"file_index": 6116,
		"source_file": "bin/spiral_mountain/image_0061_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0004",
		"pointer_table_index": 25,
		"file_index": 6117,
		"source_file": "bin/spiral_mountain/image_0004.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0011",
		"pointer_table_index": 25,
		"file_index": 6118,
		"source_file": "bin/spiral_mountain/image_0011.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0050",
		"pointer_table_index": 25,
		"file_index": 6119,
		"source_file": "bin/spiral_mountain/image_0050.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0050_pal",
		"pointer_table_index": 25,
		"file_index": 6120,
		"source_file": "bin/spiral_mountain/image_0050_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0057",
		"pointer_table_index": 25,
		"file_index": 6121,
		"source_file": "bin/spiral_mountain/image_0057.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0070",
		"pointer_table_index": 25,
		"file_index": 6122,
		"source_file": "bin/spiral_mountain/image_0070.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0070_pal",
		"pointer_table_index": 25,
		"file_index": 6123,
		"source_file": "bin/spiral_mountain/image_0070_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0044",
		"pointer_table_index": 25,
		"file_index": 6124,
		"source_file": "bin/spiral_mountain/image_0044.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0044_pal",
		"pointer_table_index": 25,
		"file_index": 6125,
		"source_file": "bin/spiral_mountain/image_0044_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0072",
		"pointer_table_index": 25,
		"file_index": 6126,
		"source_file": "bin/spiral_mountain/image_0072.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0072_pal",
		"pointer_table_index": 25,
		"file_index": 6127,
		"source_file": "bin/spiral_mountain/image_0072_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0073",
		"pointer_table_index": 25,
		"file_index": 6128,
		"source_file": "bin/spiral_mountain/image_0073.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0073_pal",
		"pointer_table_index": 25,
		"file_index": 6129,
		"source_file": "bin/spiral_mountain/image_0073_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0049",
		"pointer_table_index": 25,
		"file_index": 6130,
		"source_file": "bin/spiral_mountain/image_0049.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0049_pal",
		"pointer_table_index": 25,
		"file_index": 6131,
		"source_file": "bin/spiral_mountain/image_0049_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0045",
		"pointer_table_index": 25,
		"file_index": 6132,
		"source_file": "bin/spiral_mountain/image_0045.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0045_pal",
		"pointer_table_index": 25,
		"file_index": 6133,
		"source_file": "bin/spiral_mountain/image_0045_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0043",
		"pointer_table_index": 25,
		"file_index": 6134,
		"source_file": "bin/spiral_mountain/image_0043.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0043_pal",
		"pointer_table_index": 25,
		"file_index": 6135,
		"source_file": "bin/spiral_mountain/image_0043_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0062",
		"pointer_table_index": 25,
		"file_index": 6136,
		"source_file": "bin/spiral_mountain/image_0062.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0042",
		"pointer_table_index": 25,
		"file_index": 6137,
		"source_file": "bin/spiral_mountain/image_0042.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0042_pal",
		"pointer_table_index": 25,
		"file_index": 6138,
		"source_file": "bin/spiral_mountain/image_0042_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0051",
		"pointer_table_index": 25,
		"file_index": 6139,
		"source_file": "bin/spiral_mountain/image_0051.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0051_pal",
		"pointer_table_index": 25,
		"file_index": 6140,
		"source_file": "bin/spiral_mountain/image_0051_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0071",
		"pointer_table_index": 25,
		"file_index": 6141,
		"source_file": "bin/spiral_mountain/image_0071.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0054",
		"pointer_table_index": 25,
		"file_index": 6142,
		"source_file": "bin/spiral_mountain/image_0054.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0053",
		"pointer_table_index": 25,
		"file_index": 6143,
		"source_file": "bin/spiral_mountain/image_0053.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0053_pal",
		"pointer_table_index": 25,
		"file_index": 6144,
		"source_file": "bin/spiral_mountain/image_0053_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0074",
		"pointer_table_index": 25,
		"file_index": 6145,
		"source_file": "bin/spiral_mountain/image_0074.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0052",
		"pointer_table_index": 25,
		"file_index": 6146,
		"source_file": "bin/spiral_mountain/image_0052.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0066",
		"pointer_table_index": 25,
		"file_index": 6147,
		"source_file": "bin/lair_entrance/image_0066.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0066_pal",
		"pointer_table_index": 25,
		"file_index": 6148,
		"source_file": "bin/lair_entrance/image_0066_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0052",
		"pointer_table_index": 25,
		"file_index": 6149,
		"source_file": "bin/lair_entrance/image_0052.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0052_pal",
		"pointer_table_index": 25,
		"file_index": 6150,
		"source_file": "bin/lair_entrance/image_0052_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0070",
		"pointer_table_index": 25,
		"file_index": 6151,
		"source_file": "bin/lair_entrance/image_0070.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0067",
		"pointer_table_index": 25,
		"file_index": 6152,
		"source_file": "bin/lair_entrance/image_0067.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0069",
		"pointer_table_index": 25,
		"file_index": 6153,
		"source_file": "bin/lair_entrance/image_0069.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0068",
		"pointer_table_index": 25,
		"file_index": 6154,
		"source_file": "bin/lair_entrance/image_0068.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0051",
		"pointer_table_index": 25,
		"file_index": 6155,
		"source_file": "bin/lair_entrance/image_0051.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0050",
		"pointer_table_index": 25,
		"file_index": 6156,
		"source_file": "bin/lair_entrance/image_0050.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0049",
		"pointer_table_index": 25,
		"file_index": 6157,
		"source_file": "bin/lair_entrance/image_0049.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0048",
		"pointer_table_index": 25,
		"file_index": 6158,
		"source_file": "bin/lair_entrance/image_0048.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0044",
		"pointer_table_index": 25,
		"file_index": 6159,
		"source_file": "bin/lair_entrance/image_0044.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0043",
		"pointer_table_index": 25,
		"file_index": 6160,
		"source_file": "bin/lair_entrance/image_0043.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0036",
		"pointer_table_index": 25,
		"file_index": 6161,
		"source_file": "bin/lair_entrance/image_0036.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0037",
		"pointer_table_index": 25,
		"file_index": 6162,
		"source_file": "bin/lair_entrance/image_0037.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0042",
		"pointer_table_index": 25,
		"file_index": 6163,
		"source_file": "bin/lair_entrance/image_0042.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0038",
		"pointer_table_index": 25,
		"file_index": 6164,
		"source_file": "bin/lair_entrance/image_0038.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0039",
		"pointer_table_index": 25,
		"file_index": 6165,
		"source_file": "bin/lair_entrance/image_0039.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0040",
		"pointer_table_index": 25,
		"file_index": 6166,
		"source_file": "bin/lair_entrance/image_0040.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0047",
		"pointer_table_index": 25,
		"file_index": 6167,
		"source_file": "bin/lair_entrance/image_0047.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0046",
		"pointer_table_index": 25,
		"file_index": 6168,
		"source_file": "bin/lair_entrance/image_0046.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0041",
		"pointer_table_index": 25,
		"file_index": 6169,
		"source_file": "bin/lair_entrance/image_0041.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0045",
		"pointer_table_index": 25,
		"file_index": 6170,
		"source_file": "bin/lair_entrance/image_0045.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0063",
		"pointer_table_index": 25,
		"file_index": 6171,
		"source_file": "bin/lair_entrance/image_0063.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0063_pal",
		"pointer_table_index": 25,
		"file_index": 6172,
		"source_file": "bin/lair_entrance/image_0063_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0000",
		"pointer_table_index": 25,
		"file_index": 6173,
		"source_file": "bin/lair_entrance/image_0000.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0000_pal",
		"pointer_table_index": 25,
		"file_index": 6174,
		"source_file": "bin/lair_entrance/image_0000_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0062",
		"pointer_table_index": 25,
		"file_index": 6175,
		"source_file": "bin/lair_entrance/image_0062.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0062_pal",
		"pointer_table_index": 25,
		"file_index": 6176,
		"source_file": "bin/lair_entrance/image_0062_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0003",
		"pointer_table_index": 25,
		"file_index": 6177,
		"source_file": "bin/lair_entrance/image_0003.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0003_pal",
		"pointer_table_index": 25,
		"file_index": 6178,
		"source_file": "bin/lair_entrance/image_0003_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0026",
		"pointer_table_index": 25,
		"file_index": 6179,
		"source_file": "bin/lair_entrance/image_0026.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0026_pal",
		"pointer_table_index": 25,
		"file_index": 6180,
		"source_file": "bin/lair_entrance/image_0026_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0009",
		"pointer_table_index": 25,
		"file_index": 6181,
		"source_file": "bin/lair_entrance/image_0009.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0009_pal",
		"pointer_table_index": 25,
		"file_index": 6182,
		"source_file": "bin/lair_entrance/image_0009_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0025",
		"pointer_table_index": 25,
		"file_index": 6183,
		"source_file": "bin/lair_entrance/image_0025.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0025_pal",
		"pointer_table_index": 25,
		"file_index": 6184,
		"source_file": "bin/lair_entrance/image_0025_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0034",
		"pointer_table_index": 25,
		"file_index": 6185,
		"source_file": "bin/lair_entrance/image_0034.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0034_pal",
		"pointer_table_index": 25,
		"file_index": 6186,
		"source_file": "bin/lair_entrance/image_0034_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0010",
		"pointer_table_index": 25,
		"file_index": 6187,
		"source_file": "bin/lair_entrance/image_0010.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0010_pal",
		"pointer_table_index": 25,
		"file_index": 6188,
		"source_file": "bin/lair_entrance/image_0010_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0035",
		"pointer_table_index": 25,
		"file_index": 6189,
		"source_file": "bin/lair_entrance/image_0035.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0035_pal",
		"pointer_table_index": 25,
		"file_index": 6190,
		"source_file": "bin/lair_entrance/image_0035_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0054",
		"pointer_table_index": 25,
		"file_index": 6191,
		"source_file": "bin/lair_entrance/image_0054.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0053",
		"pointer_table_index": 25,
		"file_index": 6192,
		"source_file": "bin/lair_entrance/image_0053.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0023",
		"pointer_table_index": 25,
		"file_index": 6193,
		"source_file": "bin/lair_entrance/image_0023.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0023_pal",
		"pointer_table_index": 25,
		"file_index": 6194,
		"source_file": "bin/lair_entrance/image_0023_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0024",
		"pointer_table_index": 25,
		"file_index": 6195,
		"source_file": "bin/lair_entrance/image_0024.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0012",
		"pointer_table_index": 25,
		"file_index": 6196,
		"source_file": "bin/lair_entrance/image_0012.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0012_pal",
		"pointer_table_index": 25,
		"file_index": 6197,
		"source_file": "bin/lair_entrance/image_0012_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0015",
		"pointer_table_index": 25,
		"file_index": 6198,
		"source_file": "bin/lair_entrance/image_0015.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0015_pal",
		"pointer_table_index": 25,
		"file_index": 6199,
		"source_file": "bin/lair_entrance/image_0015_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0013",
		"pointer_table_index": 25,
		"file_index": 6200,
		"source_file": "bin/lair_entrance/image_0013.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0013_pal",
		"pointer_table_index": 25,
		"file_index": 6201,
		"source_file": "bin/lair_entrance/image_0013_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0018",
		"pointer_table_index": 25,
		"file_index": 6202,
		"source_file": "bin/lair_entrance/image_0018.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0020",
		"pointer_table_index": 25,
		"file_index": 6203,
		"source_file": "bin/lair_entrance/image_0020.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0019",
		"pointer_table_index": 25,
		"file_index": 6204,
		"source_file": "bin/lair_entrance/image_0019.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0021",
		"pointer_table_index": 25,
		"file_index": 6205,
		"source_file": "bin/lair_entrance/image_0021.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0028",
		"pointer_table_index": 25,
		"file_index": 6206,
		"source_file": "bin/lair_entrance/image_0028.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0022",
		"pointer_table_index": 25,
		"file_index": 6207,
		"source_file": "bin/lair_entrance/image_0022.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0027",
		"pointer_table_index": 25,
		"file_index": 6208,
		"source_file": "bin/lair_entrance/image_0027.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0027_pal",
		"pointer_table_index": 25,
		"file_index": 6209,
		"source_file": "bin/lair_entrance/image_0027_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0058",
		"pointer_table_index": 25,
		"file_index": 6210,
		"source_file": "bin/lair_entrance/image_0058.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0058_pal",
		"pointer_table_index": 25,
		"file_index": 6211,
		"source_file": "bin/lair_entrance/image_0058_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0059",
		"pointer_table_index": 25,
		"file_index": 6212,
		"source_file": "bin/lair_entrance/image_0059.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0059_pal",
		"pointer_table_index": 25,
		"file_index": 6213,
		"source_file": "bin/lair_entrance/image_0059_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0056",
		"pointer_table_index": 25,
		"file_index": 6214,
		"source_file": "bin/lair_entrance/image_0056.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0056_pal",
		"pointer_table_index": 25,
		"file_index": 6215,
		"source_file": "bin/lair_entrance/image_0056_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0001",
		"pointer_table_index": 25,
		"file_index": 6216,
		"source_file": "bin/lair_entrance/image_0001.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0001_pal",
		"pointer_table_index": 25,
		"file_index": 6217,
		"source_file": "bin/lair_entrance/image_0001_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0005",
		"pointer_table_index": 25,
		"file_index": 6218,
		"source_file": "bin/lair_entrance/image_0005.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0005_pal",
		"pointer_table_index": 25,
		"file_index": 6219,
		"source_file": "bin/lair_entrance/image_0005_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0004",
		"pointer_table_index": 25,
		"file_index": 6220,
		"source_file": "bin/lair_entrance/image_0004.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0004_pal",
		"pointer_table_index": 25,
		"file_index": 6221,
		"source_file": "bin/lair_entrance/image_0004_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0006",
		"pointer_table_index": 25,
		"file_index": 6222,
		"source_file": "bin/lair_entrance/image_0006.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0006_pal",
		"pointer_table_index": 25,
		"file_index": 6223,
		"source_file": "bin/lair_entrance/image_0006_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0064",
		"pointer_table_index": 25,
		"file_index": 6224,
		"source_file": "bin/lair_entrance/image_0064.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0017",
		"pointer_table_index": 25,
		"file_index": 6225,
		"source_file": "bin/lair_entrance/image_0017.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0017_pal",
		"pointer_table_index": 25,
		"file_index": 6226,
		"source_file": "bin/lair_entrance/image_0017_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0065",
		"pointer_table_index": 25,
		"file_index": 6227,
		"source_file": "bin/lair_entrance/image_0065.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0065_pal",
		"pointer_table_index": 25,
		"file_index": 6228,
		"source_file": "bin/lair_entrance/image_0065_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0060",
		"pointer_table_index": 25,
		"file_index": 6229,
		"source_file": "bin/lair_entrance/image_0060.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0032",
		"pointer_table_index": 25,
		"file_index": 6230,
		"source_file": "bin/lair_entrance/image_0032.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0032_pal",
		"pointer_table_index": 25,
		"file_index": 6231,
		"source_file": "bin/lair_entrance/image_0032_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0031",
		"pointer_table_index": 25,
		"file_index": 6232,
		"source_file": "bin/lair_entrance/image_0031.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0031_pal",
		"pointer_table_index": 25,
		"file_index": 6233,
		"source_file": "bin/lair_entrance/image_0031_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0033",
		"pointer_table_index": 25,
		"file_index": 6234,
		"source_file": "bin/lair_entrance/image_0033.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0033_pal",
		"pointer_table_index": 25,
		"file_index": 6235,
		"source_file": "bin/lair_entrance/image_0033_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0014",
		"pointer_table_index": 25,
		"file_index": 6236,
		"source_file": "bin/lair_entrance/image_0014.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0014_pal",
		"pointer_table_index": 25,
		"file_index": 6237,
		"source_file": "bin/lair_entrance/image_0014_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0011",
		"pointer_table_index": 25,
		"file_index": 6238,
		"source_file": "bin/lair_entrance/image_0011.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0011_pal",
		"pointer_table_index": 25,
		"file_index": 6239,
		"source_file": "bin/lair_entrance/image_0011_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0016",
		"pointer_table_index": 25,
		"file_index": 6240,
		"source_file": "bin/lair_entrance/image_0016.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0016_pal",
		"pointer_table_index": 25,
		"file_index": 6241,
		"source_file": "bin/lair_entrance/image_0016_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0061",
		"pointer_table_index": 25,
		"file_index": 6242,
		"source_file": "bin/lair_entrance/image_0061.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0061_pal",
		"pointer_table_index": 25,
		"file_index": 6243,
		"source_file": "bin/lair_entrance/image_0061_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0007",
		"pointer_table_index": 25,
		"file_index": 6244,
		"source_file": "bin/lair_entrance/image_0007.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0007_pal",
		"pointer_table_index": 25,
		"file_index": 6245,
		"source_file": "bin/lair_entrance/image_0007_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0008",
		"pointer_table_index": 25,
		"file_index": 6246,
		"source_file": "bin/lair_entrance/image_0008.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0008_pal",
		"pointer_table_index": 25,
		"file_index": 6247,
		"source_file": "bin/lair_entrance/image_0008_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0055",
		"pointer_table_index": 25,
		"file_index": 6248,
		"source_file": "bin/lair_entrance/image_0055.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0055_pal",
		"pointer_table_index": 25,
		"file_index": 6249,
		"source_file": "bin/lair_entrance/image_0055_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0029",
		"pointer_table_index": 25,
		"file_index": 6250,
		"source_file": "bin/lair_entrance/image_0029.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0029_pal",
		"pointer_table_index": 25,
		"file_index": 6251,
		"source_file": "bin/lair_entrance/image_0029_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0002",
		"pointer_table_index": 25,
		"file_index": 6252,
		"source_file": "bin/lair_entrance/image_0002.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0002_pal",
		"pointer_table_index": 25,
		"file_index": 6253,
		"source_file": "bin/lair_entrance/image_0002_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0030",
		"pointer_table_index": 25,
		"file_index": 6254,
		"source_file": "bin/lair_entrance/image_0030.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0030_pal",
		"pointer_table_index": 25,
		"file_index": 6255,
		"source_file": "bin/lair_entrance/image_0030_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0057",
		"pointer_table_index": 25,
		"file_index": 6256,
		"source_file": "bin/lair_entrance/image_0057.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0057_pal",
		"pointer_table_index": 25,
		"file_index": 6257,
		"source_file": "bin/lair_entrance/image_0057_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0005",
		"pointer_table_index": 25,
		"file_index": 6258,
		"source_file": "bin/mumbosmountain/image_0005.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0005_pal",
		"pointer_table_index": 25,
		"file_index": 6259,
		"source_file": "bin/mumbosmountain/image_0005_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0006",
		"pointer_table_index": 25,
		"file_index": 6260,
		"source_file": "bin/mumbosmountain/image_0006.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0006_pal",
		"pointer_table_index": 25,
		"file_index": 6261,
		"source_file": "bin/mumbosmountain/image_0006_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0007",
		"pointer_table_index": 25,
		"file_index": 6262,
		"source_file": "bin/mumbosmountain/image_0007.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0007_pal",
		"pointer_table_index": 25,
		"file_index": 6263,
		"source_file": "bin/mumbosmountain/image_0007_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0004",
		"pointer_table_index": 25,
		"file_index": 6264,
		"source_file": "bin/mumbosmountain/image_0004.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0004_pal",
		"pointer_table_index": 25,
		"file_index": 6265,
		"source_file": "bin/mumbosmountain/image_0004_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0025",
		"pointer_table_index": 25,
		"file_index": 6266,
		"source_file": "bin/mumbosmountain/image_0025.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0025_pal",
		"pointer_table_index": 25,
		"file_index": 6267,
		"source_file": "bin/mumbosmountain/image_0025_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0026",
		"pointer_table_index": 25,
		"file_index": 6268,
		"source_file": "bin/mumbosmountain/image_0026.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0026_pal",
		"pointer_table_index": 25,
		"file_index": 6269,
		"source_file": "bin/mumbosmountain/image_0026_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0019",
		"pointer_table_index": 25,
		"file_index": 6270,
		"source_file": "bin/mumbosmountain/image_0019.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0019_pal",
		"pointer_table_index": 25,
		"file_index": 6271,
		"source_file": "bin/mumbosmountain/image_0019_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0050",
		"pointer_table_index": 25,
		"file_index": 6272,
		"source_file": "bin/mumbosmountain/image_0050.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0050_pal",
		"pointer_table_index": 25,
		"file_index": 6273,
		"source_file": "bin/mumbosmountain/image_0050_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0049",
		"pointer_table_index": 25,
		"file_index": 6274,
		"source_file": "bin/mumbosmountain/image_0049.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0049_pal",
		"pointer_table_index": 25,
		"file_index": 6275,
		"source_file": "bin/mumbosmountain/image_0049_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0053",
		"pointer_table_index": 25,
		"file_index": 6276,
		"source_file": "bin/mumbosmountain/image_0053.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0053_pal",
		"pointer_table_index": 25,
		"file_index": 6277,
		"source_file": "bin/mumbosmountain/image_0053_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0052",
		"pointer_table_index": 25,
		"file_index": 6278,
		"source_file": "bin/mumbosmountain/image_0052.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0052_pal",
		"pointer_table_index": 25,
		"file_index": 6279,
		"source_file": "bin/mumbosmountain/image_0052_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0000",
		"pointer_table_index": 25,
		"file_index": 6280,
		"source_file": "bin/mumbosmountain/image_0000.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0000_pal",
		"pointer_table_index": 25,
		"file_index": 6281,
		"source_file": "bin/mumbosmountain/image_0000_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0015",
		"pointer_table_index": 25,
		"file_index": 6282,
		"source_file": "bin/mumbosmountain/image_0015.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0027",
		"pointer_table_index": 25,
		"file_index": 6283,
		"source_file": "bin/mumbosmountain/image_0027.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0027_pal",
		"pointer_table_index": 25,
		"file_index": 6284,
		"source_file": "bin/mumbosmountain/image_0027_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0028",
		"pointer_table_index": 25,
		"file_index": 6285,
		"source_file": "bin/mumbosmountain/image_0028.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0028_pal",
		"pointer_table_index": 25,
		"file_index": 6286,
		"source_file": "bin/mumbosmountain/image_0028_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0022",
		"pointer_table_index": 25,
		"file_index": 6287,
		"source_file": "bin/mumbosmountain/image_0022.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0022_pal",
		"pointer_table_index": 25,
		"file_index": 6288,
		"source_file": "bin/mumbosmountain/image_0022_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0014",
		"pointer_table_index": 25,
		"file_index": 6289,
		"source_file": "bin/mumbosmountain/image_0014.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0014_pal",
		"pointer_table_index": 25,
		"file_index": 6290,
		"source_file": "bin/mumbosmountain/image_0014_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0021",
		"pointer_table_index": 25,
		"file_index": 6291,
		"source_file": "bin/mumbosmountain/image_0021.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0021_pal",
		"pointer_table_index": 25,
		"file_index": 6292,
		"source_file": "bin/mumbosmountain/image_0021_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0029",
		"pointer_table_index": 25,
		"file_index": 6293,
		"source_file": "bin/mumbosmountain/image_0029.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0029_pal",
		"pointer_table_index": 25,
		"file_index": 6294,
		"source_file": "bin/mumbosmountain/image_0029_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0051",
		"pointer_table_index": 25,
		"file_index": 6295,
		"source_file": "bin/mumbosmountain/image_0051.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0002",
		"pointer_table_index": 25,
		"file_index": 6296,
		"source_file": "bin/mumbosmountain/image_0002.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0054",
		"pointer_table_index": 25,
		"file_index": 6297,
		"source_file": "bin/mumbosmountain/image_0054.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0001",
		"pointer_table_index": 25,
		"file_index": 6298,
		"source_file": "bin/mumbosmountain/image_0001.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0039",
		"pointer_table_index": 25,
		"file_index": 6299,
		"source_file": "bin/mumbosmountain/image_0039.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0032",
		"pointer_table_index": 25,
		"file_index": 6300,
		"source_file": "bin/mumbosmountain/image_0032.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0032_pal",
		"pointer_table_index": 25,
		"file_index": 6301,
		"source_file": "bin/mumbosmountain/image_0032_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0010",
		"pointer_table_index": 25,
		"file_index": 6302,
		"source_file": "bin/mumbosmountain/image_0010.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0048",
		"pointer_table_index": 25,
		"file_index": 6303,
		"source_file": "bin/mumbosmountain/image_0048.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0048_pal",
		"pointer_table_index": 25,
		"file_index": 6304,
		"source_file": "bin/mumbosmountain/image_0048_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0047",
		"pointer_table_index": 25,
		"file_index": 6305,
		"source_file": "bin/mumbosmountain/image_0047.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0047_pal",
		"pointer_table_index": 25,
		"file_index": 6306,
		"source_file": "bin/mumbosmountain/image_0047_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0009",
		"pointer_table_index": 25,
		"file_index": 6307,
		"source_file": "bin/mumbosmountain/image_0009.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0009_pal",
		"pointer_table_index": 25,
		"file_index": 6308,
		"source_file": "bin/mumbosmountain/image_0009_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0046",
		"pointer_table_index": 25,
		"file_index": 6309,
		"source_file": "bin/mumbosmountain/image_0046.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0038",
		"pointer_table_index": 25,
		"file_index": 6310,
		"source_file": "bin/mumbosmountain/image_0038.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0036",
		"pointer_table_index": 25,
		"file_index": 6311,
		"source_file": "bin/mumbosmountain/image_0036.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0036_pal",
		"pointer_table_index": 25,
		"file_index": 6312,
		"source_file": "bin/mumbosmountain/image_0036_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0035",
		"pointer_table_index": 25,
		"file_index": 6313,
		"source_file": "bin/mumbosmountain/image_0035.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0035_pal",
		"pointer_table_index": 25,
		"file_index": 6314,
		"source_file": "bin/mumbosmountain/image_0035_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0034",
		"pointer_table_index": 25,
		"file_index": 6315,
		"source_file": "bin/mumbosmountain/image_0034.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0034_pal",
		"pointer_table_index": 25,
		"file_index": 6316,
		"source_file": "bin/mumbosmountain/image_0034_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0003",
		"pointer_table_index": 25,
		"file_index": 6317,
		"source_file": "bin/mumbosmountain/image_0003.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0016",
		"pointer_table_index": 25,
		"file_index": 6318,
		"source_file": "bin/mumbosmountain/image_0016.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0016_pal",
		"pointer_table_index": 25,
		"file_index": 6319,
		"source_file": "bin/mumbosmountain/image_0016_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0017",
		"pointer_table_index": 25,
		"file_index": 6320,
		"source_file": "bin/mumbosmountain/image_0017.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0017_pal",
		"pointer_table_index": 25,
		"file_index": 6321,
		"source_file": "bin/mumbosmountain/image_0017_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0024",
		"pointer_table_index": 25,
		"file_index": 6322,
		"source_file": "bin/mumbosmountain/image_0024.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0024_pal",
		"pointer_table_index": 25,
		"file_index": 6323,
		"source_file": "bin/mumbosmountain/image_0024_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0011",
		"pointer_table_index": 25,
		"file_index": 6324,
		"source_file": "bin/mumbosmountain/image_0011.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0011_pal",
		"pointer_table_index": 25,
		"file_index": 6325,
		"source_file": "bin/mumbosmountain/image_0011_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0023",
		"pointer_table_index": 25,
		"file_index": 6326,
		"source_file": "bin/mumbosmountain/image_0023.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0023_pal",
		"pointer_table_index": 25,
		"file_index": 6327,
		"source_file": "bin/mumbosmountain/image_0023_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0020",
		"pointer_table_index": 25,
		"file_index": 6328,
		"source_file": "bin/mumbosmountain/image_0020.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0020_pal",
		"pointer_table_index": 25,
		"file_index": 6329,
		"source_file": "bin/mumbosmountain/image_0020_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0018",
		"pointer_table_index": 25,
		"file_index": 6330,
		"source_file": "bin/mumbosmountain/image_0018.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0018_pal",
		"pointer_table_index": 25,
		"file_index": 6331,
		"source_file": "bin/mumbosmountain/image_0018_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0037",
		"pointer_table_index": 25,
		"file_index": 6332,
		"source_file": "bin/mumbosmountain/image_0037.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0033",
		"pointer_table_index": 25,
		"file_index": 6333,
		"source_file": "bin/mumbosmountain/image_0033.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0033_pal",
		"pointer_table_index": 25,
		"file_index": 6334,
		"source_file": "bin/mumbosmountain/image_0033_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0030",
		"pointer_table_index": 25,
		"file_index": 6335,
		"source_file": "bin/mumbosmountain/image_0030.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0008",
		"pointer_table_index": 25,
		"file_index": 6336,
		"source_file": "bin/mumbosmountain/image_0008.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0008_pal",
		"pointer_table_index": 25,
		"file_index": 6337,
		"source_file": "bin/mumbosmountain/image_0008_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0031",
		"pointer_table_index": 25,
		"file_index": 6338,
		"source_file": "bin/mumbosmountain/image_0031.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0012",
		"pointer_table_index": 25,
		"file_index": 6339,
		"source_file": "bin/mumbosmountain/image_0012.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0013",
		"pointer_table_index": 25,
		"file_index": 6340,
		"source_file": "bin/mumbosmountain/image_0013.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0057",
		"pointer_table_index": 25,
		"file_index": 6341,
		"source_file": "bin/mumbosmountain/image_0057.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0056",
		"pointer_table_index": 25,
		"file_index": 6342,
		"source_file": "bin/mumbosmountain/image_0056.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0055",
		"pointer_table_index": 25,
		"file_index": 6343,
		"source_file": "bin/mumbosmountain/image_0055.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0041",
		"pointer_table_index": 25,
		"file_index": 6344,
		"source_file": "bin/mumbosmountain/image_0041.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0043",
		"pointer_table_index": 25,
		"file_index": 6345,
		"source_file": "bin/mumbosmountain/image_0043.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0043_pal",
		"pointer_table_index": 25,
		"file_index": 6346,
		"source_file": "bin/mumbosmountain/image_0043_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0042",
		"pointer_table_index": 25,
		"file_index": 6347,
		"source_file": "bin/mumbosmountain/image_0042.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0042_pal",
		"pointer_table_index": 25,
		"file_index": 6348,
		"source_file": "bin/mumbosmountain/image_0042_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0045",
		"pointer_table_index": 25,
		"file_index": 6349,
		"source_file": "bin/mumbosmountain/image_0045.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0040",
		"pointer_table_index": 25,
		"file_index": 6350,
		"source_file": "bin/mumbosmountain/image_0040.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0040_pal",
		"pointer_table_index": 25,
		"file_index": 6351,
		"source_file": "bin/mumbosmountain/image_0040_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0044",
		"pointer_table_index": 25,
		"file_index": 6352,
		"source_file": "bin/mumbosmountain/image_0044.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0044_pal",
		"pointer_table_index": 25,
		"file_index": 6353,
		"source_file": "bin/mumbosmountain/image_0044_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0081",
		"pointer_table_index": 25,
		"file_index": 6354,
		"source_file": "bin/lair_floor_2/image_0081.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0081_pal",
		"pointer_table_index": 25,
		"file_index": 6355,
		"source_file": "bin/lair_floor_2/image_0081_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0000",
		"pointer_table_index": 25,
		"file_index": 6356,
		"source_file": "bin/lair_floor_2/image_0000.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0000_pal",
		"pointer_table_index": 25,
		"file_index": 6357,
		"source_file": "bin/lair_floor_2/image_0000_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0030",
		"pointer_table_index": 25,
		"file_index": 6358,
		"source_file": "bin/lair_floor_2/image_0030.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0030_pal",
		"pointer_table_index": 25,
		"file_index": 6359,
		"source_file": "bin/lair_floor_2/image_0030_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0040",
		"pointer_table_index": 25,
		"file_index": 6360,
		"source_file": "bin/lair_floor_2/image_0040.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0040_pal",
		"pointer_table_index": 25,
		"file_index": 6361,
		"source_file": "bin/lair_floor_2/image_0040_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0044",
		"pointer_table_index": 25,
		"file_index": 6362,
		"source_file": "bin/lair_floor_2/image_0044.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0041",
		"pointer_table_index": 25,
		"file_index": 6363,
		"source_file": "bin/lair_floor_2/image_0041.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0043",
		"pointer_table_index": 25,
		"file_index": 6364,
		"source_file": "bin/lair_floor_2/image_0043.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0042",
		"pointer_table_index": 25,
		"file_index": 6365,
		"source_file": "bin/lair_floor_2/image_0042.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0077",
		"pointer_table_index": 25,
		"file_index": 6366,
		"source_file": "bin/lair_floor_2/image_0077.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0075",
		"pointer_table_index": 25,
		"file_index": 6367,
		"source_file": "bin/lair_floor_2/image_0075.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0073",
		"pointer_table_index": 25,
		"file_index": 6368,
		"source_file": "bin/lair_floor_2/image_0073.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0072",
		"pointer_table_index": 25,
		"file_index": 6369,
		"source_file": "bin/lair_floor_2/image_0072.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0071",
		"pointer_table_index": 25,
		"file_index": 6370,
		"source_file": "bin/lair_floor_2/image_0071.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0065",
		"pointer_table_index": 25,
		"file_index": 6371,
		"source_file": "bin/lair_floor_2/image_0065.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0066",
		"pointer_table_index": 25,
		"file_index": 6372,
		"source_file": "bin/lair_floor_2/image_0066.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0067",
		"pointer_table_index": 25,
		"file_index": 6373,
		"source_file": "bin/lair_floor_2/image_0067.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0078",
		"pointer_table_index": 25,
		"file_index": 6374,
		"source_file": "bin/lair_floor_2/image_0078.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0079",
		"pointer_table_index": 25,
		"file_index": 6375,
		"source_file": "bin/lair_floor_2/image_0079.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0074",
		"pointer_table_index": 25,
		"file_index": 6376,
		"source_file": "bin/lair_floor_2/image_0074.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0080",
		"pointer_table_index": 25,
		"file_index": 6377,
		"source_file": "bin/lair_floor_2/image_0080.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0076",
		"pointer_table_index": 25,
		"file_index": 6378,
		"source_file": "bin/lair_floor_2/image_0076.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0069",
		"pointer_table_index": 25,
		"file_index": 6379,
		"source_file": "bin/lair_floor_2/image_0069.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0070",
		"pointer_table_index": 25,
		"file_index": 6380,
		"source_file": "bin/lair_floor_2/image_0070.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0068",
		"pointer_table_index": 25,
		"file_index": 6381,
		"source_file": "bin/lair_floor_2/image_0068.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0039",
		"pointer_table_index": 25,
		"file_index": 6382,
		"source_file": "bin/lair_floor_2/image_0039.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0039_pal",
		"pointer_table_index": 25,
		"file_index": 6383,
		"source_file": "bin/lair_floor_2/image_0039_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0048",
		"pointer_table_index": 25,
		"file_index": 6384,
		"source_file": "bin/lair_floor_2/image_0048.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0045",
		"pointer_table_index": 25,
		"file_index": 6385,
		"source_file": "bin/lair_floor_2/image_0045.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0047",
		"pointer_table_index": 25,
		"file_index": 6386,
		"source_file": "bin/lair_floor_2/image_0047.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0046",
		"pointer_table_index": 25,
		"file_index": 6387,
		"source_file": "bin/lair_floor_2/image_0046.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0064",
		"pointer_table_index": 25,
		"file_index": 6388,
		"source_file": "bin/lair_floor_2/image_0064.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0062",
		"pointer_table_index": 25,
		"file_index": 6389,
		"source_file": "bin/lair_floor_2/image_0062.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0054",
		"pointer_table_index": 25,
		"file_index": 6390,
		"source_file": "bin/lair_floor_2/image_0054.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0063",
		"pointer_table_index": 25,
		"file_index": 6391,
		"source_file": "bin/lair_floor_2/image_0063.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0058",
		"pointer_table_index": 25,
		"file_index": 6392,
		"source_file": "bin/lair_floor_2/image_0058.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0056",
		"pointer_table_index": 25,
		"file_index": 6393,
		"source_file": "bin/lair_floor_2/image_0056.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0057",
		"pointer_table_index": 25,
		"file_index": 6394,
		"source_file": "bin/lair_floor_2/image_0057.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0055",
		"pointer_table_index": 25,
		"file_index": 6395,
		"source_file": "bin/lair_floor_2/image_0055.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0050",
		"pointer_table_index": 25,
		"file_index": 6396,
		"source_file": "bin/lair_floor_2/image_0050.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0049",
		"pointer_table_index": 25,
		"file_index": 6397,
		"source_file": "bin/lair_floor_2/image_0049.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0051",
		"pointer_table_index": 25,
		"file_index": 6398,
		"source_file": "bin/lair_floor_2/image_0051.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0052",
		"pointer_table_index": 25,
		"file_index": 6399,
		"source_file": "bin/lair_floor_2/image_0052.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0053",
		"pointer_table_index": 25,
		"file_index": 6400,
		"source_file": "bin/lair_floor_2/image_0053.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0059",
		"pointer_table_index": 25,
		"file_index": 6401,
		"source_file": "bin/lair_floor_2/image_0059.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0060",
		"pointer_table_index": 25,
		"file_index": 6402,
		"source_file": "bin/lair_floor_2/image_0060.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0061",
		"pointer_table_index": 25,
		"file_index": 6403,
		"source_file": "bin/lair_floor_2/image_0061.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0009",
		"pointer_table_index": 25,
		"file_index": 6404,
		"source_file": "bin/lair_floor_2/image_0009.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0009_pal",
		"pointer_table_index": 25,
		"file_index": 6405,
		"source_file": "bin/lair_floor_2/image_0009_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0033",
		"pointer_table_index": 25,
		"file_index": 6406,
		"source_file": "bin/lair_floor_2/image_0033.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0033_pal",
		"pointer_table_index": 25,
		"file_index": 6407,
		"source_file": "bin/lair_floor_2/image_0033_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0034",
		"pointer_table_index": 25,
		"file_index": 6408,
		"source_file": "bin/lair_floor_2/image_0034.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0034_pal",
		"pointer_table_index": 25,
		"file_index": 6409,
		"source_file": "bin/lair_floor_2/image_0034_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0032",
		"pointer_table_index": 25,
		"file_index": 6410,
		"source_file": "bin/lair_floor_2/image_0032.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0032_pal",
		"pointer_table_index": 25,
		"file_index": 6411,
		"source_file": "bin/lair_floor_2/image_0032_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0018",
		"pointer_table_index": 25,
		"file_index": 6412,
		"source_file": "bin/lair_floor_2/image_0018.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0018_pal",
		"pointer_table_index": 25,
		"file_index": 6413,
		"source_file": "bin/lair_floor_2/image_0018_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0017",
		"pointer_table_index": 25,
		"file_index": 6414,
		"source_file": "bin/lair_floor_2/image_0017.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0031",
		"pointer_table_index": 25,
		"file_index": 6415,
		"source_file": "bin/lair_floor_2/image_0031.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0031_pal",
		"pointer_table_index": 25,
		"file_index": 6416,
		"source_file": "bin/lair_floor_2/image_0031_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0035",
		"pointer_table_index": 25,
		"file_index": 6417,
		"source_file": "bin/lair_floor_2/image_0035.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0035_pal",
		"pointer_table_index": 25,
		"file_index": 6418,
		"source_file": "bin/lair_floor_2/image_0035_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0036",
		"pointer_table_index": 25,
		"file_index": 6419,
		"source_file": "bin/lair_floor_2/image_0036.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0036_pal",
		"pointer_table_index": 25,
		"file_index": 6420,
		"source_file": "bin/lair_floor_2/image_0036_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0037",
		"pointer_table_index": 25,
		"file_index": 6421,
		"source_file": "bin/lair_floor_2/image_0037.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0037_pal",
		"pointer_table_index": 25,
		"file_index": 6422,
		"source_file": "bin/lair_floor_2/image_0037_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0038",
		"pointer_table_index": 25,
		"file_index": 6423,
		"source_file": "bin/lair_floor_2/image_0038.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0025",
		"pointer_table_index": 25,
		"file_index": 6424,
		"source_file": "bin/lair_floor_2/image_0025.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0025_pal",
		"pointer_table_index": 25,
		"file_index": 6425,
		"source_file": "bin/lair_floor_2/image_0025_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0026",
		"pointer_table_index": 25,
		"file_index": 6426,
		"source_file": "bin/lair_floor_2/image_0026.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0026_pal",
		"pointer_table_index": 25,
		"file_index": 6427,
		"source_file": "bin/lair_floor_2/image_0026_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0027",
		"pointer_table_index": 25,
		"file_index": 6428,
		"source_file": "bin/lair_floor_2/image_0027.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0027_pal",
		"pointer_table_index": 25,
		"file_index": 6429,
		"source_file": "bin/lair_floor_2/image_0027_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0028",
		"pointer_table_index": 25,
		"file_index": 6430,
		"source_file": "bin/lair_floor_2/image_0028.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0028_pal",
		"pointer_table_index": 25,
		"file_index": 6431,
		"source_file": "bin/lair_floor_2/image_0028_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0019",
		"pointer_table_index": 25,
		"file_index": 6432,
		"source_file": "bin/lair_floor_2/image_0019.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0019_pal",
		"pointer_table_index": 25,
		"file_index": 6433,
		"source_file": "bin/lair_floor_2/image_0019_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0006",
		"pointer_table_index": 25,
		"file_index": 6434,
		"source_file": "bin/lair_floor_2/image_0006.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0006_pal",
		"pointer_table_index": 25,
		"file_index": 6435,
		"source_file": "bin/lair_floor_2/image_0006_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0015",
		"pointer_table_index": 25,
		"file_index": 6436,
		"source_file": "bin/lair_floor_2/image_0015.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0015_pal",
		"pointer_table_index": 25,
		"file_index": 6437,
		"source_file": "bin/lair_floor_2/image_0015_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0016",
		"pointer_table_index": 25,
		"file_index": 6438,
		"source_file": "bin/lair_floor_2/image_0016.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0016_pal",
		"pointer_table_index": 25,
		"file_index": 6439,
		"source_file": "bin/lair_floor_2/image_0016_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0022",
		"pointer_table_index": 25,
		"file_index": 6440,
		"source_file": "bin/lair_floor_2/image_0022.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0022_pal",
		"pointer_table_index": 25,
		"file_index": 6441,
		"source_file": "bin/lair_floor_2/image_0022_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0024",
		"pointer_table_index": 25,
		"file_index": 6442,
		"source_file": "bin/lair_floor_2/image_0024.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0024_pal",
		"pointer_table_index": 25,
		"file_index": 6443,
		"source_file": "bin/lair_floor_2/image_0024_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0029",
		"pointer_table_index": 25,
		"file_index": 6444,
		"source_file": "bin/lair_floor_2/image_0029.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0020",
		"pointer_table_index": 25,
		"file_index": 6445,
		"source_file": "bin/lair_floor_2/image_0020.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0020_pal",
		"pointer_table_index": 25,
		"file_index": 6446,
		"source_file": "bin/lair_floor_2/image_0020_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0023",
		"pointer_table_index": 25,
		"file_index": 6447,
		"source_file": "bin/lair_floor_2/image_0023.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0001",
		"pointer_table_index": 25,
		"file_index": 6448,
		"source_file": "bin/lair_floor_2/image_0001.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0001_pal",
		"pointer_table_index": 25,
		"file_index": 6449,
		"source_file": "bin/lair_floor_2/image_0001_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0021",
		"pointer_table_index": 25,
		"file_index": 6450,
		"source_file": "bin/lair_floor_2/image_0021.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0021_pal",
		"pointer_table_index": 25,
		"file_index": 6451,
		"source_file": "bin/lair_floor_2/image_0021_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0007",
		"pointer_table_index": 25,
		"file_index": 6452,
		"source_file": "bin/lair_floor_2/image_0007.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0007_pal",
		"pointer_table_index": 25,
		"file_index": 6453,
		"source_file": "bin/lair_floor_2/image_0007_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0011",
		"pointer_table_index": 25,
		"file_index": 6454,
		"source_file": "bin/lair_floor_2/image_0011.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0011_pal",
		"pointer_table_index": 25,
		"file_index": 6455,
		"source_file": "bin/lair_floor_2/image_0011_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0010",
		"pointer_table_index": 25,
		"file_index": 6456,
		"source_file": "bin/lair_floor_2/image_0010.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0010_pal",
		"pointer_table_index": 25,
		"file_index": 6457,
		"source_file": "bin/lair_floor_2/image_0010_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0008",
		"pointer_table_index": 25,
		"file_index": 6458,
		"source_file": "bin/lair_floor_2/image_0008.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0008_pal",
		"pointer_table_index": 25,
		"file_index": 6459,
		"source_file": "bin/lair_floor_2/image_0008_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0014",
		"pointer_table_index": 25,
		"file_index": 6460,
		"source_file": "bin/lair_floor_2/image_0014.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0014_pal",
		"pointer_table_index": 25,
		"file_index": 6461,
		"source_file": "bin/lair_floor_2/image_0014_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0005",
		"pointer_table_index": 25,
		"file_index": 6462,
		"source_file": "bin/lair_floor_2/image_0005.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0005_pal",
		"pointer_table_index": 25,
		"file_index": 6463,
		"source_file": "bin/lair_floor_2/image_0005_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0012",
		"pointer_table_index": 25,
		"file_index": 6464,
		"source_file": "bin/lair_floor_2/image_0012.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0012_pal",
		"pointer_table_index": 25,
		"file_index": 6465,
		"source_file": "bin/lair_floor_2/image_0012_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0013",
		"pointer_table_index": 25,
		"file_index": 6466,
		"source_file": "bin/lair_floor_2/image_0013.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0013_pal",
		"pointer_table_index": 25,
		"file_index": 6467,
		"source_file": "bin/lair_floor_2/image_0013_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0003",
		"pointer_table_index": 25,
		"file_index": 6468,
		"source_file": "bin/lair_floor_2/image_0003.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0003_pal",
		"pointer_table_index": 25,
		"file_index": 6469,
		"source_file": "bin/lair_floor_2/image_0003_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0002",
		"pointer_table_index": 25,
		"file_index": 6470,
		"source_file": "bin/lair_floor_2/image_0002.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0002_pal",
		"pointer_table_index": 25,
		"file_index": 6471,
		"source_file": "bin/lair_floor_2/image_0002_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0004",
		"pointer_table_index": 25,
		"file_index": 6472,
		"source_file": "bin/lair_floor_2/image_0004.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0004_pal",
		"pointer_table_index": 25,
		"file_index": 6473,
		"source_file": "bin/lair_floor_2/image_0004_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0000",
		"pointer_table_index": 25,
		"file_index": 6474,
		"source_file": "bin/lair_floor_3/image_0000.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0000_pal",
		"pointer_table_index": 25,
		"file_index": 6475,
		"source_file": "bin/lair_floor_3/image_0000_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0023",
		"pointer_table_index": 25,
		"file_index": 6476,
		"source_file": "bin/lair_floor_3/image_0023.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0023_pal",
		"pointer_table_index": 25,
		"file_index": 6477,
		"source_file": "bin/lair_floor_3/image_0023_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0009",
		"pointer_table_index": 25,
		"file_index": 6478,
		"source_file": "bin/lair_floor_3/image_0009.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0009_pal",
		"pointer_table_index": 25,
		"file_index": 6479,
		"source_file": "bin/lair_floor_3/image_0009_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0002",
		"pointer_table_index": 25,
		"file_index": 6480,
		"source_file": "bin/lair_floor_3/image_0002.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0002_pal",
		"pointer_table_index": 25,
		"file_index": 6481,
		"source_file": "bin/lair_floor_3/image_0002_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0052",
		"pointer_table_index": 25,
		"file_index": 6482,
		"source_file": "bin/lair_floor_3/image_0052.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0052_pal",
		"pointer_table_index": 25,
		"file_index": 6483,
		"source_file": "bin/lair_floor_3/image_0052_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0019",
		"pointer_table_index": 25,
		"file_index": 6484,
		"source_file": "bin/lair_floor_3/image_0019.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0019_pal",
		"pointer_table_index": 25,
		"file_index": 6485,
		"source_file": "bin/lair_floor_3/image_0019_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0008",
		"pointer_table_index": 25,
		"file_index": 6486,
		"source_file": "bin/lair_floor_3/image_0008.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0008_pal",
		"pointer_table_index": 25,
		"file_index": 6487,
		"source_file": "bin/lair_floor_3/image_0008_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0035",
		"pointer_table_index": 25,
		"file_index": 6488,
		"source_file": "bin/lair_floor_3/image_0035.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0017",
		"pointer_table_index": 25,
		"file_index": 6489,
		"source_file": "bin/lair_floor_3/image_0017.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0017_pal",
		"pointer_table_index": 25,
		"file_index": 6490,
		"source_file": "bin/lair_floor_3/image_0017_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0033",
		"pointer_table_index": 25,
		"file_index": 6491,
		"source_file": "bin/lair_floor_3/image_0033.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0033_pal",
		"pointer_table_index": 25,
		"file_index": 6492,
		"source_file": "bin/lair_floor_3/image_0033_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0024",
		"pointer_table_index": 25,
		"file_index": 6493,
		"source_file": "bin/lair_floor_3/image_0024.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0024_pal",
		"pointer_table_index": 25,
		"file_index": 6494,
		"source_file": "bin/lair_floor_3/image_0024_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0020",
		"pointer_table_index": 25,
		"file_index": 6495,
		"source_file": "bin/lair_floor_3/image_0020.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0020_pal",
		"pointer_table_index": 25,
		"file_index": 6496,
		"source_file": "bin/lair_floor_3/image_0020_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0021",
		"pointer_table_index": 25,
		"file_index": 6497,
		"source_file": "bin/lair_floor_3/image_0021.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0021_pal",
		"pointer_table_index": 25,
		"file_index": 6498,
		"source_file": "bin/lair_floor_3/image_0021_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0032",
		"pointer_table_index": 25,
		"file_index": 6499,
		"source_file": "bin/lair_floor_3/image_0032.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0032_pal",
		"pointer_table_index": 25,
		"file_index": 6500,
		"source_file": "bin/lair_floor_3/image_0032_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0006",
		"pointer_table_index": 25,
		"file_index": 6501,
		"source_file": "bin/lair_floor_3/image_0006.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0006_pal",
		"pointer_table_index": 25,
		"file_index": 6502,
		"source_file": "bin/lair_floor_3/image_0006_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0034",
		"pointer_table_index": 25,
		"file_index": 6503,
		"source_file": "bin/lair_floor_3/image_0034.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0034_pal",
		"pointer_table_index": 25,
		"file_index": 6504,
		"source_file": "bin/lair_floor_3/image_0034_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0027",
		"pointer_table_index": 25,
		"file_index": 6505,
		"source_file": "bin/lair_floor_3/image_0027.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0027_pal",
		"pointer_table_index": 25,
		"file_index": 6506,
		"source_file": "bin/lair_floor_3/image_0027_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0031",
		"pointer_table_index": 25,
		"file_index": 6507,
		"source_file": "bin/lair_floor_3/image_0031.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0031_pal",
		"pointer_table_index": 25,
		"file_index": 6508,
		"source_file": "bin/lair_floor_3/image_0031_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0029",
		"pointer_table_index": 25,
		"file_index": 6509,
		"source_file": "bin/lair_floor_3/image_0029.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0029_pal",
		"pointer_table_index": 25,
		"file_index": 6510,
		"source_file": "bin/lair_floor_3/image_0029_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0030",
		"pointer_table_index": 25,
		"file_index": 6511,
		"source_file": "bin/lair_floor_3/image_0030.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0030_pal",
		"pointer_table_index": 25,
		"file_index": 6512,
		"source_file": "bin/lair_floor_3/image_0030_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0028",
		"pointer_table_index": 25,
		"file_index": 6513,
		"source_file": "bin/lair_floor_3/image_0028.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0028_pal",
		"pointer_table_index": 25,
		"file_index": 6514,
		"source_file": "bin/lair_floor_3/image_0028_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0045",
		"pointer_table_index": 25,
		"file_index": 6515,
		"source_file": "bin/lair_floor_3/image_0045.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0045_pal",
		"pointer_table_index": 25,
		"file_index": 6516,
		"source_file": "bin/lair_floor_3/image_0045_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0046",
		"pointer_table_index": 25,
		"file_index": 6517,
		"source_file": "bin/lair_floor_3/image_0046.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0046_pal",
		"pointer_table_index": 25,
		"file_index": 6518,
		"source_file": "bin/lair_floor_3/image_0046_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0012",
		"pointer_table_index": 25,
		"file_index": 6519,
		"source_file": "bin/lair_floor_3/image_0012.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0012_pal",
		"pointer_table_index": 25,
		"file_index": 6520,
		"source_file": "bin/lair_floor_3/image_0012_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0014",
		"pointer_table_index": 25,
		"file_index": 6521,
		"source_file": "bin/lair_floor_3/image_0014.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0014_pal",
		"pointer_table_index": 25,
		"file_index": 6522,
		"source_file": "bin/lair_floor_3/image_0014_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0011",
		"pointer_table_index": 25,
		"file_index": 6523,
		"source_file": "bin/lair_floor_3/image_0011.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0011_pal",
		"pointer_table_index": 25,
		"file_index": 6524,
		"source_file": "bin/lair_floor_3/image_0011_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0016",
		"pointer_table_index": 25,
		"file_index": 6525,
		"source_file": "bin/lair_floor_3/image_0016.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0013",
		"pointer_table_index": 25,
		"file_index": 6526,
		"source_file": "bin/lair_floor_3/image_0013.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0018",
		"pointer_table_index": 25,
		"file_index": 6527,
		"source_file": "bin/lair_floor_3/image_0018.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0018_pal",
		"pointer_table_index": 25,
		"file_index": 6528,
		"source_file": "bin/lair_floor_3/image_0018_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0047",
		"pointer_table_index": 25,
		"file_index": 6529,
		"source_file": "bin/lair_floor_3/image_0047.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0047_pal",
		"pointer_table_index": 25,
		"file_index": 6530,
		"source_file": "bin/lair_floor_3/image_0047_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0037",
		"pointer_table_index": 25,
		"file_index": 6531,
		"source_file": "bin/lair_floor_3/image_0037.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0037_pal",
		"pointer_table_index": 25,
		"file_index": 6532,
		"source_file": "bin/lair_floor_3/image_0037_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0036",
		"pointer_table_index": 25,
		"file_index": 6533,
		"source_file": "bin/lair_floor_3/image_0036.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0036_pal",
		"pointer_table_index": 25,
		"file_index": 6534,
		"source_file": "bin/lair_floor_3/image_0036_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0004",
		"pointer_table_index": 25,
		"file_index": 6535,
		"source_file": "bin/lair_floor_3/image_0004.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0004_pal",
		"pointer_table_index": 25,
		"file_index": 6536,
		"source_file": "bin/lair_floor_3/image_0004_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0026",
		"pointer_table_index": 25,
		"file_index": 6537,
		"source_file": "bin/lair_floor_3/image_0026.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0007",
		"pointer_table_index": 25,
		"file_index": 6538,
		"source_file": "bin/lair_floor_3/image_0007.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0007_pal",
		"pointer_table_index": 25,
		"file_index": 6539,
		"source_file": "bin/lair_floor_3/image_0007_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0022",
		"pointer_table_index": 25,
		"file_index": 6540,
		"source_file": "bin/lair_floor_3/image_0022.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0022_pal",
		"pointer_table_index": 25,
		"file_index": 6541,
		"source_file": "bin/lair_floor_3/image_0022_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0025",
		"pointer_table_index": 25,
		"file_index": 6542,
		"source_file": "bin/lair_floor_3/image_0025.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0025_pal",
		"pointer_table_index": 25,
		"file_index": 6543,
		"source_file": "bin/lair_floor_3/image_0025_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0038",
		"pointer_table_index": 25,
		"file_index": 6544,
		"source_file": "bin/lair_floor_3/image_0038.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0038_pal",
		"pointer_table_index": 25,
		"file_index": 6545,
		"source_file": "bin/lair_floor_3/image_0038_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0005",
		"pointer_table_index": 25,
		"file_index": 6546,
		"source_file": "bin/lair_floor_3/image_0005.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0005_pal",
		"pointer_table_index": 25,
		"file_index": 6547,
		"source_file": "bin/lair_floor_3/image_0005_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0042",
		"pointer_table_index": 25,
		"file_index": 6548,
		"source_file": "bin/lair_floor_3/image_0042.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0042_pal",
		"pointer_table_index": 25,
		"file_index": 6549,
		"source_file": "bin/lair_floor_3/image_0042_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0040",
		"pointer_table_index": 25,
		"file_index": 6550,
		"source_file": "bin/lair_floor_3/image_0040.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0040_pal",
		"pointer_table_index": 25,
		"file_index": 6551,
		"source_file": "bin/lair_floor_3/image_0040_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0041",
		"pointer_table_index": 25,
		"file_index": 6552,
		"source_file": "bin/lair_floor_3/image_0041.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0041_pal",
		"pointer_table_index": 25,
		"file_index": 6553,
		"source_file": "bin/lair_floor_3/image_0041_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0003",
		"pointer_table_index": 25,
		"file_index": 6554,
		"source_file": "bin/lair_floor_3/image_0003.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0003_pal",
		"pointer_table_index": 25,
		"file_index": 6555,
		"source_file": "bin/lair_floor_3/image_0003_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0039",
		"pointer_table_index": 25,
		"file_index": 6556,
		"source_file": "bin/lair_floor_3/image_0039.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0043",
		"pointer_table_index": 25,
		"file_index": 6557,
		"source_file": "bin/lair_floor_3/image_0043.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0048",
		"pointer_table_index": 25,
		"file_index": 6558,
		"source_file": "bin/lair_floor_3/image_0048.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0048_pal",
		"pointer_table_index": 25,
		"file_index": 6559,
		"source_file": "bin/lair_floor_3/image_0048_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0044",
		"pointer_table_index": 25,
		"file_index": 6560,
		"source_file": "bin/lair_floor_3/image_0044.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0015",
		"pointer_table_index": 25,
		"file_index": 6561,
		"source_file": "bin/lair_floor_3/image_0015.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0010",
		"pointer_table_index": 25,
		"file_index": 6562,
		"source_file": "bin/lair_floor_3/image_0010.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0001",
		"pointer_table_index": 25,
		"file_index": 6563,
		"source_file": "bin/lair_floor_3/image_0001.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0050",
		"pointer_table_index": 25,
		"file_index": 6564,
		"source_file": "bin/lair_floor_3/image_0050.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0051",
		"pointer_table_index": 25,
		"file_index": 6565,
		"source_file": "bin/lair_floor_3/image_0051.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0049",
		"pointer_table_index": 25,
		"file_index": 6566,
		"source_file": "bin/lair_floor_3/image_0049.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0053",
		"pointer_table_index": 25,
		"file_index": 6567,
		"source_file": "bin/lair_floor_3/image_0053.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0054",
		"pointer_table_index": 25,
		"file_index": 6568,
		"source_file": "bin/lair_floor_3/image_0054.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0055",
		"pointer_table_index": 25,
		"file_index": 6569,
		"source_file": "bin/lair_floor_3/image_0055.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0056",
		"pointer_table_index": 25,
		"file_index": 6570,
		"source_file": "bin/lair_floor_3/image_0056.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0057",
		"pointer_table_index": 25,
		"file_index": 6571,
		"source_file": "bin/lair_floor_3/image_0057.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0063",
		"pointer_table_index": 25,
		"file_index": 6572,
		"source_file": "bin/lair_floor_3/image_0063.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0064",
		"pointer_table_index": 25,
		"file_index": 6573,
		"source_file": "bin/lair_floor_3/image_0064.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0065",
		"pointer_table_index": 25,
		"file_index": 6574,
		"source_file": "bin/lair_floor_3/image_0065.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0062",
		"pointer_table_index": 25,
		"file_index": 6575,
		"source_file": "bin/lair_floor_3/image_0062.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0061",
		"pointer_table_index": 25,
		"file_index": 6576,
		"source_file": "bin/lair_floor_3/image_0061.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0058",
		"pointer_table_index": 25,
		"file_index": 6577,
		"source_file": "bin/lair_floor_3/image_0058.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0059",
		"pointer_table_index": 25,
		"file_index": 6578,
		"source_file": "bin/lair_floor_3/image_0059.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0060",
		"pointer_table_index": 25,
		"file_index": 6579,
		"source_file": "bin/lair_floor_3/image_0060.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0005",
		"pointer_table_index": 25,
		"file_index": 6580,
		"source_file": "bin/tickers_tower/image_0005.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0005_pal",
		"pointer_table_index": 25,
		"file_index": 6581,
		"source_file": "bin/tickers_tower/image_0005_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0003",
		"pointer_table_index": 25,
		"file_index": 6582,
		"source_file": "bin/tickers_tower/image_0003.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0003_pal",
		"pointer_table_index": 25,
		"file_index": 6583,
		"source_file": "bin/tickers_tower/image_0003_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0004",
		"pointer_table_index": 25,
		"file_index": 6584,
		"source_file": "bin/tickers_tower/image_0004.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0004_pal",
		"pointer_table_index": 25,
		"file_index": 6585,
		"source_file": "bin/tickers_tower/image_0004_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0001",
		"pointer_table_index": 25,
		"file_index": 6586,
		"source_file": "bin/tickers_tower/image_0001.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0001_pal",
		"pointer_table_index": 25,
		"file_index": 6587,
		"source_file": "bin/tickers_tower/image_0001_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0000",
		"pointer_table_index": 25,
		"file_index": 6588,
		"source_file": "bin/tickers_tower/image_0000.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0000_pal",
		"pointer_table_index": 25,
		"file_index": 6589,
		"source_file": "bin/tickers_tower/image_0000_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0002",
		"pointer_table_index": 25,
		"file_index": 6590,
		"source_file": "bin/tickers_tower/image_0002.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0002_pal",
		"pointer_table_index": 25,
		"file_index": 6591,
		"source_file": "bin/tickers_tower/image_0002_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0001",
		"pointer_table_index": 25,
		"file_index": 6592,
		"source_file": "bin/mumbos_skull/image_0001.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0001_pal",
		"pointer_table_index": 25,
		"file_index": 6593,
		"source_file": "bin/mumbos_skull/image_0001_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0002",
		"pointer_table_index": 25,
		"file_index": 6594,
		"source_file": "bin/mumbos_skull/image_0002.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0004",
		"pointer_table_index": 25,
		"file_index": 6595,
		"source_file": "bin/mumbos_skull/image_0004.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0004_pal",
		"pointer_table_index": 25,
		"file_index": 6596,
		"source_file": "bin/mumbos_skull/image_0004_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0008",
		"pointer_table_index": 25,
		"file_index": 6597,
		"source_file": "bin/mumbos_skull/image_0008.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0008_pal",
		"pointer_table_index": 25,
		"file_index": 6598,
		"source_file": "bin/mumbos_skull/image_0008_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0024",
		"pointer_table_index": 25,
		"file_index": 6599,
		"source_file": "bin/mumbos_skull/image_0024.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0024_pal",
		"pointer_table_index": 25,
		"file_index": 6600,
		"source_file": "bin/mumbos_skull/image_0024_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0007",
		"pointer_table_index": 25,
		"file_index": 6601,
		"source_file": "bin/mumbos_skull/image_0007.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0005",
		"pointer_table_index": 25,
		"file_index": 6602,
		"source_file": "bin/mumbos_skull/image_0005.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0006",
		"pointer_table_index": 25,
		"file_index": 6603,
		"source_file": "bin/mumbos_skull/image_0006.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0000",
		"pointer_table_index": 25,
		"file_index": 6604,
		"source_file": "bin/mumbos_skull/image_0000.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0000_pal",
		"pointer_table_index": 25,
		"file_index": 6605,
		"source_file": "bin/mumbos_skull/image_0000_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0010",
		"pointer_table_index": 25,
		"file_index": 6606,
		"source_file": "bin/mumbos_skull/image_0010.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0010_pal",
		"pointer_table_index": 25,
		"file_index": 6607,
		"source_file": "bin/mumbos_skull/image_0010_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0003",
		"pointer_table_index": 25,
		"file_index": 6608,
		"source_file": "bin/mumbos_skull/image_0003.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0012",
		"pointer_table_index": 25,
		"file_index": 6609,
		"source_file": "bin/mumbos_skull/image_0012.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0012_pal",
		"pointer_table_index": 25,
		"file_index": 6610,
		"source_file": "bin/mumbos_skull/image_0012_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0014",
		"pointer_table_index": 25,
		"file_index": 6611,
		"source_file": "bin/mumbos_skull/image_0014.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0014_pal",
		"pointer_table_index": 25,
		"file_index": 6612,
		"source_file": "bin/mumbos_skull/image_0014_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0013",
		"pointer_table_index": 25,
		"file_index": 6613,
		"source_file": "bin/mumbos_skull/image_0013.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0013_pal",
		"pointer_table_index": 25,
		"file_index": 6614,
		"source_file": "bin/mumbos_skull/image_0013_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0011",
		"pointer_table_index": 25,
		"file_index": 6615,
		"source_file": "bin/mumbos_skull/image_0011.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0011_pal",
		"pointer_table_index": 25,
		"file_index": 6616,
		"source_file": "bin/mumbos_skull/image_0011_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0020",
		"pointer_table_index": 25,
		"file_index": 6617,
		"source_file": "bin/lair_ttc_entrance/image_0020.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0020_pal",
		"pointer_table_index": 25,
		"file_index": 6618,
		"source_file": "bin/lair_ttc_entrance/image_0020_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0009",
		"pointer_table_index": 25,
		"file_index": 6619,
		"source_file": "bin/lair_ttc_entrance/image_0009.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0009_pal",
		"pointer_table_index": 25,
		"file_index": 6620,
		"source_file": "bin/lair_ttc_entrance/image_0009_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0004",
		"pointer_table_index": 25,
		"file_index": 6621,
		"source_file": "bin/lair_ttc_entrance/image_0004.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0004_pal",
		"pointer_table_index": 25,
		"file_index": 6622,
		"source_file": "bin/lair_ttc_entrance/image_0004_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0007",
		"pointer_table_index": 25,
		"file_index": 6623,
		"source_file": "bin/lair_ttc_entrance/image_0007.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0007_pal",
		"pointer_table_index": 25,
		"file_index": 6624,
		"source_file": "bin/lair_ttc_entrance/image_0007_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0008",
		"pointer_table_index": 25,
		"file_index": 6625,
		"source_file": "bin/lair_ttc_entrance/image_0008.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0006",
		"pointer_table_index": 25,
		"file_index": 6626,
		"source_file": "bin/lair_ttc_entrance/image_0006.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0006_pal",
		"pointer_table_index": 25,
		"file_index": 6627,
		"source_file": "bin/lair_ttc_entrance/image_0006_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0005",
		"pointer_table_index": 25,
		"file_index": 6628,
		"source_file": "bin/lair_ttc_entrance/image_0005.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0005_pal",
		"pointer_table_index": 25,
		"file_index": 6629,
		"source_file": "bin/lair_ttc_entrance/image_0005_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0003",
		"pointer_table_index": 25,
		"file_index": 6630,
		"source_file": "bin/lair_ttc_entrance/image_0003.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0003_pal",
		"pointer_table_index": 25,
		"file_index": 6631,
		"source_file": "bin/lair_ttc_entrance/image_0003_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0002",
		"pointer_table_index": 25,
		"file_index": 6632,
		"source_file": "bin/lair_ttc_entrance/image_0002.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0002_pal",
		"pointer_table_index": 25,
		"file_index": 6633,
		"source_file": "bin/lair_ttc_entrance/image_0002_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0000",
		"pointer_table_index": 25,
		"file_index": 6634,
		"source_file": "bin/lair_ttc_entrance/image_0000.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0000_pal",
		"pointer_table_index": 25,
		"file_index": 6635,
		"source_file": "bin/lair_ttc_entrance/image_0000_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0010",
		"pointer_table_index": 25,
		"file_index": 6636,
		"source_file": "bin/lair_ttc_entrance/image_0010.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0010_pal",
		"pointer_table_index": 25,
		"file_index": 6637,
		"source_file": "bin/lair_ttc_entrance/image_0010_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0015",
		"pointer_table_index": 25,
		"file_index": 6638,
		"source_file": "bin/lair_ttc_entrance/image_0015.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0011",
		"pointer_table_index": 25,
		"file_index": 6639,
		"source_file": "bin/lair_ttc_entrance/image_0011.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0011_pal",
		"pointer_table_index": 25,
		"file_index": 6640,
		"source_file": "bin/lair_ttc_entrance/image_0011_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0012",
		"pointer_table_index": 25,
		"file_index": 6641,
		"source_file": "bin/lair_ttc_entrance/image_0012.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0012_pal",
		"pointer_table_index": 25,
		"file_index": 6642,
		"source_file": "bin/lair_ttc_entrance/image_0012_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0001",
		"pointer_table_index": 25,
		"file_index": 6643,
		"source_file": "bin/lair_ttc_entrance/image_0001.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0001_pal",
		"pointer_table_index": 25,
		"file_index": 6644,
		"source_file": "bin/lair_ttc_entrance/image_0001_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0014",
		"pointer_table_index": 25,
		"file_index": 6645,
		"source_file": "bin/lair_ttc_entrance/image_0014.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0014_pal",
		"pointer_table_index": 25,
		"file_index": 6646,
		"source_file": "bin/lair_ttc_entrance/image_0014_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0013",
		"pointer_table_index": 25,
		"file_index": 6647,
		"source_file": "bin/lair_ttc_entrance/image_0013.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0013_pal",
		"pointer_table_index": 25,
		"file_index": 6648,
		"source_file": "bin/lair_ttc_entrance/image_0013_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0016",
		"pointer_table_index": 25,
		"file_index": 6649,
		"source_file": "bin/lair_ttc_entrance/image_0016.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0016_pal",
		"pointer_table_index": 25,
		"file_index": 6650,
		"source_file": "bin/lair_ttc_entrance/image_0016_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0018",
		"pointer_table_index": 25,
		"file_index": 6651,
		"source_file": "bin/lair_ttc_entrance/image_0018.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0018_pal",
		"pointer_table_index": 25,
		"file_index": 6652,
		"source_file": "bin/lair_ttc_entrance/image_0018_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0017",
		"pointer_table_index": 25,
		"file_index": 6653,
		"source_file": "bin/lair_ttc_entrance/image_0017.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0017_pal",
		"pointer_table_index": 25,
		"file_index": 6654,
		"source_file": "bin/lair_ttc_entrance/image_0017_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0019",
		"pointer_table_index": 25,
		"file_index": 6655,
		"source_file": "bin/lair_ttc_entrance/image_0019.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0019_pal",
		"pointer_table_index": 25,
		"file_index": 6656,
		"source_file": "bin/lair_ttc_entrance/image_0019_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0021",
		"pointer_table_index": 25,
		"file_index": 6657,
		"source_file": "bin/lair_ttc_entrance/image_0021.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0021_pal",
		"pointer_table_index": 25,
		"file_index": 6658,
		"source_file": "bin/lair_ttc_entrance/image_0021_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0024",
		"pointer_table_index": 25,
		"file_index": 6659,
		"source_file": "bin/lair_ttc_entrance/image_0024.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0024_pal",
		"pointer_table_index": 25,
		"file_index": 6660,
		"source_file": "bin/lair_ttc_entrance/image_0024_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0023",
		"pointer_table_index": 25,
		"file_index": 6661,
		"source_file": "bin/lair_ttc_entrance/image_0023.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0023_pal",
		"pointer_table_index": 25,
		"file_index": 6662,
		"source_file": "bin/lair_ttc_entrance/image_0023_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0022",
		"pointer_table_index": 25,
		"file_index": 6663,
		"source_file": "bin/lair_ttc_entrance/image_0022.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0022_pal",
		"pointer_table_index": 25,
		"file_index": 6664,
		"source_file": "bin/lair_ttc_entrance/image_0022_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0025",
		"pointer_table_index": 25,
		"file_index": 6665,
		"source_file": "bin/lair_ttc_entrance/image_0025.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0026",
		"pointer_table_index": 25,
		"file_index": 6666,
		"source_file": "bin/lair_ttc_entrance/image_0026.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0026_pal",
		"pointer_table_index": 25,
		"file_index": 6667,
		"source_file": "bin/lair_ttc_entrance/image_0026_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0001",
		"pointer_table_index": 25,
		"file_index": 6668,
		"source_file": "bin/ttc/image_0001.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0001_pal",
		"pointer_table_index": 25,
		"file_index": 6669,
		"source_file": "bin/ttc/image_0001_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0010",
		"pointer_table_index": 25,
		"file_index": 6670,
		"source_file": "bin/ttc/image_0010.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0010_pal",
		"pointer_table_index": 25,
		"file_index": 6671,
		"source_file": "bin/ttc/image_0010_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0009",
		"pointer_table_index": 25,
		"file_index": 6672,
		"source_file": "bin/ttc/image_0009.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0009_pal",
		"pointer_table_index": 25,
		"file_index": 6673,
		"source_file": "bin/ttc/image_0009_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0004",
		"pointer_table_index": 25,
		"file_index": 6674,
		"source_file": "bin/ttc/image_0004.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0004_pal",
		"pointer_table_index": 25,
		"file_index": 6675,
		"source_file": "bin/ttc/image_0004_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0007",
		"pointer_table_index": 25,
		"file_index": 6676,
		"source_file": "bin/ttc/image_0007.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0007_pal",
		"pointer_table_index": 25,
		"file_index": 6677,
		"source_file": "bin/ttc/image_0007_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0006",
		"pointer_table_index": 25,
		"file_index": 6678,
		"source_file": "bin/ttc/image_0006.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0006_pal",
		"pointer_table_index": 25,
		"file_index": 6679,
		"source_file": "bin/ttc/image_0006_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0003",
		"pointer_table_index": 25,
		"file_index": 6680,
		"source_file": "bin/ttc/image_0003.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0003_pal",
		"pointer_table_index": 25,
		"file_index": 6681,
		"source_file": "bin/ttc/image_0003_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0005",
		"pointer_table_index": 25,
		"file_index": 6682,
		"source_file": "bin/ttc/image_0005.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0005_pal",
		"pointer_table_index": 25,
		"file_index": 6683,
		"source_file": "bin/ttc/image_0005_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0018",
		"pointer_table_index": 25,
		"file_index": 6684,
		"source_file": "bin/ttc/image_0018.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0018_pal",
		"pointer_table_index": 25,
		"file_index": 6685,
		"source_file": "bin/ttc/image_0018_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0019",
		"pointer_table_index": 25,
		"file_index": 6686,
		"source_file": "bin/ttc/image_0019.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0019_pal",
		"pointer_table_index": 25,
		"file_index": 6687,
		"source_file": "bin/ttc/image_0019_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0017",
		"pointer_table_index": 25,
		"file_index": 6688,
		"source_file": "bin/ttc/image_0017.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0017_pal",
		"pointer_table_index": 25,
		"file_index": 6689,
		"source_file": "bin/ttc/image_0017_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0016",
		"pointer_table_index": 25,
		"file_index": 6690,
		"source_file": "bin/ttc/image_0016.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0016_pal",
		"pointer_table_index": 25,
		"file_index": 6691,
		"source_file": "bin/ttc/image_0016_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0015",
		"pointer_table_index": 25,
		"file_index": 6692,
		"source_file": "bin/ttc/image_0015.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0015_pal",
		"pointer_table_index": 25,
		"file_index": 6693,
		"source_file": "bin/ttc/image_0015_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0012",
		"pointer_table_index": 25,
		"file_index": 6694,
		"source_file": "bin/ttc/image_0012.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0012_pal",
		"pointer_table_index": 25,
		"file_index": 6695,
		"source_file": "bin/ttc/image_0012_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0014",
		"pointer_table_index": 25,
		"file_index": 6696,
		"source_file": "bin/ttc/image_0014.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0014_pal",
		"pointer_table_index": 25,
		"file_index": 6697,
		"source_file": "bin/ttc/image_0014_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0000",
		"pointer_table_index": 25,
		"file_index": 6698,
		"source_file": "bin/ttc/image_0000.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0000_pal",
		"pointer_table_index": 25,
		"file_index": 6699,
		"source_file": "bin/ttc/image_0000_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0013",
		"pointer_table_index": 25,
		"file_index": 6700,
		"source_file": "bin/ttc/image_0013.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0013_pal",
		"pointer_table_index": 25,
		"file_index": 6701,
		"source_file": "bin/ttc/image_0013_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0026",
		"pointer_table_index": 25,
		"file_index": 6702,
		"source_file": "bin/ttc/image_0026.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0026_pal",
		"pointer_table_index": 25,
		"file_index": 6703,
		"source_file": "bin/ttc/image_0026_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0002",
		"pointer_table_index": 25,
		"file_index": 6704,
		"source_file": "bin/ttc/image_0002.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0002_pal",
		"pointer_table_index": 25,
		"file_index": 6705,
		"source_file": "bin/ttc/image_0002_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0011",
		"pointer_table_index": 25,
		"file_index": 6706,
		"source_file": "bin/ttc/image_0011.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0011_pal",
		"pointer_table_index": 25,
		"file_index": 6707,
		"source_file": "bin/ttc/image_0011_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0024",
		"pointer_table_index": 25,
		"file_index": 6708,
		"source_file": "bin/ttc/image_0024.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0024_pal",
		"pointer_table_index": 25,
		"file_index": 6709,
		"source_file": "bin/ttc/image_0024_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0020",
		"pointer_table_index": 25,
		"file_index": 6710,
		"source_file": "bin/ttc/image_0020.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0020_pal",
		"pointer_table_index": 25,
		"file_index": 6711,
		"source_file": "bin/ttc/image_0020_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0008",
		"pointer_table_index": 25,
		"file_index": 6712,
		"source_file": "bin/ttc/image_0008.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0008_pal",
		"pointer_table_index": 25,
		"file_index": 6713,
		"source_file": "bin/ttc/image_0008_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0021",
		"pointer_table_index": 25,
		"file_index": 6714,
		"source_file": "bin/ttc/image_0021.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0021_pal",
		"pointer_table_index": 25,
		"file_index": 6715,
		"source_file": "bin/ttc/image_0021_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0023",
		"pointer_table_index": 25,
		"file_index": 6716,
		"source_file": "bin/ttc/image_0023.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0023_pal",
		"pointer_table_index": 25,
		"file_index": 6717,
		"source_file": "bin/ttc/image_0023_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0028",
		"pointer_table_index": 25,
		"file_index": 6718,
		"source_file": "bin/ttc/image_0028.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0028_pal",
		"pointer_table_index": 25,
		"file_index": 6719,
		"source_file": "bin/ttc/image_0028_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0039",
		"pointer_table_index": 25,
		"file_index": 6720,
		"source_file": "bin/ttc/image_0039.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0039_pal",
		"pointer_table_index": 25,
		"file_index": 6721,
		"source_file": "bin/ttc/image_0039_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0035",
		"pointer_table_index": 25,
		"file_index": 6722,
		"source_file": "bin/ttc/image_0035.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0035_pal",
		"pointer_table_index": 25,
		"file_index": 6723,
		"source_file": "bin/ttc/image_0035_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0034",
		"pointer_table_index": 25,
		"file_index": 6724,
		"source_file": "bin/ttc/image_0034.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0034_pal",
		"pointer_table_index": 25,
		"file_index": 6725,
		"source_file": "bin/ttc/image_0034_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0038",
		"pointer_table_index": 25,
		"file_index": 6726,
		"source_file": "bin/ttc/image_0038.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0038_pal",
		"pointer_table_index": 25,
		"file_index": 6727,
		"source_file": "bin/ttc/image_0038_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0027",
		"pointer_table_index": 25,
		"file_index": 6728,
		"source_file": "bin/ttc/image_0027.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0027_pal",
		"pointer_table_index": 25,
		"file_index": 6729,
		"source_file": "bin/ttc/image_0027_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0033",
		"pointer_table_index": 25,
		"file_index": 6730,
		"source_file": "bin/ttc/image_0033.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0033_pal",
		"pointer_table_index": 25,
		"file_index": 6731,
		"source_file": "bin/ttc/image_0033_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0029",
		"pointer_table_index": 25,
		"file_index": 6732,
		"source_file": "bin/ttc/image_0029.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0029_pal",
		"pointer_table_index": 25,
		"file_index": 6733,
		"source_file": "bin/ttc/image_0029_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0032",
		"pointer_table_index": 25,
		"file_index": 6734,
		"source_file": "bin/ttc/image_0032.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0032_pal",
		"pointer_table_index": 25,
		"file_index": 6735,
		"source_file": "bin/ttc/image_0032_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0036",
		"pointer_table_index": 25,
		"file_index": 6736,
		"source_file": "bin/ttc/image_0036.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0025",
		"pointer_table_index": 25,
		"file_index": 6737,
		"source_file": "bin/ttc/image_0025.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0025_pal",
		"pointer_table_index": 25,
		"file_index": 6738,
		"source_file": "bin/ttc/image_0025_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0022",
		"pointer_table_index": 25,
		"file_index": 6739,
		"source_file": "bin/ttc/image_0022.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0022_pal",
		"pointer_table_index": 25,
		"file_index": 6740,
		"source_file": "bin/ttc/image_0022_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0031",
		"pointer_table_index": 25,
		"file_index": 6741,
		"source_file": "bin/ttc/image_0031.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0031_pal",
		"pointer_table_index": 25,
		"file_index": 6742,
		"source_file": "bin/ttc/image_0031_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0044",
		"pointer_table_index": 25,
		"file_index": 6743,
		"source_file": "bin/ttc/image_0044.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0045",
		"pointer_table_index": 25,
		"file_index": 6744,
		"source_file": "bin/ttc/image_0045.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0045_pal",
		"pointer_table_index": 25,
		"file_index": 6745,
		"source_file": "bin/ttc/image_0045_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0046",
		"pointer_table_index": 25,
		"file_index": 6746,
		"source_file": "bin/ttc/image_0046.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0046_pal",
		"pointer_table_index": 25,
		"file_index": 6747,
		"source_file": "bin/ttc/image_0046_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0043",
		"pointer_table_index": 25,
		"file_index": 6748,
		"source_file": "bin/ttc/image_0043.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0043_pal",
		"pointer_table_index": 25,
		"file_index": 6749,
		"source_file": "bin/ttc/image_0043_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0041",
		"pointer_table_index": 25,
		"file_index": 6750,
		"source_file": "bin/ttc/image_0041.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0041_pal",
		"pointer_table_index": 25,
		"file_index": 6751,
		"source_file": "bin/ttc/image_0041_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0042",
		"pointer_table_index": 25,
		"file_index": 6752,
		"source_file": "bin/ttc/image_0042.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0042_pal",
		"pointer_table_index": 25,
		"file_index": 6753,
		"source_file": "bin/ttc/image_0042_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0040",
		"pointer_table_index": 25,
		"file_index": 6754,
		"source_file": "bin/ttc/image_0040.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0040_pal",
		"pointer_table_index": 25,
		"file_index": 6755,
		"source_file": "bin/ttc/image_0040_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0030",
		"pointer_table_index": 25,
		"file_index": 6756,
		"source_file": "bin/ttc/image_0030.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0030_pal",
		"pointer_table_index": 25,
		"file_index": 6757,
		"source_file": "bin/ttc/image_0030_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0037",
		"pointer_table_index": 25,
		"file_index": 6758,
		"source_file": "bin/ttc/image_0037.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0037_pal",
		"pointer_table_index": 25,
		"file_index": 6759,
		"source_file": "bin/ttc/image_0037_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0047",
		"pointer_table_index": 25,
		"file_index": 6760,
		"source_file": "bin/ttc/image_0047.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0047_pal",
		"pointer_table_index": 25,
		"file_index": 6761,
		"source_file": "bin/ttc/image_0047_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0048",
		"pointer_table_index": 25,
		"file_index": 6762,
		"source_file": "bin/ttc/image_0048.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0048_pal",
		"pointer_table_index": 25,
		"file_index": 6763,
		"source_file": "bin/ttc/image_0048_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0049",
		"pointer_table_index": 25,
		"file_index": 6764,
		"source_file": "bin/ttc/image_0049.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0049_pal",
		"pointer_table_index": 25,
		"file_index": 6765,
		"source_file": "bin/ttc/image_0049_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0050",
		"pointer_table_index": 25,
		"file_index": 6766,
		"source_file": "bin/ttc/image_0050.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0050_pal",
		"pointer_table_index": 25,
		"file_index": 6767,
		"source_file": "bin/ttc/image_0050_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0027",
		"pointer_table_index": 25,
		"file_index": 6768,
		"source_file": "bin/sandcastle/image_0027.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0027_pal",
		"pointer_table_index": 25,
		"file_index": 6769,
		"source_file": "bin/sandcastle/image_0027_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0029",
		"pointer_table_index": 25,
		"file_index": 6770,
		"source_file": "bin/sandcastle/image_0029.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0029_pal",
		"pointer_table_index": 25,
		"file_index": 6771,
		"source_file": "bin/sandcastle/image_0029_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0030",
		"pointer_table_index": 25,
		"file_index": 6772,
		"source_file": "bin/sandcastle/image_0030.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0028",
		"pointer_table_index": 25,
		"file_index": 6773,
		"source_file": "bin/sandcastle/image_0028.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0028_pal",
		"pointer_table_index": 25,
		"file_index": 6774,
		"source_file": "bin/sandcastle/image_0028_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0031",
		"pointer_table_index": 25,
		"file_index": 6775,
		"source_file": "bin/sandcastle/image_0031.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0031_pal",
		"pointer_table_index": 25,
		"file_index": 6776,
		"source_file": "bin/sandcastle/image_0031_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0032",
		"pointer_table_index": 25,
		"file_index": 6777,
		"source_file": "bin/sandcastle/image_0032.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0032_pal",
		"pointer_table_index": 25,
		"file_index": 6778,
		"source_file": "bin/sandcastle/image_0032_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0034",
		"pointer_table_index": 25,
		"file_index": 6779,
		"source_file": "bin/sandcastle/image_0034.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0034_pal",
		"pointer_table_index": 25,
		"file_index": 6780,
		"source_file": "bin/sandcastle/image_0034_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0033",
		"pointer_table_index": 25,
		"file_index": 6781,
		"source_file": "bin/sandcastle/image_0033.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0033_pal",
		"pointer_table_index": 25,
		"file_index": 6782,
		"source_file": "bin/sandcastle/image_0033_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0023",
		"pointer_table_index": 25,
		"file_index": 6783,
		"source_file": "bin/sandcastle/image_0023.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0023_pal",
		"pointer_table_index": 25,
		"file_index": 6784,
		"source_file": "bin/sandcastle/image_0023_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0020",
		"pointer_table_index": 25,
		"file_index": 6785,
		"source_file": "bin/sandcastle/image_0020.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0020_pal",
		"pointer_table_index": 25,
		"file_index": 6786,
		"source_file": "bin/sandcastle/image_0020_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0018",
		"pointer_table_index": 25,
		"file_index": 6787,
		"source_file": "bin/sandcastle/image_0018.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0018_pal",
		"pointer_table_index": 25,
		"file_index": 6788,
		"source_file": "bin/sandcastle/image_0018_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0022",
		"pointer_table_index": 25,
		"file_index": 6789,
		"source_file": "bin/sandcastle/image_0022.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0022_pal",
		"pointer_table_index": 25,
		"file_index": 6790,
		"source_file": "bin/sandcastle/image_0022_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0008",
		"pointer_table_index": 25,
		"file_index": 6791,
		"source_file": "bin/sandcastle/image_0008.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0008_pal",
		"pointer_table_index": 25,
		"file_index": 6792,
		"source_file": "bin/sandcastle/image_0008_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0003",
		"pointer_table_index": 25,
		"file_index": 6793,
		"source_file": "bin/sandcastle/image_0003.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0003_pal",
		"pointer_table_index": 25,
		"file_index": 6794,
		"source_file": "bin/sandcastle/image_0003_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0013",
		"pointer_table_index": 25,
		"file_index": 6795,
		"source_file": "bin/sandcastle/image_0013.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0013_pal",
		"pointer_table_index": 25,
		"file_index": 6796,
		"source_file": "bin/sandcastle/image_0013_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0016",
		"pointer_table_index": 25,
		"file_index": 6797,
		"source_file": "bin/sandcastle/image_0016.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0016_pal",
		"pointer_table_index": 25,
		"file_index": 6798,
		"source_file": "bin/sandcastle/image_0016_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0011",
		"pointer_table_index": 25,
		"file_index": 6799,
		"source_file": "bin/sandcastle/image_0011.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0011_pal",
		"pointer_table_index": 25,
		"file_index": 6800,
		"source_file": "bin/sandcastle/image_0011_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0012",
		"pointer_table_index": 25,
		"file_index": 6801,
		"source_file": "bin/sandcastle/image_0012.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0012_pal",
		"pointer_table_index": 25,
		"file_index": 6802,
		"source_file": "bin/sandcastle/image_0012_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0015",
		"pointer_table_index": 25,
		"file_index": 6803,
		"source_file": "bin/sandcastle/image_0015.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0015_pal",
		"pointer_table_index": 25,
		"file_index": 6804,
		"source_file": "bin/sandcastle/image_0015_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0014",
		"pointer_table_index": 25,
		"file_index": 6805,
		"source_file": "bin/sandcastle/image_0014.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0014_pal",
		"pointer_table_index": 25,
		"file_index": 6806,
		"source_file": "bin/sandcastle/image_0014_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0019",
		"pointer_table_index": 25,
		"file_index": 6807,
		"source_file": "bin/sandcastle/image_0019.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0019_pal",
		"pointer_table_index": 25,
		"file_index": 6808,
		"source_file": "bin/sandcastle/image_0019_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0004",
		"pointer_table_index": 25,
		"file_index": 6809,
		"source_file": "bin/sandcastle/image_0004.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0004_pal",
		"pointer_table_index": 25,
		"file_index": 6810,
		"source_file": "bin/sandcastle/image_0004_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0002",
		"pointer_table_index": 25,
		"file_index": 6811,
		"source_file": "bin/sandcastle/image_0002.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0002_pal",
		"pointer_table_index": 25,
		"file_index": 6812,
		"source_file": "bin/sandcastle/image_0002_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0009",
		"pointer_table_index": 25,
		"file_index": 6813,
		"source_file": "bin/sandcastle/image_0009.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0009_pal",
		"pointer_table_index": 25,
		"file_index": 6814,
		"source_file": "bin/sandcastle/image_0009_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0006",
		"pointer_table_index": 25,
		"file_index": 6815,
		"source_file": "bin/sandcastle/image_0006.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0006_pal",
		"pointer_table_index": 25,
		"file_index": 6816,
		"source_file": "bin/sandcastle/image_0006_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0000",
		"pointer_table_index": 25,
		"file_index": 6817,
		"source_file": "bin/sandcastle/image_0000.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0000_pal",
		"pointer_table_index": 25,
		"file_index": 6818,
		"source_file": "bin/sandcastle/image_0000_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0025",
		"pointer_table_index": 25,
		"file_index": 6819,
		"source_file": "bin/sandcastle/image_0025.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0025_pal",
		"pointer_table_index": 25,
		"file_index": 6820,
		"source_file": "bin/sandcastle/image_0025_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0021",
		"pointer_table_index": 25,
		"file_index": 6821,
		"source_file": "bin/sandcastle/image_0021.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0021_pal",
		"pointer_table_index": 25,
		"file_index": 6822,
		"source_file": "bin/sandcastle/image_0021_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0017",
		"pointer_table_index": 25,
		"file_index": 6823,
		"source_file": "bin/sandcastle/image_0017.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0017_pal",
		"pointer_table_index": 25,
		"file_index": 6824,
		"source_file": "bin/sandcastle/image_0017_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0005",
		"pointer_table_index": 25,
		"file_index": 6825,
		"source_file": "bin/sandcastle/image_0005.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0005_pal",
		"pointer_table_index": 25,
		"file_index": 6826,
		"source_file": "bin/sandcastle/image_0005_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0024",
		"pointer_table_index": 25,
		"file_index": 6827,
		"source_file": "bin/sandcastle/image_0024.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0024_pal",
		"pointer_table_index": 25,
		"file_index": 6828,
		"source_file": "bin/sandcastle/image_0024_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0007",
		"pointer_table_index": 25,
		"file_index": 6829,
		"source_file": "bin/sandcastle/image_0007.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0007_pal",
		"pointer_table_index": 25,
		"file_index": 6830,
		"source_file": "bin/sandcastle/image_0007_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0001",
		"pointer_table_index": 25,
		"file_index": 6831,
		"source_file": "bin/sandcastle/image_0001.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0001_pal",
		"pointer_table_index": 25,
		"file_index": 6832,
		"source_file": "bin/sandcastle/image_0001_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0010",
		"pointer_table_index": 25,
		"file_index": 6833,
		"source_file": "bin/sandcastle/image_0010.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0010_pal",
		"pointer_table_index": 25,
		"file_index": 6834,
		"source_file": "bin/sandcastle/image_0010_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0026",
		"pointer_table_index": 25,
		"file_index": 6835,
		"source_file": "bin/sandcastle/image_0026.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0026_pal",
		"pointer_table_index": 25,
		"file_index": 6836,
		"source_file": "bin/sandcastle/image_0026_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0000",
		"pointer_table_index": 25,
		"file_index": 6837,
		"source_file": "bin/blubbers_ship/image_0000.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0000_pal",
		"pointer_table_index": 25,
		"file_index": 6838,
		"source_file": "bin/blubbers_ship/image_0000_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0006",
		"pointer_table_index": 25,
		"file_index": 6839,
		"source_file": "bin/blubbers_ship/image_0006.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0001",
		"pointer_table_index": 25,
		"file_index": 6840,
		"source_file": "bin/blubbers_ship/image_0001.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0001_pal",
		"pointer_table_index": 25,
		"file_index": 6841,
		"source_file": "bin/blubbers_ship/image_0001_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0002",
		"pointer_table_index": 25,
		"file_index": 6842,
		"source_file": "bin/blubbers_ship/image_0002.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0002_pal",
		"pointer_table_index": 25,
		"file_index": 6843,
		"source_file": "bin/blubbers_ship/image_0002_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0004",
		"pointer_table_index": 25,
		"file_index": 6844,
		"source_file": "bin/blubbers_ship/image_0004.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0003",
		"pointer_table_index": 25,
		"file_index": 6845,
		"source_file": "bin/blubbers_ship/image_0003.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0005",
		"pointer_table_index": 25,
		"file_index": 6846,
		"source_file": "bin/blubbers_ship/image_0005.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0007",
		"pointer_table_index": 25,
		"file_index": 6847,
		"source_file": "bin/blubbers_ship/image_0007.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0008",
		"pointer_table_index": 25,
		"file_index": 6848,
		"source_file": "bin/blubbers_ship/image_0008.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0008_pal",
		"pointer_table_index": 25,
		"file_index": 6849,
		"source_file": "bin/blubbers_ship/image_0008_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0009",
		"pointer_table_index": 25,
		"file_index": 6850,
		"source_file": "bin/blubbers_ship/image_0009.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0009_pal",
		"pointer_table_index": 25,
		"file_index": 6851,
		"source_file": "bin/blubbers_ship/image_0009_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0010",
		"pointer_table_index": 25,
		"file_index": 6852,
		"source_file": "bin/blubbers_ship/image_0010.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0010_pal",
		"pointer_table_index": 25,
		"file_index": 6853,
		"source_file": "bin/blubbers_ship/image_0010_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0007",
		"pointer_table_index": 25,
		"file_index": 6854,
		"source_file": "bin/lair_pipe_room/image_0007.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0007_pal",
		"pointer_table_index": 25,
		"file_index": 6855,
		"source_file": "bin/lair_pipe_room/image_0007_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0009",
		"pointer_table_index": 25,
		"file_index": 6856,
		"source_file": "bin/lair_pipe_room/image_0009.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0009_pal",
		"pointer_table_index": 25,
		"file_index": 6857,
		"source_file": "bin/lair_pipe_room/image_0009_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0006",
		"pointer_table_index": 25,
		"file_index": 6858,
		"source_file": "bin/lair_pipe_room/image_0006.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0006_pal",
		"pointer_table_index": 25,
		"file_index": 6859,
		"source_file": "bin/lair_pipe_room/image_0006_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0005",
		"pointer_table_index": 25,
		"file_index": 6860,
		"source_file": "bin/lair_pipe_room/image_0005.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0005_pal",
		"pointer_table_index": 25,
		"file_index": 6861,
		"source_file": "bin/lair_pipe_room/image_0005_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0004",
		"pointer_table_index": 25,
		"file_index": 6862,
		"source_file": "bin/lair_pipe_room/image_0004.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0001",
		"pointer_table_index": 25,
		"file_index": 6863,
		"source_file": "bin/lair_pipe_room/image_0001.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0001_pal",
		"pointer_table_index": 25,
		"file_index": 6864,
		"source_file": "bin/lair_pipe_room/image_0001_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0008",
		"pointer_table_index": 25,
		"file_index": 6865,
		"source_file": "bin/lair_pipe_room/image_0008.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0008_pal",
		"pointer_table_index": 25,
		"file_index": 6866,
		"source_file": "bin/lair_pipe_room/image_0008_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0000",
		"pointer_table_index": 25,
		"file_index": 6867,
		"source_file": "bin/lair_pipe_room/image_0000.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0010",
		"pointer_table_index": 25,
		"file_index": 6868,
		"source_file": "bin/lair_pipe_room/image_0010.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0003",
		"pointer_table_index": 25,
		"file_index": 6869,
		"source_file": "bin/lair_pipe_room/image_0003.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0003_pal",
		"pointer_table_index": 25,
		"file_index": 6870,
		"source_file": "bin/lair_pipe_room/image_0003_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0013",
		"pointer_table_index": 25,
		"file_index": 6871,
		"source_file": "bin/lair_pipe_room/image_0013.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0012",
		"pointer_table_index": 25,
		"file_index": 6872,
		"source_file": "bin/lair_pipe_room/image_0012.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0012_pal",
		"pointer_table_index": 25,
		"file_index": 6873,
		"source_file": "bin/lair_pipe_room/image_0012_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0011",
		"pointer_table_index": 25,
		"file_index": 6874,
		"source_file": "bin/lair_pipe_room/image_0011.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0011_pal",
		"pointer_table_index": 25,
		"file_index": 6875,
		"source_file": "bin/lair_pipe_room/image_0011_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0002",
		"pointer_table_index": 25,
		"file_index": 6876,
		"source_file": "bin/lair_pipe_room/image_0002.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0002_pal",
		"pointer_table_index": 25,
		"file_index": 6877,
		"source_file": "bin/lair_pipe_room/image_0002_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0014",
		"pointer_table_index": 25,
		"file_index": 6878,
		"source_file": "bin/lair_pipe_room/image_0014.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0016",
		"pointer_table_index": 25,
		"file_index": 6879,
		"source_file": "bin/banjos_house/image_0016.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0003",
		"pointer_table_index": 25,
		"file_index": 6880,
		"source_file": "bin/banjos_house/image_0003.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0003_pal",
		"pointer_table_index": 25,
		"file_index": 6881,
		"source_file": "bin/banjos_house/image_0003_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0012",
		"pointer_table_index": 25,
		"file_index": 6882,
		"source_file": "bin/banjos_house/image_0012.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0012_pal",
		"pointer_table_index": 25,
		"file_index": 6883,
		"source_file": "bin/banjos_house/image_0012_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0000",
		"pointer_table_index": 25,
		"file_index": 6884,
		"source_file": "bin/banjos_house/image_0000.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0000_pal",
		"pointer_table_index": 25,
		"file_index": 6885,
		"source_file": "bin/banjos_house/image_0000_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0002",
		"pointer_table_index": 25,
		"file_index": 6886,
		"source_file": "bin/banjos_house/image_0002.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0002_pal",
		"pointer_table_index": 25,
		"file_index": 6887,
		"source_file": "bin/banjos_house/image_0002_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0001",
		"pointer_table_index": 25,
		"file_index": 6888,
		"source_file": "bin/banjos_house/image_0001.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0001_pal",
		"pointer_table_index": 25,
		"file_index": 6889,
		"source_file": "bin/banjos_house/image_0001_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0006",
		"pointer_table_index": 25,
		"file_index": 6890,
		"source_file": "bin/banjos_house/image_0006.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0006_pal",
		"pointer_table_index": 25,
		"file_index": 6891,
		"source_file": "bin/banjos_house/image_0006_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0005",
		"pointer_table_index": 25,
		"file_index": 6892,
		"source_file": "bin/banjos_house/image_0005.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0014",
		"pointer_table_index": 25,
		"file_index": 6893,
		"source_file": "bin/banjos_house/image_0014.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0014_pal",
		"pointer_table_index": 25,
		"file_index": 6894,
		"source_file": "bin/banjos_house/image_0014_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0011",
		"pointer_table_index": 25,
		"file_index": 6895,
		"source_file": "bin/banjos_house/image_0011.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0011_pal",
		"pointer_table_index": 25,
		"file_index": 6896,
		"source_file": "bin/banjos_house/image_0011_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0017",
		"pointer_table_index": 25,
		"file_index": 6897,
		"source_file": "bin/banjos_house/image_0017.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0017_pal",
		"pointer_table_index": 25,
		"file_index": 6898,
		"source_file": "bin/banjos_house/image_0017_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0013",
		"pointer_table_index": 25,
		"file_index": 6899,
		"source_file": "bin/banjos_house/image_0013.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0013_pal",
		"pointer_table_index": 25,
		"file_index": 6900,
		"source_file": "bin/banjos_house/image_0013_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0007",
		"pointer_table_index": 25,
		"file_index": 6901,
		"source_file": "bin/banjos_house/image_0007.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0007_pal",
		"pointer_table_index": 25,
		"file_index": 6902,
		"source_file": "bin/banjos_house/image_0007_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0009",
		"pointer_table_index": 25,
		"file_index": 6903,
		"source_file": "bin/banjos_house/image_0009.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0009_pal",
		"pointer_table_index": 25,
		"file_index": 6904,
		"source_file": "bin/banjos_house/image_0009_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0010",
		"pointer_table_index": 25,
		"file_index": 6905,
		"source_file": "bin/banjos_house/image_0010.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0010_pal",
		"pointer_table_index": 25,
		"file_index": 6906,
		"source_file": "bin/banjos_house/image_0010_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0008",
		"pointer_table_index": 25,
		"file_index": 6907,
		"source_file": "bin/banjos_house/image_0008.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0008_pal",
		"pointer_table_index": 25,
		"file_index": 6908,
		"source_file": "bin/banjos_house/image_0008_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0004",
		"pointer_table_index": 25,
		"file_index": 6909,
		"source_file": "bin/banjos_house/image_0004.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0004_pal",
		"pointer_table_index": 25,
		"file_index": 6910,
		"source_file": "bin/banjos_house/image_0004_pal.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0015",
		"pointer_table_index": 25,
		"file_index": 6911,
		"source_file": "bin/banjos_house/image_0015.bin",
		"do_not_extract": True
	},
	{
		"name": "image_0015_pal",
		"pointer_table_index": 25,
		"file_index": 6912,
		"source_file": "bin/banjos_house/image_0015_pal.bin",
		"do_not_extract": True
	}
]

map_replacements = [
	{
		"name": "Banjo's House",
		"map_index": 0x1D,
		"map_folder": "maps/banjos_house/"
	},
	{
		"name": "Spiral Mountain",
		"map_index": 0xAB,
		"map_folder": "maps/spiral_mountain/"
	},
	{
		"name": "Lair Entrance",
		"map_index": 0xA9,
		"map_folder": "maps/lair_entrance/"
	},
	{
		"name": "Mumbo's Mountain",
		"map_index": 0x13,
		"map_folder": "maps/mumbos_mountain/"
	},
	{
		"name": "Ticker's Tower",
		"map_index": 0x15,
		"map_folder": "maps/tickers_tower/"
	},
	{
		"name": "Mumbo's Skull",
		"map_index": 0x16,
		"map_folder": "maps/mumbos_skull/"
	},
	{
		"name": "Lair F2",
		"map_index": 0xAD,
		"map_folder": "maps/lair_f2/"
	},
	{
		"name": "Lair F3",
		"map_index": 0xAE,
		"map_folder": "maps/lair_f3/"
	},
	{
		"name": "Lair TTC Entrance",
		"map_index": 0xAF,
		"map_folder": "maps/lair_ttc_entrance/"
	},
	{
		"name": "Lair Pipe Room",
		"map_index": 0xB2,
		"map_folder": "maps/lair_pipe_room/"
	},
	{
		"name": "TTC",
		"map_index": 0x5A,
		"map_folder": "maps/ttc/"
	},
	{
		"name": "Sandcastle",
		"map_index": 0x5B,
		"map_folder": "maps/sandcastle/"
	},
	{
		"name": "Sandcastle",
		"map_index": 0x5C,
		"map_folder": "maps/blubbers_ship/"
	},
	{
		"name": "Main Menu",
		"map_index": 0x50,
		"map_folder": "maps/main_menu/"
	}	
]

# Test all map replacements at once
# from map_names import maps
# for mapIndex, mapName in enumerate(maps):
# 	mapPath = "maps/" + str(mapIndex) + " - " + make_safe_filename(mapName) + "/"
# 	map_replacements.append({
# 		"name": mapName,
# 		"map_index": mapIndex,
# 		"map_folder": mapPath,
# 	})

with open(ROMName, "rb") as fh:
	print("[2 / 8] - Parsing pointer tables")
	parsePointerTables(fh)
	readOverlayOriginalData(fh)

	for x in map_replacements:
		print(" - Processing map replacement " + x["name"])
		if os.path.exists(x["map_folder"]):
			found_geometry = False
			found_floors = False
			found_walls = False
			should_compress_walls = True
			should_compress_floors = True
			for y in pointer_tables:
				if not "encoded_filename" in y:
					continue

				# Convert decoded_filename to encoded_filename using the encoder function
				# Eg. exits.json to exits.bin
				if "encoder" in y and callable(y["encoder"]):
					if "decoded_filename" in y and os.path.exists(x["map_folder"] + y["decoded_filename"]):
						y["encoder"](x["map_folder"] + y["decoded_filename"], x["map_folder"] + y["encoded_filename"])
				
				if os.path.exists(x["map_folder"] + y["encoded_filename"]):
					if y["index"] == 1:
						with open(x["map_folder"] + y["encoded_filename"], "rb") as fg:
							byte_read = fg.read(10)
							should_compress_walls = (byte_read[9] & 0x1) != 0
							should_compress_floors = (byte_read[9] & 0x2) != 0
						found_geometry = True
					elif y["index"] == 2:
						found_walls = True
					elif y["index"] == 3:
						found_floors = True

			# Check that all walls|floors|geometry files exist on disk, or that none of them do
			walls_floors_geometry_valid = (found_geometry == found_walls) and (found_geometry == found_floors)

			if not walls_floors_geometry_valid:
				print("  - WARNING: In map replacement: " + x["name"])
				print("    - Need all 3 files present to replace walls, floors, and geometry.")
				print("    - Only found 1 or 2 of them out of 3. Make sure all 3 exist on disk.")
				print("    - Will skip replacing walls, floors, and geometry to prevent crashes.")

			for y in pointer_tables:
				if not "encoded_filename" in y:
					continue

				if os.path.exists(x["map_folder"] + y["encoded_filename"]):
					# Special case to prevent crashes with custom level geometry, walls, and floors
					# Some of the files are compressed in ROM, some are not
					if y["index"] in [1, 2, 3] and not walls_floors_geometry_valid:
						continue

					do_not_compress = "do_not_compress" in y and y["do_not_compress"]
					if y["index"] == 2:
						do_not_compress = not should_compress_walls
					elif y["index"] == 3:
						do_not_compress = not should_compress_floors

					print("  - Found " + x["map_folder"] + y["encoded_filename"])
					file_dict.append({
						"name": x["name"] + y["name"],
						"pointer_table_index": y["index"],
						"file_index": x["map_index"],
						"source_file": x["map_folder"] + y["encoded_filename"],
						"do_not_extract": True,
						"do_not_compress": do_not_compress,
						"use_external_gzip": "use_external_gzip" in y and y["use_external_gzip"],
					})

	print("[3 / 8] - Extracting files from ROM")
	for x in file_dict:
		# N64Tex conversions do not need to be extracted to disk from ROM
		if "texture_format" in x:
			x["do_not_extract"] = True
			x["output_file"] = x["source_file"].replace(".png", "." + x["texture_format"])

		if not "output_file" in x:
			x["output_file"] = x["source_file"]

		# gzip.exe appends .gz to the filename, we'll do the same
		if "use_external_gzip" in x and x["use_external_gzip"]:
			x["output_file"] = x["output_file"] + ".gz"

		# If we're not extracting the file to disk, we're using a custom .bin that shoudn't be deleted
		if "do_not_extract" in x and x["do_not_extract"]:
			x["do_not_delete_source"] = True

		# Extract the compressed file from ROM
		if not ("do_not_extract" in x and x["do_not_extract"]):
			byte_read = bytes()
			if "pointer_table_index" in x and "file_index" in x:
				file_info = getFileInfo(x["pointer_table_index"], x["file_index"])
				if file_info:
					x["start"] = file_info["new_absolute_address"]
					x["compressed_size"] = len(file_info["data"])

			fh.seek(x["start"])
			byte_read = fh.read(x["compressed_size"])

			if not ("do_not_delete_source" in x and x["do_not_delete_source"]):
				if os.path.exists(x["source_file"]):
					os.remove(x["source_file"])

				with open(x["source_file"], "wb") as fg:
					dec = zlib.decompress(byte_read, 15 + 32)
					fg.write(dec)

print("[4 / 8] - Patching Extracted Files")
for x in file_dict:
	if "patcher" in x and callable(x["patcher"]):
		print(" - Running patcher for " + x["source_file"])
		x["patcher"](x["source_file"])

with open(newROMName, "r+b") as fh:
	print("[5 / 8] - Writing patched files to ROM")
	for x in file_dict:
		if "texture_format" in x:
			if x["texture_format"] in ["rgba5551", "i4", "ia4", "i8", "ia8"]:
				subprocess.run(["./build/n64tex.exe", x["texture_format"], x["source_file"]])
			else:
				print(" - ERROR: Unsupported texture format " + x["texture_format"])

		if "use_external_gzip" in x and x["use_external_gzip"]:
			if os.path.exists(x["source_file"]):
				subprocess.run(["./build/gzip.exe", "-f", "-n", "-k", "-q", "-9", x["output_file"].replace(".gz", "")])
				if os.path.exists(x["output_file"]):
					with open(x["output_file"], "r+b") as outputFile:
						# Chop off gzip footer
						outputFile.truncate(len(outputFile.read()) - 8)

		if os.path.exists(x["output_file"]):
			byte_read = bytes()
			uncompressed_size = 0
			with open(x["output_file"], "rb") as fg:
				byte_read = fg.read()
				uncompressed_size = len(byte_read)

			if "do_not_compress" in x and x["do_not_compress"]:
				compress = bytearray(byte_read)
			elif "use_external_gzip" in x and x["use_external_gzip"]:
				compress = bytearray(byte_read)
			elif "use_zlib" in x and x["use_zlib"]:
				compressor = zlib.compressobj(zlib.Z_BEST_COMPRESSION, zlib.DEFLATED, 25)
				compress = compressor.compress(byte_read)
				compress += compressor.flush()
				compress = bytearray(compress)
				# Zero out timestamp in gzip header to make builds deterministic
				compress[4] = 0
				compress[5] = 0
				compress[6] = 0
				compress[7] = 0
				# They used "Unix" as their Operating System ID, let's do the same
				compress[9] = 3
			else:
				compress = bytearray(gzip.compress(byte_read, compresslevel=9))
				# Zero out timestamp in gzip header to make builds deterministic
				compress[4] = 0
				compress[5] = 0
				compress[6] = 0
				compress[7] = 0
				# They used "Unix" as their Operating System ID, let's do the same
				compress[9] = 3

			print(" - Writing " + x["output_file"] + " (" + hex(len(compress)) + ") to ROM")
			if "pointer_table_index" in x and "file_index" in x:
				# More complicated write, update the pointer tables to point to the new data
				replaceROMFile(x["pointer_table_index"], x["file_index"], compress, uncompressed_size, x["output_file"])
			elif "start" in x:
				if isROMAddressOverlay(x["start"]):
					replaceOverlayData(x["start"], compress)
				else:
					# Simply write the bytes at the absolute address in ROM specified by x["start"]
					fh.seek(x["start"])
					fh.write(compress)
			else:
				print("  - WARNING: Can't find address information in file_dict entry to write " + x["output_file"] + " (" + hex(len(compress)) + ") to ROM")
		else:
			print(x["output_file"] + " does not exist")

		# Cleanup temporary files
		if not ("do_not_delete" in x and x["do_not_delete"]):
			if not ("do_not_delete_output" in x and x["do_not_delete_output"]):
				if os.path.exists(x["output_file"]) and x["output_file"] != x["source_file"]:
					os.remove(x["output_file"])
			if not ("do_not_delete_source" in x and x["do_not_delete_source"]):
				if os.path.exists(x["source_file"]):
					os.remove(x["source_file"])

	print("[6 / 8] - Writing recomputed pointer tables to ROM")
	writeModifiedPointerTablesToROM(fh)
	writeModifiedOverlaysToROM(fh)

	print("[7 / 8] - Dumping details of all pointer tables to rom/pointer_tables_modified.log")
	dumpPointerTableDetails("rom/pointer_tables_modified.log", fh)

# For compatibility with real hardware, the ROM size needs to be aligned to 0x10 bytes
with open(newROMName, "r+b") as fh:
    to_add = len(fh.read()) % 0x10
    if to_add > 0:
        to_add = 0x10 - to_add
        for x in range(to_add):
            fh.write(bytes([0]))

print("[8 / 8] - Generating BizHawk RAM watch")
import generate_watch_file

# Write custom ASM code to ROM
subprocess.run(["build/armips.exe", "asm\main.asm", "-sym", "rom\dk64-newhack-dev.sym"])

# Fix CRC
from n64crc import fixCRC
fixCRC(newROMName)

# Remove temporary .o files
# shutil.rmtree('obj')

end_time = time.time()
with open(newROMName, "rb") as fh:
	print()
	print("Built " + newROMName + " in " + str(round(end_time - start_time, 3)) + " seconds")
	print("SHA1: " + hashlib.sha1(fh.read()).hexdigest().upper())