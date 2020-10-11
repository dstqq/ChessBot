# mode`s: 1- ход на пустую клетку. 2- объеденение 2 фигур для хода на пустую клетку. 3- ход не на пустую клетку. 4- проверка на шах

import telebot
import test
from telebot import types
import time
import random
import const
import weapon_bot
import hero_bot
import string
import json
bot = telebot.TeleBot(const.tocken)

alf = {1: "a", 2: "b", 3: "c", 4: "d", 5: "e", 6: "f", 7: "g", 8: "h"}

figures = {"00": " ", "01": "♙", "02": "♗", "03": "♘", "04": "♖", "05": "♕", "06": "♔",
                      "11": "♟", "12": "♝", "13": "♞", "14": "♜", "15": "♛", "16": "♚"}


board = {"a1": "04", "b1": "03", "c1": "02", "d1": "05", "e1": "06", "f1": "02", "g1": "03", "h1": "04",
         "a2": "01", "b2": "01", "c2": "01", "d2": "01", "e2": "01", "f2": "01", "g2": "01", "h2": "01",
         "a3": "00", "b3": "00", "c3": "00", "d3": "00", "e3": "00", "f3": "00", "g3": "00", "h3": "00",
         "a4": "00", "b4": "00", "c4": "00", "d4": "00", "e4": "00", "f4": "00", "g4": "00", "h4": "00",
         "a5": "00", "b5": "00", "c5": "00", "d5": "00", "e5": "00", "f5": "00", "g5": "00", "h5": "00",
         "a6": "00", "b6": "00", "c6": "00", "d6": "00", "e6": "00", "f6": "00", "g6": "00", "h6": "00",
         "a7": "11", "b7": "11", "c7": "11", "d7": "11", "e7": "11", "f7": "11", "g7": "11", "h7": "11",
         "a8": "14", "b8": "13", "c8": "12", "d8": "15", "e8": "16", "f8": "12", "g8": "13", "h8": "14"}

"""board = {"a1" : "♖", "b1" : "♘", "c1" : "♗", "d1" : "♕", "e1" : "♔", "f1" : "♗", "g1" : "♘", "h1" : "♖",
         "a2" : "♙", "b2" : "♙" , "c2" : "♙", "d2" : "♙", "e2" : "♙", "f2" : "♙", "g2" : "♙", "h2" : "♙",
         "a3" : " ", "b3" : " " , "c3" : " ", "d3" : " ", "e3" : " ", "f3" : " ", "g3" : " ", "h3" : " ",
         "a4" : " ", "b4" : " " , "c4" : " ", "d4" : " ", "e4" : " ", "f4" : " ", "g4" : " ", "h4" : " ",
         "a5" : " ", "b5" : " " , "c5" : " ", "d5" : " ", "e5" : " ", "f5" : " ", "g5" : " ", "h5" : " ",
         "a6" : " ", "b6" : " " , "c6" : " ", "d6" : " ", "e6" : " ", "f6" : " ", "g6" : " ", "h6" : " ",
         "a7" : "♟", "b7" : "♟" , "c7" : "♟", "d7" : "♟", "e7" : "♟", "f7" : "♟", "g7" : "♟", "h7" : "♟",
         "a8" : "♜", "b8" : "♞" , "c8" : "♝", "d8" : "♛", "e8" : "♚", "f8" : "♝", "g8" : "♞", "h8" : "♜"}"""


def build_message_used(message):
    """
    Сообщение об использовании бота в каком-либо чате
    Full information about chat were bot was used
    """
    msg = (
        "В этом чате попытались воспользоваться ботом!\n"
        "Информация о чате:\n"
        "chat_title: " + f"<b>{message.chat.title}</b>\n"
        "chat_id: " + f"{message.chat.id}\n"
        "Информация о пользователе:\n"
        "full_name: " + f"<b>{message.from_user.first_name}" + " " + f"{message.from_user.last_name}</b>\n"
        "username: @" + f"{message.from_user.username}\n"
        "user_id: " + f"{message.from_user.id}\n"
        "text: " + f"{message.text}"
    )
    bot.send_message(const.admin, parse_mode="HTML", text=msg)

def load_json(file):
    with open(file, 'r') as f_obj:
        return json.load(f_obj)


def reg_new_game(message):
    with open("botinfo.json") as f_object:
        gameinfo = json.load(f_object)
    gamename = "game" + gameinfo["game"] + ".json"
    msg = (
        "Вы создали игру <b>№</b>" + f"<b>{gameinfo['game']}</b>\n"
        "Что б приглосить игрока, он должен отправить это сообщение в игрового бота"
    )
    bot.send_message(message.chat.id, parse_mode="HTML", text=msg)
    name = " "
    if str(message.from_user.first_name) != "None":
        name = str(message.from_user.first_name)
    if str(message.from_user.last_name) != "None":
        name += str(message.from_user.last_name)
    gamer = {"white": message.chat.id, "black": " ", "turn": "white", "nameWhite": name, "nameBlack": " ", "userWhite": str(message.from_user.username), "userBlack": " "}
    with open(gamename, 'w') as f_object:
        json.dump(gamer, f_object)


def init_board(game_num):
    filename = "board" + game_num + ".json"
    with open(filename, 'w') as f_obj:
        json.dump(board, f_obj)
    turnname = "turn" + game_num + ".json"
    with open(turnname, 'w') as f_object:
        json.dump(' ', f_object)

    castling = {1: "0", 2: "0", 3: "0", 4: "0", 5: "0", 6: "0"}
    castlingname = "castling" + game_num + ".json"
    with open(castlingname, 'w') as f_object:
        json.dump(castling, f_object)


