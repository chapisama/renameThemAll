# User Manual - Symmetry

&nbsp;

## General Description

The symmetry system allows you to add symmetry tokens in the naming structure.

&nbsp;

## Format

- Symmetry tokens must contain letters
- Case (uppercase/lowercase) is preserved

&nbsp;

## Optional

- The symmetry is optional by default. It can be made optional by checking the "optional" box.
- If the optional box is checked, it means that even if there is no symmetry specified in your object's name, the set will still be considered valid in the outliner.
- Conversely, if the optional box is not checked, the object name must contain a valid symmetry, otherwise this name will be displayed as "invalid" in the outliner.

&nbsp;

## Default Values

If no value is specified, the default values are:

- Left: L
- Right: R

&nbsp;

## Valid Examples

1. Simple symmetry:

   ```
   L    ✔️
   R    ✔️
   ```

2. Mixed case:
   ```
   l    ✔️
   r    ✔️
   ```

&nbsp;

## Invalid Examples

1. With numbers:

   ```
   L1    ❌
   R2    ❌
   ```

2. With special characters:

   ```
   L-R    ❌
   L_R    ❌
   ```

3. With spaces:
   ```
   L R    ❌
   ```

&nbsp;

## Usage

- The symmetry is activated when the [symmetry] token is in the name structure
- Only one symmetry token can be used at a time
