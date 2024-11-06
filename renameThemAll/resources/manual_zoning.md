# User Manual - Zoning

&nbsp;

## General Description

The zoning system allows you to add zoning tokens in the naming structure.

&nbsp;

## Format

- Zones must contain only letters
- Case (uppercase/lowercase) is preserved

&nbsp;

## Optional

- The zoning is optional by default. It can be made optional by checking the "optional" box.
- If the optional box is checked, it means that even if there is no zoning specified in your object's name, the set will still be considered valid in the outliner.
- Conversely, if the optional box is not checked, the object name must contain a valid zoning, otherwise this name will be displayed as "invalid" in the outliner.

&nbsp;

## Default Values

If no value is specified, the default values are:

- Left: Lt
- Center: Ct
- Right: Rt
- Top: Tp
- Middle: Md
- Bottom: Bt
- Front: Ft
- Back: Bk

&nbsp;

## Valid Examples

1. Simple positions:
   ```
   Lt   ✔️
   Ct   ✔️
   Rt   ✔️
   ```

&nbsp;

## Invalid Examples

1. With numbers:
   ```
   Lt1   ❌
   Tp2   ❌
   ```

&nbsp;

## Usage

- The zoning is activated when the [zoning] token is in the name structure
