def transcript(word):
    new_word_letters=[]
    word=word.lower()
    word_chars=list(word)
    for letter in word_chars:
        if letter=='а':
            new_word_letters.append('a')
        elif letter=='б':
            new_word_letters.append('b')
        elif letter=='в':
            new_word_letters.append('v')
        elif letter=='г':
            new_word_letters.append('g')
        elif letter=='д':
            new_word_letters.append('d')
        elif letter=='е':
            new_word_letters.append('e')
        elif letter=='ё':
            new_word_letters.append('jo')
        elif letter=='ж':
            new_word_letters.append('zh')
        elif letter=='з':
            new_word_letters.append('z')
        elif letter=='и':
            new_word_letters.append('i')
        elif letter=='й':
            new_word_letters.append('i')
        elif letter=='к':
            new_word_letters.append('k')
        elif letter=='л':
            new_word_letters.append('l')
        elif letter=='м':
            new_word_letters.append('m')
        elif letter=='н':
            new_word_letters.append('n')
        elif letter=='о':
            new_word_letters.append('o')
        elif letter=='п':
            new_word_letters.append('p')
        elif letter=='р':
            new_word_letters.append('r')
        elif letter=='с':
            new_word_letters.append('s')
        elif letter=='т':
            new_word_letters.append('t')
        elif letter=='у':
            new_word_letters.append('u')
        elif letter=='ф':
            new_word_letters.append('f')
        elif letter=='х':
            new_word_letters.append('x')
        elif letter=='ц':
            new_word_letters.append('c')
        elif letter=='ч':
            new_word_letters.append('ch')
        elif letter=='ш':
            new_word_letters.append('sh')
        elif letter=='щ':
            new_word_letters.append('sh')
        elif letter=='ъ':
            new_word_letters.append('"')
        elif letter=='ы':
            new_word_letters.append('i')
        elif letter=='ь':
            new_word_letters.append("'")
        elif letter=='э':
            new_word_letters.append('e')
        elif letter=='ю':
            new_word_letters.append('ju')
        elif letter=='я':
            new_word_letters.append('ja')
        elif letter=='-':
            new_word_letters.append('-')
        elif letter=='/':
            new_word_letters.append('/')
        elif letter=='_':
            new_word_letters.append('_')
        elif letter=='=':
            new_word_letters.append('=')
        elif letter=='+':
            new_word_letters.append('+')
        elif letter=='/':
            new_word_letters.append('/')
        else:
            return('None')
        new_word = ''.join(new_word_letters)
    return(new_word)