from angelina.parser_processing import parser_processing
from angelina.parser import create_parser

def startapp():
    '''Точка входа в приложение.'''
    parser_processing(create_parser())

