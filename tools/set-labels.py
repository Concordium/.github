#!/usr/bin/env python3

# Update labels on a given github repository to the given set.
# The script should be run with the following parameters
#
# Environment variable GH_TOKEN should contain a github personal access token, see https://github.com/settings/tokens/
#
# The first argument should be a JSON file containing descriptions of the labels for the repository.
# This must be a list of objects with fields 'name', 'color', and 'description' in the following format
# {
#     "name": "[Prio] Low",
#     "color": "FBCA04",
#     "description": "Should be fixed if time permits but can be postponed."
# }
# The last argument should be the name of the repository (inside the Concordium group).
#
# An example invocation would be
# GH_TOKEN=... ./set-labels.py new_labels.json concordium-base
# to set the labels of the `concordium-base` repository to the given ones.

# The script depends on the requests library, which can be installed with.
# `pip3 install requests`.

# The script does the following
#
# - if a label with a specified name already exists then the script will either
# do nothing, if the details of the label are the same, or update it if they are
# not.
#
# - if an existing label is not among the new labels it will be deleted
# - any new labels will be added
#
# The script terminates at the first unsuccessful request.

import urllib

import requests
import json
import sys
import os


def run(new_labels, repo, token):
    url = f"https://api.github.com/repos/Concordium/{repo}/labels"
    params = {"per_page": 100} # needs to be enough to cover all the labels
    headers = {"Accept": "application/vnd.github.v3+json",
               "Authorization": f"Bearer {token}"
               }
    labels = []
    for label in requests.get(url, params=params, headers=headers).json():
        extract = {key: label[key] for key in {'name', 'color', 'description'}}
        labels.append(extract)
    new_labels_dict = {val['name']: val for val in new_labels}
    for existing in labels:
        name = existing['name']
        update_url = f"{url}/{urllib.parse.quote(name)}"
        # if a label with the name exists in the new set of labels just update it
        # See https://docs.github.com/en/rest/reference/issues#update-a-label
        if name in new_labels_dict:
            if new_labels_dict[name] != existing:
                resp = requests.patch(update_url, json=new_labels_dict[name], headers=headers)
                if not resp.ok:
                    print(f"Could not update label {resp.status_code}/{resp.text}")
                    return
                else:
                    print(f"Updated label {name}")
            else:
                print(f"'{name}' is already the same label")
            # and remove so we don't consider it again
            del new_labels_dict[name]
        else:
            # Otherwise delete the label, see https://docs.github.com/en/rest/reference/issues#delete-a-label
            resp = requests.delete(update_url, headers=headers)
            if not resp.ok:
                print(f"Could not delete label {resp.status_code}/{resp.url}/{resp.text}")
                return
            else:
                print(f"Deleted label {name}")
    # for any remaining labels in new_labels_dict, add them
    for label in new_labels_dict.values():
        resp = requests.post(url, json=label, headers=headers)
        if not resp.ok:
            print(f"Could not add label {resp.status_code}/{resp.text}")
            return


if __name__ == '__main__':
    GH_TOKEN = os.environ.get("GH_TOKEN")
    if GH_TOKEN is None:
        print("Need github access token.")
        sys.exit(1)
    with open(sys.argv[1]) as input_labels_f:
        input_labels = json.load(input_labels_f)
        run(input_labels, sys.argv[2], GH_TOKEN)
