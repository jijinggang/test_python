import dis
TEST_CODE = """
def f1(x):
    return 2 * x
def f2(x,y):
    return f1(x) + y
print(f2(10,1))
"""


class Function:
    def __init__(self, code, globals={}):
        self._locals = {}
        self._globals = globals
        self._stack = []
        self._code = code

    def __call__(self, *args):
        return self.run(*args)

    def _run_command(self, instruction, arg):
        #print(opname, arg)
        opname = dis.opname[instruction]
        func = getattr(self, opname)
        func(arg)

    def _parse_arg(self, instruction, value, pos):
        if(instruction in dis.hasname):
            arg = self._code.co_names[value]
        elif(instruction in dis.hasconst):
            arg = self._code.co_consts[value]
        elif(instruction in dis.haslocal):
            arg = self._code.co_varnames[value]
        elif(instruction in dis.hasjrel):
            arg = pos + value
        else:
            arg = value
        return arg

    def run(self, *args):
        for arg in args:
            self._stack.append(arg)

        pos = 0
        co_code = self._code.co_code
        while pos < len(co_code):
            instruction = co_code[pos]
            pos += 1
            arg = None
            if(instruction >= dis.HAVE_ARGUMENT):
                arg = self._parse_arg(instruction, co_code[pos], pos+1)
                pos += 1
            result = self._run_command(instruction, arg)
            if result is not None:
                return result

    def _popn(self, n):
        v = self._stack[-n:]
        self._stack[-n:] = []
        return v

    def _load(self, name, list):
        if name in list:
            return list[name]
        return None

    def _load_local(self, name):
        return self._load(name, self._locals)

    def _load_global(self, name):
        v = self._load(name, self._globals)
        if not v:
            v = self._load(name, __builtins__)
        return v

    def LOAD_CONST(self, arg):
        self._stack.append(arg)

    def LOAD_GLOBAL(self, name):
        v = self._load_global(name)
        self._stack.append(v)

    def LOAD_FAST(self, name):
        v = self._load_local(name)
        self._stack.append(v)

    def LOAD_NAME(self, name):
        v = self._load_local(name)
        if not v:
            v = self._load_global(name)
        self._stack.append(v)

    def STORE_NAME(self, arg):
        self._locals[arg] = self._stack.pop()

    def MAKE_FUNCTION(self, default_argc):
        name = self._stack.pop()
        code = self._stack.pop()
        defaults = self._popn(default_argc)
        vm = Function(code, *defaults, self._locals)
        self._stack.append(vm)

    def CALL_FUNCTION(self, argc):
        args = self._popn(argc)
        func = self._stack.pop()
        result = func(*args)
        self._stack.push(result)

    def POP_TOP(self, arg):
        self._stack.pop()

    def RETURN_VALUE(self, arg):
        return self._stack.pop()

    def BINARY_ADD(self, arg):
        a1 = self._stack.pop()
        a2 = self._stack.pop()
        self._stack.push(operator.add(a1, a2))

    def BINARY_MULTIPLY(self, arg):
        a1 = self._stack.pop()
        a2 = self._stack.pop()
        self._stack.push(operator.mul(a1, a2))


vm = Function(compile(TEST_CODE, "", "exec"))
vm.run()