def show_board(chat_id, b, game_num, mode, call):
    turnname = "turn" + game_num + ".json"
    pos = load_json(turnname)

    keyboardW = types.InlineKeyboardMarkup()  # Белая клава
    keyboardB = types.InlineKeyboardMarkup()  # Черная клава

    # ------------------------------------ПЕРВЫЙ РЯД---------------------------------------
    callback_button1 = types.InlineKeyboardButton(text=figures[b["a1"]], callback_data="a1")
    callback_button2 = types.InlineKeyboardButton(text=figures[b["b1"]], callback_data="b1")
    callback_button3 = types.InlineKeyboardButton(text=figures[b["c1"]], callback_data="c1")
    callback_button4 = types.InlineKeyboardButton(text=figures[b["d1"]], callback_data="d1")
    callback_button5 = types.InlineKeyboardButton(text=figures[b["e1"]], callback_data="e1")
    callback_button6 = types.InlineKeyboardButton(text=figures[b["f1"]], callback_data="f1")
    callback_button7 = types.InlineKeyboardButton(text=figures[b["g1"]], callback_data="g1")
    callback_button8 = types.InlineKeyboardButton(text=figures[b["h1"]], callback_data="h1")

    # ------------------------------------ВТОРОЙ РЯД---------------------------------------
    callback_button9 = types.InlineKeyboardButton(text=figures[b["a2"]], callback_data="a2")
    callback_button10 = types.InlineKeyboardButton(text=figures[b["b2"]], callback_data="b2")
    callback_button11 = types.InlineKeyboardButton(text=figures[b["c2"]], callback_data="c2")
    callback_button12 = types.InlineKeyboardButton(text=figures[b["d2"]], callback_data="d2")
    callback_button13 = types.InlineKeyboardButton(text=figures[b["e2"]], callback_data="e2")
    callback_button14 = types.InlineKeyboardButton(text=figures[b["f2"]], callback_data="f2")
    callback_button15 = types.InlineKeyboardButton(text=figures[b["g2"]], callback_data="g2")
    callback_button16 = types.InlineKeyboardButton(text=figures[b["h2"]], callback_data="h2")

    # ------------------------------------ТРЕТИЙ РЯД------------------==--------------------
    callback_button17 = types.InlineKeyboardButton(text=figures[b["a3"]], callback_data="a3")
    callback_button18 = types.InlineKeyboardButton(text=figures[b["b3"]], callback_data="b3")
    callback_button19 = types.InlineKeyboardButton(text=figures[b["c3"]], callback_data="c3")
    callback_button20 = types.InlineKeyboardButton(text=figures[b["d3"]], callback_data="d3")
    callback_button21 = types.InlineKeyboardButton(text=figures[b["e3"]], callback_data="e3")
    callback_button22 = types.InlineKeyboardButton(text=figures[b["f3"]], callback_data="f3")
    callback_button23 = types.InlineKeyboardButton(text=figures[b["g3"]], callback_data="g3")
    callback_button24 = types.InlineKeyboardButton(text=figures[b["h3"]], callback_data="h3")
    # ------------------------------------ЧЕТВЕРТЫЙ РЯД-------------------------------------
    callback_button25 = types.InlineKeyboardButton(text=figures[b["a4"]], callback_data="a4")
    callback_button26 = types.InlineKeyboardButton(text=figures[b["b4"]], callback_data="b4")
    callback_button27 = types.InlineKeyboardButton(text=figures[b["c4"]], callback_data="c4")
    callback_button28 = types.InlineKeyboardButton(text=figures[b["d4"]], callback_data="d4")
    callback_button29 = types.InlineKeyboardButton(text=figures[b["e4"]], callback_data="e4")
    callback_button30 = types.InlineKeyboardButton(text=figures[b["f4"]], callback_data="f4")
    callback_button31 = types.InlineKeyboardButton(text=figures[b["g4"]], callback_data="g4")
    callback_button32 = types.InlineKeyboardButton(text=figures[b["h4"]], callback_data="h4")

    # ------------------------------------ПЯТЫЙ РЯД-------------------------------------
    callback_button33 = types.InlineKeyboardButton(text=figures[b["a5"]], callback_data="a5")
    callback_button34 = types.InlineKeyboardButton(text=figures[b["b5"]], callback_data="b5")
    callback_button35 = types.InlineKeyboardButton(text=figures[b["c5"]], callback_data="c5")
    callback_button36 = types.InlineKeyboardButton(text=figures[b["d5"]], callback_data="d5")
    callback_button37 = types.InlineKeyboardButton(text=figures[b["e5"]], callback_data="e5")
    callback_button38 = types.InlineKeyboardButton(text=figures[b["f5"]], callback_data="f5")
    callback_button39 = types.InlineKeyboardButton(text=figures[b["g5"]], callback_data="g5")
    callback_button40 = types.InlineKeyboardButton(text=figures[b["h5"]], callback_data="h5")

    # ------------------------------------ШЕСТОЙ РЯД-------------------------------------
    callback_button41 = types.InlineKeyboardButton(text=figures[b["a6"]], callback_data="a6")
    callback_button42 = types.InlineKeyboardButton(text=figures[b["b6"]], callback_data="b6")
    callback_button43 = types.InlineKeyboardButton(text=figures[b["c6"]], callback_data="c6")
    callback_button44 = types.InlineKeyboardButton(text=figures[b["d6"]], callback_data="d6")
    callback_button45 = types.InlineKeyboardButton(text=figures[b["e6"]], callback_data="e6")
    callback_button46 = types.InlineKeyboardButton(text=figures[b["f6"]], callback_data="f6")
    callback_button47 = types.InlineKeyboardButton(text=figures[b["g6"]], callback_data="g6")
    callback_button48 = types.InlineKeyboardButton(text=figures[b["h6"]], callback_data="h6")

    # ------------------------------------СЕДЬМОЙ РЯД-------------------------------------
    callback_button49 = types.InlineKeyboardButton(text=figures[b["a7"]], callback_data="a7")
    callback_button50 = types.InlineKeyboardButton(text=figures[b["b7"]], callback_data="b7")
    callback_button51 = types.InlineKeyboardButton(text=figures[b["c7"]], callback_data="c7")
    callback_button52 = types.InlineKeyboardButton(text=figures[b["d7"]], callback_data="d7")
    callback_button53 = types.InlineKeyboardButton(text=figures[b["e7"]], callback_data="e7")
    callback_button54 = types.InlineKeyboardButton(text=figures[b["f7"]], callback_data="f7")
    callback_button55 = types.InlineKeyboardButton(text=figures[b["g7"]], callback_data="g7")
    callback_button56 = types.InlineKeyboardButton(text=figures[b["h7"]], callback_data="h7")

    # ------------------------------------ВОСЬМОЙ РЯД-------------------------------------
    callback_button57 = types.InlineKeyboardButton(text=figures[b["a8"]], callback_data="a8")
    callback_button58 = types.InlineKeyboardButton(text=figures[b["b8"]], callback_data="b8")
    callback_button59 = types.InlineKeyboardButton(text=figures[b["c8"]], callback_data="c8")
    callback_button60 = types.InlineKeyboardButton(text=figures[b["d8"]], callback_data="d8")
    callback_button61 = types.InlineKeyboardButton(text=figures[b["e8"]], callback_data="e8")
    callback_button62 = types.InlineKeyboardButton(text=figures[b["f8"]], callback_data="f8")
    callback_button63 = types.InlineKeyboardButton(text=figures[b["g8"]], callback_data="g8")
    callback_button64 = types.InlineKeyboardButton(text=figures[b["h8"]], callback_data="h8")

    if pos == " ":
        callback_button65 = types.InlineKeyboardButton(text="ХОД", callback_data="pass")
    else:
        callback_button65 = types.InlineKeyboardButton(text="ХОД" + figures[b[pos]], callback_data="pass")

    keyboardW.row(callback_button57, callback_button58, callback_button59, callback_button60, callback_button61, callback_button62, callback_button63, callback_button64)
    keyboardW.row(callback_button49, callback_button50, callback_button51, callback_button52, callback_button53, callback_button54, callback_button55, callback_button56)
    keyboardW.row(callback_button41, callback_button42, callback_button43, callback_button44, callback_button45, callback_button46, callback_button47, callback_button48)
    keyboardW.row(callback_button33, callback_button34, callback_button35, callback_button36, callback_button37, callback_button38, callback_button39, callback_button40)
    keyboardW.row(callback_button25, callback_button26, callback_button27, callback_button28, callback_button29, callback_button30, callback_button31, callback_button32)
    keyboardW.row(callback_button17, callback_button18, callback_button19, callback_button20, callback_button21, callback_button22, callback_button23, callback_button24)
    keyboardW.row(callback_button9, callback_button10, callback_button11, callback_button12, callback_button13, callback_button14, callback_button15, callback_button16)
    keyboardW.row(callback_button1, callback_button2, callback_button3, callback_button4, callback_button5, callback_button6, callback_button7, callback_button8)
    keyboardW.add(callback_button65)

    keyboardB.row(callback_button1, callback_button2, callback_button3, callback_button4, callback_button5, callback_button6, callback_button7, callback_button8)
    keyboardB.row(callback_button9, callback_button10, callback_button11, callback_button12, callback_button13, callback_button14, callback_button15, callback_button16)
    keyboardB.row(callback_button17, callback_button18, callback_button19, callback_button20, callback_button21, callback_button22, callback_button23, callback_button24)
    keyboardB.row(callback_button25, callback_button26, callback_button27, callback_button28, callback_button29, callback_button30, callback_button31, callback_button32)
    keyboardB.row(callback_button33, callback_button34, callback_button35, callback_button36, callback_button37, callback_button38, callback_button39, callback_button40)
    keyboardB.row(callback_button41, callback_button42, callback_button43, callback_button44, callback_button45, callback_button46, callback_button47, callback_button48)
    keyboardB.row(callback_button49, callback_button50, callback_button51, callback_button52, callback_button53, callback_button54, callback_button55, callback_button56)
    keyboardB.row(callback_button57, callback_button58, callback_button59, callback_button60, callback_button61, callback_button62, callback_button63, callback_button64)
    keyboardB.add(callback_button65)

    gamename = "game" + game_num + ".json"
    players = load_json(gamename)
    if players["turn"] == "white":
        t = "♔ Белого короля"
    else:
        t = "♚ Черного короля"
    msg = (
        "Шахматная дуэль между:\n"
        "Белый король: " + f'<a href=\'https://t.me/{players["userWhite"]}\'>{players["nameWhite"]}</a>\n'
        "<b>VS</b>\n"
        "Черный король: " + f'<a href=\'https://t.me/{players["userBlack"]}\'>{players["nameBlack"]}</a>\n'
        "Сейчас ход " + f"<b>{t}</b>"
    )
    if mode == "both":
        bot.send_message(int(players["white"]), parse_mode = "HTML", disable_web_page_preview = True, text = msg, reply_markup=keyboardW)
        bot.send_message(int(players["black"]), parse_mode = "HTML", disable_web_page_preview = True, text = msg, reply_markup=keyboardB)
    else:
        if chat_id == int(players["white"]):
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, parse_mode = "HTML", disable_web_page_preview = True, text=msg, reply_markup=keyboardW)
        elif chat_id == int(players["black"]):
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, parse_mode = "HTML", disable_web_page_preview = True, text=msg, reply_markup=keyboardB)

