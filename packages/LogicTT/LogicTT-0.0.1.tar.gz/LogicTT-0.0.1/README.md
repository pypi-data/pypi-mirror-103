# Logic Truth Table Generator
Generate Truth Table for your Logic Exercises

> ## Installation
```sh
pip install LogicTT
```

> ## Project Demo
```python
from LogicTT import TT
```
To start using the module for Logical operations, call the function **generateTruthRows()** in the TT module. The funtion accepts the number of inputs\propositions as parameters and returns a list of Truth objects corresponding to the number of Inputs supplied
```python
p, q = TT.generateTruthRows(2)
```
Each Truth object contains the list of 1s/True and 0s/False generated accordingly. The function also takes a boolean optional parameter ***reversed*** to specify if truth rows should start with 1s or 0s (False by default i.e. start with 1s)

> ### **Printing Truth Table**
The function **printTT()** can be used to print the truth table, it takes in a dictionary as parameter. The keys of the dictionary are the headings of the table while the values are the table data
```python
TT.printTT({"p": p, "q": q})
```
```
Output:
+-------------------+
|    p    |    q    |
+-------------------+
|    T    |    T    |
|    T    |    F    |
|    F    |    T    |
|    F    |    F    |
+-------------------+
```
The ***printTT()*** takes some other keywords arguments:
- **space**: to specify the numbers of space to leave between each columns (integers only)
- **binaryRepr**: To use 1 and 0 for representation instead of T and F (boolean values only)
- **perfectAlign**: To leave equal amount of space between the columns of the Truth Table (also takes boolean values)
```python
A, B = TT.generateTruthRows(2)

TT.printTT(
    {
        "Column 1":A,
        "Second Column":B, 
    }, space=5, binaryRepr=True, perfectAlign=True
)
```
```
Output:
+-----------------------------------------------+
|        Column 1       |     Second Column     |
+-----------------------------------------------+
|           1           |           1           |
|           1           |           0           |
|           0           |           1           |
|           0           |           0           |
+-----------------------------------------------+
```
Alternative to the ***printTT()*** function you can use the ***simplePrint()*** to print the truth table in a way that can be used externally. It also takes a dictionary of the table data as parameter. Other parameters for the function includes *colSeperator*, *rowSeperator* which by default take the values "\t" and "\n" respectively.
```python
A, B = TT.generateTruthRows(2)

TT.simplePrint(
    {
        "A":A,
        "B":B, 
    }, colSeperator="\t", rowSeperator="\n", binaryRepr=True
)
```
```
Output:
A       B
1       1
1       0
0       1
0       0
```
> ### **Logical Operations on Truth Objects**
Logical operations can performed on the Truth Objects as follows:
```python
p, q = TT.generateTruthRows(2)

notP = ~ p       # NOT operation on p (can also use -p)
both = p & q     # AND operation on p and q (can also use p * q)
either = p | q   # OR operation on p and q (can also use p + q)

TT.printTT(
    {
        "P": p,
        "Q": q,
        "~ P": notP,
        "P Λ Q": both,
        "P V Q": either
    }, space=3
)
```
```
Output:
+-------------------------------------------------+
|   P   |   Q   |   ~ P   |   P Λ Q   |   P V Q   |
+-------------------------------------------------+
|   T   |   T   |    F    |     T     |     T     |
|   T   |   F   |    F    |     F     |     T     |
|   F   |   T   |    T    |     F     |     T     |
|   F   |   F   |    T    |     F     |     F     |
+-------------------------------------------------+
```
> ### Logical Operations (NOR, NAND, XOR, XNOR)

