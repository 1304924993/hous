import os

from flask import Blueprint, request, render_template, session, jsonify

from app.models import User, House, Facility, HouseImage, Area
from utils.setting import MEDIA_PATH

hous = Blueprint('hous', __name__)


@hous.route('/index/', methods=['GET'])
def index():
    if request.method == 'GET':
        return render_template('index.html')


@hous.route('/indexs/', methods=['GET'])
def indexs():
    if request.method == 'GET':
        user_id = session.get('user_id')
        if user_id:
            user = User.query.get(user_id)
            username = user.name
        else:
            username = ''
        houses = House.query.filter(House.index_image_url != '')
        houses_image = [house.to_dict() for house in houses]
        return jsonify({'code': 200, 'msg': '成功', 'username': username, 'house': houses_image})


@hous.route('/myhouse/', methods=['GET'])
def myhouse():
    return render_template('myhouse.html')


@hous.route('/myhous/', methods=['GET'])
def myhous():
    user_id = session['user_id']
    user = User.query.filter(User.id == user_id).first()
    us = user.to_auth_dict()
    return jsonify({'code': 200, 'msg': '成功', 'auth': us})


@hous.route('/newhouse/', methods=['GET'])
def newhouse():
    return render_template('newhouse.html')


@hous.route('/newhouse/', methods=['POST'])
def my_newhouse():
    if request.method == 'POST':
        house = House()
        house.user_id = session['user_id']
        house.title = request.form.get('title')
        house.price = request.form.get('price')
        house.area_id = request.form.get('area_id')
        house.address = request.form.get('address')
        house.room_count = request.form.get('room_count')
        house.acreage = request.form.get('acreage')
        house.unit = request.form.get('unit')
        house.capacity = request.form.get('capacity')
        house.beds = request.form.get('beds')
        house.deposit = request.form.get('deposit')
        house.min_days = request.form.get('min_days')
        house.max_days = request.form.get('max_days')
        facilitys = request.form.getlist('facility')
        for facility_id in facilitys:
            facility = Facility.query.get(facility_id)
            house.facilities.append(facility)
        house.add_update()
        return jsonify({'code': 200, 'house_id': house.id})


@hous.route('/hous_img/', methods=['PATCH'])
def hous_img():
    if request.method == 'PATCH':
        house_id = request.form.get('house_id')
        img = request.files.get('house_image')
        save_url = os.path.join(MEDIA_PATH, img.filename)
        img.save(save_url)
        # 保存房屋和图片信息
        house_image = HouseImage()
        house_image.house_id = house_id
        image_url = os.path.join(img.filename)
        house_image.url = image_url
        house_image.add_update()
        # 创建房屋首图
        house = House.query.get(house_id)
        if not house.index_image_url:
            house.index_image_url = image_url
            house.add_update()
        return jsonify({'code': 200, 'image_url': image_url})


@hous.route('/facility/', methods=['GET'])
def facility():
    # 获取城区信息
    areas = Area.query.all()
    # 获取设施信息
    facilitys = Facility.query.all()
    # 遍历出城区所对应的区域id和区域name
    areas_json = [area.to_dict() for area in areas]
    # 遍历出设施信息所对应的 设施编号id 和 设施名字name 设施展示的图标css
    facilitys_json = [facility.to_dict() for facility in facilitys]
    return jsonify({'code': 200, 'areas': areas_json, 'facilitys': facilitys_json})


@hous.route('/user_house/', methods=['GET'])
def user_house():
    houses = House.query.filter(House.user_id == session['user_id']).all()
    houses_list = [house.to_dict() for house in houses]
    return jsonify({'code': 200, 'houses_list': houses_list})


@hous.route('/detail/', methods=['GET'])
def detail():
    return render_template('detail.html')


@hous.route('/hou_detail/<int:id>/', methods=['GET'])
def hou_detail(id):
    houses = House.query.get(id)
    house = houses.to_full_dict()
    return jsonify({'code': 200, 'house': house})