def get_turn(game_num):
    turnname = "turn" + game_num + ".json"
    try:
        turn = load_json(turnname)
    except FileNotFoundError:
        turn = " "

    return turn


def get_board(game_num):
    filename = "board" + game_num + ".json"
    try:
        b = load_json(filename)
    except FileNotFoundError:
        b = board

    return b

def save_board(b, game_num):
    filename = "board" +game_num +".json"
    with open(filename, 'w') as f_object:
        json.dump(b, f_object)

def save_turn(turn, game_num):
    turnname = "turn" + game_num + ".json"
    with open(turnname, 'w') as f_object:
        json.dump(turn, f_object)

def change_castling(turn, game_num):
    castlingname = "castling" + game_num + ".json"
    with open(castlingname) as f_object:
        castling = json.load(f_object)
    if turn == "a1":
        castling["1"] = "1"
    elif turn == "h1":
        castling["3"] = "1"
    elif turn == "a8":
        castling["4"] = "1"
    elif turn == "h8":
        castling["6"] = "1"
    elif turn == "e1":
        castling["2"] = "1"
    with open(castlingname, 'w') as f_object:
        json.dump(castling, f_object)


def change_turn(game_num):
    gamename = "game" + game_num + ".json"
    players = load_json(gamename)

    if players["turn"] == "white":
        players["turn"] = "black"
    elif players["turn"] == "black":
        players["turn"] = "white"

    with open(gamename, 'w') as f_object:
        json.dump(players, f_object)


