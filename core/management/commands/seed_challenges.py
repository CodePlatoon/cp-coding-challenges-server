from django.core.management.base import BaseCommand
from core.models import CodingChallenge


CHALLENGES = [
    {
        "order": 1,
        "mini_lesson": """# Lesson: Print & Variables

In Python, you store values in **variables** and display them with `print()`.

```python
name = "Alice"
print(name)  # Output: Alice

age = 25
print(age)   # Output: 25
```

A variable is like a labeled box that holds a value. You can name it almost anything, but use lowercase letters and underscores (e.g., `my_name`).

**Your challenge:** Create a variable called `greeting` that holds the string `"Hello, World!"` and print it.
""",
        "init_temp": """# Write your solution below
greeting =

print(greeting)
""",
        "tests": {
            "test_code": """
assert greeting == "Hello, World!", f"Expected 'Hello, World!' but got '{greeting}'"
print("All tests passed!")
"""
        },
    },
    {
        "order": 2,
        "mini_lesson": """# Lesson: String Methods

Strings have built-in **methods** — actions you can perform on them.

```python
name = "alice"
print(name.upper())       # Output: ALICE
print(name.capitalize())  # Output: Alice
print(name.replace("a", "o"))  # Output: "olice"
```

Call a method with a dot (`.`) after the variable name, followed by the method name and parentheses.

**Your challenge:** Given the variable `word = "python"`, create a new variable called `shout` that holds the uppercase version and print it.
""",
        "init_temp": """word = "python"

# Create a variable called 'shout' with the uppercase version of word
shout =

print(shout)
""",
        "tests": {
            "test_code": """
assert shout == "PYTHON", f"Expected 'PYTHON' but got '{shout}'"
print("All tests passed!")
"""
        },
    },
    {
        "order": 3,
        "mini_lesson": """# Lesson: Basic Arithmetic

Python handles math with these operators:

| Operator | Meaning       | Example  | Result |
|----------|--------------|----------|--------|
| `+`      | Add          | `3 + 2`  | `5`    |
| `-`      | Subtract     | `5 - 1`  | `4`    |
| `*`      | Multiply     | `4 * 3`  | `12`   |
| `/`      | Divide       | `10 / 2` | `5.0`  |
| `**`     | Power        | `2 ** 3` | `8`    |

**Your challenge:** Create a variable `result` that holds the value of `7 * 6` and print it.
""",
        "init_temp": """# Calculate 7 multiplied by 6 and store it in 'result'
result =

print(result)
""",
        "tests": {
            "test_code": """
assert result == 42, f"Expected 42 but got {result}"
print("All tests passed!")
"""
        },
    },
    {
        "order": 4,
        "mini_lesson": """# Lesson: Lists & Indexing

A **list** stores multiple values in order. Access items by their **index** (position), starting from 0.

```python
fruits = ["apple", "banana", "cherry"]
print(fruits[0])  # Output: apple
print(fruits[1])  # Output: banana
print(fruits[2])  # Output: cherry
print(fruits[-1]) # Output: cherry (last item)
```

**Your challenge:** Given `colors = ["red", "green", "blue"]`, create a variable `first` that holds the first color and print it.
""",
        "init_temp": """colors = ["red", "green", "blue"]

# Get the first color using indexing
first =

print(first)
""",
        "tests": {
            "test_code": """
assert first == "red", f"Expected 'red' but got '{first}'"
print("All tests passed!")
"""
        },
    },
    {
        "order": 5,
        "mini_lesson": """# Lesson: Booleans & Comparisons

A **boolean** is either `True` or `False`. Comparisons return booleans.

```python
print(5 > 3)   # True
print(2 == 2)  # True
print(4 != 4)  # False
print(10 < 7)  # False
```

Common comparison operators: `==` (equal), `!=` (not equal), `>`, `<`, `>=`, `<=`.

**Your challenge:** Create a variable `is_greater` that holds the result of `10 > 3` and print it.
""",
        "init_temp": """# Store the result of the comparison 10 > 3 in 'is_greater'
is_greater =

print(is_greater)
""",
        "tests": {
            "test_code": """
assert is_greater == True, f"Expected True but got {is_greater}"
print("All tests passed!")
"""
        },
    },
    {
        "order": 6,
        "mini_lesson": """# Lesson: Defining Functions

A **function** is a reusable block of code. Define one with `def`, give it a name, and use `return` to send back a value.

```python
def greet(name):
    return "Hello, " + name

print(greet("Alice"))  # Output: Hello, Alice
```

The value inside the parentheses is called a **parameter** — it's a placeholder for the input.

**Your challenge:** Define a function called `double` that takes a number `n` and returns `n * 2`.
""",
        "init_temp": """# Define a function called 'double' that returns n * 2
def double(n):
    return

print(double(5))  # Should print 10
""",
        "tests": {
            "test_code": """
assert double(5) == 10, f"Expected 10 but got {double(5)}"
assert double(0) == 0, f"Expected 0 but got {double(0)}"
assert double(-3) == -6, f"Expected -6 but got {double(-3)}"
print("All tests passed!")
"""
        },
    },
    {
        "order": 7,
        "mini_lesson": """# Lesson: If / Else

Use `if` and `else` to make decisions in your code.

```python
temperature = 30

if temperature > 25:
    print("It's hot!")
else:
    print("It's cool.")
```

Python uses **indentation** (4 spaces) to define what's inside the `if` or `else` block.

**Your challenge:** Define a function called `is_even` that takes a number `n` and returns `True` if it's even, `False` otherwise. (Hint: use the `%` operator — `n % 2 == 0` is True when n is even.)
""",
        "init_temp": """def is_even(n):
    if n % 2 == 0:
        return
    else:
        return

print(is_even(4))   # Should print True
print(is_even(7))   # Should print False
""",
        "tests": {
            "test_code": """
assert is_even(4) == True, f"Expected True but got {is_even(4)}"
assert is_even(7) == False, f"Expected False but got {is_even(7)}"
assert is_even(0) == True, f"Expected True but got {is_even(0)}"
assert is_even(-2) == True, f"Expected True but got {is_even(-2)}"
print("All tests passed!")
"""
        },
    },
    {
        "order": 8,
        "mini_lesson": """# Lesson: Loops

A `for` loop repeats code for each item in a sequence.

```python
numbers = [1, 2, 3, 4, 5]
total = 0
for num in numbers:
    total = total + num
print(total)  # Output: 15
```

You can also loop over a range: `for i in range(5)` gives you 0, 1, 2, 3, 4.

**Your challenge:** Define a function called `sum_list` that takes a list of numbers and returns their sum.
""",
        "init_temp": """def sum_list(numbers):
    total = 0
    for num in numbers:
        total =
    return total

print(sum_list([1, 2, 3, 4, 5]))  # Should print 15
""",
        "tests": {
            "test_code": """
assert sum_list([1, 2, 3]) == 6, f"Expected 6 but got {sum_list([1, 2, 3])}"
assert sum_list([10, 20, 30]) == 60, f"Expected 60 but got {sum_list([10, 20, 30])}"
assert sum_list([]) == 0, f"Expected 0 but got {sum_list([])}"
print("All tests passed!")
"""
        },
    },
    {
        "order": 9,
        "mini_lesson": """# Lesson: List Comprehensions

A **list comprehension** is a concise way to build a list.

```python
# Long way
squares = []
for n in range(5):
    squares.append(n ** 2)

# Short way (list comprehension)
squares = [n ** 2 for n in range(5)]
print(squares)  # Output: [0, 1, 4, 9, 16]
```

You can also add a condition:
```python
evens = [n for n in range(10) if n % 2 == 0]
print(evens)  # Output: [0, 2, 4, 6, 8]
```

**Your challenge:** Define a function called `get_evens` that takes a list of numbers and returns a new list containing only the even numbers, using a list comprehension.
""",
        "init_temp": """def get_evens(numbers):
    return [n for n in numbers if ]

print(get_evens([1, 2, 3, 4, 5, 6]))  # Should print [2, 4, 6]
""",
        "tests": {
            "test_code": """
assert get_evens([1, 2, 3, 4, 5, 6]) == [2, 4, 6], f"Expected [2, 4, 6] but got {get_evens([1, 2, 3, 4, 5, 6])}"
assert get_evens([1, 3, 5]) == [], f"Expected [] but got {get_evens([1, 3, 5])}"
assert get_evens([2, 4, 6]) == [2, 4, 6], f"Expected [2, 4, 6] but got {get_evens([2, 4, 6])}"
print("All tests passed!")
"""
        },
    },
]


class Command(BaseCommand):
    help = 'Seed the database with 9 coding challenges (idempotent)'

    def handle(self, *args, **options):
        created = 0
        for data in CHALLENGES:
            obj, was_created = CodingChallenge.objects.get_or_create(
                order=data['order'],
                defaults={
                    'mini_lesson': data['mini_lesson'],
                    'tests': data['tests'],
                    'init_temp': data['init_temp'],
                },
            )
            if was_created:
                created += 1
                self.stdout.write(self.style.SUCCESS(f"  Created: Challenge #{data['order']}"))
            else:
                self.stdout.write(f"  Already exists: Challenge #{data['order']}")

        self.stdout.write(self.style.SUCCESS(f"\nDone. {created} new challenges created."))
