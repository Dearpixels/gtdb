import json

class Gtdb:
	def __init__(self, db_name: str):
		self.db_name = db_name
		self.create_db()
	
	def create_db(self) -> bool:
		"""
		Функции который отвечает за создание JSON-файл.
		
		Returns:
			bool: True если создался False если не создался.
		"""
		try:
			with open(self.db_name, "x") as file:
				json.dump({}, file)
				return True
		except Exception:
			return False
	
	def all(self) -> dict:
		"""
		Функция которая возвращает информация из JSON-файл.
		
		Returns:
			dict: Информация которая возвращается.
		"""
		try:
			with open(self.db_name, "r") as file:
				return json.load(file)
		except FileNotFoundError:
			print(f"[{self.db_name}] Файл не найден.")
		except json.JSONDecodeError as json_error:
			print(f"[{self.db_name}] Ошибка декодирования JSON: {json_error}")
	
	def add(self, data: dict) -> None:
		"""
		Функция для того чтобы записать данные в JSON-файл.
		
		Parameters:
			data (dict): Данные которые нужно записать.
			indent (int): Чтобы указать отступы.
		"""
		try:
			try:
				with open(self.db_name, "r") as file:
					existing_data = json.load(file)
			except json.JSONDecodeError:
				existing_data = {}
			# обновляем существующие данные на новые
			existing_data.update(data)
			
			with open(self.db_name, "w") as file:
				json.dump(existing_data, file, indent=4)
		except TypeError as e:
			print(f"[{self.db_name}] Ошибка сериализации JSON: {e}")
		except json.JSONDecodeError as json_error:
			print(f"[{self.db_name}] Ошибка декодирования JSON: {json_error}")
		except UnicodeDecodeError as ude:
			print(f"[{self.db_name}] Ошибка кодировки JSON: {ude}")