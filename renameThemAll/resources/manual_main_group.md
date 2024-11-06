# User Manual - Main Group

&nbsp;

## General Description

The main group is the name of the parent group that will contain all your objects.
In most productions, this group corresponds to the content that will be exported, in .FBX format for example.

&nbsp;

## Notes

- Currently, this tool does not allow displaying the content of multiple groups at the same time. A future update of the tool will fix this issue.

&nbsp;

## Format

- The name must contain only letters and underscores (\_)
- Spaces are not allowed
- Case (uppercase/lowercase) is preserved

&nbsp;

## Default Value

If no value is specified, the default value is:

```
ALL
```

&nbsp;

## Valid Examples

1. Simple name:

   ```
   ALL   ✔️
   ```

2. Compound name with underscore:
   ```
   MAIN_GROUP  ✔️
   ```

&nbsp;

## Invalid Examples

1. With special characters:

   ```
   MAIN-GROUP  ❌
   ```

2. With spaces:

   ```
   MAIN GROUP  ❌
   ```

3. With numbers:
   ```
   GROUP_01  ❌
   ```

&nbsp;

## Usage

If it exists in your Maya scene, the main group will be displayed in this outliner.

&nbsp;

## Tip

- Avoid names that could conflict with other elements in your scene.
