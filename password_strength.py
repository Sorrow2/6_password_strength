import re


def load_wordlist_file(filepath):
    wordlist_set = set()
    with open(filepath) as file:
        for line in file.readlines():
            wordlist_set.add(line.strip())
    return wordlist_set


def check_upper_and_lower_case(password):
    return not password.islower() and not password.isupper()


def check_special_characters(password):
    return re.search('[^a-zа-яё0-9]', password, re.IGNORECASE)


def check_digits(password):
    return re.search('\d', password)


def check_russian_and_english_letters(password):
    return re.search('[a-z]', password, re.IGNORECASE) and re.search('[а-яё]', password, re.IGNORECASE)


def check_date_and_plate_number(password):
    return re.match('\d+(января|февраля|марта|апреля|мая|июня|июля|августа|сентября|октября|ноября|декабря|rus|рус)',
                    password, re.IGNORECASE)


def get_password_strength(password):
    password_length = len(password)

    if password_length < 6:
        return 0, 'Длина пароля слишком маленькая.'

    if password in most_common_passwords:
        return 0, 'Этот пароль один из наиболее часто используемых.'

    count = 1
    if password_length > 10:
        count += 1

    if password not in ru_en_wordlist:
        count += 1

    if not check_date_and_plate_number(password):
        count += 1

    if check_upper_and_lower_case(password):
        count += 1

    if check_digits:
        count += 1

    if check_special_characters(password):
        count += 2

    if check_russian_and_english_letters(password):
        count += 2

    return count, ''


if __name__ == '__main__':
    most_common_passwords = load_wordlist_file('10000_common_passwords.txt')
    ru_en_wordlist = load_wordlist_file('russian_words.txt') | load_wordlist_file(
        'english_words.txt') | load_wordlist_file('translit_words.txt')

    while 1:
        password = input('Введите пароль: ').strip()
        if password in ('quit', 'exit'):
            print('Программа завершена.')
            break
        score, msg = get_password_strength(password)
        print('Сложность вашего пароля: {}/10. {}'.format(score, msg))
