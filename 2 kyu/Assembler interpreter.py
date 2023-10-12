class Interpreter:
    def __init__(self):
        self.instructions = {
            'mov': self.mov, 'inc': self.inc, 'dec': self.dec, 'add': self.add,
            'sub': self.sub, 'mul': self.mul, 'div': self.div, 'jmp': self.jmp,
            'cmp': self.cmp, 'jne': self.jne, 'je': self.je, 'jge': self.jge,
            'jg': self.jg, 'jle': self.jle, 'jl': self.jl, 'call': self.call,
            'ret': self.ret, 'msg': self.msg
        }
        self.flags = {'zf': False, 'sf': False}
        self.registers = {'pc': 0, 'lr': None}
        self.output = ""
        self.__get_value = lambda x: self.registers[x] if x in self.registers else int(x)

    def mov(self, register, val):
        self.registers[register] = self.__get_value(val)
        self.registers['pc'] += 1

    def inc(self, register):
        self.registers[register] += 1
        self.registers['pc'] += 1

    def dec(self, register):
        self.registers[register] -= 1
        self.registers['pc'] += 1

    def add(self, register, val):
        self.registers[register] += self.__get_value(val)
        self.registers['pc'] += 1

    def sub(self, register, val):
        self.registers[register] -= self.__get_value(val)
        self.registers['pc'] += 1

    def mul(self, register, val):
        self.registers[register] *= self.__get_value(val)
        self.registers['pc'] += 1

    def div(self, register, val):
        self.registers[register] //= self.__get_value(val)
        self.registers['pc'] += 1

    def jmp(self, label):
        self.registers['pc'] = self.labels[label]

    def cmp(self, x, y):
        x, y = self.__get_value(x), self.__get_value(y)
        self.flags['zf'] = x == y
        self.flags['sf'] = x < y
        self.registers['pc'] += 1

    def jne(self, lbl):
        if not self.flags['zf']: self.jmp(lbl)
        else : self.registers['pc'] += 1

    def je(self, lbl):
        if self.flags['zf']: self.jmp(lbl)
        else : self.registers['pc'] += 1

    def jge(self, lbl):
        if self.flags['zf'] or not self.flags['sf']: self.jmp(lbl)
        else : self.registers['pc'] += 1

    def jg(self, lbl):
        if not self.flags['zf'] and not self.flags['sf']: self.jmp(lbl)
        else : self.registers['pc'] += 1

    def jle(self, lbl):
        if self.flags['zf'] or self.flags['sf']: self.jmp(lbl)
        else : self.registers['pc'] += 1

    def jl(self, lbl):
        if not self.flags['zf'] and self.flags['sf']: self.jmp(lbl)
        else : self.registers['pc'] += 1

    def call(self, label):
        if not self.registers['lr']: self.registers['lr'] = self.registers['pc'] + 1
        self.jmp(label)

    def ret(self):
        if self.registers['lr']:
            self.registers['pc'] = self.registers['lr']
            self.registers['lr'] = None

    def msg(self, *args):
        message = ' '.join(args)
        string = ""
        idx = 0
        current_char = message[idx]

        def advance(c, i):
            i += 1
            c = message[i] if i < len(message) else None
            return c, i

        while current_char:
            if current_char == "'":
                current_char, idx = advance(current_char, idx)
                while current_char != "'":
                    string += current_char
                    current_char, idx = advance(current_char, idx)
                current_char, idx = advance(current_char, idx)
            elif current_char.isalpha():
                string += str(self.registers[current_char])
                current_char, idx = advance(current_char, idx)
            current_char, idx = advance(current_char, idx)

        self.output = string
        self.registers['pc'] += 1

    def interpret(self, source):
        program = preprocess(source)
        self.labels = make_labels(program)

        while self.registers['pc'] < len(program):
            command = program[self.registers['pc']]
            args = command.replace(',', ' ').split() if not command.startswith('msg') else command.split()
            instruction = args[0]
            if instruction == 'end': return self.output
            self.instructions[instruction](*args[1:])

        self.output = -1


preprocess = lambda source: [l.split(';')[0].strip() for l in [l.strip() for l in source.splitlines() if l.strip()] if not l.startswith(';')]


def make_labels(program):
    labels = {}
    for i, line in enumerate(program): 
        if line.endswith(':'): labels[line[:-1]] = i + 1
    return labels


def assembler_interpreter(source):
    interpreter = Interpreter()
    interpreter.interpret(source)
    return interpreter.output
