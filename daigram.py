import requests
from bs4 import BeautifulSoup


def parse_from_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    data = []

    rows = soup.find_all("tr")

    for row in rows[1:]:  # skip header
        cols = row.find_all("td")

        if len(cols) != 3:
            continue

        try:
            x = int(cols[0].get_text(strip=True))
            y = int(cols[2].get_text(strip=True))

            # 🔥 Important: handle character extraction
            char_cell = cols[1]

            char = char_cell.get_text(strip=True)

            # fallback if empty (sometimes happens)
            if not char:
                char = "█"   # default fallback (you can adjust)

            data.append((x, char, y))

        except Exception as e:
            continue

    return data


def build_grid(data):
    if not data:
        print("❌ No data parsed — parsing failed")
        return

    max_x = max(x for x, _, _ in data)
    max_y = max(y for _, _, y in data)

    grid = [[" " for _ in range(max_x + 1)] for _ in range(max_y + 1)]

    for x, char, y in data:
        grid[y][x] = char

    for y in range(max_y, -1, -1):
        print("".join(grid[y]))


def print_grid_from_url(url):
    data = parse_from_url(url)

    print("Parsed points:", len(data))  # debug

    build_grid(data)


# RUN
url = "https://docs.google.com/document/d/e/2PACX-1vSvM5gDlNvt7npYHhp_XfsJvuntUhq184By5xO_pA4b_gCWeXb6dM6ZxwN8rE6S4ghUsCj2VKR21oEP/pub"

print_grid_from_url(url)