import csv
import io
import zipfile
import requests

url = "https://www.ssa.gov/oact/babynames/names.zip"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

print("Downloading SSA baby names...")
response = requests.get(url, headers=headers)
zip_file = zipfile.ZipFile(io.BytesIO(response.content))

output_file = "ssa-baby-names.csv"
print(f"Extracting and compiling into {output_file}...")

with open(output_file, "w", newline="") as out:
    writer = csv.writer(out)
    writer.writerow(["year", "name", "sex", "count"])

    for file_name in sorted(zip_file.namelist()):
        if file_name.startswith("yob") and file_name.endswith(".txt"):
            year = int(file_name[3:7])
            with zip_file.open(file_name) as f:
                for line in io.TextIOWrapper(f, encoding="utf-8"):
                    parts = line.strip().split(",")
                    if len(parts) == 3:
                        writer.writerow([year, parts[0], parts[1], parts[2]])

print(f"Saved {output_file} successfully.")
