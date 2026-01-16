from .Lexer import Lexer
from .Grammar import Grammar

class Parser():
    def __init__(self, lexer: Lexer, grammar: Grammar) -> None:
        self.lexer = lexer
        self.grammar = grammar

    
    def parse(self, input: str) -> str:
        tokens = self.lexer.lex(input)
        new_tokens = [t for t in tokens if t[0] != "SPACE"]

        return self.grammar.cykParse(new_tokens)