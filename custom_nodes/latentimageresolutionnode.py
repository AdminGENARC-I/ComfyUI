class LatentImageResolutionNode:
    """
    A node that determines the latent image resolution based on the selected aspect ratio and resolution.

    Class methods
    -------------
    INPUT_TYPES (dict): 
        Defines input parameters of the node.

    Attributes
    ----------
    RETURN_TYPES (tuple): 
        The type of each element in the output tuple.
    FUNCTION (str):
        The name of the entry-point method.
    CATEGORY (str):
        The category the node should appear in the UI.
    execute(s) -> tuple || None:
        The entry point method.
    """
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(cls):
        """
        Returns a dictionary which contains configuration for all input fields.
        """
        return {
            "required": {
                "aspect_ratio": (["1:1 (Square)", "3:2 (Horizontal)", "4:3 (Horizontal)", 
                                  "16:9 (Horizontal)", "19:9 (Cinematic Horizontal)", 
                                  "3:4 (Vertical)", "9:16 (Vertical)", "2:3 (Vertical)", 
                                  "9:19 (Vertical)"],),
                "resolution": (["SD (480p)", "HD (720p)", "FULL HD (1080p)", 
                                "QHD (1440p)"],),  # Descriptive resolution options
            },
        }

    RETURN_TYPES = ("INT", "INT")  # Outputs will be width and height
    RETURN_NAMES = ("image_width", "image_height")
    FUNCTION = "calculate_dimensions"
    CATEGORY = "Image Processing"

    def calculate_dimensions(self, aspect_ratio, resolution):
        # Define the shorter side based on the selected resolution
        resolution_map = {
            "SD (480p)": 480,     # 480p
            "HD (720p)": 720,     # 720p
            "FULL HD (1080p)": 1080,  # 1080p
            "QHD (1440p)": 1440,  # 1440p
        }
        
        short_side = resolution_map[resolution]
        width, height = 0, 0

        # Calculate width and height based on the aspect ratio
        if aspect_ratio == '1:1 (Square)':
            width = height = short_side  # Square format
        elif aspect_ratio == '3:2 (Horizontal)':
            height = short_side
            width = int(height * (3/2))  # 3:2 aspect ratio
        elif aspect_ratio == '4:3 (Horizontal)':
            height = short_side
            width = int(height * (4/3))  # 4:3 aspect ratio
        elif aspect_ratio == '16:9 (Horizontal)':
            height = short_side
            width = int(height * (16/9))  # 16:9 aspect ratio
        elif aspect_ratio == '19:9 (Cinematic Horizontal)':
            height = short_side
            width = int(height * (19/9))  # 19:9 aspect ratio
        elif aspect_ratio == '3:4 (Vertical)':
            width = short_side  # Width set to short side
            height = int(width * (4/3))  # 4:3 aspect ratio
        elif aspect_ratio == '9:16 (Vertical)':
            width = short_side  # Set width as short side
            height = int(width * (16/9))  # 9:16 aspect ratio
        elif aspect_ratio == '2:3 (Vertical)':
            width = short_side  # Width set to short side
            height = int(width * (3/2))  # 2:3 aspect ratio
        elif aspect_ratio == '9:19 (Vertical)':
            width = short_side  # Width set to short side
            height = int(width * (19/9))  # 9:19 aspect ratio

        return (width, height)

# A dictionary that contains all nodes you want to export with their names
NODE_CLASS_MAPPINGS = {
    "LatentImageResolution": LatentImageResolutionNode
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "LatentImageResolution": "Latent Image Resolution"
}
