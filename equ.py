# -*- coding: utf-8 -*-
import requests
import unittest
import hashlib
import urllib3
import re
import json
import io
import sys
urllib3.disable_warnings() 
#sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')
s = requests.session()  
class Test_Equ(unittest.TestCase):

	def setUp(self):                   #初始化数据
		self.url = 'https://www.eq28.cn'
		self.username = 15602945263
		self.pwd = 'lxn612536'



	def md_5(self):                    #定义一个函数，密码用MD5加密
		r = hashlib.md5()
		r.update(self.pwd.encode("utf-8"))
		password=r.hexdigest()
		return password


	def test_login(self):
		try:
			login_url=self.url + '/webLogin/login'
			data = {'username':self.username,'password':self.md_5()}
			response = s.post(login_url,data=data,verify=False)
			#print('login:',response.status_code)
			#print(response.text)
			response_dict=response.json()                    #转为dict
			self.assertEqual(response_dict['status'],'0')
			return response.cookies                      #必须str类型才能获取到cookies           
		except BaseException as e:
			print('登录接口异常:', str(e))


	def test_productDetail(self):       #商品详情页
		try:
			url = self.url + '/efunProductDetail/productDetail?productId=402231'
			response = s.get(url,verify=False)
			#print(response.text)
			print('productDetail:',response.status_code)
		except BaseException as e:
			print('商品详情页接口异常:', str(e))


	def test_cartCount(self):           #商品_购物车页面
		try:                           
			url = self.url + '/webEfunCart/cartCount'
			response = s.post(url,verify=False).json()
			self.assertEqual(response['msg'],'操作成功')
			self.assertEqual(response['status'],'0')
			print('cartCount:',response)
		except BaseException as e:
			print('商品_购物车页面接口异常:', str(e))



	def test_add_cart(self):             #点击加入购物车
		try:                            
			url = self.url + '/webEfunCart/add'
			data = {'skuCode':'a5005e827127689fcbf5f78f73108b53','proNum':1,'orderShopId':''}
			cookie = self.test_login()                                                   #引用登录函数
			response = s.post(url,data=data,cookies=cookie,verify=False).json()          #此处需要set登录后返回的cookie进来
			self.assertEqual(response['status'],'0') 
			print('add_cart:',response)
		except BaseException as e:
			print('加入购物车接口异常:',str(e))	


	def test_cart_list(self):            #购物车列表
		try:
			url = self.url + '/efunCart/list'
			r = s.get(url,verify=False)
			# print('cart_list:',r.status_code)
			# print('cart_list:',r.text)
			token = re.findall(r'name="jfinal_token" value="(.*?)"/>',r.text)                 #正则表达式提取token
			return str(token[0])
		except BaseException as e:
			print('购物车列表接口异常了',str(e))


	def test_cart_submit(self):         #购物车列表--提交支付
		try:
			url= self.url + '/webEfunOrder/submitFromCart'
			#print(self.test_cart_list())
			value=self.test_cart_list()
			data={'jfinal_token':value,'cartIds':'4212679','useCash':'0','useIntegral':'0'}
			#data= {'jfinal_token':'value','payPassword':'','useCash':0,'useIntegral':0,'carId':'','cartIds':'4212679'}
			response = s.post(url,data=data,verify=False).json()
			print('cart_submit:',response)
			self.assertEqual(response['data'],None)	
		except BaseException as e:
			print('购物车列表--提交支付接口异常了',str(e))



	# def test_submit_pay(self):          #购物车列表--确认支付
	# 	url = self.url + '/efunOrder/submitCartToPay?orderIds=5475c309005a4f8cb9e2e3f90ffb93d2'
	# 	response = s.get(url,verify=False)
	# 	print('submit_pay:%s' %response.status_code)


	def test_jifen(self):                #积分签到
		try:
			url = self.url + '/webUser/center/signIn/singIn'          
			response = s.post(url,verify=False)
			print('积分签到:',response.text)
		except BaseException as e:
			print('签到接口异常了',str(e))

	def test_jifen2(self):                #积分签到
		try:
			url = self.url + '/webUser/center/signIn/singIn'          
			response = s.post(url,verify=False)
			print('积分签到:',response.text)
		except BaseException as e:
			print('签到接口异常了',str(e))
			
	def test_print(self):
		print("test")

if __name__ == '__main__':
	unittest.main()





