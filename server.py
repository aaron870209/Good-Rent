from flask import Flask, render_template, request, redirect, send_file,send_from_directory
from pymysql import ProgrammingError

from MySQL import MySQL
import folium
import json
from dotenv import load_dotenv
import os
load_dotenv()
app = Flask(__name__)


@app.route("/")
def home_page(paging=0,tag=0):
    data = []
    try:
        paging = int(request.args.get("paging",paging))
        tag = int(request.args.get("tag",tag))
        if tag == 0:
            house_list,total = MySQL.get_all_info_from_house(paging)
            total = total["count(*)"]
            limit_page = int(total/15)
            if paging > limit_page:
                return render_template("404.html")
            else:
                for house in house_list:
                    data_dict = {"id":house["house_id"],"title":house["title"],"price":house["price"],"address":house["address"],"img":house["img"],
                            "size":house["size"],"floor":house["floor"]+"F","longitude":house["longitude"],"latitude":house["latitude"],
                            "city":house["city"],"type":house["house_type"],"paging":paging,"tag":tag}
                    data.append(data_dict)
                return render_template("home_page.html", data=data, total=total)
        elif tag == 1 or tag == 2 or tag == 3:
            house_list,total = MySQL.get_filter_info_from_house(paging,tag)
            total = total["count(*)"]
            limit_page = int(total / 15)
            if paging > limit_page:
                return render_template("404.html")
            else:
                for house in house_list:
                    data_dict = {"id": house["house_id"], "title": house["title"], "price": house["price"],
                                 "address": house["address"], "img": house["img"],
                                 "size": house["size"], "floor": house["floor"] + "F", "longitude": house["longitude"],
                                 "latitude": house["latitude"],
                                 "city": house["city"], "type": house["house_type"], "paging": paging, "tag": tag}
                    data.append(data_dict)
                return render_template("home_page.html", data=data,total=total)
        else:
            return render_template("404.html")
    except ValueError:
        return render_template("404.html")


@app.route("/search", methods=['POST'])
def search_page():
    tag = json.loads(request.data)
    print(tag)
    data,total = MySQL.search_house(tag["data"], tag["page"])
    total = total["count(*)"]
    dict = {"data": data, "page": tag["page"],"total":total}
    return dict


@app.route("/detail", methods=["GET"])
def detail_page():
    id = request.args.get('id')
    print(id)
    if id == None:
        return render_template('404.html')
    else:
        try:
            detail = MySQL.get_house_detail_by_id(int(id))
            truck_position = MySQL.get_truck_house_distance(id)
            school_position = MySQL.get_school_house_distance(id)
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
            print(detail["house_type"])
            if detail["house_type"] == "整層住家":
                show_school = True
            else:
                show_school = False
            feature_group = folium.FeatureGroup(name='學校', show=show_school)
            for school in school_position:
                school_id = school["school_id"]
                position =MySQL.get_school_lon_lat_by_id(school_id)
                longitude = position["longitude"]
                latitude = position["latitude"]
                list = [latitude, longitude]
                iframe = folium.IFrame(f'<b>{position["name"]}</b>')
                popup = folium.Popup(iframe, min_width=300, max_width=300, min_height=40, max_height=80)
                folium.Marker(location=list, opacity=0.8,popup=popup,
                              icon=folium.Icon(icon='graduation-cap', color='red', prefix='fa')).add_to(feature_group)
            feature_group.add_to(m)
            folium.LayerControl().add_to(m)
            m = m._repr_html_()
            if "電梯" in detail["tag"]:
                elevator = "有"
            else:
                elevator = "無"
            return render_template("main_page.html", detail=detail, map=m, elevator=elevator)
        except TypeError:
            return render_template("404.html")
        except ValueError:
            return render_template("404.html")

@app.route('/admin_monitor')
def log_in():
    return render_template('login.html')


@app.route('/admin_dashboard',methods=['GET','POST'])
def dashboard():
    email = request.form.get("email")
    password = request.form.get("password")
    try:
        result_email,result_password = MySQL.login(email)
        if email == result_email and password == result_password:
            return render_template("dashboard.html")
        else:
            return render_template("login.html",wrong=1)
    except TypeError:
        return render_template("login.html", wrong=1)
    except ProgrammingError:
        return render_template("login.html", wrong=2)


@app.route('/dashboard_data',methods=["POST"])
def monitor_data():
    new_data = []
    date = []
    Taipei_591_list = []
    New_Taipei_591_list = []
    Taipei_lewu_list = []
    New_Taipei_lewu_list = []
    for data in MySQL.get_monitor_data():
        if data["new_data_count"] == None:
            count = 0
            new_data.append(count)
        else:
            count = data["new_data_count"]
            new_data.append(count)
        day = data["date"]
        date.append(day)
        Taipei_591 = data["mongo_data_count_591_Taipei"]
        New_Taipei_591 = data["mongo_data_count_591_NewTaipei"]
        Taipei_lewu = data["mongo_data_count_lewu_Taipei"]
        New_Taipei_lewu = data["mongo_data_count_lewu_NewTaipei"]
        Taipei_591_list.append(Taipei_591)
        New_Taipei_591_list.append(New_Taipei_591)
        Taipei_lewu_list.append(Taipei_lewu)
        New_Taipei_lewu_list.append(New_Taipei_lewu)
    dict = {"new_data":new_data,"date":date,"Taipei_591":Taipei_591_list,"New_Taipei_591":New_Taipei_591_list,
            "Taipei_lewu":Taipei_lewu_list,"New_Taipei_lewu":New_Taipei_lewu_list}
    return dict


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000)


