from .Lexer import Lexer
from .Grammar import Grammar

class Parser():
    def __init__(self, lexer: Lexer, grammar: Grammar) -> None:
        self.lexer = lexer
        self.grammar = grammar

    
    def parse(self, input: str) -> str:
        pass
        