def do_turn(chat_id, call, game_num):  # механизм перемещения фигуры
    turn = get_turn(game_num)
    b = get_board(game_num)

    b[call.data] = b[turn] 
    b[turn] = "00"
    turn = " "
    save_board(b, game_num)
    save_turn(turn, game_num)

    change_turn(game_num)

    show_board(chat_id, b, game_num, "both", call)


def show_white_transformation(call_data):
    keyboard = types.InlineKeyboardMarkup()

    callback_buttonQ = types.InlineKeyboardButton(text=figures["05"], callback_data="p05"+call_data)  # Королева
    callback_buttonE = types.InlineKeyboardButton(text=figures["02"], callback_data="p05"+call_data)  # Слон
    callback_buttonR = types.InlineKeyboardButton(text=figures["04"], callback_data="p04"+call_data)  # Ладья
    callback_buttonH = types.InlineKeyboardButton(text=figures["03"], callback_data="p03"+call_data)  # Конь

    keyboard.row(callback_buttonQ, callback_buttonE, callback_buttonR, callback_buttonH)

    return keyboard


def white_transformation(chat_id, call_data):  # ферзя, слона, ладью или коня
    keyboard = show_white_transformation(call_data)
    bot.send_message(chat_id=chat_id, text="Выбери фигуру: ",
                     reply_markup=keyboard)


def show_black_transformation(call_data):
    keyboard = types.InlineKeyboardMarkup()

    callback_buttonQ = types.InlineKeyboardButton(text=figures["15"], callback_data="p15"+call_data)  # Королева
    callback_buttonE = types.InlineKeyboardButton(text=figures["12"], callback_data="p15"+call_data)  # Слон
    callback_buttonR = types.InlineKeyboardButton(text=figures["14"], callback_data="p14"+call_data)  # Ладья
    callback_buttonH = types.InlineKeyboardButton(text=figures["13"], callback_data="p13"+call_data)  # Конь

    keyboard.row(callback_buttonQ, callback_buttonE, callback_buttonR, callback_buttonH)

    return keyboard


def black_transformation(chat_id, call_data):  # ферзя, слона, ладью или коня
    keyboard = show_black_transformation(call_data)
    bot.send_message(chat_id=chat_id, text="Выбери фигуру: ",
                     reply_markup=keyboard)