```python
p, q = TT.generateTruthRows(2)

norPQ = p.NOR(q)        # NOR operation on p and q (which is the same as ~(q + p))

nandPQ = p.NAND(q)      # NAND operation on p and q (also the same as  ~ (p * q))

xorPQ = p.XOR(q)        # XOR operation on p and q

xnorPQ = p.XNOR(q)      # XNOR operation on p and q (same as ~(p.XOR(q))

TT.printTT(
    {
        "p": p,
        "q": q,
        "p NOR q": norPQ,
        "p NAND q": nandPQ,
        "p XOR q": xorPQ,
        "p XNOR q": xnorPQ
    }, space=2
)
```
```
Output:
+-------------------------------------------------------------+
|  p  |  q  |  p NOR q  |  p NAND q  |  p XOR q  |  p XNOR q  |
+-------------------------------------------------------------+
|  T  |  T  |     F     |     F      |     F     |     T      |
|  T  |  F  |     F     |     T      |     T     |     F      |
|  F  |  T  |     F     |     T      |     T     |     F      |
|  F  |  F  |     T     |     T      |     F     |     T      |
+-------------------------------------------------------------+
```
> ### Other Logical Operations (Implication(If Then) and Biconditional (If And Only If))
The '>=' and '=<' signs can be used to perform the Implication operation While the '==' sign can be used to express Logical Equivalence (Biconditional)
```python
p, q = TT.generateTruthRows(2)

pTHENq = p >= q     # Same as q <= p
qTHENp = q >= p     # Same as p <= q 
m = ~ (p + q)       # Compound expression for NOR operation
n =  ~p * ~q        # AND operation and NOT operation
k = (m == n)        # Logical Equivalence

TT.printTT(
    {
        "p": p,
        "q": q,
        "p --> q": pTHENq,
        "q --> p": qTHENp,
        "m = ~(p V q)": m,
        "n = ~p Λ ~q": n,
        "m <--> n":k
    }, space=2
)
```
```
Output:
+---------------------------------------------------------------------------------+
|  p  |  q  |  p --> q  |  q --> p  |  m = ~(p V q)  |  n = ~p Λ ~q  |  m <--> n  |
+---------------------------------------------------------------------------------+
|  T  |  T  |     T     |     T     |       F        |       F       |     T      |
|  T  |  F  |     F     |     T     |       F        |       F       |     T      |
|  F  |  T  |     T     |     F     |       F        |       F       |     T      |
|  F  |  F  |     T     |     T     |       T        |       T       |     T      |
+---------------------------------------------------------------------------------+
```
The methods *IMP()* and *BICON()* can be used respectively for Implication and Biconditional Operations

> ## LOGIC GATES
A Logic Gate is an electronic device that makes logical decisions based on the different combinations 
of digital signals present on its inputs. Basic logic gates perform 
logical operations of AND, OR and NOT on binary numbers. A logic gate may have more than one input 
but only has one digital output.

The TT module contain functions that can simulate these gates. These gate functions takes in the Truth Object as parameters and returns a Truth object also which the speciefied operation has been carried on. The gates function include:

- ### Single Input Gate
    - **NOTgate()**: Takes in a single Truth Object and returns a NOT logically operated Truth Object
- ### Multiple Inputs Gates
    - ***ORgate()***: Performs logical OR operation on two or more Truth Object Inputs
    - ***NORgate()***: Performs the Operation of logical NOT on the output of the ORgate() on multiple Truth object inputs
    - ***ANDgate()***: Performs logical AND operation on two or more Truth Object Inputs
    - ***NANDgate()***: Performs the Operation of logical NOT on the output of the ANDgate() on multiple Truth Object inputs
    - ***XORgate()***: Operation of logical Exclusive OR on the Inputs
    - ***XNORgate()***: Operation of logical NOT on the output of the XORgate() on multiple Truth Object inputs

