## Description

Rename them all is a tool designed to facilitate the renaming of 3D elements in your projects, while meeting production-imposed criteria.
It aims to be as configurable as possible to handle a maximum number of use cases.

# Installation Instructions

To install the scripts available in this repository for Autodesk Maya and Substance Painter, please follow these steps:

> **Compatibility** : Maya 2024 and latest versions

### Maya installation:

- Locate the **renameThemAll** folder in this repository.
- Copy the **entire** renameThemAll folder.
- Paste the copied renameThemAll folder into Maya's default script directory. The default script directory for Maya is
  typically:

> C:\Users\<YourUsername>\Documents\maya\<MayaVersion>\scripts

### Shelf installation:

- Open the script editor in Maya.
- Add a Python tab.
- Paste the following code into the Python tab:
``` 
from renameThemAll import main_ui as main
def launch_ui():
  try:
    main.RenameThemAllUI.close() # pylint: disable=E0601
    main.RenameThemAllUI.deleteLater()
  except:
    pass
renameThemAll = main.RenameThemAllUI()
renameThemAll.show()
``` 
 

- Save the Python tab. (file > save script to shelf)

After completing these steps, the scripts and shelf should be properly installed and ready for use in Maya.
