import os
import re

from flask import Blueprint, request, render_template, session, jsonify

from app.models import User, House
from utils.function import generateImageCode
from utils.setting import MEDIA_PATH

user = Blueprint('user', __name__)


@user.route('/verify/', methods=['GET','POST'])
def verify():
    if request.method == 'POST':
        code = generateImageCode()
        session['code'] = code
        return jsonify({'code': 200, 'msg': '验证成功', 'verify': code})


@user.route('/register/', methods=['GET'])
def register():
    if request.method == 'GET':
        return render_template('register.html')

@user.route('/register/', methods=['POST'])
def my_register():
    if request.method == 'POST':
        mobile = request.form.get('phone')
        imagecode = request.form.get('imagecode')
        password = request.form.get('password')
        password2 = request.form.get('password2')
        # 验证参数是否完整
        if not all([mobile, imagecode, password, password2]):
            return jsonify({'code': 7001, 'msg': '请把字段填写完整'})
        # 验证验证码是否一致
        if session['code'] != imagecode:
            return jsonify({'code': 7002, 'msg': '验证码不一致请重新填写'})
        # 验证手机号是否正确
        if not re.match(r'^1[3456789]\d{9}$', mobile):
            return jsonify({'code': 7003, 'msg': '该手机号无效'})
        # 验证密码是否一致
        if password != password2:
            return jsonify({'code': 7004, 'msg': '密码不一致'})
        # 验证手机号是否已经被注册
        if User.query.filter(User.phone == mobile).count():
            return jsonify({'code': 7005, 'msg': '该手机号已被注册'})
        # 该手机号如果不存在就添加到数据库
        user = User()
        user.phone = mobile
        user.password = password
        user.name = mobile
        user.save()
        return jsonify({'code': 200, 'msg': '请求成功'})


@user.route('/login/', methods=['GET'])
def login():
    return render_template('login.html')


@user.route('/login/', methods=['POST'])
def my_login():
    mobile = request.form.get('mobile')
    password = request.form.get('password')
    if not all([mobile, password]):
        return jsonify({'code': 7001, 'msg': '字段请填写完整'})
    # 验证手机号格式
    if not re.match(r'^1[3456789]\d{9}$', mobile):
        return jsonify({'code': 7002, 'msg': '该手机号格式错误'})
    # 获取登录账号是否注册
    user = User.query.filter(User.phone == mobile).first()
    if not user:
        return jsonify({'code': 7003, 'msg': '该手机号没有注册，请去注册!'})
    if not user.check_pwd(password):
        return jsonify({'code': 7004, 'msg': '账号或密码不正确!'})
    session['user_id'] = user.id
    return jsonify({'code': 200, 'msg': '成功'})


@user.route('/my/', methods=['GET'])
def my():
    if request.method == 'GET':
        return render_template('my.html')


@user.route('/user_info/', methods=['GET'])
def user_info():
    if request.method == 'GET':
        user_id = session['user_id']
        user = User.query.get(user_id)
        us = user.to_basic_dict()
        return jsonify({'code': 200, 'msg': '成功', 'user': us})


@user.route('/profile/', methods=['GET'])
def profile():
    if request.method == 'GET':
        return render_template('profile.html')


@user.route('/profile/', methods=['PATCH'])
def imy_profile():
    if request.method == 'PATCH':
        avatar = request.files.get('avatar')
        if avatar:
            # 判断图片格式是否正确
            if not re.match(r'image/*', avatar.mimetype):
                return jsonify({'code': 7001, 'msg': '请上传正确图片格式'})
            # 保存图片
            avatars = os.path.join(MEDIA_PATH, avatar.filename)
            avatar.save(avatars)
            # 修改图片字段
            user = User.query.get(session['user_id'])
            user.avatar = avatar.filename
            user.save()
            try:
                user.add_update()
                return jsonify(code=200, avatar=avatar)
            except:
                return jsonify({'code': 500, 'msg': '罩不住了'})


@user.route('/profile/', methods=['POST'])
def my_profile():
    name = request.form.get('name')
    if name:
        if User.query.filter(User.name==name).count():
            return jsonify({'code': 7002, 'msg': '名字重复无需更改'})
        user = User.query.get(session['user_id'])
        user.name = name
        try:
            user.add_update()
            return jsonify(code=200)
        except:
            return jsonify({'code': 7003, 'msg': '啊啊啊啊啊'})


@user.route('/auth/', methods=['GET'])
def auth():
    if request.method == 'GET':
        return render_template('auth.html')


@user.route('/auth/', methods=['POST'])
def my_auth():
    if request.method == 'POST':
        id_name = request.form.get('real_name')
        id_card = request.form.get('id_card')
        if not all([id_name, id_card]):
            return jsonify({'code': 7001, 'msg': '请把字段填写完整'})
        if not re.match(r'[1-9]\d{5}(18|19|([23]\d))\d{2}((0[1-9])|(10|11|12))(([0-2][1-9])|10|20|30|31)\d{3}[0-9Xx]$', id_card):
            return jsonify({'code': 7002, 'msg': '身份证格式错误'})
        if not re.match(r'[\u4E00-\u9FA5A-Za-z]+$', id_name):
            return jsonify({'code': 7003, 'msg': '该姓名无效'})
        user_id = session['user_id']
        user = User.query.filter(User.id==user_id).first()
        user.id_card = id_card
        user.id_name = id_name
        user.save()
        return jsonify({'code': 200, 'msg': '成功'})


@user.route('/user_auth/', methods=['GET'])
def user_auth():
    if request.method == 'GET':
        user_id = session['user_id']
        user = User.query.filter(User.id == user_id).first()
        user_card = user.to_auth_dict()
        return jsonify({'code': 200, 'msg': '成功', 'user': user_card})

