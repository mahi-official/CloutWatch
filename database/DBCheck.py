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
				itemInDB = rows[0] #get row
				#if what exists in the dabase is not equal to what we just scraped
				if(itemInDB != item):
					change = {}
					#if price is not equal
					if(item['price'] != itemInDB['price']):
						changeStr += "price update!"
						notification("price", item)

						change['price'] = itemInDB['price']
					else:
						change['price'] = item['price']

					#if the availability is not equal
					if(item['available'] != item['available']):
						changeStr += "available update!"
						notification("available", item)

						change['available'] = itemInDB['available']
					else:
						change['available'] = item['available']

					change['name'], change['link'], change['unavailable'] = item['name'], item['link'], item['unavailable']	

					if(changeStr == ""):
						pass
						#print("Nothing Changed {}".format(change['name']))
					else:
						print("Updated {}: {}".format(change['name'], changeStr))
						
					update(change)
				else:
					print("{} allready exist in database!".format(item['name']))


		except Exception as e:
			print("DB ERROR: {}".format(e))
			errorLog.log("DB ERROR: {}".format(e))

def emptyItem(brand, item, connector):
	with connector.cursor() as cursor:
		#put item in dbfails because its empty
		try:
			cursor.execute("""INSERT INTO emptyItem (name, price, link, available, unavailable) VALUES ("{}", "{}","{}", "{}", "{}")""".format(item['name'],
																																		  item['price'], 
																																		  item['link'], 
																																		  item['available'], 
																																		  item['unavailable']))
			connector.commit()
		except Exception as e:
			print(e)
			errorLog.log(e)

