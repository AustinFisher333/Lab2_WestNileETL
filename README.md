# West Nile Virus Outbreak - Final Project

This project identifies Boulder-area addresses at risk for West Nile Virus transmission and prepares safe pesticide spraying zones.

## Files

- `finalproject.py`: Sets spatial reference and creates `final_analysis` via Erase.
- `spatial_join_and_query.py`: Joins addresses with spray zones and filters them using a definition query.
- `export_target_addresses.py`: Exports filtered addresses to CSV (Extra Credit).

## Requirements

- ArcGIS Pro with arcpy environment
- Open `.aprx` project before running scripts via Python window

## How to Run

1. Open ArcGIS Pro project `WestNileOutbreak.aprx`
2. Use ArcGIS Python window to run scripts like:

```python
exec(open(r"path\to\finalproject.py", encoding="utf-8").read())
