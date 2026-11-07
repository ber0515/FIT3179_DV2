import galah
import pandas as pd

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

galah.galah_config(
    atlas="Australia",
    email="berniceloojieyi@gmail.com",
)

all_rows = []

for species in SPECIES:

    print("Fetching:", species)

    try:
        df = galah.atlas_occurrences(
            taxa=species,
            filters=[
                "year>=2021",
                "year<=2025",
                "country=Australia",
                "basisOfRecord=HUMAN_OBSERVATION"
            ],
            fields="basic",
            use_data_profile=True
        )

    except Exception as e:
        print("Failed:", species, e)
        continue

    if df is None or df.empty:
        print("No records:", species)
        continue

    print("Returned:", len(df))

    df = df.dropna(
        subset=[
            "decimalLatitude",
            "decimalLongitude"
        ]
    )

    df["decimalLatitude"] = pd.to_numeric(
        df["decimalLatitude"],
        errors="coerce"
    )

    df["decimalLongitude"] = pd.to_numeric(
        df["decimalLongitude"],
        errors="coerce"
    )

    df = df.dropna(
        subset=[
            "decimalLatitude",
            "decimalLongitude"
        ]
    )

    df = df[
        (df["decimalLatitude"] >= -44) &
        (df["decimalLatitude"] <= -10) &
        (df["decimalLongitude"] >= 112) &
        (df["decimalLongitude"] <= 154)
    ]

    if len(df) > 120:
        df = df.sample(
            n=120,
            random_state=3179
        )

    df["common_name"] = COMMON[species]
    df["group"] = GROUPS[species]

    all_rows.append(
        df[
            [
                "common_name",
                "group",
                "decimalLatitude",
                "decimalLongitude"
            ]
        ]
    )

if all_rows:

    result = pd.concat(
        all_rows,
        ignore_index=True
    )

    result = result.rename(
        columns={
            "decimalLatitude": "latitude",
            "decimalLongitude": "longitude"
        }
    )

    result.to_csv(
        "data/observation_points.csv",
        index=False
    )

    print()
    print("DONE")
    print("Rows:", len(result))
    print("Created: data/observation_points.csv")

else:
    print("No records returned.")