from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
import requests
from kivymd.uix.list import OneLineListItem, MDList

class LoginPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.login_button = MDRaisedButton(text="Вход",
                                           pos_hint={"center_x": 0.5, "center_y": 0.5},
                                           on_release=self.login)
        self.add_widget(self.login_button)

    def login(self, *args):
        self.manager.current = "main_screen"


class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.bmi_calculator_button = MDRaisedButton(text="Калькулятор ИМТ",
                                                    pos_hint={"center_x": 0.5, "center_y": 0.6},
                                                    on_release=self.go_to_bmi_calculator)
        self.virtual_coach_button = MDRaisedButton(text="Виртуальный тренер",
                                                   pos_hint={"center_x": 0.5, "center_y": 0.5},
                                                   on_release=self.go_to_virtual_coach)
        self.add_widget(self.bmi_calculator_button)
        self.add_widget(self.virtual_coach_button)

    def go_to_bmi_calculator(self, *args):
        self.manager.current = "bmi_calculator_screen"

    def go_to_virtual_coach(self, *args):
        self.manager.current = "virtual_coach_screen"


class BMICalculatorScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.weight_field = MDTextField(pos_hint={"center_x": 0.5, "center_y": 0.6},
                                        hint_text="Вес (kg)",
                                        size_hint=(None, None),
                                        width=200)
        self.height_field = MDTextField(pos_hint={"center_x": 0.5, "center_y": 0.5},
                                        hint_text="Рост (m)",
                                        size_hint=(None, None),
                                        width=200)
        self.calculate_button = MDRaisedButton(text="Рассчитать ИМТ",
                                               pos_hint={"center_x": 0.5, "center_y": 0.4},
                                               on_release=self.calculate_bmi)
        self.add_widget(self.weight_field)
        self.add_widget(self.height_field)
        self.add_widget(self.calculate_button)

    def calculate_bmi(self, *args):
        try:
            weight = float(self.weight_field.text)
            height = float(self.height_field.text)
            bmi = weight / (height ** 2)
            advice = self.get_advice(bmi)
            self.manager.get_screen("bmi_result_screen").update_result(bmi, advice)
            self.manager.current = "bmi_result_screen"
        except ValueError:
            print("Invalid input")

    def get_advice(self, bmi):
        if bmi < 18.5:
            return "У вас недостаточный вес. Важно убедиться, что вы получаете достаточное количество питательных веществ."
        elif 18.5 <= bmi < 25:
            return "Поздравляю! Вы находитесь в пределах здорового веса."
        elif 25 <= bmi < 30:
            return "У вас избыточный вес. Подумайте о внесении некоторых изменений в образ жизни, чтобы улучшить свое здоровье."
        else:
            return "Вы страдаете ожирением. Крайне важно сосредоточиться на улучшении своего здоровья и снижении рисков для здоровья."


class BMIResultScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.result_label = MDLabel(pos_hint={"center_x": 0.5, "center_y": 0.6},
                                    halign="center")
        self.advice_label = MDLabel(pos_hint={"center_x": 0.5, "center_y": 0.5},
                                    halign="center")
        self.repeat_button = MDRaisedButton(text="Рассчитать снова",
                                            pos_hint={"center_x": 0.5, "center_y": 0.4},
                                            on_release=self.go_to_bmi_calculator)
        self.add_widget(self.result_label)
        self.add_widget(self.advice_label)
        self.add_widget(self.repeat_button)

    def update_result(self, bmi, advice):
        self.result_label.text = f"BMI: {bmi:.2f}"
        self.advice_label.text = advice

    def go_to_bmi_calculator(self, *args):
        self.manager.current = "bmi_calculator_screen"


class VirtualCoachScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.coach_list = MDList()
        self.add_widget(self.coach_list)

        self.populate_coach_list()

    def populate_coach_list(self):
        coaches = ["Персональный тренер", "Диетолог", "Инструктор йоги", "Тренер по психическому здоровью"]
        for coach in coaches:
            item = OneLineListItem(text=coach)
            self.coach_list.add_widget(item)

        # Add a button to receive daily motivational quotes
        get_quote_button = MDRaisedButton(text="Получайте ежедневную мотивацию",
                                          pos_hint={"center_x": 0.7, "center_y": 0.6},
                                          on_release=self.get_daily_quote)
        self.add_widget(get_quote_button)

    def get_daily_quote(self, *args):
        # API request to fetch a motivational quote
        response = requests.get("https://api.quotable.io/random")
        if response.status_code == 200:
            quote_data = response.json()
            quote = quote_data["content"]
            author = quote_data["author"]
            quote_text = f'"{quote}" - {author}'
            self.show_quote(quote_text)
        else:
            self.show_quote("Не удалось получить цитату. Пожалуйста, повторите попытку позже.")

    def show_quote(self, quote):
        # Display the motivational quote
        quote_label = MDLabel(text=quote,
                              pos_hint={"center_x": 0.5, "center_y": 0.4},
                              halign="center")
        self.add_widget(quote_label)


class FitPalApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "BlueGray"

        screen_manager = ScreenManager()

        screen_manager.add_widget(LoginPage(name='login_screen'))
        screen_manager.add_widget(MainScreen(name='main_screen'))
        screen_manager.add_widget(BMICalculatorScreen(name='bmi_calculator_screen'))
        screen_manager.add_widget(BMIResultScreen(name='bmi_result_screen'))
        screen_manager.add_widget(VirtualCoachScreen(name='virtual_coach_screen'))

        return screen_manager


if __name__ == "__main__":
    FitPalApp().run()
