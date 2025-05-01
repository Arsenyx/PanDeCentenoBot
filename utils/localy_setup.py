import locale

def setup_locale():
    try:
        locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
    except locale.Error:
        try:
            locale.setlocale(locale.LC_TIME, 'Russian_Russia')
        except:
            locale.setlocale(locale.LC_TIME, '')