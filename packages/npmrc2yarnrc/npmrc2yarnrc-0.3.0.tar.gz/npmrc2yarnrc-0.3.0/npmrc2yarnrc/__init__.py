import sys
from collections import defaultdict
from os.path import expanduser
from typing import Dict, Tuple

from mergedeep import merge

import yaml


def parse_delimited_string(delim: str, s: str) -> Tuple[str, str]:
    toks = s.split(delim)
    return toks[0].strip(), delim.join(toks[1:]).strip()


def parse_npmrc(file_path: str) -> dict:
    repos: Dict[str, Dict[str, str]] = defaultdict(dict)
    with open(file_path, "r") as f:
        for line in f.readlines():
            key, value = parse_delimited_string(":", line)
            subkey, subvalue = parse_delimited_string("=", value)
            repos[key][subkey] = subvalue
    return repos


def parse_yarnrc(file_path: str) -> dict:
    try:
        with open(file_path, "r") as f:
            return yaml.load(f.read(), Loader=yaml.FullLoader)
    except FileNotFoundError:
        return {}


def merge_iotex_npmrc_into_yarnrc():
    home = expanduser("~")
    try:
        npmrc = parse_npmrc(f"{home}/.npmrc")
    except FileNotFoundError:
        print(f"{home}/.npmrc not found, nothing to do")
        return

    try:
        repo_key = npmrc["@iotex"]["registry"].replace("https://", "//")
    except KeyError:
        print("ERROR: Did you remember to run 'aws codeartifact login'?")
        sys.exit(1)

    yarnrc_from_npmrc = {
        "npmRegistries": {
            repo_key.rstrip("/"): {
                "npmAlwaysAuth": True,
                "npmAuthToken": npmrc[repo_key]["_authToken"],
            }
        },
        "npmScopes": {"iotex": {"npmRegistryServer": npmrc["@iotex"]["registry"].rstrip("/")}},
    }

    yarnrc = parse_yarnrc(f"{home}/.yarnrc.yml")

    with open(f"{home}/.yarnrc.yml", "w") as f:
        f.write(yaml.dump(merge(yarnrc, yarnrc_from_npmrc)))
