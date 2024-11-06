# User Manual - Name Structure

&nbsp;

## General Format

The naming structure allows you to organize your object names according to your needs. It uses categories in brackets, separated by underscores (\_).

Format: `[category1]_[category2]_[category3]`

&nbsp;

## Available Categories

### [name]

- **Required** - must appear once in the structure
- Represents the base name of your object
- Example: if [name] = "arm", the result will be "arm"

&nbsp;

### [type]

- Not required - if not used, the option will not be displayed in the tool
- Corresponds to the type of your objects in the outliner
- Examples of group types: "grp", "ctrl"
- Examples of mesh types: "hi", "lo"

&nbsp;

### [symmetry]

- Not required - if not used, the option will not be displayed in the tool
- Indicates the symmetry of the object
- Default values:
  - L: left side
  - R: right side

&nbsp;

### [zoning]

- Not required - if not used, the option will not be displayed in the tool
- Specifies the spatial position of the object
- Default values:
  - Lt: left
  - Ct: center
  - Rt: right
  - Tp: top
  - Md: middle
  - Bt: bottom
  - Ft: front
  - Bk: back

&nbsp;

### [orientation]

- Not required - if not used, the option will not be displayed in the tool
- Indicates the orientation of the object
- Default values:
  - Nt: north
  - St: south
  - Et: east
  - Wt: west

&nbsp;

### [alphabetical_inc]

- Not required - if not used, the option will not be displayed in the tool
- Adds alphabetical incrementation (A, B, C...)

&nbsp;

### [numerical_inc]

- Not required - if not used, the option will not be displayed in the tool
- Adds numerical incrementation (001, 002, 003...)

&nbsp;

## Valid Structure Examples

1. Minimal structure:

   `[name]`

   > Result: arm

2. Structure with [type] and [symmetry]:

   `[symmetry]_[name]_[type]`

   > Result: L_arm_grp

3. Complete structure:

   `[symmetry]_[type]_[name][zoning][orientation][alphabetical_inc]_[numerical_inc]`

   > Result: L_armLtNtA_001_hi

&nbsp;

## Important Rules

1. The [name] category is mandatory
2. Other categories are optional
3. Each category can only appear once
4. Categories can be separated by an underscore (\_)
5. Multiple underscores are not allowed
6. The structure must not start or end with an underscore

&nbsp;

## Usage Tips

- Keep the structure as simple as possible while meeting your needs
- Test your structure with a few examples before using it on a large scale
- Some cases may not work properly, test and modify if necessary.
  (example: [Symmetry][Orientation] may display incorrect output in the case of LLt: the succession of two identical capital letters is not taken into account. However, finding this configuration in a nomenclature would be unusual!)
- Use presets to save your frequently used structures
