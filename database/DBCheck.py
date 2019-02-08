import time

def check(brand, item, connector):

	with connector.cursor() as cursor:

		def insert(CurrentItem):
			cursor.execute("""INSERT INTO data (name, price, link, available, unavailable) VALUES ("{}", "{}","{}", "{}", "{}")""".format(CurrentItem['name'],
																																		  CurrentItem['price'], 
																																		  CurrentItem['link'], 
																																		  CurrentItem['available'], 
																																		  CurrentItem['unavailable']))
			connector.commit()

		def notification(Ntype, item):
			cursor.execute("""INSERT INTO notification (type, item, unixTime) VALUES ("{}", "{}","{}")""".format(str(Ntype),str(item),str(time.time())))
			connector.commit()

		#check in db if item exists
		#if it does -> do nothign
		#if it doesnt -> replace the item

		try:
			cursor.execute("SELECT * FROM data WHERE name = '{}'".format(item['name']))
			rows = cursor.fetchall()
			if(len(rows) == 0):
				insert(item)
				notification("new", item)
				print("{} put in {} DB".format(item['name'], brand))
			else:
				print("{} allready exist in database!".format(item['name']))

				shoe = rows[0]
				change = {'price': '$000',
						  'link': 'https://shoe.com',
						  'available': '[1,2,3]'}

				if(item['price'] != shoe['price']):
					notification("price", item)
					change['price'] = shoe['price']
				else:
					change['price'] = item['price']

				if(item['available'] != item['available']):
					notification("available", item)
					change['available'] = shoe['available']
				else:
					change['available'] = item['available']
					

				### CHANGE THIS TO EDIT OR SOMETHING
				insert(shoe)


		except Exception as e:
			print(e)

def emptyItem(brand, item, connector):
	with connector.cursor() as cursor:
		#put item in dbfails because its empty
		try:
			cursor.execute("""INSERT INTO emptyitem (name, price, link, available, unavailable) VALUES ("{}", "{}","{}", "{}", "{}")""".format(item['name'],
																																		  item['price'], 
																																		  item['link'], 
																																		  item['available'], 
																																		  item['unavailable']))
			connector.commit()
		except Exception as e:
			print(e)

