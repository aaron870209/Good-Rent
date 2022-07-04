from flask import Flask, render_template, request, redirect, send_file,send_from_directory
from MySQL import MySQL
import folium
import json
app = Flask(__name__)


@app.route("/")
def home_page(paging=0,tag=0):
    data = []
    paging = int(request.args.get("paging",paging))
    tag = int(request.args.get("tag",tag))
    if tag == 0:
        for house in MySQL.get_all_info_from_house(paging):
            data_dict = {"id":house["house_id"],"title":house["title"],"price":house["price"],"address":house["address"],"img":house["img"],
                    "size":house["size"],"floor":house["floor"]+"F","longitude":house["longitude"],"latitude":house["latitude"],
                    "city":house["city"],"type":house["house_type"],"paging":paging,"tag":tag}
            data.append(data_dict)
        return render_template("home_page.html",data=data)
    else:
        for house in MySQL.get_filter_info_from_house(paging,tag):
            data_dict = {"id": house["house_id"], "title": house["title"], "price": house["price"],
                         "address": house["address"], "img": house["img"],
                         "size": house["size"], "floor": house["floor"] + "F", "longitude": house["longitude"],
                         "latitude": house["latitude"],
                         "city": house["city"], "type": house["house_type"], "paging": paging, "tag": tag}
            data.append(data_dict)
        return render_template("home_page.html", data=data)


@app.route("/search", methods=['POST'])
def search_page():
    tag = json.loads(request.data)
    print(tag)
    data = MySQL.search_house(tag["data"], tag["page"])
    dict = {"data": data, "page": tag["page"]}
    return dict


@app.route("/detail", methods=["GET"])
def detail_page():
    id = request.args.get('id')
    detail = MySQL.get_house_detail_by_id(int(id))
    truck_position = MySQL.get_truck_house_distance(id)
    print(truck_position)
    truck_position_list = []
    print(truck_position_list)
    m = folium.Map(location=[detail["latitude"],detail["longitude"]],zoom_start=16)
    print(detail["title"])
    iframe = folium.IFrame(f'<b>{detail["title"]}</b>')
    popup = folium.Popup(iframe, min_width=300,max_width=300,min_height=40,max_height=80)
    m.add_child(folium.Marker(location=[detail["latitude"],detail["longitude"]],popup=popup,
                              icon=folium.Icon(icon='home',color='green')))
    for truck in truck_position:
        truck_id = truck["truck_spot_id"]
        position = MySQL.get_truck_lon_lat_by_id(truck_id)
        longitude = position["longitude"]
        latitude = position["latitude"]
        list = [latitude,longitude]
        m.add_child(folium.Marker(location=list, opacity=0.8,
                                  icon=folium.Icon(icon='truck', color='blue', prefix='fa')))
    m = m._repr_html_()
    return render_template("main_page.html", detail=detail, map=m)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000)