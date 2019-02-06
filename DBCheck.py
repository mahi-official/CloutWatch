def check(brand, item, connector):

	with connector.cursor() as cursor:

		#check in db if item exists
		#if it does -> do nothign
		#if it doesnt -> replace the item

		try:
			cursor.execute("SELECT * FROM data WHERE name = {}".format(item['name']))
			connection.commit()
		except Exception as e:
			print(e)