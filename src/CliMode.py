'''
 # @ Author: Laroustine
 # @ Modified time: 10/07 20:34
 # @ Modified by: Laroustine
 # @ Description: This script has been made by me ↖(^▽^)↗
 '''

import argparse
from os import walk
from os.path import join, isdir
from MusicMaker import check_files, get_factions, make_music_file, make_all_file, make_faction_file, remove_unwanted


def main(args):
    sound_location = join(args.music, "sounds/music/cbm/")
    mod_location = join(args.path, "")
    faction_list = []

    if (not isdir(sound_location)):
        print("This mod does not have the folders to make the operation possible.")
        return 1
    check_files(mod_location)
    faction_list = remove_unwanted(sorted(set(next(walk(sound_location))[1])))
    all_faction = sorted(
        set(faction_list[1:] + get_factions(args.faction) + args.name))

    make_music_file(sound_location, mod_location)
    for k in faction_list:
        if k == "00":
            print(f"All Factions have:")
            make_all_file(sound_location, mod_location, all_faction, args.only)
        else:
            print(f"Faction : {k}")
            make_faction_file(sound_location, mod_location, k, single=True)
        print(5 * "_")
    return 0


def arg_checker(manual_value=""):
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
    if manual_value == "":
        args = parser.parse_args()
    else:
        args = parser.parse_args(manual_value)
    exit(main(args))


if __name__ == "__main__":
    arg_checker()
