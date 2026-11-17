#!/usr/bin/env python3

import argparse
import re
from pathlib import Path
from urllib.request import urlopen
from urllib.parse import urlencode


def load_airports(filename):
    """Load airport ICAO identifiers from a text file."""

    airports = []

    with open(filename, "r") as file:
        for line in file:
            airport = line.strip().upper()

            if airport and not airport.startswith("#"):
                airports.append(airport)

    return airports


def fetch_metars(airport, hours=24):
    """Fetch METAR reports from Aviation Weather Center."""

    url = "https://aviationweather.gov/api/data/metar"

    params = urlencode({
        "ids": airport,
        "hours": hours,
        "sep": "true",
    })

    with urlopen(f"{url}?{params}", timeout=30) as response:
        return response.read().decode("utf-8")


def check_hail(metars):
    """Return METAR reports containing hail."""

    pattern = r"(?<!\S)(?:\+|-|VC)?(?:TS|SH)?(?:GR|GS)(?!\S)"

    return [
        line for line in metars.splitlines()
        if re.search(pattern, line)
    ]


def main():
    parser = argparse.ArgumentParser(
        description="Check multiple airports for reported hail."
    )

    parser.add_argument(
        "--airports",
        default="airports.txt",
        help="File containing airport ICAO identifiers"
    )

    parser.add_argument(
        "--hours",
        type=int,
        default=24,
        help="Lookback period in hours (default: 24)"
    )

    args = parser.parse_args()

    airports = load_airports(args.airports)

    for airport in airports:
        try:
            metars = fetch_metars(airport, args.hours)
            hail_reports = check_hail(metars)

            if hail_reports:
                print(f"[ALERT] Hail reported at {airport}!")

                for report in hail_reports:
                    print(f"  {report}")

            else:
                print(f"[OK] No hail reported at {airport}.")

        except Exception as error:
            print(f"[ERROR] Failed to check {airport}: {error}")


if __name__ == "__main__":
    main()
