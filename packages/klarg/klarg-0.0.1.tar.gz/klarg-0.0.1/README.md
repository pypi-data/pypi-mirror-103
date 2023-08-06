# Klarg

A **K**ommand **L**ine **ARG**ument parsing library.

Klarg is a small and simple command line argument parsing library built with no 3rd party dependencies.


# Why use klarg?
## Simple syntax
It abstracts all the complexities away so that you can focus on developing the appication itself. 

```py
# example.py
import klarg
name = klarg.get_str("name")
print(f"Your name is: {name}")

# python example.py --name klarg
# Your name is: klarg
```

## Easy configuring
It makes use of the powerful dictionary data type to make configuring klarg a breeze.

```py
# example.py
import klarg

# Replace -- with +
CONFIG["long_prefix"] = "+"
name = klarg.get_str("name")
print(f"Your name is: {name}")

# python example.py +name klarg
# Your name is klarg
```

## Simple data types
Klarg only returns basic data types such as `int`, `float`, `str` and `bool`. This means no converting from strings to integers, or to booleans, klarg already does that.

```py
# example.py
import klarg

is_there = klarg.get_bool("is-there")
if is_there:
    print("I am here")
else:
    print("I am not here")

# python example.py --is-there
# I am here
```

## No 3rd party dependencies
Klarg was specifically designed not to include any external dependencies, helping to keep the size small. 

# Installation
Installing klarg is incredibly simple, just type in
```sh
pip install klarg
```

# How to use?
```py
# example.py
import klarg
klarg_is_cool = klargs.get_bool(long="klarg-cool", short="k")
klargs.on_help(do_something)

if (klarg_is_cool):
    print("Oh, my, klarg is cool.")

# python example.py --klarg-cool
# Oh, my, klarg is cool.

# python example.py -k
# Oh, my, klarg is cool.
```
Check out the [Documentation](https://github.com/tominekan/klarg/blob/main/DOCS.md) for more. 