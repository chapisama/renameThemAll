# User Manual - Incrementation

&nbsp;

## General Description

Allows you to define the number of digits in the numerical incrementation.

&nbsp;

## Format

- Numerical increment length must contain only digits
- The numerical increment length must be greater than 0

&nbsp;

## Default Values

If no value is specified, the default values are:

- Numerical increment length: 3 (resulting in: 001, 002, 003, etc.)

&nbsp;

## Invalid Examples

1. Negative numbers:

   ```
   -1   ❌
   ```

2. With letters in numerical increment:

   ```
   A01   ❌
   1B2   ❌
   ```

3. With special characters:
   ```
   001#   ❌
   A@B    ❌
   ```

&nbsp;

## Usage

- Numerical incrementation is activated when the [numerical_inc] token is in the name structure
