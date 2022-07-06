'''
 # @ Author: Laroustine
 # @ Modified time: 05/07 17:07
 # @ Modified by: Laroustine
 # @ Description: This script has been made by me ↖(^▽^)↗
 '''

import argparse
import json
import csv
from os import walk, makedirs
from os.path import isdir, join, isfile
from pathlib import Path

BASE_FACTION = [
    "pirates",
    "hegemony",
    "independent",
    "tritachyon",
    "sindrian_diktat",
    "lions_guard",
    "knights_of_ludd",
    "luddic_church",
    "luddic_path",
    "persean_league",
    "derelict",
    "remnants",
    "omega",
    "scavengers",
    "sleeper",
    "mercenary"
]


def make_file_entry(location: str, faction: str, mtype: str):
    entry_data = {"source": join("sounds/music/cbm", join(faction, mtype)),
                  "volume": 0.1,
                  "files": next(walk(join(location, mtype)))[2],
                  "randomStart": False}
    return [entry_data]


def make_music_info(location: str):
    music_data = {"music": {}}

    for faction in sorted(next(walk(join(location, "")))[1]):
        for mtype in next(walk(join(location, faction)))[1]:
            music_data["music"][f"{faction}_{mtype}"] = make_file_entry(
                join(location, faction), faction, mtype)
    return music_data


def make_music_file(location: str, location_current: str):
    print("Sounds File in progress")
    with open(f"{join(location_current, 'data/config/sounds.json')}", mode="w") as json_file:
        json.dump(make_music_info(location), json_file, indent=4)
    print("Sounds File done")


def make_faction_info(location: str, faction: str, song: str = "") -> object:
    result = faction if song == "" else song
    filenames = next(walk(join(location, result)))[1]
    faction_data = {"music": {}}

    for k in filenames:
        faction_data["music"][k] = f"{result}_{k}"
    print(f"{faction}: {faction_data}")
    return faction_data


def edit_faction_info(faction_data: object, location: str, faction: str, song: str = "") -> object:
    result = faction if song == "" else song
    filenames = next(walk(join(location, result)))[1]

    for k in filenames:
        faction_data["music"][k] = f"{result}_{k}"
    print(f"Edited {faction}: {faction_data}")
    return faction_data


def make_faction_file(location: str, mod_loc: str, faction: str, song: str = "", single: bool = False):
    location_current = join(mod_loc, "data/world/factions")

    if isfile(join(location_current, faction + '.faction')) and single:
        with open(f"{join(location_current, faction + '.faction')}", mode="r+") as json_file:
            data = json.load(json_file)
            json_file.seek(0)
            json.dump(edit_faction_info(
                data, location, faction, song), json_file, indent=4)
    elif not isfile(join(location_current, faction + '.faction')):
        with open(f"{join(location_current, faction + '.faction')}", mode="w") as json_file:
            json.dump(make_faction_info(
                location, faction, song), json_file, indent=4)


def make_all_file(location: str, mod_loc: str, factions: list = [], only_file: bool = False):
    if (only_file):
        print("Make Base Faction")
        for k in BASE_FACTION:
            make_faction_file(location, mod_loc, k, "00")
    print("Make Modded Faction")
    for k in factions:
        make_faction_file(location, mod_loc, k, "00")


def check_files(location):
    if (not isdir(join(location, "data"))):
        makedirs(join(location, "data"))
    if (not isdir(join(location, "data/config"))):
        makedirs(join(location, "data/config"))
    if (not isdir(join(location, "data/world"))):
        makedirs(join(location, "data/world"))
    if (not isdir(join(location, "data/world/factions"))):
        makedirs(join(location, "data/world/factions"))


def get_factions(file_list: list):
    result = []

    for file_csv in file_list:
        for k in csv.reader(file_csv):
            value = k[0]
            if (value != "faction"):
                result.append(value.split("/")[-1].split(".faction")[0])
    return result


def main(args):
    sound_location = join(args.music, "sounds/music/cbm/")
    mod_location = join(args.path, "")
    faction_list = []

    if (not isdir(sound_location)):
        print("This mod does not have the folders to make the operation possible.")
        return 1
    check_files(mod_location)
    faction_list = sorted(set(next(walk(sound_location))[1]))
    all_faction = sorted(
        set(faction_list[1:] + get_factions(args.faction) + args.name))

    make_music_file(sound_location, mod_location)
    for k in faction_list:
        if (k == "00"):
            print(f"All Factions have:")
            make_all_file(sound_location, mod_location, all_faction, args.only)
        else:
            print(f"Faction : {k}")
            make_faction_file(sound_location, mod_location, k, single=True)
        print(5 * "_")
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="MusicListMaker")
    parser.add_argument(
        "path", help='Path to Custom Battle Music', metavar="CBM_PATH")
    parser.add_argument(
        "music", help='Path to the musics location', metavar="MUSIC_PATH")
    parser.add_argument('-o', '--only', required=False, action='store_false',
                        help='Only adds the CSV factions')
    parser.add_argument('-f', '--faction', required=False, action='append', type=argparse.FileType('r'),
                        help='Factions from a csv file are added to the "00" option', default=[], metavar="FACTION_CSV")
    parser.add_argument('-n', '--name', required=False, action='append', type=str,
                        help='faction name', default=[], metavar="FACTION")
    args = parser.parse_args()
    exit(main(args))