def physics_white_pawn(game_num, chat_id, call, x1, y1, x2, y2, mode):
    b = get_board(game_num)
    if mode == 1:
        if x1 != x2:  # если переходит в другой ряд
            bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                      text="Пешка не может переходить в другой ряд!")

        elif int(y2) < int(y1):  # если ход назад
            bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                      text="Пешка не может ходить назад!")

        elif y1 == "2" and (int(y2) - int(y1)) > 2:  # если при первом ходе пешки ходит более чем на 2
            bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                      text="Пешка не может ходить дальше чем на 2 клетки первый раз!")

        elif y1 == "2" and b[x1 + "3"] != "00":  # если при первом ходе на 2 клетки перед пешкой есть объект
            bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                      text="Пешка не может перепрыгивать фигуры!")

        elif y1 != "2" and (int(y2) - int(y1)) > 1:  # если ходит больше чем на 1 не в первый раз
            bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                      text="Пешка не может ходить дальше чем на 1 клетку!")

        else:  # если все хорошо то проходит
            if y2 == "8":
                white_transformation(chat_id, call.data)
            else:
                do_turn(chat_id, call, game_num)

    if mode == 3:
        i = 1  # x1
        j = 1  # x2
        while alf[i] != x1:
            i += 1
        while alf[j] != x2:
            j += 1
        if (j == i - 1 or j == i + 1) and int(y2) == int(y1) + 1:
            if y2 == "8":
                white_transformation(chat_id, call.data)
            else:
                do_turn(chat_id, call, game_num)
        else:
            bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                      text="Пешка не может так бить!")


def physics_black_pawn(game_num, chat_id, call, x1, y1, x2, y2, mode):
    b = get_board(game_num)
    if mode == 1:
        if x1 != x2:  # если переходит в другой ряд
            bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                      text="Пешка не может переходить в другой ряд!")

        elif int(y1) < int(y2):  # если ход назад
            bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                      text="Пешка не может ходить назад!")

        elif y1 == "7" and (int(y1) - int(y2)) > 2:  # если при первом ходе пешки ходит более чем на 2
            bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                      text="Пешка не может ходить дальше чем на 2 клетки первый раз!")

        elif y1 == "7" and b[x1 + "6"] != "00":  # если при первом ходе на 2 клетки перед пешкой есть объект
            bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                      text="Пешка не может перепрыгивать фигуры!")

        elif y1 != "7" and (int(y1) - int(y2)) > 1:  # если ходит больше чем на 1 не в первый раз
            bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                      text="Пешка не может ходить дальше чем на 1 клетку!")

        else:  # если все хорошо то проходит
            do_turn(chat_id, call, game_num)
            if y2 == "1":
                black_transformation(chat_id, call.data)
    if mode == 3:
        i = 1  # x1
        j = 1  # x2
        while alf[i] != x1:
            i += 1
        while alf[j] != x2:
            j += 1
        if (j == i - 1 or j == i + 1) and int(y2) == int(y1) - 1:
            do_turn(chat_id, call, game_num)
            if y2 == "1":
                black_transformation(chat_id, call.data)
        else:
            bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                      text="Пешка не может так бить!")

def physics_rook(game_num, chat_id, call, x1, y1, x2, y2, mode):  # x1, x2 - буквы y1, y2 - цифры
    turn = get_turn(game_num)
    b = get_board(game_num)

    if x1 != x2 and y1 != y2:  # обе координаты меняются
        if mode == 1 or mode == 3:
            bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                      text="Ладья так не ходит!")
        if mode == 2:
            bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                      text="Ферзь так не ходит!")
    if x1 == x2 and y1 != y2:  # ход по вертикали
        if int(y2) > int(y1):  # ход вверх
            i = int(y1) + 1
            while i < int(y2):
                if b[x1+str(i)] != "00":
                    if mode == 1 or mode == 3:
                        bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                                  text="Ладья не может перепрыгивать через фигуры!")
                    if mode == 2:
                        bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                                  text="Ферзь не может перепрыгивать через фигуры!")
                    break
                i += 1
            if i == int(y2):
                do_turn(chat_id, call, game_num)

        if int(y2) < int(y1):  # ход вниз
            i = int(y1) - 1
            while i != int(y2):
                if b[x1 + str(i)] != "00":
                    if mode == 1 or mode == 3:
                        bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                                  text="Ладья не может перепрыгивать через фигуры!")
                    if mode == 2:
                        bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                                  text="Ферзь не может перепрыгивать через фигуры!")
                    break
                i -= 1
            if i == int(y2):
                do_turn(chat_id, call, game_num)

    if x1 != x2 and y1 == y2:  # ход по горизонтали
        i = 1  # x1
        j = 1  # x2
        while alf[i] != x1:
            i += 1
        while alf[j] != x2:
            j += 1
        if i < j:  # x1 < x2, ход вправо
            i += 1
            while i != j:
                if b[alf[i]+y1] != "00":
                    if mode == 1 or mode == 3:
                        bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                                  text="Ладья не может перепрыгивать через фигуры!")
                    if mode == 2:
                        bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                                  text="Ферзь не может перепрыгивать через фигуры!")
                    break
                i += 1
            if i == j:
                do_turn(chat_id, call, game_num)
        if i > j:  # x1 > x2, ход влево
            j += 1
            while j != i:
                if b[alf[j]+y1] != "00":
                    if mode == 1 or mode == 3:
                        bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                                  text="Ладья не может перепрыгивать через фигуры!")
                    if mode == 2:
                        bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                                  text="Ферзь не может перепрыгивать через фигуры!")
                    break
                j += 1
            if i == j:
                do_turn(chat_id, call, game_num)


def physics_horses(game_num, chat_id, call, x1, y1, x2, y2, mode):
    i = 1
    j = 1
    while alf[i] != x1:
        i += 1
    while alf[j] != x2:
        j += 1
    if abs(j - i) + abs(int(y1) - int(y2)) == 3 and x1 != x2 and y1 != y2:
        do_turn(chat_id, call, game_num)
    else:
        if mode == 1:
            bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                      text="Конь так не ходит!")
        elif mode == 3:
            bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                      text="Конь не может бить эту фигуру!")

