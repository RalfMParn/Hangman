from GameTime import GameTime
from Model import Model
from View import View


class Controller:
    def __init__(self, db_name=None):
        self.__model = Model()
        self.__view = View(self, self.__model)
        if db_name is not None:
            self.__model.database = db_name
        self.__game_time = GameTime(self.__view.lbl_time)


    def main(self):
        self.__view.main()

    def btn_scoreboard_click(self):
        window = self.__view.create_scoreboard_window()
        data = self.__model.read_scores_data()
        self.__view.draw_scoreboard(window, data)

    def buttons_no_game(self):
        self.__view.btn_new['state'] = 'normal'
        self.__view.btn_cancel['state'] = 'disable'
        self.__view.btn_send['state'] = 'disabled'
        self.__view.char_input.delete(0, 'end')  # Tühjendab sisestus kasti
        self.__view.char_input['state'] = 'disabled'

    def buttons_to_game(self):
        self.__view.btn_new['state'] = 'disable'
        self.__view.btn_cancel['state'] = 'normal'
        self.__view.btn_send['state'] = 'normal'
        self.__view.char_input['state'] = 'normal'
        self.__view.char_input.focus()

    def btn_new_click(self):  # Uus mäng
        self.__game_time.reset()
        self.__game_time.start()
        self.buttons_to_game()
        self.__model.new_game()
        self.__view.change_image(0)  # Muudab piltile id-ga 0
        self.__view.lbl_error.config(fg="black")

        # Muudab tekst bootom framis valitudjuhuslikuks sõnaks
        self.__view.lbl_result.config(text=f'{self.__model.blank_word}', font=self.__view.big_font)

        # print(f"Randomly Selected word: {self.__model.random_word}") Testimiseks

        self.__view.lbl_error.config(text=f'Vigased tähed: ')  # Kustutab eelmisest mängus jäänud vigased tähed

        # xTODO Seadista mudelis uus mäng. Juhuslik sõna andmebaasist vaja kätte saada
        # xTODO Näita äraarvatavat sõna aga iga tähe asemel on allkriips. Kirjastiil on big_font
        # xTODO Veateadete label muuda tekst "Vigased tähed:"

    def btn_cancel_click(self):
        self.__game_time.stop()
        self.buttons_no_game()
        self.__view.change_image(-1)

    def btn_send_click(self):
        default_words = 'Vigased tähed: '
        usr_guess = self.__view.char_input.get()
        self.__view.char_input.delete(0, "end")
        if usr_guess:
            self.__model.guess_checker(usr_guess)
            self.__view.change_image(self.__model.image_id)
            self.__view.lbl_result.config(text=f'{self.__model.blank_word}')
            self.is_game_over()
            if self.__model.guess_checker and len(self.__model.incorect_guess) > 0:
                self.__view.lbl_error.config(text=f"{default_words}{self.__model.incorect_guess}", fg="red")
        else:
            print("Sisestus kast ei tohi tühi olla")

        # self.__view.lbl_result.config(text=)

        # xTODO Loe sisestus kastist saadud info ja suuna mudelisse infot töötlema
        # xTODO Muuda teksti tulemus aknas (äraarvatav sõna)
        # xTODO Muuda teksti Vigased tähed
        # xTODO Tühjanda sisestus kast (ISESESIVALT TUNNIS KOHE)
        # xTODO KUI on vigu tekkinud, muuda alati vigade tekst punaseks ning näita vastavalt vea numbrile õiget pilti
        # xTODO on mäng läbi. MEETOD siin samas klassis.

    def is_game_over(self):
        # Kontrollib kas mäng on läbi
        if self.__model.image_id == 11:
            print("Kautasid!")
            self.__game_time.stop()
            self.buttons_no_game()
            self.__view.lbl_result.config(text=self.__model.random_word, font=self.__view.big_font)
        elif '_' not in self.__model.blank_word:
            print("Võitsid!")
            self.__game_time.stop()
            self.buttons_no_game()
            usr_name = self.__view.ask_usr_name()
            self.__model.name_time_to_database(usr_name, self.__game_time.counter)



    # xTODO Meetod on mäng on läbi.
    # xTODO Kontrollida kas mäng on läbi.
    # xTODO JAH puhul peata mänguaeg
    # xTODO Seadista nupud õigeks (meetod juba siin klassis olemas)
    # xTODO Küsi mängija nime (simpledialog.askstring)
    # xTODO Saada sisestatud mängija nimi ja mängu aeg sekundites mudelisse kus toimub kogu muu tegevus kasutajanimega
    # xTODO mänguaeg on muutujas self.__game_time.counter
