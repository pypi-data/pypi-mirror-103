class Truth:
    """Truth Object Class"""
    def __init__(self, truthValues):
        self.truthValues = truthValues
    
    def __len__(self):
        return len(self.truthValues)
    
    def __getitem__(self, level):
        if isinstance(level, str):
            if level == "true":
                return {i:self.truthValues[i] for i in range(len(self.truthValues)) if self.truthValues[i] == True}
            elif level== "false":
                return {i:self.truthValues[i] for i in range(len(self.truthValues)) if self.truthValues[i] == False}
    
    def lenTrue(self):
        """Returns the number of True/1 present in the Truth Object"""
        return len(self["true"].values())
    
    def lenFalse(self):
        """Returns the number of False/0 present in the Truth Object"""
        return len(self["false"].values())

    def __str__(self):
        return str(self.truthValues)
    
    def __repr__(self):
        return self.__str__()
        
    def __mul__(self, other):
        return Truth(binaryOperation(self.truthValues, other.truthValues, "and"))
    
    def __and__(self, other):
        return self.__mul__(other)
    
    def __add__(self, other):
        return Truth(binaryOperation(self.truthValues, other.truthValues, "or"))
    
    def __or__(self, other):
        return self.__add__(other)
    
    def __xor__(self, other):
        return Truth(binaryOperation(self.truthValues, other.truthValues, "or"))

    def __invert__(self):
        return Truth(unaryOperation(self.truthValues))

    def __neg__(self):
        return self.__invert__()
    
    def __not__(self):
        return self.__invert__()
    
    def __eq__(self, other):
        return Truth(binaryOperation(self.truthValues, other.truthValues, "xnor"))
    
    def __ne__(self, other):
        return ~(self == other)
    
    def __ge__(self, other):
        return Truth(binaryOperation(self.truthValues, other.truthValues, "imp"))
    
    def __le__(self, other):
        return Truth(binaryOperation(other.truthValues, self.truthValues, "imp"))
    
    def __bool__(self):
        return self.truthValues == (self == self).truthValues
    
    def NOT(self):
        """NOT operation"""
        return ~self

    def AND(self, *Inputs):
        """AND operation"""
        return ANDgate(self, *Inputs)

    def NAND(self, *Inputs):
        """NAND operation (Negation of AND operation)"""
        return NANDgate(self, *Inputs)

    def OR(self, *Inputs):
        """OR operation"""
        return ORgate(self, *Inputs)

    def NOR(self, *Inputs):
        """NOR operation (Negation of OR operation))"""
        return NORgate(self, *Inputs)

    def XOR(self, *Inputs):
        """Exclusive OR operation"""
        return XORgate(self, *Inputs)

    def XNOR(self, *Inputs):
        """Exclusive NOR operation (Negation of XOR operation)"""
        return XNOR(self, *Inputs)
    
    def IMP(self, other):
        """Implication operation (If ... Then)"""
        return self > other
        
    def BICON(self, other):
        """Equivalence Operation (If and only If)"""
        return self == other


def NOT(p):
    return not p

def AND(p, q):
    return p and q

def NAND(p, q):
    return not (p and q)

def OR(p, q):
    return p or q

def NOR(p, q):
    return not (p or q)

def XOR(p, q):
    return p != q

def XNOR(p, q):
    return p == q

def IMP(p, q):
    return (p == q) or q

def BICON(p, q):
    return p == q



def binaryOperation(truthRowP, truthRowQ, operator):
    """Logical Binary Operation on list/tuple of boolean values
        \noperator argument values:
        \n"or" --> OR operation
        \n"nor" --> NOR operation
        \n"xor" --> XOR operation
        \n"and" --> AND operation
        \n"nand" --> NAND operation
        \n"imp" --> Implication Operation
        \n"xnor" --> XNOR operation
    """
    symbols = {"or": OR, "nor": NOR, "xor": XOR, "and": AND, "nand": NAND, "imp": IMP, "xnor": XNOR}
    return tuple([symbols[operator](truthRowP[i], truthRowQ[i]) for i in range(len(truthRowP))])

