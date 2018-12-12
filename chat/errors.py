import sys


def message(title):
    e_type, e_obj, e_tb = sys.exc_info()
    return "%s : %s (%d)" % (title, str(e_obj), e_tb.tb_lineno)


def json(title):
    return {
        "message": message('Error creating message')
    }
