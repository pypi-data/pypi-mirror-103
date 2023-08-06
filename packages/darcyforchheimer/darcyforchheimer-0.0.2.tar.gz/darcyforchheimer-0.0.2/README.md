# darcy-forchheimer calculator

The goal of the package is to help obtaining the Darcy and Forchheimer coefficients, very useful for porous material fluid simulations.

## Installation

Run the following to install:

```python
pip install darcyforchheimer
```

## Use

```python
from darcyforchheimer import calculate_coeficients
calculate_coefficients([velocity], [pressure], thickness, density, viscosity)
```

If you want to calculate absolute coefficients, not depending on thickness, include the argument

```python
calculate_coefficients(..., absolute=True)
```