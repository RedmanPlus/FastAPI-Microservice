import datetime
import uvicorn
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
	port: int

class StatEntry(BaseModel):
	id: int
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
		'password': db_data.password,
		'port': db_data.port
	}

	return_body = db.connection_establisher(cred_dict)

	return return_body

@app.get('/get-stats/{date_first}/{date_last}')
def find_stats(date_first: str, date_last: str, order_by: Optional[str] = 'Дата'):
	queries = db.get_information((datetime.datetime.strptime(date_first, '%Y-%m-%d'), datetime.datetime.strptime(date_last, '%Y-%m-%d')), cred_dict)

	return_list = []

	for query in queries:
		return_list.append({
			'Дата': query[1],
			'Показы': query[2],
			'Клики': query[3],
			'Цена кликов': query[4],
			'Средняя стоимость клика': round(float(query[4])/query[3], 2),
			'Средняя стоимость тысячи показов': round((float(query[4])/query[2])*1000, 2)
		})

	return_list = sorted(return_list, key=lambda x: x[order_by])

	return_body = {}
	for ind, elem in enumerate(return_list):
		return_body[ind] = elem

	return return_body

@app.post('/add-stats/')
def add_stats(data: StatEntry):
	data = (data.id, data.date, data.views, data.clicks, data.price)
	return_body = db.post_information(data, cred_dict)

	return return_body

@app.delete('/delete-stats/')
def delete_stats():
	return_body = db.delete_information(cred_dict)

	return return_body

if __name__ == "__main__":
	uvicorn.run(app, host='127.0.0.1', port=8000)