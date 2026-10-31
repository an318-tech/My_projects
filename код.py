import random

# Функция для прочтения слов из файла
def load_words(filename):
    words = []
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            # возвращаю список строк
            lines = f.readlines()
            # прохожу по списку
            for line in lines:
                # убираю пробелы и привожу к нижнему регистру
                cleaned = line.strip()
                cleaned = cleaned.lower()
                # если строка пустая, пропускаем ее
                if cleaned:
                    words.append(cleaned)
    # Вызываю пустой список если файл не найден
    except FileNotFoundError:
        print('Файл не найден')
        return []
    # Вызываю пустой список если проблема в кодировке
    except UnicodeDecodeError:
        print('Не удалось прочитать файл')
        return []

    # Вызываю готовый список слов
    return words

# Функция которая выбирает рандомное слово
def choose_word(words):
    # проверяю есть ли слова в файле
    if not words:
        print('Нет слов')
        return None
    # вывожу случайный элемент из списка
    return random.choice(words)

# функция которая показывает текущее состояние игры
def display_game_state(secret_word, guessed_letters, attempts_left=5):
    displayed = []
    # прохожусь по каждой букве в загаданном слове
    for letter in secret_word:
        # если буква есть добавляю в список
        if letter in guessed_letters:
            displayed.append(letter)
        # если нет добавляю символ _
        else:
            displayed.append('_')
    # делаю пробелы между буквами
    word_line = ' '.join(displayed)
    # список угаданных букв
    if guessed_letters:
        guessed_line = ', '.join(sorted(guessed_letters))
    else:
        guessed_line = '(пока нет угаданных букв)'

    print('\n--- Состояние игры ---')
    print(f'Слово: {word_line}')
    print(f'Угаданные буквы: {guessed_line}')
    print(f'Попыток осталось: {attempts_left}')
    print('______________________\n')

# функция запрашивает у игрока букву и возвращает ее
def get_player_guess(guessed_letters):
    while True:
        # запрашиваю у игрока букву
        user_input = input('Введите одну букву: ')
        # проверяю длину
        if len(user_input) != 1:
            print('Пожалуйста, введите одну букву')
            continue # переходим к следующей итерации цикла

        # проверяю что это буква
        if not user_input.isalpha():
            print('Это не буква. Пожалуйста введите букву')
            continue

        # привожу к нижнему регистру
        letter = user_input.lower()

        # проверяю не называл ли игрок эту букву
        if letter in guessed_letters:
            print(f'Вы уже называли букву: {letter}')
            continue

        return letter

# основная логика одного раунда игры
def play_round(word):
    # множество для названных букв
    guessed_letters = set()
    # классическое число попыток
    attempts_left = 5

    # основной игровой цикл, играем пока есть попытки
    while attempts_left > 0 :
        # показываю текущее состояние игры
        display_game_state(word, guessed_letters, attempts_left)
        
        # получаю проверенную букву от игрока
        letter = get_player_guess(guessed_letters)
        
        # добавляю букву в множество угаданных
        guessed_letters.add(letter)

        # проверяю есть ли буквы в слове
        if letter in word:
            print('Угадали!')
            # проверка на победу. все буквы угаданы
            if set(word).issubset(guessed_letters):
                # показываю финальное состояние
                display_game_state(word, guessed_letters, attempts_left)
                print('Поздравляем! Вы угадали все слово') 
                return 'win'

        else:
            # буквы нет в слове уменьшаем попытки
            attempts_left -= 1
            print(f'Мимо! Осталось попыток: {attempts_left}')

    # если попытки закончились:
    display_game_state(word, guessed_letters, attempts_left)
    print(f'Вы проиграли. Загаданное слово было: {word}')
    return 'lose'

# повторная игра
def main():
    filename = 'words.txt'
    # загружаю слова из файла один раз
    words_list = load_words(filename)

    if not words_list:
        print('Нет слов для игры')
        return
    
    wins = 0
    losses = 0
    
    # бесконечный цикл для повторных игр
    while True:
        # выбираю новое слово для раунда
        secret_word = choose_word(words_list)
        if secret_word is None:
            print('Не удалось выбрать слово')
            break

        # запускаю раунд
        result = play_round(secret_word)

        # победы и поражения
        if result == 'win':
            wins += 1
        else:
            losses += 1

        answer = input('Сыграем еще раз? (да/нет)').strip().lower()

        # набор допустимых вариантов 'да'
        yes_variants = {"да", "д", "y", "yes"}

        # если ответ не входит в варианты 'да' выходим из игры
        if answer not in yes_variants:
            print(f'Спасибо за игру! До встречи!\nВаша статистика: {wins} побед, {losses} поражений')
            break

if __name__ == '__main__':
    main()