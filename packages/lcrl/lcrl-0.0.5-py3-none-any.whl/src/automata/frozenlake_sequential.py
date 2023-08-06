from src.automata.ldba import LDBA

# an example automaton for "goal1 then goal2 then goal 3 then goal 4 while avoiding unsafe" or
# "F (goal1 & XF (goal2 & XF (goal3 & XF goal4))) & G !unsafe"
# only the automaton "step" function and the "accepting_sets" attribute need to be specified
# "accepting_sets" for Generalised Büchi Accepting (more details here https://bit.ly/ldba_paper)
frozenlake_sequential = LDBA(accepting_sets=[[4]])


# "step" function for the automaton transitions (input: label, output: automaton_state, un-accepting sink state is "-1")
def step(self, label):
    # state 0
    if self.automaton_state == 0:
        if 'goal1' in label and 'unsafe' not in label:
            self.automaton_state = 1
        elif 'unsafe' in label:
            self.automaton_state = -1  # un-accepting sink state
        else:
            self.automaton_state = 0
    # state 1
    if self.automaton_state == 1:
        if 'goal2' in label and 'unsafe' not in label:
            self.automaton_state = 2
        elif 'unsafe' in label:
            self.automaton_state = -1  # un-accepting sink state
        else:
            self.automaton_state = 1
    # state 2
    if self.automaton_state == 2:
        if 'goal3' in label and 'unsafe' not in label:
            self.automaton_state = 3
        elif 'unsafe' in label:
            self.automaton_state = -1  # un-accepting sink state
        else:
            self.automaton_state = 2
    # state 3
    if self.automaton_state == 3:
        if 'goal4' in label and 'unsafe' not in label:
            self.automaton_state = 4
        elif 'unsafe' in label:
            self.automaton_state = -1  # un-accepting sink state
        else:
            self.automaton_state = 3
    # state 4
    if self.automaton_state == 4:
        self.automaton_state = 4

    # step function returns the new automaton state
    return self.automaton_state


# now override the step function
LDBA.step = step.__get__(frozenlake_sequential, LDBA)

# finally, does the LDBA contains an epsilon transition? if so then
# for each state with outgoing epsilon-transition define a different epsilon
# example: <LDBA_object>.epsilon_transitions = {0: ['epsilon_0'], 4: ['epsilon_1']}
# "0" and "4" are automaton_states
# (for more details refer to https://bit.ly/ldba_paper)
