#!/usr/bin/env python
# -*- coding: utf-8 -*-
# by vellhe 2017/7/9
from flask import Flask, request
import os
import datetime
import pymysql
import json

app = Flask(__name__)
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8' 

@app.route("/")
def home():
   return "Jaron"

@app.route('/Seller/Create', methods=['POST'])
def SellerCreate():
	  order_name = request.form.get('OrderName')
	  order_size = request.form.get('OrderSize')
	  order_count = request.form.get('OrderCount')
	  order_desc = request.form.get('OrderDesc')
	  order_total= request.form.get('OrderTotal')
	  order_percent = request.form.get('OrderPercent')
	  order_deposit = request.form.get('OrderDeposit')
	  order_balance = request.form.get('OrderBalance')
	  buyer_name = request.form.get('BuyerName')
	  sql="select user_id from tb_user where user_name=%s"
	  data =(buyer_name)
	  buyer_id = getOneData(sql,data)
	  product_time = request.form.get('ProductTime')
	  data = (buyer_id,1002,115,order_name,order_size,order_desc,order_count,order_total,order_percent,60,order_deposit,order_balance,product_time)
	  sql = "INSERT INTO tb_order ( buyer_id,sell_id,order_status_id,order_name,order_size,order_desc,order_count,order_total,order_percent_id,order_fee,order_deposit,order_balance,product_time) VALUES  (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
	  str_result = EditData(sql,data)
	  return str_result

@app.route('/Buyer/PayDeposit', methods=['POST'])
def BuyerPayDeposit():
	  orderId = request.form.get('orderId')
	  payType = request.form.get('payType')
	  cargoType = request.form.get('cargoType')
	  cargoTime = request.form.get('cargoTime')
	  bank= request.form.get('bank')
	  accountNum = request.form.get('accountNum')
	  data = (117,payType,cargoType,cargoTime,bank,accountNum,'頭款',orderId)
	  sql = "update tb_order set order_status_id=%s,order_pay_type =%s ,cargo_type =%s ,cargo_time = %s,order_bank=%s,order_account_num=%s,deposit_detail=%s where order_id=%s"

	  str_result = EditData(sql,data)
	  return str_result

@app.route('/Buyer/PayBalance', methods=['POST'])
def BuyerPayBalance():
	  orderId = request.form.get('orderId')
	  data = (120,'尾款＋運費',orderId)
	  sql = "update tb_order set order_status_id=%s,balance_detail=%s where order_id=%s"

	  str_result = EditData(sql,data)
	  return str_result

@app.route('/Seller/Finish', methods=['POST'])
def SellerFinish():
	  orderId = request.form.get('orderId')
	  cargoCompany = request.form.get('cargoCompany')
	  cargoId = request.form.get('cargoId')
	  data = (122,cargoCompany,cargoId,orderId)
	  sql = "update tb_order set order_status_id=%s,cargo_company=%s,cargo_id=%s where order_id=%s"

	  str_result = EditData(sql,data)
	  return str_result

@app.route('/All/SetStatus', methods=['POST'])
def AllSetStatus():
	  orderId = request.form.get('orderId')
	  statusId = request.form.get('statusId')
	  data = (statusId,orderId)
	  sql = "update tb_order set order_status_id=%s where order_id=%s"

	  str_result = EditData(sql,data)
	  return str_result


@app.route('/Buyer/GetList', methods=['POST'])
def BuyerGetList():
  statusId = request.form.get('statusId')
  sql = "SELECT o.order_id as \'OrderId\', o.order_name as \'OrderName\',s.status_name as \'StatusName\' FROM  tb_order o INNER JOIN v_status s ON o.order_status_id = s.status_id where o.order_status_id= \'" + statusId + "\'"
  str_result = getData(sql)
  return str_result

@app.route('/Buyer/GetWaiDeposit', methods=['POST'])
def BuyerGetWaiDeposit():
  orderId = request.form.get('orderId')
  sql="select o.order_id as \'OrderId\' ,o.order_name as \'OrderName\',o.order_desc as \'OrderDesc\',u.user_name as \'Buyer\',o.order_count as \'Count\',p.product_time_name as \'Time\',o.order_total as \'Total\',o.order_deposit as \'Deposit\',o.order_balance as \'Balance\' from tb_order o inner join tb_user u on o.buyer_id = u.user_id  inner join v_product_time p on o.product_time = p.product_time_id where o.order_id= \'" + orderId + "\'"
  str_result = getData(sql)
  return str_result

@app.route('/All/GetDetail', methods=['POST'])
def AllGetDetail():
  orderId = request.form.get('orderId')
  sql="select o.order_id as \'OrderId\',s.status_name as \'OrderStatus\',o.order_name as \'OrderName\',o.order_desc  as \'OrderDesc\',pt.product_time_name as  \'ProductTime\',o.order_count as \'Count\',o.order_total as \'Total\' ,p.percent_name as \'Percent\',o.order_deposit as \'Deposit\' ,o.order_balance as \'Balance\',o.order_fee as \'Fee\',u.user_name as \'Name\',u.user_phone as \'Phone\',u.user_address as \'Address\',u.user_email as \'Email\',o.order_pay_type as \'PayType\',o.order_bank as \'Bank\',o.order_account_num as \'AccountNum\',o.cargo_type as \'CargoType\',o.cargo_time as \'CargoTime\',o.cargo_company as \'CargoCompany\',o.cargo_id as \'CargoId\',o.deposit_detail as \'DepositDetail\',o.balance_detail s \'BalanceDetail\', order_balance + order_fee as \'BalanceFee\',order_total+order_fee as \'TotalFee\' from tb_order o inner join tb_user u on o.buyer_id = u.user_id inner join v_status s on o.order_status_id = s.status_id inner join v_percent p on o.order_percent_id = p.percent_id inner join v_product_time pt on o.product_time = pt.product_time_id  where o.order_id= \'" + orderId + "\'"
  str_result = getData(sql)
  return str_result





def EditData(sql,data):
  conn = pymysql.connect(host = '59.127.224.170', user = 'yali',  passwd = "qazxcdews",  db = 'Purchasing', port = 3307)  
  cur = conn.cursor() 
  cur.execute(sql,data)
  conn.commit()
  str_result = '{"data": "Success"}'
  return str_result

def getData(sql):
  conn = pymysql.connect(host = '59.127.224.170', user = 'yali',  passwd = "qazxcdews",  db = 'Purchasing', port = 3307) 
 
  cur = conn.cursor() 
  cur.execute(sql)
  num_fields = len(cur.description)
  column_list = [i[0] for i in cur.description]
  str_result = ''
  result = []
  datas = {}
  for row in cur:
    rowdata = {}
    for idx, i in enumerate(column_list, start = 0):
      value = row[idx]
      if value is None:
        rowdata[column_list[idx]] = ''
      elif type(value) is datetime.datetime:
        rowdata[column_list[idx]] = myconverter(row[idx])
      elif type(value) is int:
        rowdata[column_list[idx]] = str(row[idx]).strip()
      else:
        rowdata[column_list[idx]] = row[idx].strip()
    result.append(rowdata)
  datas['data'] = result
  str_result = json.dumps(datas)
  return str_result


def getOneData(sql,data):
  conn = pymysql.connect(host = '59.127.224.170', user = 'yali',  passwd = "qazxcdews",  db = 'Purchasing', port = 3307)

  cur = conn.cursor()
  #print(sql)
  #print(data)
  cur.execute(sql,data)
  data = cur.fetchone()
  return data


def myconverter(o):
  if isinstance(o, datetime.datetime):
    return o.__str__()


if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=1234)
