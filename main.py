import requests
from fake_useragent import UserAgent
import json

ua = UserAgent()


def collect_data(pages, catalog_type=2):
   #minPrice = int(input())
   #maxPrice = int(input())
    offset = 0
    result = []
    count = 0

    for _ in range(pages):
        URL = f'https://inventories.cs.money/5.0/load_bots_inventory/730?buyBonus=40&isStore=true&limit=60&maxPrice=10000&minPrice=1&offset={offset}&type={catalog_type}&withStack=true'
        r = requests.get(URL, headers={'user-agent': f'{ua.random}'})

        offset += 60

        data = r.json()
        items = data.get('items')

        for item in items:
            if item.get('overprice') is not None:
                result.append(
                    {
                        'full_name': item.get('fullName'),
                        '3d': item.get('3d'),
                        'float': item.get('float'),
                        'price': item.get('price'),
                        'overprice': item.get('overprice')
                    }
                )

        if len(items) < 60:
            break

        count += 1
        print(f'[+] Proccessed: Page #{count}')

    with open('result.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=4, ensure_ascii=False)
    print('[INFO] Data successfully dumped!')


def main():
    collect_data()


if __name__ == '__main__':
    main()
