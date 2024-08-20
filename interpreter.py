"""
This is the solution for the software homework exercise for MLabs.
Author: Jacobo Fernandez Vargas
"""

def load_instructions(file: str) -> list[str]:
    """
    Auxiliary function to read an instruction text file.
    :param file: Path to the file with the instructions
    :return: A list with the instructions.
    """
    with open(file, 'r') as f:
        lines = f.readlines()
    instructions = []
    for l in lines:
        instructions += l.trim().split()
    return instructions

def translate(lowLevel: list[str]) -> list[str]:
    """
    Function that translate the instruction set into python code to be executed by the eval function.
    :param lowLevel: List of instructions in low level.
    :return: Instruction set in python.
    """
    unary = ['LOAD_VARIABLE', 'LOAD_CONSTANT', 'ASSIGN_VARIABLE']
    binary = []
    python = []
    idx = 0
    while idx != len(lowLevel):
        if lowLevel[idx] in unary:
            if lowLevel[idx] == 'LOAD_VARIABLE':
                python.append(f'inst.{lowLevel[idx].lower()}("{lowLevel[idx + 1]}")')
            else:
                python.append(f'inst.{lowLevel[idx].lower()}({lowLevel[idx + 1]})')
            idx += 2
        elif lowLevel[idx] in binary:
            python.append(f'inst.{lowLevel[idx].lower()}({lowLevel[idx + 1]}, {lowLevel[idx + 2]})')
            idx += 3
        elif lowLevel[idx] == "RETURN":
            python.append('inst.end()')
            idx += 1
        else:
            python.append(f'inst.{lowLevel[idx].lower()}()')
            idx += 1
    return python


class Function:
    """
    Class that manages a memory space. It is defined by the input arguments and the instruction set.
    :cvar variables: Dictionary with the variables defined in the function. Acts as the memory of the system.
    """
    variables = {}

    def __init__(self, arguments: list[str], instructions: list[str]):
        """
        :param arguments: List of the name of the arguments that this function needs when it is called.
        :param instructions: The instruction list that define the function.
        """
        self.variables = {}
        self.functions_args = arguments
        self.function_inst = translate(instructions)

    def assign_variable(self, name, value):
        """
        Updates the value of a variable. If it doesn't exist it will create it. This variable can only be accessed
        inside this function.
        :param name: Name of the variable
        :param value: Value of the variable.
        """
        self.variables[name] = value

    def parse_inputs(self, values: list[float]):
        """
        Creates the variables corresponding to the input of the function.
        :param values: Values of the arguments of the function.
        """
        for n,v in zip(self.functions_args, values):
            self.assign_variable(n, v)

    def __call__(self, args: list[float]) -> float:
        """
        This function takes the role of the interpreter. It will execute all the instructions in the function in
        addition to load the arguments.
        :param args: Arguments to be inputed to the function.
        :return: Value returned by the function
        """
        inst = Instruction(self)
        instructions = [f'self.parse_inputs({args})'] + self.function_inst
        for i in instructions:
            ret = eval(i)
        return ret


class Instruction:
    """
    Class that implements all the arithmetic capabilities of the language.
    :cvar operands: Queue of the operands that are used by the different operations.
    """
    operands = []

    def __init__(self, function: Function):
        """
        :param function: Function instance that holds the variables.
        """
        self.function = function


    def multiply(self):
        """
        Multiplies the first two operands in the queue.
        """
        o1 = self.operands.pop(0)
        o2 = self.operands.pop(0)
        self.operands.append(o1 * o2)

    def add(self):
        """
        Adds the first two operands in the queue.
        """
        o1 = self.operands.pop(0)
        o2 = self.operands.pop(0)
        self.operands.append(o1 + o2)

    def load_constant(self, value: float):
        """
        Inserts into the queue a constant
        :param value: Value to be inserted
        """
        self.operands.append(value)

    def load_variable(self, name: str):
        """
        Inserts into the queue the value of a variable
        :param name: Name of the variable
        """
        self.operands.append(self.function.variables[name])

    def assign_variable(self, name):
        """
        Pops the first value of the queue and updates / creates a variable with that value.
        :param name: Name of the variable
        """
        value = self.operands.pop(0)
        self.function.assign_variable(name, value)

    def end(self) -> float:
        """
        Pops the first value of the queue and returns it.
        :return: Value to be returned
        """
        return self.operands.pop(0)


instructions = ['LOAD_VARIABLE', 'x',
                'LOAD_CONSTANT', 2,
                'MULTIPLY',
                'LOAD_VARIABLE', 'y',
                'ADD',
                'RETURN'
                ]
arguments = ['x', 'y']
f = Function(arguments, instructions)
print(f([2, 3]))

