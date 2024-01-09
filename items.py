import requests

class Items:
    def __init__(self, API_KEY):
        """
        Init of Items data
        """
        self.items = None
        self.items_data = {}
        self.None_info = {
            'name': 'None',
            'avg': 'N/A',
            'avg_per_slot': 'N/A',
            'trader': 'N/A'
        }
        self.API_KEY = API_KEY
        self.update_data()

    def req(self):
        headers = {
            'x-api-key': self.API_KEY,
            'Content-Type': 'application/json',
        }
        response = requests.get(
            'https://api.tarkov-market.app/api/v1/items/all?sort=price&sort_direction=desc&lang=eng', headers=headers)

        print(f'Response: {response.status_code}')
        response = response.json()

        for row in response:
            self.items_data[row['name']] = {
                'name': row['name'],
                'avg': row['avg24hPrice'],
                'avg_per_slot': int(round(int(row['avg24hPrice']) / int(row['slots']), 0)),
                'trader': row['traderPrice']
            }


    def find(self, item_hash):
        """
        Method will return item_hash and item_state
        """

        item_data = None
        if item_hash:
            if item_hash in self.items_data:
                item_data = self.items_data[item_hash]

            if not item_data:
                name = item_hash[1:][:-1]
                for items in self.items_data:
                    if name in items:
                        item_data = self.items_data[items]


            if item_data:
                return item_data, True, True

            else:
                print(f'{item_hash} not found')
                return self.None_info, False, True

        else:
            return self.None_info, False, False

    def update_data(self):
        """
        Method will get data from google spreadsheets
        """
        self.req()
        print(f'Loaded: {len(self.items_data)} items')
        print("Data loaded\n")
