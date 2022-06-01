import psycopg2

def connection_establisher(credentials: dict) -> dict:
	
	conn = None
	cur = None

	try:
		conn = psycopg2.connect(**credentials)
		cur = conn.cursor()

		cur.execute("""SELECT table_name FROM information_schema.tables
			       WHERE table_schema = 'public';""")

		if ('stats',) not in cur.fetchall():
			script = """
				CREATE TABLE stats (
					id INT,
					date_of_event DATE,
					num_of_views INT,
					num_of_clicks INT,
					price_for_click NUMERIC(12,2),
				);
			"""
			cur.execute(script)
			conn.commit()

	except Exception as error:
		print(error)
	finally:
		if cur is not None:
			cur.close()
		if conn is not None:
			conn.close()

		return {'Success':'Connection is established'}




def get_information(requirements: tuple, credentials: dict) -> list:
	
	conn = None
	cur = None

	try:
		conn = psycopg2.connect(**credentials)
		cur = conn.cursor()

		script = """
				SELECT date_of_event, num_of_views, num_of_clicks, price_for_click FROM stats
					WHERE date_of_event > %s AND date_of_event < %s;
			"""
		cur.execute(script, requirements)
		required_query = cur.fetchall()

		return required_query

	except Exception as error:
		print(error)
	finally:
		if cur is not None:
			cur.close()
		if conn is not None:
			conn.close()



def post_information(data: list, credentials: dict) -> dict:

	conn = None
	cur = None

	try:
		conn = psycopg2.connect(**credentials)
		cur = conn.cursor()

		script = """
				INSERT INTO stats (date_of_event, num_of_views, num_of_clicks, price_for_click)
					VALUES (%s, %s, %s, %s);
			"""

		cur.execute(script, data)
		conn.commit()

		return {'Success': 'Query added'}

	except Exception as error:
		print(error)
	finally:
		if cur is not None:
			cur.close()
		if conn is not None:
			conn.close()




def delete_information(credentials: dict) -> dict:
	
	conn = None
	cur = None

	try:
		conn = psycopg2.connect(**credentials)
		cur = conn.cursor()

		script = """
				DELETE FROM stats;
			"""
		cur.execute(script, requirements)
		conn.commit()

		return {'Success':'Information deleted'}

	except Exception as error:
		print(error)
	finally:
		if cur is not None:
			cur.close()
		if conn is not None:
			conn.close()