def physics_elefats(game_num, chat_id, call, x1, y1, x2, y2, mode):
    i = 1
    j = 1
    while alf[i] != x1:
        i += 1
    while alf[j] != x2:
        j += 1
    b = get_board(game_num)
    if abs(i - j) == abs(int(y1) - int(y2)) and x1 != x2 and y1 != y2:
        if int(y2) > int(y1) and j > i:  # ходит в сторону первой четверти
            k = 1
            while i + k != j:
                if b[alf[i + k] + str(int(y1) + k)] != "00":
                    if mode == 1 or mode == 3:
                        bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Слон не может перепрыгивать фигуры!")
                    elif mode == 2:
                        bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                                  text="Ферзь не может перепрыгивать фигуры!")
                    break
                k += 1
            if i + k == j:
                do_turn(chat_id, call, game_num)
        elif int(y2) < int(y1) and j > i:  # ходит в сторону второй четверти
            k = 1
            while i + k != j:
                if b[alf[i + k] + str(int(y1) - k)] != "00":
                    if mode == 1 or mode == 3:
                        bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                                  text="Слон не может перепрыгивать фигуры!")
                    elif mode == 2:
                        bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                                  text="Ферзь не может перепрыгивать фигуры!")
                    break
                k += 1
            if i + k == j:
                do_turn(chat_id, call, game_num)
        elif int(y2) < int(y1) and j < i:  # ходит в сторону третьей четверти
            k = 1
            while int(y1) - k != int(y2) or i - k != j:
                if b[alf[i - k] + str(int(y1) - k)] != "00":
                    if mode == 1 or mode == 3:
                        bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                                  text="Слон не может перепрыгивать фигуры!")
                    elif mode == 2:
                        bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                                  text="Ферзь не может перепрыгивать фигуры!")
                    break
                k += 1
            if int(y1) - k == int(y2) or i - k == j:
                do_turn(chat_id, call, game_num)
        elif int(y2) > int(y1) and j < i:  # ходит в сторону четвертой четверти
            k = 1
            while int(y1) + k != int(y2) or i - k != j:
                if b[alf[i - k] + str(int(y1) + k)] != "00":
                    if mode == 1 or mode == 3:
                        bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                                  text="Слон не может перепрыгивать фигуры!")
                    elif mode == 2:
                        bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                                  text="Ферзь не может перепрыгивать фигуры!")
                    break
                k += 1
            if int(y1) + k == int(y2) or i - k == j:
                do_turn(chat_id, call, game_num)
    else:
        if mode == 1 or mode == 3:
            bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                                    text="Слон так не ходит!")
        if mode == 2:
            physics_rook(game_num, chat_id, call, x1, y1, x2, y2, mode)


def physics_queens(game_num, chat_id, call, x1, y1, x2, y2, mode):
    i = 1
    j = 1
    while alf[i] != x1:
        i += 1
    while alf[j] != x2:
        j += 1
    b = get_board(game_num)

    physics_elefats(game_num, chat_id, call, x1, y1, x2, y2, mode)
    turn = get_turn(game_num)
    if turn != " ":
        physics_rook(game_num, chat_id, call, x1, y1, x2, y2, mode)



