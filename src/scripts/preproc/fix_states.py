def at_i(array, index):
    try:
        return array[index]
    except:
        return ''


def fix_states(text):
    """
    Text is an array of words.
    """
    result = []

    for i, word in enumerate(text):
        if(
                at_i(text, i) == 'rio' and
                at_i(text, i+1) == 'de' and
                at_i(text, i+2) == 'janeiro'):
            result.append('riodejaneiro')
        elif(
            at_i(text, i) == 'de' or
            at_i(text, i) == 'janeiro'
        ):
            continue

        elif(
                at_i(text, i) == 'sao' and
                at_i(text, i+1) == 'paulo'
        ):
            result.append('saopaulo')
        elif(
            at_i(text, i) == 'spaulo'
        ):
            result.append('saopaulo')

        elif(
            at_i(text, i) == 'paulo'
        ):
            continue

        elif(
            at_i(text, i) == 'minas' and
            at_i(text, i+1) == 'gerais'
        ):
            result.append('minasgerais')
        elif(
            at_i(text, i) == 'gerais'
        ):
            continue

        elif(
            at_i(text, i) == 'espirito' and
            at_i(text, i+1) == 'santo'
        ):
            result.append('espiritosanto')
        elif(
            at_i(text, i) == 'santo'
        ):
            continue

        elif(
            at_i(text, i) == 'distrito' and
            at_i(text, i+1) == 'federal'
        ):
            result.append('distritofederal')

        elif(
            at_i(text, i) == 'mato' and
            at_i(text, i+1) == 'grosso' and
            at_i(text, i+2) == 'do' and
            at_i(text, i+3) == 'sul'
        ):
            result.append('matogrossodosul')

        elif(
            at_i(text, i) == 'mato' and
            at_i(text, i+1) == 'grosso' and
            at_i(text, i+2) != 'do'
        ):
            result.append('matogrosso')

        elif(
            at_i(text, i) == 'rio' and
            at_i(text, i+1) == 'grande' and
            at_i(text, i+2) == 'do' and
            at_i(text, i+3) == 'sul'
        ):
            result.append('riograndedosul')

        elif(
            at_i(text, i) == 'rio' and
            at_i(text, i+1) == 'grande' and
            at_i(text, i+2) == 'do' and
            at_i(text, i+3) == 'norte'
        ):
            result.append('riograndedonorte')

        elif(
            at_i(text, i) == 'grosso' or
            at_i(text, i) == 'norte' or
            at_i(text, i) == 'sul' or
            at_i(text, i) == 'grande'
        ):
            continue

        elif(
            at_i(text, i) == 'santa' and
            at_i(text, i+1) == 'catarina'
        ):
            result.append('santacatarina')

        elif(
            at_i(text, i) == 'catarina'
        ):
            continue

        else:
            result.append(word)

    return result
