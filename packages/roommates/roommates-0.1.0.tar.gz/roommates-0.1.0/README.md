# Roommates

`roommates` helps you figure out equalization payments

## Installation

```
pip install roommates
```

## Usage

```
from roommates import split

# Register all previous payments
ribs = {
    'Alice': 50.25,
    'Bob':   30,
    'Eve':   0,
}

ice_cream = {
    'Bob': 20,
    'Eve': 15,
}

# Print equalization payments
split(ribs, ice_cream)
```

## Concerns

For any concerns, please email michael [dot] lindner [dot] daddario [at] gmail [dot] com
