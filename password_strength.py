import re


def load_wordlist_file(filepath):
    wordlist_set = set()
    with open(filepath) as file:
        for line in file.readlines():
            wordlist_set.add(line.strip())
    return wordlist_set


def get_password_strength(password):
    count = 0
    password_length = len(password)

    if password_length > 3:
        count += 1
    if password_length > 6:
        count += 1
    if password_length > 10:
        count += 1
    if password_length > 18:
        count += 1

    if password not in most_common_passwords:
        count += 1

    if password not in ru_en_wordlist:
        count += 1

    if not password.islower() and not password.isupper():
        count += 1

    if re.search('\d', password):
        count += 1

    if re.search('[^a-zа-яё0-9]', password, re.IGNORECASE):
        count += 1

    if re.search('[a-z]', password, re.IGNORECASE) and re.search('[а-яё]', password, re.IGNORECASE):
        count += 1

    return count


if __name__ == '__main__':
    most_common_passwords = load_wordlist_file('10000_common_passwords.txt')
    ru_en_wordlist = load_wordlist_file('russian_words.txt') | load_wordlist_file(
        'english_words.txt') | load_wordlist_file('translit_words.txt')

    while 1:
        password = input('Введите пароль: ')
        if password in ('quit', 'exit'):
            print('Программа завершена.')
            break
        score = get_password_strength(password)
        print('Сложность вашего пароля: {}/10.'.format(score))