def physics_king(game_num, chat_id, call, x1, y1, x2, y2, mode):
    i = 1
    j = 1
    while alf[i] != x1:
        i += 1
    while alf[j] != x2:
        j += 1
    turn = get_turn(game_num)
    b = get_board(game_num)
    castlingname = "castling.json"
    with open(castlingname) as f_object:
        castling = json.load(f_object)
    if b[turn] == "06" and call.data == "g1" and castling["2"] == "0":  # если белый король делает короткую рокировку
        print(1)
        if castling["2"] == "0" and castling["3"] == "0":  # если король и правая ладья не ходили за игру
            if b["f1"] == "00":  # Если поле f1 пустое, то можно делать рокировку
                b["e1"] = "00"  # вместо короля
                b["f1"] = "04"  # новая ладья
                b["g1"] = "06"  # новый король
                b["h1"] = "00"  # вместо ладьи
                save_board(b, game_num)
                change_turn(game_num)
                show_board(chat_id, b, game_num, "both", call)
                bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                          text="Короткая рокировка успешна!")
                change_castling(turn, game_num)
            else:
                bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                          text="Рокировка невозможна, препядствие на f1!")
        else:
            if castling["2"] == "1":
                bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                          text="Рокировка невозможна, король уже покидал свою позицию")
            else:
                bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                          text="Рокировка невозможна, ладья уже покидала свою позицию")

    elif b[turn] == "06" and call.data == "c1" and castling["2"] == "0":  # если белый король делает длинную рокировку
        if castling["1"] == "0" and castling["2"] == "0":  # если король и левая ладья не ходили за игру
            if b["b1"] == "00" and b["d1"] == "00":  #  Если поле f1 пустое, то можно делать рокировку
                b["a1"] = "00"  # вместо ладьи
                b["c1"] = "06"  # новый король
                b["d1"] = "04"  # новая ладьи
                b["e1"] = "00"  # вместо короля
                save_board(b, game_num)
                change_turn(game_num)
                show_board(chat_id, b, game_num, "both", call)
                bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                          text="Длинная рокировка успешна!")
                change_castling(turn, game_num)
            else:
                bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                          text="Рокировка невозможна, препядствие на пути!")
        else:
            if castling["2"] == "1":
                bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                          text="Рокировка невозможна, король уже покидал свою позицию")
            else:
                bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                          text="Рокировка невозможна, ладья уже покидала свою позицию")
    if b[turn] == "16" and call.data == "g8" and castling["5"] == "0":  # если ЧЕРНЫЙ король делает короткую рокировку
        print(1)
        if castling["5"] == "0" and castling["6"] == "0":  # если король и правая ладья не ходили за игру
            if b["f8"] == "00":  # Если поле f8 пустое, то можно делать рокировку
                b["e8"] = "00"  # вместо короля
                b["f8"] = "14"  # новая ладья
                b["g8"] = "16"  # новый король
                b["h8"] = "00"  # вместо ладьи
                save_board(b, game_num)
                change_turn(game_num)
                show_board(chat_id, b, game_num, "both", call)
                bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                          text="Короткая рокировка успешна!")
                change_castling(turn, game_num)
            else:
                bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                          text="Рокировка невозможна, препядствие на f8!")
        else:
            if castling["5"] == "1":
                bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                          text="Рокировка невозможна, король уже покидал свою позицию")
            else:
                bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                          text="Рокировка невозможна, ладья уже покидала свою позицию")
    elif b[turn] == "16" and call.data == "c8" and castling["5"] == "0":  # если Черный король делает длинную рокировку
        if castling["4"] == "0" and castling["5"] == "0":  # если король и левая ладья не ходили за игру
            if b["b8"] == "00" and b["d8"] == "00":  # Если поле f1 пустое, то можно делать рокировку
                b["a8"] = "00"  # вместо ладьи
                b["c8"] = "16"  # новый король
                b["d8"] = "14"  # новая ладьи
                b["e8"] = "00"  # вместо короля
                save_board(b, game_num)
                change_turn(game_num)
                show_board(chat_id, b, game_num, "both", call)
                bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                          text="Длинная рокировка успешна!")
                change_castling(turn, game_num)
            else:
                bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                          text="Рокировка невозможна, препядствие на пути!")
        else:
            if castling["5"] == "1":
                bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                          text="Рокировка невозможна, король уже покидал свою позицию")
            else:
                bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                          text="Рокировка невозможна, ладья уже покидала свою позицию")
    else:
        if abs(i-j)+abs(int(y1)-int(y2)) < 3 and (abs(i-j) == 0 and abs(int(y1)-int(y2)) == 1) or (abs(i-j) == 1 and abs(int(y1)-int(y2) == 0)) or (abs(i-j) == 1 and abs(int(y1)-int(y2)) == 1):
            do_turn(chat_id, call, game_num)
            change_castling(turn, game_num)
        else:
            if mode == 1:
                bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                          text="Король так не ходит!")


@bot.message_handler(commands=['cr'])
def create_message(message):
    game = {"game" : "1"}
    with open("botinfo.json", 'w') as f_object:
        json.dump(game, f_object)
    players = {"386760687" : "1", "736079601": "1"}
    with open("players.json", 'w') as f_object:
        json.dump(players, f_object)


@bot.message_handler(commands=['start', 'settings'])
def start_message(message):
    msg = (
        "Hi there, " + f"<b>{message.from_user.first_name}" + " " + f"{message.from_user.last_name}</b>!\n"
        "Choose your language:\n"
        "🇷🇺 - /set_language_rus\n"
        "🇺🇸 - /set_language_eng\n\n"
        "For start game tap /startgame"
    )
    bot.send_message(message.chat.id, parse_mode="HTML", text=msg)

@bot.message_handler(commands=['startgame'])
def start_message(message):
    reg_new_game(message)
    """init_board()
    keyboard = show_board(message.chat.id, board)
    bot.send_message(message.chat.id, "Выбери поле: ", reply_markup=keyboard)"""


@bot.message_handler(commands=['about_withdrawing'])
async def about_withdrawing(message: types.Message):
    if await is_access_forbidden(message):
        return
    ans = (
        'Бот может выдавать ссылки на депозит и выдачу ресурсов. Для этого нужно написать в '
        'чат: "дай {код итема} {количество}". Вы можете отправить запрос на выдачу больше одного итема. Если вы '
        'запросите только один итем, то бот даст ссылки и на выдачу, и на сдачу.'
        '\n\nК сожалению, пока что бот не умеет определять, верен ли ваш запрос, '
        'поэтому заботьтьесь сами об этом вопросе (но мы планируем скоро это исправить).'
    )
    await message.reply(ans, reply=False)


