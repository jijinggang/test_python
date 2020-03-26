import dis
import inspect
import operator
import builtins
TEST_CODE = """
def f1(x):
    if(x < 0) :
        return 0
    else:
        return  (x ** 2) + 2*x + 1
def f2(x,y):
    return (f1(x) +f1(y))/2
print(f2(-3,4))
"""


class Function:
    def __init__(self, code, globals={}):
        self._locals = {}  # 本地变量
        self._globals = globals  # 全局变量
        self._stack = []  # 指令栈
        self._code = code  # 字节码

    def __call__(self, *args):
        return self.run(*args)

    def _dispatch(self, instruction, arg):
        opname = dis.opname[instruction]
        #print(opname, arg)
        if opname.startswith("BINARY_"):
            return self.BINARY_Any(opname[len("BINARY_"):])
        elif opname.startswith("UNARY_"):
            return self.UNARY_Any(opname[len("UNARY_"):])
        else:
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
        # 把参数列表信息存入本地变量区
        func = dis.types.FunctionType(self._code, self._globals)
        kwargs = inspect.getcallargs(func, *args)
        self._locals.update(kwargs)

        self._instruction_pos = 0
        co_code = self._code.co_code
        while self._instruction_pos < len(co_code):
            instruction = co_code[self._instruction_pos]
            self._instruction_pos += 1
            # if(instruction >= dis.HAVE_ARGUMENT):
            # 指令和参数各占一个字节
            arg = self._parse_arg(
                instruction, co_code[self._instruction_pos], self._instruction_pos+1)
            self._instruction_pos += 1
            result = self._dispatch(instruction, arg)
            if result is not None:
                #print("return ", result)
                return result[0]

    def _jump(self, pos):
        self._instruction_pos = pos

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

    def POP_TOP(self, arg):
        self._stack.pop()

    # 只有此指令直接返回,其他指令无返回(即为None), 采用数组返回避免出现值本身是None
    def RETURN_VALUE(self, arg):
        return [self._stack.pop()]

    # 函数,采用递归调用处理

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

    # 跳转指令

    def POP_JUMP_IF_FALSE(self, arg):
        x = self._stack.pop()
        if not x:
            self._jump(arg)

    def POP_JUMP_IF_TRUE(self, arg):
        x = self._stack.pop()
        if x:
            self._jump(arg)

    # 一元操作符
    UNARY_OP = {
        'POSITIVE': operator.pos,
        'NEGATIVE': operator.neg,
        'NOT':      operator.not_,
        'INVERT':   operator.invert,
    }

    def UNARY_Any(self, opname):
        x = self._stack.pop()
        self._stack.append(self.UNARY_OP[opname](x))

    # 二元操作符
    BINARY_OP = {
        'POWER':    operator.pow,
        'MULTIPLY': operator.mul,
        'FLOOR_DIVIDE': operator.floordiv,
        'TRUE_DIVIDE':  operator.truediv,
        'MODULO':   operator.mod,
        'ADD':      operator.add,
        'SUBTRACT': operator.sub,
        'SUBSCR':   operator.getitem,
        'LSHIFT':   operator.lshift,
        'RSHIFT':   operator.rshift,
        'AND':      operator.and_,
        'XOR':      operator.xor,
        'OR':       operator.or_,
    }

    def BINARY_Any(self, opname):
        x, y = self._popn(2)
        self._stack.append(self.BINARY_OP[opname](x, y))

    # 比较操作符
    COMPARE_OP_FUNC = [
        operator.lt,
        operator.le,
        operator.eq,
        operator.ne,
        operator.gt,
        operator.ge,
        lambda x, y: x in y,
        lambda x, y: x not in y,
        lambda x, y: x is y,
        lambda x, y: x is not y,
        lambda x, y: issubclass(x, Exception) and issubclass(x, y),
    ]

    def COMPARE_OP(self, compare_op_code):
        x, y = self._popn(2)
        self._stack.append(self.COMPARE_OP_FUNC[compare_op_code](x, y))


vm = Function(compile(TEST_CODE, "", "exec"))
vm.run()
