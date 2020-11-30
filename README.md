# Tuf
Tuf is an abreviation of stack stuff, this is a stack based programming language i'm working on.

## Examples
> printing a string and 3 numbers
```python
def (main)

  new (3)    # creating a new stack
  select (3) # selecting the stack

  emit ("hey" ASC LEN) # getting ascii value of "hey" and putting it on the stack, putting its length and then printing it
  CB # clearing the string buffer (you dont need to do this anymore)
  1  # putting 1, 2 and 3 on the stack
  2
  3
  . . . # printing the 3 numbers on the top of the stack

endef

main # calling the main function
```



> conditionals
```python
 def (main)
 
  ~add 1 2 # the ~ metacommand postfixes the word after it, for example, the '~add 1 2' will result in '1 2 add'
  ~ne 3 # this will pop 3 and 3 from the stack and apply a NOT operation
    # this is the body of the condition
    emit ("this will not be printed since the condition (3 != 3) is false" ASC LEN)
  en # this closes the NE, you can see that it's the inverse of it
 
 endef
 
 main
```
