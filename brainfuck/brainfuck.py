from collections import defaultdict

def _bound_value(n, boundary):
    '''
    Bounds n to [0, boundary)

    Parameters
    ----------

    n : int
        Some number to bound.

    boundary : non-negative int
        The boundary for n. When set to 0, will return n as-is.

    Returns
    -------
    int
        Returns n modulo boundary when boundary is larger than 0. Returns n
        unmodified when boundary equals 0.
    '''
    assert boundary >= 0, 'negative boundary: {}'.format(boundary)
    return n % boundary if boundary else n


def validate_src(src):
    '''
    Returns true if the source code has no unbalanced brackets.
    '''

    depth = 0
    brackets = [c for c in src if c in '[]']
    for b in brackets:
        depth += {'[': 1, ']': -1}[b]
        if depth < 0: return False

    return depth == 0


class InputException(Exception):
    pass

class InvalidSrcException(Exception):
    pass

class BrainfuckMachine(object):

    def __init__(self, tape_size=0, loop_max=0):
        assert type(tape_size) is int
        assert tape_size >= 0
        assert type(loop_max) is int
        assert loop_max >= 0
        self._tape_size = tape_size
        self._loop_max = loop_max

    def _reset(self, src, input_data):
        '''
        Set back
        '''
        self._head = 0  # Position of the tape head
        self._instruction_ptr = 0  # Position of the current instruction
        self._tape = defaultdict(int)  # the tape
        self._output = ''  # The output
        self._src = src
        self._input = input_data

    def _get_tape(self):
        '''
        Get the value of the tape at the head position.
        '''
        assert type(self._head) is int
        assert self._head == _bound_value(self._head, self._tape_size)
        assert type(self._tape[self._head]) is int
        assert self._tape[self._head] == _bound_value(self._tape[self._head],
                                                      0x110000)

        return self._tape[self._head]

    def _set_tape(self, value):
        '''
        Set the value of the tape at the head position. Makes sure that the
        value is whithin the correct boundary.
        '''
        assert type(self._head) is int
        assert self._head == _bound_value(self._head, self._tape_size)
        assert type(value) is int, 'Non int value: {}'.format(value)

        # chr(x) works untill 0x110000
        self._tape[self._head] = _bound_value(value, 0x110000)

    def _get_instr(self):
        assert type(self._instruction_ptr) is int
        assert type(self._src) is str
        assert self._instruction_ptr == _bound_value(self._instruction_ptr,
                                                     len(self._src))
        return self._src[self._instruction_ptr]

    # --------------------------------------------------------------------------
    # Brainfuck Instructions
    # --------------------------------------------------------------------------

    def _head_right(self):
        '''>'''
        assert type(self._head) is int
        assert self._head == _bound_value(self._head, self._tape_size)
        self._head = _bound_value(self._head + 1, self._tape_size)

    def _head_left(self):
        '''<'''
        assert type(self._head) is int
        assert self._head == _bound_value(self._head, self._tape_size)
        self._head = _bound_value(self._head - 1, self._tape_size)

    def _inc_tape(self):
        '''+'''
        self._set_tape(self._get_tape() + 1)

    def _dec_tape(self):
        '''-'''
        self._set_tape(self._get_tape() - 1)

    def _read_from_input(self):
        ''','''
        try:
            c = ord(self._input[0])
            self._set_tape(c)
            self._input = self._input[1:]
        except:
            raise InputException()

    def _write_to_output(self):
        '''.'''
        self._output += chr(self._get_tape())

    def _begin_while_loop(self):
        '''['''
        # If the tape reads a 0, the loop is to be ignored. Move the
        # instruction_ptr to the enclosing bracket.
        # Because the code was validated, it is guaranteed that the enclosing
        # bracket exists.
        if self._get_tape() == 0:
            loop = 1
            while loop:
                self._instruction_ptr += 1
                if self._get_instr() == '[':
                    loop += 1
                elif self._get_instr() == ']':
                    loop -= 1
        # At the end, the instruction_ptr is positioned in the enclosing
        # bracket


    def _end_while_loop(self):
        ''']'''
        # Get back to the opening bracket.
        loop = 1
        while loop:
            self._instruction_ptr -= 1
            if self._get_instr() == '[':
                loop -= 1
            elif self._get_instr() == ']':
                loop += 1
        self._instruction_ptr -= 1


    # --------------------------------------------------------------------------
    # Public methods.
    # --------------------------------------------------------------------------

    def eval(self, src, input_data=''):
        assert type(src) is str
        assert type(input_data) is str

        if not validate_src(src):
            raise InvalidSrcException()

        self._reset(src, input_data)

        while self._instruction_ptr < len(src):

            if self._get_instr() == '>':
                self._head_right()
            elif self._get_instr() == '<':
                self._head_left()
            elif self._get_instr() == '+':
                self._inc_tape()
            elif self._get_instr() == '-':
                self._dec_tape()
            elif self._get_instr() == '.':
                self._write_to_output()
            elif self._get_instr() == ',':
                self._read_from_input()
            elif self._get_instr() == '[':
                self._begin_while_loop()
            elif self._get_instr() == ']':
                self._end_while_loop()

            self._instruction_ptr += 1

        return self._output

