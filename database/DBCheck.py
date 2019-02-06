def check(brand, item, connector):

	with connector.cursor() as cursor:

		#check in db if item exists
		#if it does -> do nothign
		#if it doesnt -> replace the item

		try:
			cursor.execute("SELECT * FROM data WHERE name = '{}'".format(item['name']))
			rows = cursor.fetchall()
			if(len(rows) == 0):
				cursor.execute("""INSERT INTO data (name, price, link, available, unavailable) VALUES ("{}", "{}","{}", "{}", "{}")""".format(item['name'],
																																		  item['price'], 
																																		  item['link'], 
																																		  item['available'], 
																																		  item['unavailable']))
				connector.commit()
				print("{} put in {} DB".format(item['name'], brand))
			else:
				print(rows)
		except Exception as e:
			print(e)