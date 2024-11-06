# User Manual - Orientation

&nbsp;

## General Description

The orientation system allows you to add orientation tokens in the naming structure. It helps specify the directional facing of objects in Maya using cardinal points.

&nbsp;

## Format

- Orientations must contain only letters
- Case (uppercase/lowercase) is preserved

&nbsp;

## Optional

- The orientation is optional by default. It can be made optional by checking the "optional" box.
- If the optional box is checked, it means that even if there is no orientation specified in your object's name, the set will still be considered valid in the outliner.
- Conversely, if the optional box is not checked, the object name must contain a valid orientation, otherwise this name will be displayed as "invalid" in the outliner.

&nbsp;

## Default Values

If no value is specified, the default values are:

- North: Nt
- South: St
- East: Et
- West: Wt

&nbsp;

## Valid Examples

1. Simple orientations:

   ```
   Nt   ✔️
   St   ✔️
   Et   ✔️
   Wt   ✔️
   ```

2. Mixed case:
   ```
   Nt   ✔️
   nt   ✔️
   ```

&nbsp;

## Invalid Examples

1. With numbers:

   ```
   Nt1   ❌
   St2   ❌
   ```

2. With special characters:

   ```
   Nt-St   ❌
   Et_Wt   ❌
   ```

3. With spaces:
   ```
   Nt St   ❌
   ```

&nbsp;

## Usage

- The orientation is activated when the [orientation] token is in the name structure
