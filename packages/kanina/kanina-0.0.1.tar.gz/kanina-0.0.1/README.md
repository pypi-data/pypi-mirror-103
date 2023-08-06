# A simple calculator package

Calculator has memory inside. 
So you just have to do operations having this in mind. 
For exmaple if 10 is currently in memory, adding 2 will result in 12. 
When creating new Calculator instance you can initialize starting value.


install:

```python
pip install kanina
```

usage:
```python
import kanina
calc = kanina.calculator.Calculator()
calc.add(10)
calc.sub(5)
calc.mult(2)
calc.div(10)
calc.pow(2)
calc.root(2)
print(calt.cval())
calc.reset()
```

