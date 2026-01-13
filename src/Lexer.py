from .Regex import Regex, parse_regex
from .NFA import NFA, EPSILON
from functools import reduce

class Lexer:
    def __init__(self, spec: list[tuple[str, str]]) -> None:
        self.spec = spec
        self.nfa_list = []

        for index, (token_name, regex_str) in enumerate(spec):
            nfa_name = parse_regex(regex_str).thompson()
            self.nfa_list.append((token_name, index, nfa_name))

        self.q0 = 0

        states = {self.q0}
        transitions = {}
        final_states = {}
        alphabet = set()

        offset = 1

        for token_name, index, nfa in self.nfa_list:
            nfa_remapped = nfa.remap_states(lambda s, off=offset: s + off)
            offset += len(nfa.K)

            states |= nfa_remapped.K
            transitions.setdefault((self.q0, EPSILON), set()).add(nfa_remapped.q0)
            transitions.update(nfa_remapped.d)

            alphabet |= nfa_remapped.S

            for fstate in nfa_remapped.F:
                final_states[fstate] = (token_name, index)

        new_nfa = NFA(
            S = alphabet,
            K = states,
            q0 = self.q0,
            d = transitions,
            F = set(final_states.keys())
        )

        self.final_states = final_states

        self.dfa = new_nfa.subset_construction()
        self.dfa_min = self.dfa.minimize()
    
    def lex(self, word: str) -> list[tuple[str, str]]:

        result = []
        i = 0
        line = 0

        while i < len(word):
            current_state = self.dfa_min.q0

            last_final_index = -1
            last_final_state = None

            j = i

            while j < len(word):
                symbol = word[j]

                if (current_state, symbol) not in self.dfa_min.d:
                    break

                current_state = self.dfa_min.d[(current_state, symbol)]

                if current_state in self.final_states:
                    last_final_index = j
                    last_final_state = current_state
                
                j += 1
            
            if last_final_index == -1:
                if j == len(word):
                    result.append(("", f"No viable alternative at character EOF, line {line}"))
                else:
                    result.append(("", f"No viable alternative at character {i}, line {line}"))
                i += 1
            else:
                token_name, _ = self.final_states[last_final_state]
                token_value = word[i:last_final_index + 1]

                result.append((token_name, token_value))

                i = last_final_index + 1

        print(result)

        return result

