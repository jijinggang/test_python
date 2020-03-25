import dis
import inspect
import operator
import builtins
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

    def _run_instruction(self, instruction, arg):
        opname = dis.opname[instruction]
        #print(opname, arg)
        func = getattr(self, opname)
        return func(arg)

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
        func = dis.types.FunctionType(self._code, self._globals)
        kwargs = inspect.getcallargs(func, *args)
        self._locals.update(kwargs)

        pos = 0
        co_code = self._code.co_code
        while pos < len(co_code):
            instruction = co_code[pos]
            pos += 1
            arg = None
            #if(instruction >= dis.HAVE_ARGUMENT):
            arg = self._parse_arg(instruction, co_code[pos], pos+1)
            pos += 1
            result = self._run_instruction(instruction, arg)
            if result is not None:
                #print("return ", result)
                return result

    def _popn(self, n):
        v = self._stack[-n:]
        self._stack[-n:] = []
        return v

    def _load_local(self, name):
        return self._locals.get(name)

    def _load_builtins(self, name):
        return builtins.__dict__.get(name)
    def _load_global(self, name):
        v = self._globals.get(name)
        if v == None:
            v = self._load_builtins(name)
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
        if v == None:
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
        self._stack.append(result)

    def POP_TOP(self, arg):
        self._stack.pop()

    def RETURN_VALUE(self, arg):
        return self._stack.pop()

    def BINARY_ADD(self, arg):
        a1 = self._stack.pop()
        a2 = self._stack.pop()
        self._stack.append(operator.add(a1, a2))

    def BINARY_MULTIPLY(self, arg):
        a1 = self._stack.pop()
        a2 = self._stack.pop()
        self._stack.append(operator.mul(a1, a2))

#print(dis.dis(compile(TEST_CODE, "", "single")))


vm = Function(compile(TEST_CODE, "", "exec"))
vm.run()
