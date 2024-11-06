from enum import Enum

class DefaultNameStructure(Enum):
    NAME_STRUCTURE = r'[symmetry]_[type]_[name][zoning][orientation][alphabetical_inc]_[numerical_inc]'
    OPTIONAL_CATEGORIES = ["symmetry", "zoning", "orientation", "alphabetical_inc", "numerical_inc"]
    MANDATORY_CATEGORIES = ["type", "name"]

class DefaultColor(Enum):
    VALID = "#74dc6f"  # light green
    VALID_SUFFIXES = "#2a9838"  # green
    INVALID = "#c12f3a"  # red
    TO_CHECK = "#d9bb42"  # yellow
    REFERENCE = "#4d91df"  # blue
    INSTANCE = "#a840af"  # purple

class DefaultGroupType(Enum):
    PRX = "prx"
    PRP = "prp"
    GRP = "grp"
    CTRL = "ctrl"
    PROXY = "proxy"
    RENDER = "render"

class DefaultMeshType(Enum):
    HI = "hi"
    LO = "lo"

class DefaultZoningSingle(Enum):
    LEFT = "Lt"
    CENTER = "Ct"
    RIGHT = "Rt"
    TOP = "Tp"
    MIDDLE = "Md"
    BOTTOM = "Bt"
    FRONT = "Ft"
    BACK = "Bk"

class DefaultOrientSingle(Enum):
    NORTH = "Nt"
    WEST = "Wt"
    EAST = "Et"
    SOUTH = "St"

class DefaultSymmetryOptions(Enum):
    LEFT = "L"
    RIGHT = "R"

class DefaultNumIncLenght(Enum):
    NUMBER_OF_DIGITS = 3

class DefaultMainGroup(Enum):
    ALL = "ALL"

'''class DefaultMainGroup(Enum):
    @staticmethod
    def get_master_grp_name() -> str:
        """
        Get the master group name by looking at the file name.

        Returns
        -------
        str
            Name of the master group.

        Raises
        ------
        RuntimeError
            If retrieving the master group name fails.
        """
        try:
            file_name = mc.file(q=True, sceneName=True, shortName=True)
            master_grp = DefaultMainGroup.dict_file_name_part(file_name).get("asset_name")
            return master_grp
        except RuntimeError as e:
            raise RuntimeError(f"Failed to get master group name: {str(e)}")

    @staticmethod
    def dict_file_name_part(file_name: str) -> dict:
        """
        Parse the file name and store all components of the asset name.

        Parameters
        ----------
        file_name : str
            Name of the file. Example: prp_jarA_001.ma
            prp: asset type
            prp_jarA: asset_name
            jarA: short name
            001: inc number
            ma: file_type

        Returns
        -------
        dict
            A dictionary containing all components of the file name.

        Raises
        ------
        RuntimeError
            If parsing the file name fails.
        """
        try:
            dict_file_name = {
                "asset_type": file_name.split("_")[0],
                "asset_name": file_name.split("_")[0] + "_" + file_name.split("_")[1],
                "asset_short_name": file_name.split("_")[1],
                "inc_number": int("{:03d}".format(int(file_name.split("_")[2].split(".")[0]))),
                "file_type": file_name.split(".")[-1],
            }
            return dict_file_name
        except (IndexError, ValueError) as e:
            raise RuntimeError(f"OutlinerLogics.dict_file_name_part: Failed to parse file name: {str(e)}")'''