```python
a, b, c = TT.generateTruthRows(3, reversed=True)

p = TT.NOTgate(a)
q = TT.NOTgate(b)
r = TT.ORgate(a, b, c)
s = TT.NORgate(a, b, c)
t = TT.ANDgate(a, b, c)
u = TT.NANDgate(a, b, c)
v = TT.XORgate(a, b, c)
w = TT.XNORgate(a, b, c)

TT.printTT(
    {
        "a":a,
        "b":b,
        "c":c,
        "p = a\'": p,
        "q = b\'": q,
        "r = a + b + c": r,
        "s = (a + b + c)\'": s,
        "t = a · b · c": t,
        "u = (a · b · c)\'": u,
        "v = (a ⨁ b ⨁ c)": v,
        "w = (a ⨁ b ⨁ c)\'": w
    }, space=2, binaryRepr=True
)
```
```
Output:
+--------------------------------------------------------------------------------------------------------------------------------------------------------------+
|  a  |  b  |  c  |  p = a'  |  q = b'  |  r = a + b + c  |  s = (a + b + c)'  |  t = a · b · c  |  u = (a · b · c)'  |  v = (a ⨁ b ⨁ c)  |  w = (a ⨁ b ⨁ c)'  |
+--------------------------------------------------------------------------------------------------------------------------------------------------------------+
|  0  |  0  |  0  |    1     |    1     |        0        |         1          |        0        |         1          |         0         |         1          |
|  0  |  0  |  1  |    1     |    1     |        1        |         0          |        0        |         1          |         1         |         0          |
|  0  |  1  |  0  |    1     |    0     |        1        |         0          |        0        |         1          |         1         |         0          |
|  0  |  1  |  1  |    1     |    0     |        1        |         0          |        0        |         1          |         0         |         1          |
|  1  |  0  |  0  |    0     |    1     |        1        |         0          |        0        |         1          |         1         |         0          |
|  1  |  0  |  1  |    0     |    1     |        1        |         0          |        0        |         1          |         0         |         1          |
|  1  |  1  |  0  |    0     |    0     |        1        |         0          |        0        |         1          |         0         |         1          |
|  1  |  1  |  1  |    0     |    0     |        1        |         0          |        1        |         0          |         1         |         0          |
+--------------------------------------------------------------------------------------------------------------------------------------------------------------+
```
> The Negation gates (NOR, NAND, XNOR) has a special keyword argument ***cascade*** which can be set to True to enable to gates to perform a chain operation on the inputs. For Example: NORgate(a, b, c, cascade=True) will return NOR(NOR(a, b), c)
```python
a, b, c = TT.generateTruthRows(3, reversed=True)

d = ~(a + b)            # a NOR b
e = ~(d + c)            # (a NOR b) NOR c

cascadeNOR = TT.NORgate(a, b, c, cascade=True)

R = (e == cascadeNOR)   # e is equivalent to cascadeNOR

TT.printTT(
    {
        "a": a,
        "b": b,
        "c": c,
        "d = ~(a + b)": d,
        "e = ~(d + c)": e,
        "f = cascadeNOR": cascadeNOR,
        "e <--> f": R
    }, space=2, binaryRepr=True
)
```
```
Output:
+-----------------------------------------------------------------------------------+
|  a  |  b  |  c  |  d = ~(a + b)  |  e = ~(d + c)  |  f = cascadeNOR  |  e <--> f  |
+-----------------------------------------------------------------------------------+
|  0  |  0  |  0  |       1        |       0        |        0         |     1      |
|  0  |  0  |  1  |       1        |       0        |        0         |     1      |
|  0  |  1  |  0  |       0        |       1        |        1         |     1      |
|  0  |  1  |  1  |       0        |       0        |        0         |     1      |
|  1  |  0  |  0  |       0        |       1        |        1         |     1      |
|  1  |  0  |  1  |       0        |       0        |        0         |     1      |
|  1  |  1  |  0  |       0        |       1        |        1         |     1      |
|  1  |  1  |  1  |       0        |       0        |        0         |     1      |
+-----------------------------------------------------------------------------------+
```

> ### Conclusion
Enjoy this little project to work with Truth Tables and Logic Gates and discover some hidden interesting and weird truths about Logic/Binary operations. You have a Math or Digital Logic Gate Assignment and your are required to generate a 64 rows Truth Table or more?, don't panic use TT😋😊!!!
***

> ### Acknowledgements
- The ***LISP***ers: My wonderful Team
    - [E++](https://github.com/eniolaemma904)
    - [Fadahemmy](https://github.com/Fada-Hemmy)
    - [newtraque](https://github.com/newtraque)
    - [Godwin](https://github.com/el9ty6ix)
    - Onyi
    - Ikigai
    - Blessing
- ***Dr Nancy Woods***: My wonderful Lecturer 😊 whose great teachings on Digital Logic Design inspired the development of this project.
    