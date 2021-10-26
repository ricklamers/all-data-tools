import json
import os
import argparse
import logging
import datetime

import requests

from urllib.parse import urlparse
from dateutil import parser
from collections import OrderedDict


DATETIME_FORMAT = "%Y-%m-%d %H:%M"


def _construct_base_endpoint(protocol, host, project_slug):
    return f"{protocol}://{host}/nc/{project_slug}/api/v1/"


def _merge_objects(list_a, list_b, pk="id", date_field="updated_at"):
    """Requires objs in list_a|list_b to be JSON dictionaries with a
    `pk` key and `date_field` in format `2021-10-25 12:01:02`
    (parser.parse accepts more, use at your discretion).

    Note that the order of the original list is preserved.
    New pk objects are appended.
    """
    merged_dict = OrderedDict()

    for obj in list_a:
        merged_dict[obj[pk]] = obj

    for obj in list_b:
        if obj[pk] in merged_dict:
            # Compare updated_at entries
            a = merged_dict[obj[pk]]
            b = obj

            if parser.parse(a[date_field]) < parser.parse(b[date_field]):
                merged_dict[obj[pk]] = b
        else:
            merged_dict[obj[pk]] = obj

    return list(merged_dict.values())


def _get_list_from_api(table, row_limit, nc_protocol, nc_host, project_slug, xc_key):
    get_endpoint = (
        _construct_base_endpoint(nc_protocol, nc_host, project_slug)
        + f"{table}?limit={row_limit}"
    )
    resp = requests.get(get_endpoint, headers={"xc-auth": xc_key})
    return resp.json()


def merge(
    table,
    project_slug,
    xc_key,
    nc_protocol,
    nc_host,
    row_limit,
    json_file,
    object_pk,
    object_date_field,
):

    # Start merge

    # Get all table entries as JSON
    api_tools = _get_list_from_api(
        table, row_limit, nc_protocol, nc_host, project_slug, xc_key
    )

    # Read in all existing entries as JSON from disk
    file_tools = []

    try:
        if os.path.isfile(json_file):
            with open(json_file, "rb") as f:
                file_tools = json.load(f)
    except Exception as e:
        logging.error(
            "Failed to read JSON at %s with error %s [%s]" % (json_file, e, type(e))
        )
        pass

    # Merge by letting the object with latest `object_date_field` win
    merged_file_tools = _merge_objects(
        api_tools, file_tools, object_pk, object_date_field
    )

    # Write result to disk & API

    # On disk overwrite old file
    with open(json_file, "w") as f:
        f.write(json.dumps(merged_file_tools, f, indent=2, sort_keys=True))

    # On API drop all records, and bulk insert
    bulk_endpoint = (
        _construct_base_endpoint(nc_protocol, nc_host, project_slug) + f"{table}/bulk"
    )

    # Drop all tools returned by API
    requests.delete(
        bulk_endpoint,
        json=[{object_pk: obj[object_pk]} for obj in api_tools],
        headers={"xc-auth": xc_key},
    )

    # Insert all records
    requests.post(bulk_endpoint, json=merged_file_tools, headers={"xc-auth": xc_key})


def _get_star_count(github_url):
    # Expected URL format: https://github.com/owner/repo[/...]
    # [...] ending is optional
    url = urlparse(github_url)

    _, owner, repo_name = url.path.split("/")[:3]
    repo_info = requests.get("https://api.github.com/repos/" + owner + "/" + repo_name)

    return repo_info.json()["stargazers_count"]


def update_stars(
    table,
    row_limit,
    nc_protocol,
    nc_host,
    project_slug,
    xc_key,
    object_pk,
    object_date_field,
    github_column="GitHub URL",
    github_star_column="GitHub Stars",
):
    api_tools = _get_list_from_api(
        table, row_limit, nc_protocol, nc_host, project_slug, xc_key
    )

    for tool in api_tools:
        if (
            github_column in tool
            and github_star_column in tool
            and "http" in tool[github_column]
        ):
            try:
                star_count = _get_star_count(tool[github_column])

                update_endpoint = (
                    _construct_base_endpoint(nc_protocol, nc_host, project_slug)
                    + f"{table}/{tool[object_pk]}"
                )

                # Make a PUT iff star_count changed
                if tool[github_star_column] != star_count:
                    requests.put(
                        update_endpoint,
                        json={
                            object_date_field: datetime.datetime.utcnow().strftime(
                                DATETIME_FORMAT
                            ),
                            github_star_column: star_count,
                        },
                        headers={"xc-auth": xc_key},
                    )
            except:
                logging.info(
                    "Failed to get GitHub star count for %s" % tool[github_column]
                )


if __name__ == "__main__":

    logging.basicConfig(level=logging.INFO)

    # Required environment variables
    table = os.environ.get("NC_TABLE_NAME")
    project_slug = os.environ.get("NC_PROJECT_SLUG")
    xc_key = os.environ.get("NC_XC_KEY")

    # Optional environment variables
    nc_protocol = os.environ.get("NC_PROTOCOL", "http")
    nc_host = os.environ.get("NC_HOST", "127.0.0.1:8080")
    row_limit = int(os.environ.get("NC_ROW_LIMIT", 50000))
    json_file = os.environ.get("JSON_FILE", "tools.json")
    object_pk = os.environ.get("NC_OBJECT_PK", "id")
    object_date_field = os.environ.get("NC_OBJECT_DATE_FIELD", "updated_at")

    arg_parser = argparse.ArgumentParser(prog="sync.py")
    arg_parser.add_argument("action", choices=["merge", "update-stars"])
    args = arg_parser.parse_args()

    if args.action == "merge":
        merge(
            table,
            project_slug,
            xc_key,
            nc_protocol,
            nc_host,
            row_limit,
            json_file,
            object_pk,
            object_date_field,
        )
    elif args.action == "update-stars":
        # Note, if the star count is updated, any changes
        # in the tools.json are ignored (as the API version will
        # always be newer).
        update_stars(
            table,
            row_limit,
            nc_protocol,
            nc_host,
            project_slug,
            xc_key,
            object_pk,
            object_date_field,
        )
    else:
        raise Exception("Command %s not recognized" % args.action)
