import unittest

from brainfuck.brainfuck import *
import brainfuck.brainfuck as bfk

class BrainfuckMachineTest(unittest.TestCase):

    def setUp(self):
        self.vm = BrainfuckMachine()

    def test_validate_src(self):

        self.assertTrue(validate_src(''))
        self.assertTrue(validate_src('[[[]]]'))
        self.assertTrue(validate_src('++++>>>----<<<.,...,,,[[]]'))

        self.assertFalse(validate_src('[[['))
        self.assertFalse(validate_src(']]'))
        self.assertFalse(validate_src('[[][]][]]'))
        self.assertFalse(validate_src(']'))

    def test__bound_value_when_bound_is_0(self):
        '''
        Test for _bound_value for the case when boundary equals 0.
        '''
        self.assertEqual(1, bfk._bound_value(1, 0))
        self.assertEqual(4210, bfk._bound_value(4210, 0))
        self.assertEqual(0, bfk._bound_value(0, 0))
        self.assertEqual(100, bfk._bound_value(100, 0))

    def test__bound_value_when_bound_is_0_and_n_is_negative(self):
        '''
        Test for _bound_value for the case when boundary equals 0 and n < 0.
        '''
        ns = [-1, -4210, -4214, -100, -50, -30]
        for n in ns:
            self.assertEqual(n, bfk._bound_value(n, 0))

    def test__bound_value_when_n_is_in_bound(self):
        '''
        Test for _bound_value for the case when n is in boundary.
        '''
        self.assertEqual(1, bfk._bound_value(1, 20))
        self.assertEqual(4210, bfk._bound_value(4210, 100000))
        self.assertEqual(0, bfk._bound_value(0, 1))
        self.assertEqual(100, bfk._bound_value(100, 421))

    def test__bound_value_when_n_is_out_of_bound(self):
        '''
        Test for _bound_value for the case when n is out of boundary.
        '''
        ns = [500, 30, 421, 31, -40]
        boundaries = [2, 14, 321, 3, 55]
        for n, boundary in zip(ns, boundaries):
            m = n % boundary
            self.assertEqual(m, bfk._bound_value(n, boundary))

    def test_eval_simple(self):
        vm = BrainfuckMachine()
        out = vm.eval('[].+.+.')
        expected_out = '\x00\x01\x02'
        self.assertEqual(out, expected_out)

    def test_eval_hello_world(self):
        # Hello world program
        src = '''
        ++++++++++[>+++++++>++++++++++>+++>+<<<<-]>++.>+.
        +++++++..+++.>++.<<+++++++++++++++.>.+++.------.
        --------.>+.>.
        '''
        self.assertEqual('Hello World!\n', self.vm.eval(src))

    def test_eval_sum_numbers(self):
        src = '''
        ++++     c0 is 4
        +++++++  c1 is 7

        [        begin loop in c1
        < +      inc c0
        > -      dec c1
        ]
                 now  c0 = 11; c1 = 0
        <        move to c0
        .        print chr(11)
        >        move to c1
        .        print chr(0)
        '''
        out = self.vm.eval(src)
        self.assertEqual(out, '\x0b\x00')

    def test_eval_when_source_is_invalid(self):
        vm = BrainfuckMachine()
        invalid_sources = ['[[[', ']]', '[[][]][]]', ']']
        for src in invalid_sources:
            self.assertRaises(InvalidSrcException, vm.eval, src)

