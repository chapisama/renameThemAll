# User Manual - Type

&nbsp;

## General Description

The type system allows you to specify different categories for your objects in Maya. There are two main categories:

- Group types (for organizing objects)
- Mesh types (for different versions/LODs of meshes)

&nbsp;

## Notes

- The current version only takes into account groups and meshes. Other types, such as curves, joints, etc. will be added in future versions.

&nbsp;

## Format

- Types must contain only letters
- Multiple types can be specified, separated by commas
- Spaces around types are automatically removed

&nbsp;

## Optional

- Types are mandatory by default. They can be made optional by checking the "optional" box.
- If the optional box is checked, it means that even if there is no type specified in your object's name, the set will still be considered valid in the outliner.
- Conversely, if the optional box is not checked, the object name must contain a valid type, otherwise this name will be displayed as "invalid" in the outliner.

&nbsp;

## Default Values

If no value is specified, the default values are:

- for groups: 'prx', 'prp', 'grp', 'ctrl', 'proxy', 'render'
- for meshes: 'hi', 'lo'

&nbsp;

### Group Types Examples

```
grp, ctrl
```

### Mesh Types Examples

```
hi, lo
```

&nbsp;

## Valid Examples

1. Simple types:

   ```
   grp   ✔️
   hi    ✔️
   ```

2. Multiple types:

   ```
   grp, ctrl, loc   ✔️
   hi, lo, msh      ✔️
   ```

3. Mixed case:
   ```
   Grp, Ctrl   ✔️
   Hi, Lo     ✔️
   ```

&nbsp;

## Invalid Examples

1. With numbers:

   ```
   grp1, ctrl2  ❌
   ```

2. With special characters:

   ```
   grp-ctrl  ❌
   hi_lo    ❌
   ```

3. With spaces in types:
   ```
   group ctrl  ❌
   ```

&nbsp;

## Usage

- Types are activated when the [type] token is in the name structure.
