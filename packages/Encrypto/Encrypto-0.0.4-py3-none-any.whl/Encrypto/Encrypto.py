import random


class Decrypto:
    def __init__(self, _str, _key=f"{random.randint(27, 100)},{random.randint(27, 100)},{random.randint(27, 100)},"
                                  f"{random.randint(27, 100)},{random.randint(27, 100)},{random.randint(27, 100)},"
                                  f"{random.randint(27, 100)},{random.randint(27, 100)},{random.randint(27, 100)}"):
        self.key: str = _key
        self.string: str = _str
        self.eval = 0

    def de_multiplier(self, ab_key: list, word: list):
        word_old = []
        if self.eval == 0:
            for i in word:
                i /= int(ab_key[0])
                i = int(i)
                word_old.append(i)
            self.eval = 1
        elif self.eval == 1:
            for i in word:
                i /= int(ab_key[1])
                i = int(i)
                word_old.append(i)
            self.eval = 0

        return word_old

    def handle_key(self, key: str):
        global de_a_mult, de_b_mult, de_c_mult, de_d_mult, de_e_mult, de_f_mult, de_a_mult_str
        key_list = (key.split(","))
        counter = 0
        de_mult_a_b = []
        for i in key_list:
            if counter == 0:
                de_a_mult = int(i)
                counter += 1
            elif counter == 1:
                de_b_mult = int(i)
                counter += 1
            elif counter == 2:
                de_c_mult = int(i)
                counter += 1
            elif counter == 3:
                de_d_mult = int(i)
                counter += 1
            elif counter == 4:
                de_e_mult = int(i)
                counter += 1
            elif counter == 5:
                de_f_mult = int(i)
                counter += 1
            elif counter == 6:
                de_a_mult_str = int(i)
                counter += 1
            elif counter == 7:
                mult_a = int(i)
                de_mult_a_b.append(mult_a)
                counter += 1
            elif counter == 8:
                mult_b = int(i)
                de_mult_a_b.append(mult_b)
            else:
                x_mult = 0

        return de_a_mult, de_b_mult, de_c_mult, de_d_mult, de_e_mult, de_f_mult, de_a_mult_str, de_mult_a_b

    def decrypt(self, str_: str):
        de_a_mult, de_b_mult, de_c_mult, de_d_mult, de_e_mult, de_f_mult, de_a_mult_str, de_mult_a_b = self.handle_key(
            key=self.key)
        str_ = str_.split(",")

        multiplied = []
        for ii in str_:
            ii2 = int(ii)
            mult = int(de_a_mult_str)
            ii3 = ii2 / mult
            multiplied.append(ii3)
        new2 = self.de_multiplier(ab_key=de_mult_a_b, word=multiplied)

        de_hexed = []
        for de_hex in new2:
            if de_hex == 1:
                let = "a"
            elif de_hex == 2:
                let = "b"
            elif de_hex == 3:
                let = "c"
            elif de_hex == 4:
                let = "d"
            elif de_hex == 5:
                let = "e"
            elif de_hex == 6:
                let = "f"
            elif de_hex == 7:
                let = "g"
            elif de_hex == 8:
                let = "h"
            elif de_hex == 9:
                let = "i"
            elif de_hex == int(de_a_mult):
                let = "j"
            elif de_hex == int(de_b_mult):
                let = "k"
            elif de_hex == int(de_c_mult):
                let = "l"
            elif de_hex == int(de_d_mult):
                let = "m"
            elif de_hex == int(de_e_mult):
                let = "n"
            elif de_hex == int(de_f_mult):
                let = "o"
            elif de_hex == 10:
                let = "p"
            elif de_hex == 11:
                let = "q"
            elif de_hex == 12:
                let = "r"
            elif de_hex == 13:
                let = "s"
            elif de_hex == 14:
                let = "t"
            elif de_hex == 15:
                let = "u"
            elif de_hex == 16:
                let = "v"
            elif de_hex == 17:
                let = "w"
            elif de_hex == 18:
                let = "x"
            elif de_hex == 19:
                let = "y"
            elif de_hex == 20:
                let = "z"
            else:
                let = "?"
            de_hexed.append(let)

        new = ""
        for i in de_hexed:
            i2 = str(i)
            new += i2
        return new

    def process(self):
        dec_words = []
        string = self.string.lower()
        words = string.split(",__")
        del words[len(words)-1]
        for word in words:
            old_word = self.decrypt(str_=word)
            dec_words.append(old_word)
            dec_words.append(" ")
        new = ""
        for i in dec_words:
            new += i
        return new


