from unittest import TestCase
from intcode import IntcodeComputer


class TestIntcodeComputer(TestCase):
    def setUp(self):
        self.computer = IntcodeComputer(debug=True)

    def test_add(self):
        self.computer.run([1,0,0,0,99])
        assert self.computer.get_mem(5) == [2,0,0,0,99]

    def test_multiply(self):
        self.computer.run([2,3,0,3,99])
        assert self.computer.get_mem(5) == [2,3,0,6,99]
        self.computer.run([2,4,4,5,99,0])
        assert self.computer.get_mem(6) == [2,4,4,5,99,9801]

    def test_add_multiply(self):
        self.computer.run([1,9,10,3,2,3,11,0,99,30,40,50])
        assert self.computer.get_mem(12) == [3500,9,10,70, 2,3,11,0, 99, 30,40,50]
        self.computer.run([1,1,1,4,99,5,6,0,99])
        assert self.computer.get_mem(9) == [30,1,1,4,2,5,6,0,99]

    def test_equal(self):
        # position mode: input is equal to 8; output 1 (if it is) or 0 (if it is not)
        assert self.computer.run([3,9,8,9,10,9,4,9,99,-1,8], 8) == 1
        assert self.computer.run([3,9,8,9,10,9,4,9,99,-1,8], 0) == 0
        # immediate mode: input is equal to 8; output 1 (if it is) or 0 (if it is not)
        assert self.computer.run([3,3,1108,-1,8,3,4,3,99,0,0], 8) == 1
        assert self.computer.run([3,3,1108,-1,8,3,4,3,99,0,0], 0) == 0

    def test_less_than(self):
        # position mode: input is less than equal to 8; output 1 (if it is) or 0 (if it is not)
        assert self.computer.run([3,9,7,9,10,9,4,9,99,-1,8], 7) == 1
        assert self.computer.run([3,9,7,9,10,9,4,9,99,-1,8], 9) == 0
        # immediate mode: input is less than equal to 8; output 1 (if it is) or 0 (if it is not)
        assert self.computer.run([3,3,1107,-1,8,3,4,3,99,0,0], 7) == 1
        assert self.computer.run([3,3,1107,-1,8,3,4,3,99,0,0], 9) == 0

    def test_jump(self):
        assert self.computer.run([3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9], 0) == 0
        assert self.computer.run([3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9], 1) == 1
        assert self.computer.run([3,3,1105,-1,9,1101,0,0,12,4,12,99,1], 0) == 0
        assert self.computer.run([3,3,1105,-1,9,1101,0,0,12,4,12,99,1], 1) == 1

    def test_input_output(self):
        # Use an input instruction to ask for a single number.
        # Then output 999 if the input value is below 8,
        # output 1000 if the input value is equal to 8,
        # or output 1001 if the input value is greater than 8.
        example = [3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,
                   1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,
                   999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99]
        assert self.computer.run(example, 7) == 999
        assert self.computer.run(example, 8) == 1000
        assert self.computer.run(example, 9) == 1001

    def test_extended_mem(self):
        self.computer.run([109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99], 1)
        assert self.computer.get_mem(16) == [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99]

    def test_output_imm(self):
        assert self.computer.run([104,1125899906842624,99], 1) == 1125899906842624

    def test_output_large_multiply(self):
        assert self.computer.run([1102,34915192,34915192,7,4,7,99,0], 1) == 1219070632396864

    def test_relative_offset(self):
        assert self.computer.run([103,1985,109,2000,109,19,204,-34,99], 555) == 555
