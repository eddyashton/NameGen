#!/usr/bin/env python3

import httpx
from bs4 import BeautifulSoup

base_url = "https://www.townscountiespostcodes.co.uk/towns-in-uk/letter"

names = []
for letter in [chr(i) for i in range(ord("a"), ord("z") + 1)]:
    url = f"{base_url}/{letter}"
    print(f"Fetching {url}")

    response = httpx.get(url, follow_redirects=True)
    if response.status_code != 200:
        print(f"Error fetching page: {response}")
        continue

    print("Fetched!")

    soup = BeautifulSoup(response.content, "html.parser")
    table_body = soup.find_all("tbody")
    assert len(table_body) == 1

    rows = table_body[0].find_all("tr")

    print(f"Found ~{len(rows)} names")

    for row in rows:
        if row.get("class") == ["dummy"]:
            continue

        count, name, county, country = row.find_all("td")

        # Some names contain spellings in 2 languages - add them separately
        if " (" in name.text:
            a, b = name.text.split(" (")
            names.append(a)
            names.append(b.rstrip(")"))
        else:
            names.append(name.text)

path = "data/towns"
with open(path, "w") as f:
    for name in names:
        f.write(f"{name}\n")

print(f"Wrote {len(names)} names to {path}")
