from scrapingbee import ScrapingBeeClient


def main():
    client = ScrapingBeeClient(
        api_key='E1PJA1D78TBTM320Z8O9XS2MTWHTCL1NSJXGFKIZO6TJB4XIM94OSR6KQNU415QB97MYJEP6T3O0IWR3')

    response = client.get(
        'https://indiankanoon.org/search/?formInput=army%20deaths&pagenum=2',
        params={
            'render_js': 'True',
            'premium_proxy': 'True',
        }
    )

    print('Response HTTP Status Code: ', response.status_code)
    print('Response HTTP Response Body: ', response.content)

    # Save the response to a file
    with open('../response.html', 'wb') as f:
        f.write(response.content)


if __name__ == '__main__':
    main()
