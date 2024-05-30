from random import choice, randint


def get_response(user_input: str) -> str:
    lowered: str = user_input.lower()
    
    if lowered == '':
        return 'Well, you\'re awfully silent...'
    elif '!next' in lowered:
        return 'next'
    elif 'hello' in lowered:
        return 'Hello there!'
    elif 'ping' in lowered:
        return 'pong'
    elif '!level' in lowered:
        return 'lev'
    elif 'bye' in lowered:
        return 'See you!'
    elif 'roll dice' in lowered:
        return f'You rolled: {randint(1,6)}'
    else:
        return "!"


