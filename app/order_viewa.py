from datetime import datetime

from flask import Blueprint, render_template, request, session, jsonify, render_template_string

from app.models import House, Order

order = Blueprint('order', __name__)


@order.route('/booking/', methods=['GET'])
def booking():
    return render_template('booking.html')


@order.route('/my_order/', methods=['POST'])
def my_order():
    house_id = request.form.get('house_id')
    begin_date = datetime.strptime(request.form.get('begin_date'), '%Y-%m-%d')
    end_date = datetime.strptime(request.form.get('end_date'), '%Y-%m-%d')
    house = House.query.get(house_id)
    order = Order()
    order.user_id = session['user_id']
    order.house_id = house_id
    order.begin_date = begin_date
    order.end_date = end_date
    order.days = (end_date - begin_date).days + 1
    order.house_price = house.price
    order.amount = order.days * order.house_price
    order.add_update()
    return jsonify({'code': 200, 'msg': '成功'})


@order.route('/orders/', methods=['GET'])
def orders():
    order = ''
    return render_template('orders.html', order=order)


@order.route('/user_order/', methods=['GET'])
def user_order():
    orders = Order.query.filter(Order.user_id == session['user_id']).all()
    order = [order.to_dict() for order in orders]
    return jsonify({'code': 200, 'order': order})


@order.route('/lorders/', methods=['GET'])
def lorders():
    return render_template('lorders.html')


@order.route('/my_lorders/', methods=['GET'])
def my_lorders():
    # 获取登录的session[user_id]
    user_id = session['user_id']
    houses = House.query.filter(House.user_id==user_id)
    houses_ids = [house.id for house in houses]

    orders = Order.query.filter(Order.house_id.in_(houses_ids))
    orders_list = [order.to_dict() for order in orders]
    return jsonify(code=200, order=orders_list)


@order.route('/orders/<int:id>/',methods=['PUT'])
def status(id):
    # 接收订单参数
    status = request.form.get('status')
    # 查找订单对象
    order = Order.query.get(id)
    # 修改
    order.status = status
    # 如果是拒单，需要添加原因
    if status == 'REJECTED':
        order.comment = request.form.get('comment')
    # 保存
    try:
        order.add_update()
    except:
        return jsonify({'code': 401, 'msg': '数据库错误'})
    return jsonify({'code': 200})















