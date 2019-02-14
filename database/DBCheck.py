import time
import errorLog

def check(brand, item, connector):

	with connector.cursor() as cursor:

		
		def insert(CurrentItem):
			cursor.execute("""INSERT INTO data (name, price, link, available, unavailable) VALUES ("{}", "{}","{}", "{}", "{}")""".format(CurrentItem['name'],
																																		  CurrentItem['price'], 
																																		  CurrentItem['link'], 
																																		  CurrentItem['available'], 
																																		  CurrentItem['unavailable']))
			connector.commit()

		def notification(Ntype, CurrentItem):
			cursor.execute("""INSERT INTO notification (type, unixTime, name, price, link, available, unavailable) VALUES ("{}", "{}","{}", "{}","{}", "{}", "{}")""".format(str(Ntype),
																																round(time.time()),
																																CurrentItem['name'],
																																CurrentItem['price'], 
																																CurrentItem['link'], 
																																CurrentItem['available'], 
																																CurrentItem['unavailable']))
			connector.commit()

		def update(CurrentItem):
			cursor.execute("""UPDATE data SET price = "{}", link = "{}", available = "{}", unavailable = "{}" WHERE name = "{}" """.format(CurrentItem['price'], 
																																		  CurrentItem['link'], 
																																		  CurrentItem['available'], 
																																		  CurrentItem['unavailable'],
																																		  CurrentItem['name']))
			connector.commit()

		#check in db if item exists
		#if it does -> do nothign
		#if it doesnt -> replace the item

		try:
			#gets all the entries with a certain name & matching link
			cursor.execute("SELECT * FROM data WHERE link = '{}' AND name = '{}'".format(item['link'], item['name']))
			rows = cursor.fetchall()
			#if the query returns something empty:
			if(len(rows) == 0):
				#most likely item doesnt exist yet in database
				#so we add it to the database
				insert(item)
				#also adds to notification database with type 'new'
				notification("new", item)
				print("{} put in {} DB".format(item['name'], brand))
			else:
				#item allready exists in database
				changeStr = ""
				shoe = rows[0] #get row
				#if what exists in the dabase is not equal to what we just scraped
				if(shoe != item):
					change = {'name': "shoeName",
							'price': "$000",
							'link': "https://nike.com/shoe",
							'available': [1,2,3],
							'unavailable': [-1,-2,-3]}

					#if price is not equal
					if(item['price'] != shoe['price']):
						changeStr += "||price|| "
						notification("price", item)
						change['price'] = shoe['price']
					else:
						change['price'] = item['price']

					#if the availability is not equal
					if(item['available'] != item['available']):
						changeStr += "||available|| "
						notification("available", item)
						change['available'] = shoe['available']
					else:
						change['available'] = item['available']

					change['name'] = item['name']
					change['link'] = item['link']
					change['unavailable'] = item['unavailable']	

					if(changeStr == ""):
						print("Nothing Changed {}".format(change['name']))
					else:
						print("Updated {}: {}".format(change['name'], changeStr))
						
					update(change)
				else:
					print("{} allready exist in database!".format(item['name']))


		except Exception as e:
			print(e)
			errorLog.log(e)

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
			errorLog.log(e)

