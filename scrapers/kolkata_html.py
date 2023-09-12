import requests


def download_page(number: int):
    """Download a page of judgements from the Kolkata regional bench of the Indian armed forces tribunal."""
    url = f"https://aftkolkata.nic.in/judgements/index/page:{number}"

    # Download the page and save to web_pages/kolkata/{number}.html, skip SSL verification
    response = requests.get(url, verify=False)
    with open(f"web_pages/kolkata/{number}.html", 'wb') as f:
        f.write(response.content)


def main():
    # Download the first 14 pages of judgements
    for i in range(1, 15):
        download_page(i)


if __name__ == '__main__':
    main()
