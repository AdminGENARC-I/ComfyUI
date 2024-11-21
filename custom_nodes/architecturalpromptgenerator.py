import random

class ArchitecturalPromptNode:
    """
    A node that generates architectural photography prompts based on selected parameters.
    If 'random' is selected for atmosphere, the atmosphere prompt will not be included.
    
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
                "architect": (["random", "Greg Lynn", "Eric Owen Moss", "Peter Eisenman", "Jeanne Gang", "Jon Jerde", 
                               "Rafael Vinoly", "Alejandro Aravena", "Oscar Niemeyer", "Luis Barragan", 
                               "Frank Gehry", "Jacques Herzog, Pierre de Meuron", "Peter Zumthor", "Mario Botta", 
                               "Bjarke İngels", "Alvar Aalto", "Eero Saarinen", "Rem Koolhaas", "Daniel Libeskind", 
                               "Anna Heringer", "Glenn Murcutt", "Nicholas Grimshaw", "Norman Foster", 
                               "Yvonne Farrell; Shelley McNamara", "Jean Nouvel", "Carlo Scarpa", "Aldo Rossi", 
                               "Richard Rogers", "Massimiliano Fuksas", "Renzo Piano", "Lina Bo Bardi", 
                               "Ricardo Bofill", "Enric Ruiz Geli", "Santiago Calatravva", "Manuel Aires Mateus", 
                               "Alvaro Siza Vieira", "Tadao Ando", "Kenzo Tange", "Kengo Kuma", "Kazuyo Seijama", 
                               "Shigeru Ban", "Kisho Kurokawa", "Ieoh Ming Pei", "Wang Shu", "Toyo Ito", 
                               "Vo Trong Nghia", "Balkrishna Vithaldas Doshi", "Diebedo Francis Kere", 
                               "Christian de Portzamparc", "Zaha Hadid", "Marco Zanuso", "Moshe Safdie", 
                               "Sedad Hakkı Eldem", "Behruz Çinici", "Şevki Vanlı"],),
                "region": (["random", "Africa", "Asia", "Europe", "North America", "Oceania", "South America"],),
                "building_type": (["random", "Residential Architecture", "Refurbishment", "Cultural Architecture", 
                                   "Commercial And Offices", "Hospitality Architecture", "Public Architecture", 
                                   "Healthcare Architecture", "Educational Architecture", "Sports Architecture", 
                                   "Religious Architecture", "Industrial And Infrastructure", "Landscape And Urbanism"],),
                "interior_exterior": (["none", "interior", "exterior"],),
                "atmosphere": (["random", "Cloudy", "Rainy", "Snowy", "Evening", "Morning", "Overcast", "Sunset", "Clear"],),
            }
        }

    RETURN_TYPES = ("STRING",)  # Output will be the final prompt string
    RETURN_NAMES = ("prompt",)
    FUNCTION = "generate_prompt"
    CATEGORY = "Text Generation"

    def generate_prompt(self, architect, region, building_type, interior_exterior, atmosphere):
        # Define atmosphere mapping with removed parentheses inside
        atmosphere_map = {
            "Cloudy": "A gloomy cloudy scene with dark clouds looming overhead, creating a mysterious atmosphere",
            "Rainy": "A refreshing rainy day filled with soft raindrops and a tranquil ambiance",
            "Snowy": "A magical snowy landscape, where delicate snowflakes fall gently from the sky",
            "Evening": "A serene evening scene as the sun dips below the horizon",
            "Morning": "A fresh morning atmosphere filled with the soft glow of dawn",
            "Overcast": "A moody overcast day where heavy gray clouds hang low in the sky",
            "Sunset": "A breathtaking sunset painting the sky in vibrant colors",
            "Clear": "A bright, clear day with a deep blue sky stretching endlessly overhead"
        }

        # Updated fixed prompt
        fixed_prompt = "(realistic architectural photography, architectural photography, realistic photography, realistic, photograph, ultra-high resolution, architecture, building, building photography, high quality)"

        # Handle random selections if any value is set to "random"
        if architect == "random":
            architect = random.choice([
                "Greg Lynn", "Eric Owen Moss", "Peter Eisenman", "Jeanne Gang", "Jon Jerde", 
                "Rafael Vinoly", "Alejandro Aravena", "Oscar Niemeyer", "Luis Barragan", 
                "Frank Gehry", "Jacques Herzog, Pierre de Meuron", "Peter Zumthor", "Mario Botta", 
                "Bjarke İngels", "Alvar Aalto", "Eero Saarinen", "Rem Koolhaas", "Daniel Libeskind", 
                "Anna Heringer", "Glenn Murcutt", "Nicholas Grimshaw", "Norman Foster", 
                "Yvonne Farrell; Shelley McNamara", "Jean Nouvel", "Carlo Scarpa", "Aldo Rossi", 
                "Richard Rogers", "Massimiliano Fuksas", "Renzo Piano", "Lina Bo Bardi", 
                "Ricardo Bofill", "Enric Ruiz Geli", "Santiago Calatravva", "Manuel Aires Mateus", 
                "Alvaro Siza Vieira", "Tadao Ando", "Kenzo Tange", "Kengo Kuma", "Kazuyo Seijama", 
                "Shigeru Ban", "Kisho Kurokawa", "Ieoh Ming Pei", "Wang Shu", "Toyo Ito", 
                "Vo Trong Nghia", "Balkrishna Vithaldas Doshi", "Diebedo Francis Kere", 
                "Christian de Portzamparc", "Zaha Hadid", "Marco Zanuso", "Moshe Safdie", 
                "Sedad Hakkı Eldem", "Behruz Çinici", "Şevki Vanlı"
            ])
        if region == "random":
            region = random.choice(["Africa", "Asia", "Europe", "North America", "Oceania", "South America"])
        if building_type == "random":
            building_type = random.choice([
                "Residential Architecture", "Refurbishment", "Cultural Architecture", 
                "Commercial And Offices", "Hospitality Architecture", "Public Architecture", 
                "Healthcare Architecture", "Educational Architecture", "Sports Architecture", 
                "Religious Architecture", "Industrial And Infrastructure", "Landscape And Urbanism"
            ])
        if atmosphere == "random":
            atmosphere = None  # Do not include atmosphere in the prompt

        # Construct the prompt
        prompt = f"((({architect}))), (({region})), (({building_type}))"
        if interior_exterior != "none":
            prompt += f", (({interior_exterior}))"
        if atmosphere is not None:
            prompt += f", {atmosphere_map[atmosphere]}"
        prompt += f", {fixed_prompt}"
        
        return (prompt,)  # Return as a tuple for consistency with RETURN_TYPES

# A dictionary that contains all nodes you want to export with their names
NODE_CLASS_MAPPINGS = {
    "ArchitecturalPromptNode": ArchitecturalPromptNode
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "ArchitecturalPromptNode": "Architectural Prompt Generator"
}
