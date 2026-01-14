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
        nfa_final_states = {}
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
                nfa_final_states[fstate] = (token_name, index)

        new_nfa = NFA(
            S = alphabet,
            K = states,
            q0 = self.q0,
            d = transitions,
            F = set(nfa_final_states.keys())
        )

        self.dfa = new_nfa.subset_construction()
        self.dfa_final_map = {}

        for dfa_state in self.dfa.K:
            best_prio = float('inf')
            best_token = None

            for nfa_state in dfa_state:
                if nfa_state in nfa_final_states:
                    token, prio = nfa_final_states[nfa_state]

                    if prio < best_prio:
                        best_prio = prio
                        best_token = token

            if best_token is not None:
                self.dfa_final_map[dfa_state] = (best_token, best_prio)
    
    def lex(self, word: str) -> list[tuple[str, str]]:
        result = []
        i = 0
        line = 0

        while i < len(word):
            current_state = self.dfa.q0

            last_final_index = -1
            last_final_state = None

            j = i

            while j < len(word):
                symbol = word[j]

                if (current_state, symbol) not in self.dfa.d:
                    break

                current_state = self.dfa.d[(current_state, symbol)]

                if current_state in self.dfa_final_map:
                    last_final_index = j
                    last_final_state = current_state
                
                j += 1
            
            if last_final_index == -1:
                if j == len(word) and i == j:
                    if i == len(word):
                        return []
                    if j == len(word):
                        return[("", f"No viable alternative at character EOF, line {line}")]
                    else:
                        return[("", f"No viable alternative at character {i}, line {line}")]
                else:
                    if j == len(word):
                        return [("", f"No viable alternative at character EOF, line {line}")]
                    else:
                        return [("", f"No viable alternative at character {i}, line {line}")]
            else:
                token_name, _ = self.dfa_final_map[last_final_state]
                token_value = word[i:last_final_index + 1]

                result.append((token_name, token_value))
                line += token_value.count('\n')

                i = last_final_index + 1

        print(result)

        return result

