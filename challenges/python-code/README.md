# Eval Filter

In this challenge, your input will be validated, then run through Python's `eval`.
If the result is the `code` type, you get the flag.

You'll need to use Python's introspection, since you can't import anything.
Your input can be up to 40 characters long, and may only include the following
characters:

    a-z 0-9 _ . : []

Python code objects are a low-level feature of the interpreter, and are rarely
used directly. You won't need to know the details of code objects, you just
need to find the class from which they're made.