class Encrypto:
    def __init__(self, _key=f"{random.randint(1, 100)},{random.randint(1, 100)},{random.randint(1, 100)},"
                            f"{random.randint(1, 100)},{random.randint(1, 100)},{random.randint(1, 100)},"
                            f"{random.randint(1, 100)},{random.randint(1, 100)},{random.randint(1, 100)}", _str="word"):
        self.key: str = _key
        self.string: str = _str
        self.eval = 0

    def multiplier(self, ab_key: list, word: list):
        word_new = []
        if self.eval == 0:
            for i in word:
                i *= int(ab_key[0])
                word_new.append(i)
            self.eval = 1
        elif self.eval == 1:
            for i in word:
                i *= int(ab_key[1])
                word_new.append(i)
            self.eval = 0
        return word_new

    def handle_key(self, key: str):
        global a_mult, b_mult, c_mult, d_mult, e_mult, f_mult, a_mult_str
        key_list = (key.split(","))
        counter = 0
        mult_a_b = []
        for i in key_list:
            if counter == 0:
                a_mult = int(i)+21
                counter += 1
            elif counter == 1:
                b_mult = int(i)+21
                counter += 1
            elif counter == 2:
                c_mult = int(i)+21
                counter += 1
            elif counter == 3:
                d_mult = int(i)+21
                counter += 1
            elif counter == 4:
                e_mult = int(i)+21
                counter += 1
            elif counter == 5:
                f_mult = int(i)+21
                counter += 1
            elif counter == 6:
                a_mult_str = int(i)+21
                counter += 1
            elif counter == 7:
                mult_a = int(i)+21
                mult_a_b.append(mult_a)
                counter += 1
            elif counter == 8:
                mult_b = int(i)+21
                mult_a_b.append(mult_b)
            else:
                x_mult = 0

        return a_mult, b_mult, c_mult, d_mult, e_mult, f_mult, a_mult_str, mult_a_b

    def encrypt(self, word):
        global new2
        a_mult, b_mult, c_mult, d_mult, e_mult, f_mult, a_mult_str, mult_a_b = self.handle_key(self.key)
        ints = []
        for letter in word:
            if letter == "a":
                a = 1
            elif letter == "b":
                a = 2
            elif letter == "c":
                a = 3
            elif letter == "d":
                a = 4
            elif letter == "e":
                a = 5
            elif letter == "f":
                a = 6
            elif letter == "g":
                a = 7
            elif letter == "h":
                a = 8
            elif letter == "i":
                a = 9
            elif letter == "j":
                a = 10
            elif letter == "k":
                a = 11
            elif letter == "l":
                a = 12
            elif letter == "m":
                a = 13
            elif letter == "n":
                a = 14
            elif letter == "o":
                a = 15
            elif letter == "p":
                a = 16
            elif letter == "q":
                a = 17
            elif letter == "r":
                a = 18
            elif letter == "s":
                a = 19
            elif letter == "t":
                a = 20
            elif letter == "u":
                a = 21
            elif letter == "v":
                a = 22
            elif letter == "w":
                a = 23
            elif letter == "x":
                a = 24
            elif letter == "y":
                a = 25
            elif letter == "z":
                a = 26
            else:
                a = 0
            ints.append(a)
        del a

        hexed = []
        for hexed_ in ints:
            f = hex(hexed_)
            hexed.append(f)

        replced = []
        for replaced_ in hexed:
            if replaced_ == '0x1':
                a = 1
            elif replaced_ == '0x2':
                a = 2
            elif replaced_ == '0x3':
                a = 3
            elif replaced_ == '0x4':
                a = 4
            elif replaced_ == '0x5':
                a = 5
            elif replaced_ == '0x6':
                a = 6
            elif replaced_ == '0x7':
                a = 7
            elif replaced_ == '0x8':
                a = 8
            elif replaced_ == '0x9':
                a = 9
            elif replaced_ == '0xa':
                a = a_mult
            elif replaced_ == '0xb':
                a = b_mult
            elif replaced_ == '0xc':
                a = c_mult
            elif replaced_ == '0xd':
                a = d_mult
            elif replaced_ == '0xe':
                a = e_mult
            elif replaced_ == '0xf':
                a = f_mult
            elif replaced_ == '0x10':
                a = 10
            elif replaced_ == '0x11':
                a = 11
            elif replaced_ == '0x12':
                a = 12
            elif replaced_ == '0x13':
                a = 13
            elif replaced_ == '0x14':
                a = 14
            elif replaced_ == '0x15':
                a = 15
            elif replaced_ == '0x16':
                a = 16
            elif replaced_ == '0x17':
                a = 17
            elif replaced_ == '0x18':
                a = 18
            elif replaced_ == '0x19':
                a = 19
            else:
                a = 0
            replced.append(a)

        multiplied = []
        for ii in replced:
            ii2 = int(ii)
            mult = int(a_mult_str)
            ii3 = ii2 * mult
            multiplied.append(ii3)
        new2 = self.multiplier(ab_key=mult_a_b, word=multiplied)

        new = ""
        for i in new2:
            i2 = str(i)
            new += i2 + ","
        return new

    def process(self):
        enc_words = []
        words = self.string.split(" ")
        for word in words:
            new_word = self.encrypt(word.lower())
            enc_words.append(new_word)
            enc_words.append("__")
        new = ""
        for i in enc_words:
            new += i

        key_list = (self.key.split(","))
        new_w = ""
        new_a = []
        for i in key_list:
            a: int = int(i) + 21
            b: str = str(a)
            new_a.append(b)
            new_a.append(",")
        new_a = new_a[0:len(new_a)-1]
        for c in new_a:
            new_w += c
        return new, new_w


"""
word, key = Encrypto(_str=input("Word>>")).process()
print(word)
print(Decrypto(_str=word, _key=key).process())
"""
