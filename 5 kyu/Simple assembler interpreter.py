class AssemblerInterpreter:
    def __init__(self):
        self.instructions = {
            'mov': self.mov,
            'inc': self.inc,
            'dec': self.dec,
            'jnz': self.jnz
        }
        self.program_counter = 0
        self.registers = {}
        self.__get_value = lambda x: self.registers[x] if x in self.registers else int(x)

    def mov(self, register, val):
        self.registers[register] = self.__get_value(val)
        self.program_counter += 1

    def inc(self, register):
        self.registers[register] += 1
        self.program_counter += 1

    def dec(self, register):
        self.registers[register] -= 1
        self.program_counter += 1

    def jnz(self, val, step):
        if self.__get_value(val) != 0:
            self.program_counter += self.__get_value(step)
        else:
            self.program_counter += 1

    def interpret(self, program):
        parse_command = lambda command: command.split()

        while self.program_counter < len(program):
            command = program[self.program_counter]
            args = parse_command(command)
            instruction = args[0]
            self.instructions[instruction](*args[1:])

        return self.registers


def simple_assembler(program):
    interpreter = AssemblerInterpreter()
    return interpreter.interpret(program)
