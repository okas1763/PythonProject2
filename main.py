from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
import json
import os

# Функция для загрузки данных из файла
def load_data():
    if os.path.exists("data.json"):
        with open("data.json", "r", encoding="utf-8") as file:
            return json.load(file)
    return {}

# Функция для сохранения данных в файл
def save_data(data):
    with open("data.json", "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

# Основной интерфейс
class PersonForm(RelativeLayout):
    def __init__(self, person_id=None, return_to_main=None, **kwargs):
        super().__init__(**kwargs)
        self.person_id = person_id
        self.return_to_main = return_to_main  # Функция для возврата в главное меню

        # Добавляем фоновую картинку
        self.background = Image(source="we.jpg", allow_stretch=True, keep_ratio=False)
        self.add_widget(self.background)

        # Основной контейнер для полей ввода
        self.container = BoxLayout(orientation="vertical", padding=10, spacing=10)
        self.add_widget(self.container)

        # Поля для ввода данных
        self.fields = {
            "first_name": TextInput(hint_text="Имя", background_color=(1, 1, 1, 0.7)),
            "last_name": TextInput(hint_text="Фамилия", background_color=(1, 1, 1, 0.7)),
            "middle_name": TextInput(hint_text="Отчество", background_color=(1, 1, 1, 0.7)),
            "age": TextInput(hint_text="Возраст", background_color=(1, 1, 1, 0.7)),
            "birthday": TextInput(hint_text="День рождения (ДД.ММ.ГГГГ)", background_color=(1, 1, 1, 0.7)),
            "email": TextInput(hint_text="Email", background_color=(1, 1, 1, 0.7)),
            "address": TextInput(hint_text="Место проживания", background_color=(1, 1, 1, 0.7)),
            "hobbies": TextInput(hint_text="Увлечения", background_color=(1, 1, 1, 0.7)),
            "phone": TextInput(hint_text="Номер телефона", background_color=(1, 1, 1, 0.7)),
            "telegram": TextInput(hint_text="Telegram-тег", background_color=(1, 1, 1, 0.7)),
            "gender": TextInput(hint_text="Пол", background_color=(1, 1, 1, 0.7)),
            "character": TextInput(hint_text="Тип характера", background_color=(1, 1, 1, 0.7)),
        }

        # Добавляем поля в контейнер
        for field in self.fields.values():
            self.container.add_widget(field)

        # Кнопка сохранения
        self.save_button = Button(text="Сохранить", size_hint_y=None, height=50, background_color=(0.7, 0, 0.7, 0.8))
        self.save_button.bind(on_press=self.save_person)
        self.container.add_widget(self.save_button)

        # Кнопка "Удалить" (только для редактирования существующего человека)
        if self.person_id:
            self.delete_button = Button(text="Удалить", size_hint_y=None, height=50, background_color=(0.8, 0, 0, 0.8))
            self.delete_button.bind(on_press=self.delete_person)
            self.container.add_widget(self.delete_button)

        # Кнопка "Назад"
        self.back_button = Button(text="Назад", size_hint_y=None, height=50, background_color=(0.2, 0.2, 0.2, 0.8))
        self.back_button.bind(on_press=self.go_back)
        self.container.add_widget(self.back_button)

        # Загружаем данные, если редактируем существующего человека
        if self.person_id:
            self.load_person()

    # Загрузка данных человека
    def load_person(self):
        data = load_data()
        if self.person_id in data:
            person = data[self.person_id]
            for key, value in person.items():
                if key in self.fields:
                    self.fields[key].text = value

    # Сохранение данных человека
    def save_person(self, instance):
        data = load_data()
        person_data = {key: field.text for key, field in self.fields.items()}
        if self.person_id:
            data[self.person_id] = person_data
        else:
            new_id = f"person_{len(data) + 1}"
            data[new_id] = person_data
        save_data(data)
        show_message("Данные сохранены!")

    # Удаление человека
    def delete_person(self, instance):
        data = load_data()
        if self.person_id in data:
            del data[self.person_id]
            save_data(data)
            show_message("Человек удален!")
            if self.return_to_main:
                self.return_to_main()

    # Возврат в главное меню
    def go_back(self, instance):
        if self.return_to_main:
            self.return_to_main()

# Всплывающее окно с сообщением
def show_message(message):
    popup = Popup(title="Сообщение", size_hint=(0.8, 0.4))
    popup.content = Label(text=message)
    popup.open()

# Главный экран с кнопками
class MainScreen(RelativeLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Добавляем фоновую картинку
        self.background = Image(source="we.jpg", allow_stretch=True, keep_ratio=False)
        self.add_widget(self.background)

        # Основной контейнер для кнопок
        self.container = BoxLayout(orientation="vertical", padding=10, spacing=10)
        self.add_widget(self.container)

        # Кнопка "Создать человека"
        self.create_button = Button(text="Создать человека", size_hint_y=None, height=50, background_color=(0.7, 0, 0.7, 0.8))
        self.create_button.bind(on_press=self.create_person)
        self.container.add_widget(self.create_button)

        # Кнопка "Открыть готового человека"
        self.open_button = Button(text="Открыть готового человека", size_hint_y=None, height=50, background_color=(0, 0.5, 0.8, 0.8))
        self.open_button.bind(on_press=self.open_person)
        self.container.add_widget(self.open_button)

    # Создание нового человека
    def create_person(self, instance):
        self.clear_widgets()
        self.add_widget(PersonForm(return_to_main=self.return_to_main))

    # Открытие существующего человека
    def open_person(self, instance):
        data = load_data()
        if not data:
            show_message("Нет сохраненных данных!")
            return

        # Создаем ScrollView для списка людей
        scroll = ScrollView()
        layout = BoxLayout(orientation="vertical", size_hint_y=None, spacing=10)
        layout.bind(minimum_height=layout.setter("height"))

        for person_id, person_data in data.items():
            btn = Button(text=f"{person_data['first_name']} {person_data['last_name']}", size_hint_y=None, height=50, background_color=(0.5, 0.5, 0.5, 0.8))
            btn.bind(on_press=lambda btn, pid=person_id: self.edit_person(pid))
            layout.add_widget(btn)

        scroll.add_widget(layout)
        self.clear_widgets()
        self.add_widget(scroll)

        # Кнопка "Назад"
        back_button = Button(text="Назад", size_hint_y=None, height=50, background_color=(0.2, 0.2, 0.2, 0.8))
        back_button.bind(on_press=self.return_to_main)
        self.add_widget(back_button)

    # Редактирование человека
    def edit_person(self, person_id):
        self.clear_widgets()
        self.add_widget(PersonForm(person_id=person_id, return_to_main=self.return_to_main))

    # Возврат в главное меню
    def return_to_main(self, *args):
        self.clear_widgets()
        self.__init__()

# Основное приложение
class PersonApp(App):
    def build(self):
        return MainScreen()

# Запуск приложения
if __name__ == "__main__":
    PersonApp().run()
