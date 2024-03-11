import glob
import sqlite3
import os
from Score import Score
from datetime import datetime


class Model:
    def __init__(self):
        # Ei saanud tavaline ühendus teha andmebaasile, kasutan "absolute path" asemel
        script_dir = os.path.dirname(os.path.abspath(__file__))  # Tee hetkele skripti asukohale

        relative_path = 'databases/hangman_words_ee.db'  # Paneb lõpu kus see andmebaas asub

        self.__database = os.path.join(script_dir, relative_path)  # Andmebaas pannakse muutujale

        # pip install Pillow => vajalik piltidega majandamiseks
        self.__image_files = glob.glob('*/images/*.png')  # List mängu piltidega
        self.__table_name = 'scores'
        self.__random_word = None
        self.__user_guesses = []
        self.__wrong_guesses = []
        self.__random_blank = []
        self.__wrong_counter = 0
        self.__right_guesses = []
        self.__result_string = []
        self.__joined_wrong_guesses = []

        # xTODO juhuslik sõna,
        # xTODO kõik sisestatud tähed (List)
        # xTODO vigade lugeja (s.h. pildi id)
        # xTODO kasutaja leitud tähed (visuaal muidu on seal allkriips _)

    def new_game(self):
        self.__random_word = self.make_random_word()
        self.__user_guesses = []
        self.__wrong_guesses = []
        self.__right_guesses = []
        self.__random_blank = []
        self.__wrong_counter = 0
        self.__joined_wrong_guesses = []

        for letter in self.__random_word:
            self.__random_blank.append("_")

        self.__result_string = ' '.join(self.__random_blank)

    # xTODO Meetod mis seadistab uue mängu
    # xTODO Seadistab uue sõna äraarvamiseks
    # xTODO Seadistab mõningate muutujate algväärtused (vaata ___init__ kolme viimast
    # xTODO. Neljas muutuja on eelmine rida)
    # xTODO Seadistab ühe muutuja nii et iga tähe asemel paneb allkiriipsu mida näidata aknas äraarvatavas sõnas (LIST)

    @property
    def database(self):
        return self.__database

    @property
    def image_files(self):
        return self.__image_files

    @property
    def random_word(self):
        return self.__random_word

    @property
    def blank_word(self):
        return self.__result_string

    @property
    def image_id(self):
        return self.__wrong_counter

    @property
    def incorect_guess(self):
        return self.__wrong_guesses

    @database.setter
    def database(self, value):
        self.__database = value

    def read_scores_data(self):
        # Loeb andmebaasi tabelist edetabel kõik kirjed

        connection = None
        try:

            connection = sqlite3.connect(self.__database)  # Ühendus tehakse andmebaasile
            sql = 'SELECT * FROM scores ORDER BY seconds;'
            cursor = connection.execute(sql)
            data = cursor.fetchall()
            result = []
            for row in data:
                result.append(Score(row[1], row[2], row[3], row[4], row[5]))
            return result
        except sqlite3.Error as error:
            print(f"Viga ühenduda andmebaasi {self.__database}: {error}")
        finally:
            if connection:
                connection.close()

    def make_random_word(self):
        # Loeb andmebaasi tabelist üks juhuslik sõna
        connection = None
        try:

            connection = sqlite3.connect(self.__database)
            # Ühendus tehakse andmebaasile
            sql = 'SELECT word FROM words ORDER BY random() LIMIT 1;'
            cursor = connection.execute(sql)
            data = cursor.fetchone()
            return data[0]
        except sqlite3.Error as error:
            print(f'Viga ühenduda andmebaasi {self.__database}: {error}')
        finally:
            if connection:
                connection.close()

    # xTODO Meetod mis seadistab juhusliku sõna muutujasse
    # xTODO Teeb andmebaasi ühenduse ja pärib sealt ühe juhusliku sõna ning kirjutab selle muutujasse

    def guess_checker(self, guess):
        self.__user_guesses.append(guess[0].lower())
        if guess.lower() in self.__random_word.lower():
            self.__result_string = ''
            print('Guess correct')
            self.__right_guesses.append(guess[0].lower())

            for letter in self.__random_word.lower():
                if letter in self.__right_guesses:
                    self.__result_string += letter + ' '
                elif letter not in self.__right_guesses:
                    self.__result_string += '_ '
        else:
            print("Guess incorrect")
            self.__wrong_counter += 1
            if guess[0].lower() not in self.__wrong_guesses:
                self.__joined_wrong_guesses.append(guess[0].lower())
                self.__wrong_guesses = ' '.join(self.__joined_wrong_guesses)
            return True

    # xTODO kasutaja siestuse kontroll (Vaata COntrolleris btn_send_click esimest)
    # xTODO Kui on midagi sisestatud võta sisestusest esimene märk (me saame sisestada pika teksti aga esimene täht on
    # oluline!)
    # xTODO Kui täht on otsitavas sõnas, siis asneda tulemuses allkriips õige tähega.
    # xTODO kui tähte polnud, siis vigade arv kasvab +1 ning lisa vigane täht eraldi listi

    def list_to_string(self, list_to_change):
        if not list_to_change:
            result_string = ""
            return result_string
        else:
            result_string = ', '.join(str(x).upper() for x in list_to_change if x.strip())
        return result_string
    # xTODO Meetod mis tagastab vigaste tähtede listi asemel tulemuse stringina. ['A', 'B', 'C'] => A, B, C
    # (polnud vist vaja? sain ilma meetodita seda tehtud?)

    def name_time_to_database(self, name, time):
        connection = None

        try:
            connection = sqlite3.connect(self.__database)

            current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            sql = "INSERT INTO " + self.__table_name + " (name, word, missing, seconds, date_time) VALUES (?, ?, ?, ?, ?)"
            connection.execute(sql, (name.strip(), self.__random_word, self.list_to_string(self.__wrong_guesses), time, current_date))
            connection.commit()
        except sqlite3.Error as error:
            print(f"Viga ühenduda andmebaasi {self.__database}: {error}")
        finally:
            if connection:
                connection.close()

    # xTODO Meetod mis lisab mängija ja tema aja andmebaasi (Vaata Controlleris viimast xTODO rida)
    # xTODO Võtab hetke/jooksva aja kujul AAAA-KK-PP TT:MM:SS (Y-m-d H:M:S)
    # xTODO Kui kasutaja sisestas nime, siis eemalda algusest ja lõpust tühikud
    # xTODO Tee andmebaasi ühendus ja lisa kirje tabelisse scores. Salvesta andmed tabelis ja sulge ühendus.
