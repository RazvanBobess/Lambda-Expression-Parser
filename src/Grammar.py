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
        n = len(w)

        P = [[set() for _ in range(n)] for _ in range(n + 1)]
        back = {}

        for s in range(n):
            terminal_symbol = w[s][0]

            for (lhs, rhs1, rhs2) in self.R:
                if rhs2 is None and rhs1 == terminal_symbol:
                    P[1][s].add(lhs)

        for l in range(2, n + 1):
            for s in range(n - l + 1):
                for p in range(1, l):

                    for (lhs, rhs1, rhs2) in self.R:
                        if rhs2 is not None:
                            if rhs1 in P[p][s] and rhs2 in P[l - p][s + p]:
                                P[l][s].add(lhs)

                                key = (l, s, lhs)
                                if key not in back:
                                    back[key] = []
                                back[key].append((p, rhs1, rhs2))
        if self.S in P[n][0]:
            return back
        else:
            return "not a member of language"
        

            

