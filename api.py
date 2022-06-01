from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
import db

app = FastAPI()

class DBCreds(BaseModel):
	host: str
	dbname: str
	user: str
	password: str
	port: str

class StatEntry(BaseModel):
	date: datetime.date
	views: Optional[int] = None
	clicks: Optional[int] = None
	price: Optional[float] = None

cred_dict = {'Warning': 'Use a POST request to add database credentials'}

@app.get('/')
def test():
	return cred_dict

@app.post('/')
def db_setter(db_data: DBCreds):
	global cred_dict
	cred_dict = {
		'host': db_data.host,
		'dbname': db_data.dbname,
		'user': db_data.user,
		'password': db_data.user,
		'port': db_data.port
	}

	return_body = db.connection_establisher(cred_dict)

	return return_body

@app.get('/get-stats/{date_first}/{date_last}')
def find_stats(date_first: any, date_last: any):
	queries = db.get_information((date_first, date_last), cred_dict)

	return_body = {}

	for query in queries:
		return_body[query[0]] = {
			'Дата': query[1],
			'Показы': query[2],
			'Клики': query[3],
			'Цена кликов': query[4],
			'Средняя стоимость клика': round(query[4]/query[3], 2),
			'Средняя стоимость тысячи показов': round((query[4]/query[2])*1000, 2)
		}

	return return_body

@app.post('/add-stats/')
def add_stats(data: StatEntry):
	data = (data.date, data.views, data.clicks, data.price)
	return_body = db.post_information(data, cred_dict)

	return return_body

@app.delete('/delete-stats/')
def delete_stats():
	return_body = db.delete_information(cred_dict)

	return return_body