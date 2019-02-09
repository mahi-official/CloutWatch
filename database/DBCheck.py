import time

def check(brand, item, connector):

	with connector.cursor() as cursor:

		def insert(CurrentItem):
			cursor.execute("""INSERT INTO data (name, price, link, available, unavailable) VALUES ("{}", "{}","{}", "{}", "{}")""".format(CurrentItem['name'],
																																		  CurrentItem['price'], 
																																		  CurrentItem['link'], 
																																		  str(CurrentItem['available']), 
																																		  str(CurrentItem['unavailable'])))
			connector.commit()

		def notification(Ntype, CurrentItem):
			cursor.execute("""INSERT INTO notification (type, unixTime, name, price, link, available, unavailable) VALUES ("{}", "{}","{}", "{}","{}", "{}", "{}")""".format(str(Ntype),str(time.time()),
																																CurrentItem['name'],
																																CurrentItem['price'], 
																																CurrentItem['link'], 
																																str(CurrentItem['available']), 
																																str(CurrentItem['unavailable'])))
			connector.commit()

		def update(ChangedItem):
			cursor.execute("""UPDATE data SET name = "{}", price = "{}", link = "{}", available = "{}", unavailable = "{}") VALUES ("{}", "{}","{}")""".format(ChangedItem['name'],
																																							  ChangedItem['price'], 
																																							  ChangedItem['link'], 
																																							  str(ChangedItem['available']), 
																																							  str(ChangedItem['unavailable'])))
			connector.commit()

		#check in db if item exists
		#if it does -> do nothign
		#if it doesnt -> replace the item

		try:
			cursor.execute("SELECT * FROM data WHERE link = '{}' AND name = '{}'".format(item['link'], item['name']))
			rows = cursor.fetchall()
			if(len(rows) == 0):
				insert(item)
				notification("new", item)
				print("{} put in {} DB".format(item['name'], brand))
			else:
				print("{} allready exist in database!".format(item['name']))

				shoe = rows[0]
				if(shoe != item):
					change = {'name': "shoeName",
					'price': "$000",
					'link': "https://nike.com/shoe",
					'available': [1,2,3],
					'unavailable': [-1,-2,-3]}

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
						
					change['name'] = item['name']
					change['link'] = item['link']
					change['unavailable'] = item['unavailable']	

					print("Updated {}".format(change['name']))
					update(change)


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

