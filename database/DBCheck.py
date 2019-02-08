def check(brand, item, connector):

	with connector.cursor() as cursor:

		def insert(CurrentItem):
			cursor.execute("""INSERT INTO data (name, price, link, available, unavailable) VALUES ("{}", "{}","{}", "{}", "{}")""".format(CurrentItem['name'],
																																		  CurrentItem['price'], 
																																		  CurrentItem['link'], 
																																		  CurrentItem['available'], 
																																		  CurrentItem['unavailable']))
			connector.commit()

		#check in db if item exists
		#if it does -> do nothign
		#if it doesnt -> replace the item

		try:
			cursor.execute("SELECT * FROM data WHERE name = '{}'".format(item['name']))
			rows = cursor.fetchall()
			if(len(rows) == 0):
				insert(item)
				print("{} put in {} DB".format(item['name'], brand))
			else:
				print("{} allready exist in database!".format(item['name']))

				shoe = rows[0]
				change = {'price': '$000',
						  'link': 'https://shoe.com',
						  'available': '[1,2,3]'}

				if(item['price'] != shoe['price']):
					#alert DB about pricechange
					change['price'] = shoe['price']
				else:
					change['price'] = item['price']

				if(item['link'] != shoe['link']):
					#alert DB about linkchange
					change['link'] = shoe['link']
				else:
					change['link'] = item['link']

				if(item['available'] != item['available']):
					#alert DB about new sizes in stock
					change['available'] = shoe['available']
				else:
					change['available'] = item['available']
					
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

