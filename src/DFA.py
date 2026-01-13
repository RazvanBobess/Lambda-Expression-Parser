from collections.abc import Callable
from dataclasses import dataclass
from itertools import product
from typing import TypeVar
from functools import reduce
from collections import deque

STATE = TypeVar('STATE')

@dataclass
class DFA[STATE]:
    S: set[str]
    K: set[STATE]
    q0: STATE
    d: dict[tuple[STATE, str], STATE]
    F: set[STATE]


    def accept(self, word: str) -> bool:
        current_state = self.q0

        for symbol in word:
            current_state = self.d(current_state, symbol)
    
        return current_state in self.F

    def minimize(self) -> "DFA[STATE]":
        P = [set(self.F), self.K - self.F]
        W = deque(P)

        while W:
            Q = W.popleft()

            for c in self.S:
                X = {
                    s for s in self.K
                    if self.d.get((s, c)) in Q
                }

                new_P = []
                for R in P:
                    R1 = R & X
                    R2 = R - X

                    if R1 and R2:
                        new_P.extend([R1, R2])

                        if R in W:
                            W.remove(R)
                            W.extend([R1, R2])
                        else:
                            W.append(R1 if len(R1) <= len(R2) else R2)
                    else:
                        new_P.append(R)

                P = new_P

        state_map = {}
        for i, block in enumerate(P):
            for s in block:
                state_map[s] = i

        new_K = set(state_map.values())
        new_q0 = state_map[self.q0]
        new_F = {state_map[s] for s in self.F}

        new_d = {}
        for (s, c), t in self.d.items():
            new_d[(state_map[s], c)] = state_map[t]

        return DFA(self.S, new_K, new_q0, new_d, new_F)
        
    def remap_states[OTHER_STATE](self, f: Callable[[STATE], 'OTHER_STATE']) -> 'DFA[OTHER_STATE]':

        new_k = {f(state) for state in self.K}
        new_q0 = f(self.q0)

        new_d = {}

        for (state, symbol), next_state in self.d.items():
            new_d[(f(state), symbol)] = f(next_state)

        return DFA(S=self.S, K=new_k, q0=new_q0, d=new_d, F={f(state) for state in self.F})
    