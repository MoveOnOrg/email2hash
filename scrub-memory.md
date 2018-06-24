# Scrubbing Memory in Python

    1. Python Memory Management
    2. OS Memory
    3. Conclusion

One would expect a program like email2hash.py -- which takes input a list of
email addresses and then hashes them with a cryptographic hash algorithm
(SHA3-256) -- to clear the RAM after its operation. We will attempt to explain
why this is difficult with a language like Python, and why it gives a false
sense of security even if we could make it work.

## 1. Python Memory Management

Python does not offer low-level access to the memory and memory management is
performed via automatic garbage collection. As per the manual [0],

    It is important to understand that the management of the Python heap is
    performed by the interpreter itself and that the user has no control over it,
    even if she regularly manipulates object pointers to memory blocks inside that
    heap. 

[0] - https://docs.python.org/3/c-api/memory.html 

One may argue the use of the `del` keyword:

    >>> x = 1
    >>> print(x)
    1
    >>> del x
    >>> print(x)
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    NameError: name 'x' is not defined

But this just means that `del` will unbind a name from an object but there is
''no'' guarantee that the memory will actually be cleared [1].

    Deletion of a name removes the binding of that name from the local or global
    namespace, depending on whether the name occurs in a global statement in the
    same code block. If the name is unbound, a NameError exception will be raised.

[1] - https://docs.python.org/3/reference/simple_stmts.html#the-del-statement

In short, there is no way to scrub the memory in Python because the memory is
managed by the interpreter and we have no control over it.

## 2. OS Memory

Coming back to the original argument and even if we assume that we can clear
up the memory, it assumes an attack that may not be realistic. If an attacker
would want to read the contents of your RAM, they need `root` access (for
example, reading the contents of `/proc/pid/maps` on Linux) and if that is the
case, the game is already over and clearing the memory of the Python program
is not going to be helpful.

## 3. Conclusion

Worrying about the contents of the RAM is not a realistic attack vector; we
should avoid saving plain text to disk and that's the most we can aim for.
Ultimately, the memory access is as safe as allowed by the operating system
and any optimization to that effect gives a false sense of security.