def unaryOperation(truthRow):
    """NOT peration on list/tuple of boolean values"""
    return tuple([NOT(truthRow[i]) for i in range(len(truthRow))])

def truthLiteral(p, binaryRep=False):
    if p:
        if binaryRep:
             return "1"
        else:
            return "T"
    if binaryRep:
        return "0"
    return "F"



def __GATE(gate, *Inputs):
    operated = binaryOperation(Inputs[0].truthValues, Inputs[1].truthValues, gate)

    for i in range(2, len(Inputs)):
        operated = binaryOperation(operated, Inputs[i].truthValues, gate)
    return operated


def NOTgate(Input):
    return ~Input

def ANDgate(*Inputs):
    return Truth(__GATE("and", *Inputs))

def NANDgate(*Inputs, cascade=False):
    """Perform chain operation if cascade == True"""
    if cascade:
        return Truth(__GATE("nand", *Inputs))
    return ~Truth(__GATE("and", *Inputs))
    
def ORgate(*Inputs):
    return Truth(__GATE("or", *Inputs))

def NORgate(*Inputs, cascade=False):
    """Perform chain operation if cascade == True"""
    if cascade:
        return Truth(__GATE("nor", *Inputs))
    return ~Truth(__GATE("or", *Inputs))
    
def XORgate(*Inputs):
    return Truth(__GATE("xor", *Inputs))

def XNORgate(*Inputs, cascade=False):
    """Perform chain operation if cascade == True"""
    if cascade:
        return Truth(__GATE("xnor", *Inputs))
    return ~ Truth(__GATE("xor", *Inputs))
    

def generator(maxLenght, propositionDiffNumber, reversed=False):
    truthValues = []
    truthValue = True
    for i in range(maxLenght):
        truthValues.append(truthValue)
        if (i + 1) % propositionDiffNumber == 0:
            truthValue = not truthValue
    if reversed:
        truthValues.reverse()
    
    return tuple(truthValues)

def generateTruthRows(NumOfPropositions, reversed=False):
    maxLenght = 2 ** NumOfPropositions

    return [Truth(generator(maxLenght, maxLenght//(2 ** (i + 1)), reversed)) for i in range(NumOfPropositions)]

def printTT(truthData, space=4, binaryRepr=False, perfectAlign=False):
    """Print Truth Table"""
    truthRow = len(list(truthData.values())[0])
    sepSpace = " " * space
    seperator = sepSpace + "|" + sepSpace
    starter = "|" + sepSpace
    ender = sepSpace + "|"
    
    
    if perfectAlign:
        maxLenght = max([len(i) for i in truthData])
        strRep = starter +  seperator.join([i.center(maxLenght) for i in truthData]) + ender
    
        print("+" + "-"* (len(strRep)-2) + "+")
        print(strRep)
        print("+" + "-"* (len(strRep)-2) + "+")
        
        for i in range(truthRow):
            strRep = starter + seperator.join([truthLiteral(truthData[column].truthValues[i], binaryRepr).center(maxLenght) for column in truthData]) + ender
            print(strRep)
        print("+" + "-"* (len(strRep)-2) + "+")
        return

    strRep = starter +  seperator.join([i for i in truthData]) + ender
    
    print("+" + "-"* (len(strRep)-2) + "+")
    print(strRep)
    print("+" + "-"* (len(strRep)-2) + "+")

    for i in range(truthRow):
        strRep = starter + seperator.join([truthLiteral(truthData[column].truthValues[i], binaryRepr).center(len(column)) for column in truthData]) + ender
        print(strRep)
    print("+" + "-"* (len(strRep)-2) + "+")

def simplePrint(truthData, colSeperator="\t", rowSeperator="\n", binaryRepr=False, export=False):
    truthRow = len(list(truthData.values())[0])
    strRep = colSeperator.join([i for i in truthData])
    strRep += rowSeperator
    for i in range(truthRow):
        strRep += colSeperator.join([truthLiteral(truthData[column].truthValues[i], binaryRepr) for column in truthData])
        strRep += rowSeperator
    
    if export:
        return strRep
    print(strRep)