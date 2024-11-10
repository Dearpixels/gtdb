import json

class Request:
	def __init__(self, db_name: str):
		self.db_name = db_name
		
	def load_data(self) -> dict:
		"""
		Загружает данных из JSON-файла.
		"""
		try:
			with open(self.db_name, "r") as file:
				return json.load(file)
		except FileNotFoundError:
			return {}
	
	def save_data(self, data: dict) -> None:
		"""
		Сохроняет данные в JSON-файл.
		"""
		with open(self.db_name, "w") as file:
			json.dump(data, file, indent=4)
	
	def get(self) -> dict:
		"""
		Функция которая возвращает данные из JSON-файл.
		
		Returns:
			dict: Данные из json-файла.
		"""
		return self.load_data()		
	
	def update(self, update_data: dict, id_key: str = None) -> None:
		"""
		Функция для обновления данных.
		
		Parameters:
			update_data (dict): Новый данные.
			id_key (str): Обновлять по идентификаторо.
		"""
		data = self.load_data()
		if id_key is None:
			data.update(update_data)
			self.save_data(data)
			return
		if id_key in data:
			data[id_key].update(update_data)
			self.save_data(data)
		else:
			print(f"[{self.db_name}] Идентификатор {id_key} не найден.")
	
	def increment_field(self, field: str, amount: int, id_key: str = None) -> None:
		"""
		Увеличивает (или уменьшает) числовое поле на заданную величину.
		
		Parameters:
			field (str): Название числового поля, которое нужно обновить.
			amount (int): Значение, на которое нужно изменить поле (может быть отрицательным для вычитания).
			id_key (str): Идентификатор.
		"""
		data = self.load_data()
		if id_key is None:
			if field in data and isinstance(data[field], (int, float)):
				data[field] += amount
				self.save_data(data)
			else:
				print(f"[{self.db_name}] Поле '{field}' не найдено или не является числовым.")
		else:
			if id_key in data:
				if field in data[id_key] and isinstance(data[id_key][field], (int, float)):
					data[id_key][field] += amount
					self.save_data(data)
				else:
					print(f"[{self.db_name}] Поле '{field}' не найдено или не является числовым.")
			else:
				print(f"[{self.db_name}] Идентификатор {id_key} не найден.")
	
	def update_field(self, path: str, amount: int) -> None:
		"""
		Обновляет числовое поле по заданному пути, подобно MongoDB.
		
		Parameters:
        	path (str): Путь к числовому полю в формате '123.balance' для вложенных данных.
        	amount (int): Значение, на которое нужно изменить поле (может быть отрицательным для вычитания).
		"""
		data = self.load_data()
		# Разбиваем путь на ключи для вложенных уровней.
		keys = path.split(".")
		d = data
		for key in keys[:-1]:
			if key in d and isinstance(d[key], dict):
				d = d[key]
			else:
				print(f"[{self.db_name}] Путь '{path}' не найден или не является вложенной структурой")
				return
		# Обновляем конечное числовое поле.
		final_key = keys[-1]
		if final_key in d and isinstance(d[final_key], (int, float)):
			d[final_key] += amount
			self.save_data(data)
		else:
			print(f"[{self.db_name}] Поле '{path}' не найдено или не является числовым.")
	
	def update_string_field(self, path: str, new_value: str) -> None:
		"""
		Обновляет строковое поле по заданному пути.
		
		Parameters:
			path (str): Путь к строковому полю в формате '123.profile.name' для вложенных данных.
        	new_value (str): Новое строковое значение для обновления поля.
		"""
		data = self.load_data()
		# Разбиваем путь на ключи для вложенных уровней.
		keys = path.split(".")
		d = data
		for key in keys[:-1]:
			if key in d and isinstance(d[key], dict):
				d = d[key]
			else:
				print(f"[{self.db_name}] Путь '{path}' не найден или не является вложенной структурой")
				return
		# Обновляем конечное числовое поле.
		final_key = keys[-1]
		if final_key in d and isinstance(d[final_key], (str)):
			d[final_key] = new_value
			self.save_data(data)
		else:
			print(f"[{self.db_name}] Поле '{path}' не найдено или не является строкой.")
	
	def delete_key(self, key: str) -> None:
		"""
		Функция для удаления ключа в Json-файле.
		
		Parameters:
			key (str): Название ключа которое нужно удалить.
		"""
		data = self.load_data()
		
		if key in data:
			del data[key]
			self.save_data(data)
		else:
			print(f"[{self.db_name}] Ключ '{key}' не найдено.")