from .ParseTree import ParseTree
EPSILON = ""

class Grammar:

    @classmethod
    def fromFile(cls, file_name: str):
        with open(file_name, 'r') as f:
            V = set()
            R = set()
            S = None
            line = f.readline().strip()
            while line:
                v, rest = line.split(": ")
                V.add(v)
                if not S:
                    S = v

                alternatives = rest.split("|")
                for alt in alternatives:
                    if " " in alt:
                        n1, n2 = alt.split(" ")
                        V.add(n1)
                        V.add(n2)
                        R.add((v, n1, n2))
                    else: 
                        V.add(alt)
                        R.add((v, alt, None))
            
                line = f.readline().strip()

        return cls(V, R, S)
    
    def __init__(self, V: set[str], R: set[tuple[str, str, str|None]], S: str):
        self.V = V # multimea de neterminali si terminali
        self.R = R # regulile (in FNC)
        self.S = S # simbolul de start
        
    def cykParse(self, w: list[tuple[str, str]]):
        pass
        

            

