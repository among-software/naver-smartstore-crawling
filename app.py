import json

from flask import Flask, request
from pymongo import MongoClient
from pymongo.server_api import ServerApi
import requests

app = Flask(__name__)

client = MongoClient("mongodb+srv://among_tech:tech!234@among-service.1cjhf.mongodb.net/?retryWrites=true&w=majority",
                     server_api=ServerApi('1'))
db = client.test


@app.route('/')
def home():
    query = request.args.get('query')

    if query:
        product_list = []
        product_dict = {}

        url = f"https://search.shopping.naver.com/api/search/all?frm=NVSHCHK&origQuery={query}&pagingIndex=1&pagingSize=80&productSet=checkout&query={query}&sort=rel&timestamp=&viewType=list"
        r = requests.get(url)
        json_str = json.loads(json.dumps(r.json()))
        val1 = json_str['shoppingResult']["products"]
        for idx, val in enumerate(val1):
            product_name = val["productName"]
            origin_price = val['price']
            # low_price = val["lowPrice"]
            # rank = val["rank"]
            mall_name = val["mallName"]
            category = val["category2Name"], ">", val["category3Name"], ">", val["category4Name"]

            product_dict["상품명"] = product_name
            product_dict["가격"] = origin_price
            # product_dict["세일된가격"] = low_price
            product_dict["판매처"] = mall_name
            product_dict["카테고리"] = category
            product_list.append(product_dict.copy())

        print(product_list)
        return '''<h1>successfully search</h1>'''
    else:
        return '''<h1>no value</h1>'''


if __name__ == '__main__':
    app.run(debug=True)
