## Usage

### How-To

Folder structure:
```
project_folder
|   stockpile.png
|___Data
    |___1920x1080
        |   Numbers
        |   |   +.png
        |   |   0.png
        |   |   1.png
        |   |___...
        |___Icons
            |   .44 (Crate).png
            |   .44.png
            |   ...
```

```
\project_folder> pip install foxhole-sheets
\project_folder> python -m sheets
```

json will be output into stockpile.json

### Example
**stockpile.png**

![stockpile image](https://github.com/miles-igd/foxhole_sheets/blob/master/stockpile.png "Stockpile")

`python -m sheets`

**stockpile.json**
```json
{
    "12.7mm": "16",
    "120mm": "19",
    "20mm": "113",
    "40mm": "203",
    "68mm": "20",
    "7.62mm": "359",
    "7.92mm": "548",
    "8.5mm": "1",
    "9mm SMG": "118",
    "A.T.R.P.G. Shell": "51",
    "Abisme AT-99": "8",
    "Anti-Tank Sticky Bomb": "20",
    "Argenti r.II Rifle": "126",
    "Bandages": "79",
    "Barbed Wire": "1",
    "Basic Materials": "1k+",
    "Bayonet": "57",
    "Binoculars": "8",
    "Blood Plasma": "76",
    "Bomastone Grenade": "88",
    "Bunker Supplies": "500",
    "Colonial Engineer Uniform": "35",
    "Colonial Grenade Uniform": "20",
    "Colonial Medic Uniform": "160",
    "Colonial Rain Uniform": "39",
    "Colonial Recon Uniform": "53",
    "Colonial Snow Uniform": "174",
    "Colonial Soldier Uniform": "323",
    "Cometa T2-9": "7",
    "Cutler Launcher 4": "1",
    "Daucus isg.III": "13",
    "Diesel": "5",
    "First Aid Kit": "58",
    "Garrison Supplies": "1k+",
    "Gas Mask": "54",
    "Gas Mask Filter": "94",
    "Green Ash Grenade": "67",
    "KRN886-127 Gast Machine Gun": "10",
    "KRR3-792 Auger": "8",
    "Lionclaw mc.VIII": "98",
    "Mammon 91-b": "81",
    "Mortar Shell (Flare)": "75",
    "Mortar Shell (HE)": "45",
    "Mortar Shell (Shrapnel)": "75",
    "Radio": "36",
    "Radio Backpack": "8",
    "Refined Materials": "11",
    "Shovel": "50",
    "Sledgehammer": "19",
    "Soldier Supplies": "118",
    "Trauma Kit": "14",
    "Volta r.I Repeater": "22",
    "Wreckage": "7",
    "Wrench": "18"
}
```