@bot.callback_query_handler(func=lambda call: True)  # call
def callback_inline(call):
    # Если сообщение из чата с ботом
    if call.message:
        if call.data:
            # print(call.data)
            chat_id = call.message.chat.id
            with open("players.json") as f_object:
                play = json.load(f_object)
            game_num = play[str(chat_id)]
            print(game_num)
            filename = "board" + game_num +".json"
            turnname = "turn" + game_num + ".json"
            turn = get_turn(game_num)
            with open(filename) as f_object:
                b = json.load(f_object)
            gamename = "game" + game_num + ".json"
            with open(gamename) as f_object:
                players = json.load(f_object)
            if players[players["turn"]] != call.message.chat.id:  # проверка чей ход
                bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                          text="Сейчас не ваш ход!")
            else:
                if call.data[0] == "p" and call.data != "pass":  # превращение пешки
                    b[call.data[3:5]] = call.data[1:3]
                    save_board(b, game_num)
                    show_board(chat_id, b, game_num, "both", call)
                    change_turn(game_num)
                if turn == " ":  # если фигура не выбрана
                    if call.data == "pass":
                        print("p")
                        pass
                    elif b[call.data] != "00":  # если выбрано не пустое поле для выбора фигуры

                        if players["turn"] == "white" and b[call.data][0] == "1":  # белый ходит черными
                            bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                                      text="Фигура не выбрана, ходить фигурами другого цвета если что нельзя!")
                        elif players["turn"] == "black" and b[call.data][0] == "0":  # черный ходит белыми
                            bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                                      text="Фигура не выбрана, ходить фигурами другого цвета если что нельзя!")
                        else:
                            bot.send_message(chat_id, b[call.data])  # отправка выбранной фигуры
                            bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Отлично, ты выбрал " + figures[b[call.data]] + ", теперь выбери куда походить")
                            with open(turnname, 'w') as f_obj:
                                json.dump(call.data, f_obj)
                            show_board(chat_id, b, game_num, str(chat_id), call)
                    elif b[call.data] == "00":  # пустое поле
                        bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Выбери не пустое поле!")

                if turn != " ":  # если фигура выбрана
                    x1 = turn[0]  # буква была
                    y1 = turn[1]  # цифра была

                    x2 = call.data[0]  # буква стала
                    y2 = call.data[1]  # цифра стала
                    if call.data == "pass":  # если нажата кнопка ХОД, для сброса выбранной фигуры
                        save_turn(" ", game_num)
                        show_board(chat_id, b, game_num, str(chat_id), call)


                    elif b[call.data] == "00":  # даелается ход на пустую клетку

                        if b[turn] == "01":  # если ход БЕЛОЙ пешкой (тузада)
                            physics_white_pawn(game_num, chat_id, call, x1, y1, x2, y2, 1)

                        elif b[turn] == "11":  # если ход ЧЕРНОЙ пешкой (тузада)
                            physics_black_pawn(game_num, chat_id, call, x1, y1, x2, y2, 1)

                        elif b[turn] == "04" or b[turn] == "14":  # ладьи
                            physics_rook(game_num, chat_id, call, x1, y1, x2, y2, 1)

                        elif b[turn] == "03" or b[turn] == "13":  # кони
                            physics_horses(game_num, chat_id, call, x1, y1, x2, y2, 1)

                        elif b[turn] == "02" or b[turn] == "12":  # слоны
                            physics_elefats(game_num, chat_id, call, x1, y1, x2, y2, 1)

                        elif b[turn] == "06" or b[turn] == "16":  # короли
                            physics_king(game_num, chat_id, call, x1, y1, x2, y2, 1)

                        elif b[turn] == "05" or b[turn] == "15":  # ферзи
                            physics_queens(game_num, chat_id, call, x1, y1, x2, y2, 2)

                    elif b[call.data] != "00":  # если ход не на пустую клетку
                        if b[call.data][0] == b[turn][0]:  # если выбрана фигура того же цвета
                            bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                                      text="Отлично, ты выбрал " + figures[
                                                          b[call.data]] + ", теперь выбери куда походить")
                            with open(turnname, 'w') as f_obj:
                                json.dump(call.data, f_obj)
                            show_board(chat_id, b, game_num, str(chat_id), call)
                        if b[call.data][0] != b[turn][0]:  # если выбрана фигура другого цвета
                            if b[turn] == "03" or b[turn] == "13":  # кони
                                physics_horses(game_num, chat_id, call, x1, y1, x2, y2, 3)

                            elif b[turn] == "02" or b[turn] == "12":  # слоны
                                physics_elefats(game_num, chat_id, call, x1, y1, x2, y2, 3)

                            elif b[turn] == "04" or b[turn] == "14":  # ладьи
                                physics_rook(game_num, chat_id, call, x1, y1, x2, y2, 3)

                            elif b[turn] == "05" or b[turn] == "15":  # ферзи
                                physics_queens(game_num, chat_id, call, x1, y1, x2, y2, 3)

                            elif b[turn] == "01":  # БЕЛАЯ пешка тузада
                                physics_white_pawn(game_num, chat_id, call, x1, y1, x2, y2, 3)

                            elif b[turn] == "11":  # ЧЕРНАЯ пешка тузада
                                physics_black_pawn(game_num, chat_id, call, x1, y1, x2, y2, 3)


@bot.message_handler(content_types=['text'])
def hahatalka(message):
    # print(message)
    s = message.text
    if s == "oplot":
        bot.send_message(const.admin, 'oplot')
    try:
        if message.forward_from.id == const.bot and s.find("Что б приглосить игрока") != -1:
            gamename = "game" + s[s.find("№")+1:s.find("Что б приглосить игрока")-1] + ".json"
            # print(gamename)
            init_board(s[s.find("№")+1:s.find("Что б приглосить игрока")-1])

            with open(gamename) as f_object:
                players = json.load(f_object)
            players["black"] = message.from_user.id
            name = " "
            if str(message.from_user.first_name) != "None":
                name = str(message.from_user.first_name)
            if str(message.from_user.last_name) != "None":
                name += str(message.from_user.last_name)
            players["nameBlack"] = name
            players["userBlack"] = str(message.from_user.username)
            with open(gamename, 'w') as f_object:
                json.dump(players, f_object)
            show_board(message.chat.id, board, s[s.find("№") + 1:s.find("Что б приглосить игрока") - 1], "both", 1)
    except AttributeError:
        pass


bot.polling(none_stop=True)
