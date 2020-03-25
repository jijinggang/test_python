import dis
TEST_CODE = """
def f1(x):
    return 2 * x
def f2(x,y):
    return f1(x) + y
print(f2(10,1))
"""


class Function:
    def __init__(self, code, contexts={}):
        self.locals = {}
        self.contexts = contexts
        self.stack = []
        self.code = code

    def __call__(self, *args):
        return self.run(*args)

    def runCommand(self, instruction, arg):
        #print(opname, arg)
        opname = dis.opname[instruction]
        func = getattr(self, opname)
        func(arg)

    def parseArg(self, instruction, value, pos):
        if(instruction in dis.hasname):
            arg = self.code.co_names[value]
        elif(instruction in dis.hasconst):
            arg = self.code.co_consts[value]
        elif(instruction in dis.haslocal):
            arg = self.code.co_varnames[value]
        elif(instruction in dis.hasjrel):
            arg = pos + value
        else:
            arg = value
        return arg

    def run(self, *args):
        for arg in args:
            self.stack.append(arg)

        pos = 0
        co_code = self.code.co_code
        while pos < len(co_code):
            instruction = co_code[pos]
            pos += 1
            arg = None
            if(instruction >= dis.HAVE_ARGUMENT):
                arg = self.parseArg(instruction, co_code[pos], pos+1)
                pos += 1
            result = self.runCommand(instruction, arg)
            if result is not None:
                return result

    def popn(self, n):
        v = self.stack[-n:]
        self.stack[-n:] = []
        return v

    def load(self, name, list):
        if name in list:
            return list[name]
        return None

    def loadLocal(self, name):
        return self.load(name, self.locals)

    def loadContext(self, name):
        v = self.load(name, self.contexts)
        if not v:
            v = self.load(name, __builtins__)
        return v

    def LOAD_CONST(self, arg):
        self.stack.append(arg)

    def LOAD_GLOBAL(self, name):
        v = self.loadContext(name)
        self.stack.append(v)

    def LOAD_FAST(self, name):
        v = self.loadLocal(name)
        self.stack.append(v)

    def LOAD_NAME(self, name):
        v = self.loadLocal(name)
        if not v:
            v = self.loadContext(name)
        self.stack.append(v)

    def STORE_NAME(self, arg):
        self.locals[arg] = self.stack.pop()

    def MAKE_FUNCTION(self, default_argc):
        name = self.stack.pop()
        code = self.stack.pop()
        defaults = self.popn(default_argc)
        vm = Function(code, *defaults, self.locals)
        self.stack.append(vm)

    def CALL_FUNCTION(self, argc):
        args = self.popn(argc)
        func = self.stack.pop()
        result = func(*args)
        self.stack.push(result)

    def POP_TOP(self, arg):
        self.stack.pop()

    def RETURN_VALUE(self, arg):
        return self.stack.pop()

    def BINARY_ADD(self, arg):
        a1 = self.stack.pop()
        a2 = self.stack.pop()
        self.stack.push(operator.add(a1, a2))

    def BINARY_MULTIPLY(self, arg):
        a1 = self.stack.pop()
        a2 = self.stack.pop()
        self.stack.push(operator.mul(a1, a2))


vm = Function(compile(TEST_CODE, "", "exec"))
vm.run()
