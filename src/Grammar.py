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

        if n == 0:
            for (lhs, rhs1, rhs2) in self.R:
                if lhs == self.S and rhs1 == EPSILON and rhs2 is None:
                    return ParseTree(self.S)
            return "not a member of language"

        DP = [[{} for _ in range(n)] for _ in range(n)]

        for i in range(n):
            terminal_type = w[i][0]
            token_tuple = w[i]

            for (lhs, rhs1, rhs2) in self.R:
                if rhs2 is None and rhs1 == terminal_type:
                    leaf_node = ParseTree(lhs, token_tuple)
                    DP[i][i][lhs] = leaf_node

        for length in range(2, n + 1):
            for i in range(0, n - length + 1):
                j = i + length - 1

                for k in range(i, j):
                    for (lhs, rhs1, rhs2) in self.R:
                        if rhs2 is not None:
                            left_cell = DP[i][k]
                            right_cell = DP[k + 1][j]

                            if rhs1 in left_cell and rhs2 in right_cell:
                                new_node = ParseTree(lhs)
                                new_node.add_children(left_cell[rhs1])
                                new_node.add_children(right_cell[rhs2])

                                DP[i][j][lhs] = new_node

        start_cell = DP[0][n - 1]
        if self.S in start_cell:
            return start_cell[self.S].to_string()
        else:
            return "not a member of language"

        

            

