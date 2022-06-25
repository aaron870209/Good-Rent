from flask import Flask, render_template, request, redirect, send_file,send_from_directory
from MySQL import MySQL
import json
app = Flask(__name__)


@app.route("/")
def home_page(paging=0):
    data = []
    paging = int(request.args.get("paging",paging))
    for house in MySQL.get_all_info_from_house(paging):
        data_dict = {"id":house["house_id"],"title":house["title"],"price":house["price"],"address":house["address"],"img":house["img"],
                "size":house["size"],"floor":house["floor"]+"F","longitude":house["longitude"],"latitude":house["latitude"],
                "city":house["city"],"type":house["house_type"],"paging":paging}
        data.append(data_dict)
    return render_template("home_page.html",data=data)


@app.route("/search", methods=['POST'])
def search_page():
    tag = json.loads(request.data)
    print(tag)
    data = MySQL.search_house(tag["data"])
    dict = {"data": data}
    return dict


@app.route("/detail", methods=["GET"])
def detail_page():
    id = request.args.get('id')
    detail = MySQL.get_house_detail_by_id(int(id))
    return render_template("main_page.html",detail=detail)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000)