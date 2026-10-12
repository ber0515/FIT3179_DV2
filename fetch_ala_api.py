import requests
import csv
import os
import urllib.parse

OUT_DIR = "data"
os.makedirs(OUT_DIR, exist_ok=True)

BASE = "https://api.ala.org.au/occurrences/occurrences/facets"

SPECIES = [
    "Macropus giganteus",
    "Phascolarctos cinereus",
    "Vombatus ursinus",
    "Cacatua galerita",
    "Gymnorhina tibicen",
    "Malurus cyaneus",
    "Tiliqua scincoides",
    "Varanus varius",
    "Pseudonaja textilis",
    "Crinia signifera",
    "Ranoidea caerulea",
    "Limnodynastes peronii"
]

GROUPS = {
    "Macropus giganteus": "Mammal",
    "Phascolarctos cinereus": "Mammal",
    "Vombatus ursinus": "Mammal",
    "Cacatua galerita": "Bird",
    "Gymnorhina tibicen": "Bird",
    "Malurus cyaneus": "Bird",
    "Tiliqua scincoides": "Reptile",
    "Varanus varius": "Reptile",
    "Pseudonaja textilis": "Reptile",
    "Crinia signifera": "Amphibian",
    "Ranoidea caerulea": "Amphibian",
    "Limnodynastes peronii": "Amphibian"
}

COMMON = {
    "Macropus giganteus": "Eastern Grey Kangaroo",
    "Phascolarctos cinereus": "Koala",
    "Vombatus ursinus": "Common Wombat",
    "Cacatua galerita": "Sulphur-crested Cockatoo",
    "Gymnorhina tibicen": "Australian Magpie",
    "Malurus cyaneus": "Superb Fairy-wren",
    "Tiliqua scincoides": "Eastern Blue-tongued Lizard",
    "Varanus varius": "Lace Monitor",
    "Pseudonaja textilis": "Eastern Brown Snake",
    "Crinia signifera": "Common Eastern Froglet",
    "Ranoidea caerulea": "Green Tree Frog",
    "Limnodynastes peronii": "Striped Marsh Frog"
}

DATE_FILTER = '(year:"2021" OR year:"2022" OR year:"2023" OR year:"2024" OR year:"2025")'
COUNTRY_FILTER = 'country:"Australia"'
BASIS_FILTER = 'basis_of_record:"HUMAN_OBSERVATION"'


def get_facet(species, facet, limit=1000):
    params = {
        "fq": [
            DATE_FILTER,
            COUNTRY_FILTER,
            BASIS_FILTER,
            f'scientificName:"{species}"'
        ],
        "qualityProfile": "ALA",
        "facets": facet,
        "fsort": "count",
        "flimit": limit
    }

    r = requests.get(BASE, params=params, timeout=60)
    r.raise_for_status()

    data = r.json()

    if not data:
        return []

    return data[0].get("fieldResult", [])


# 1. species totals
species_rows = []

for sp in SPECIES:
    # use year facet and sum all years
    rows = get_facet(sp, "year", 100)
    total = sum(x.get("count", 0) for x in rows)

    species_rows.append([
        sp,
        COMMON[sp],
        GROUPS[sp],
        total
    ])

with open(f"{OUT_DIR}/observations_by_species.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["scientific_name", "common_name", "group", "observations"])
    w.writerows(species_rows)


# 2. state x group
state_group_counts = {}

for sp in SPECIES:
    rows = get_facet(sp, "stateProvince", 100)

    for x in rows:
        state = x.get("label", "")
        count = x.get("count", 0)

        key = (state, GROUPS[sp])

        state_group_counts[key] = state_group_counts.get(key, 0) + count

with open(f"{OUT_DIR}/state_group_counts.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["state", "group", "observations"])

    for (state, group), count in sorted(state_group_counts.items()):
        w.writerow([state, group, count])


# 3. state totals
state_totals = {}

for (state, group), count in state_group_counts.items():
    state_totals[state] = state_totals.get(state, 0) + count

with open(f"{OUT_DIR}/observations_by_state.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["state", "observations"])

    for state, count in sorted(state_totals.items()):
        w.writerow([state, count])


# 4. month x group
month_group_counts = {}

for sp in SPECIES:
    rows = get_facet(sp, "month", 100)

    for x in rows:
        month = x.get("label", "")
        count = x.get("count", 0)

        key = (month, GROUPS[sp])

        month_group_counts[key] = month_group_counts.get(key, 0) + count

with open(f"{OUT_DIR}/month_group_counts.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["month", "group", "observations"])

    for (month, group), count in sorted(month_group_counts.items()):
        w.writerow([month, group, count])


# 5. year x species
with open(f"{OUT_DIR}/year_species_counts.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["year", "common_name", "group", "observations"])

    for sp in SPECIES:
        rows = get_facet(sp, "year", 100)

        for x in rows:
            year = x.get("label", "")
            count = x.get("count", 0)

            if year in {"2021", "2022", "2023", "2024", "2025"}:
                w.writerow([
                    year,
                    COMMON[sp],
                    GROUPS[sp],
                    count
                ])


# 6. group totals
group_totals = {}

for _, _, group, total in species_rows:
    group_totals[group] = group_totals.get(group, 0) + total

with open(f"{OUT_DIR}/observations_by_group.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["group", "observations"])

    for group, count in sorted(group_totals.items()):
        w.writerow([group, count])


print("Done.")