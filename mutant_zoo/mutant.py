class Mutant:
    def __init__(self, name: str | None = None):
        self.NAME = name
        self.SEQUENCE: str | None = None      # usually one sequence
        self.STRUCTURE: str | None = None     # path to PDB
        self.PARENT: 'Mutant' | None = None
        self.NOTES: dict = {}
        self.FILES: dict = {}
        # If you later want multiple sequences per mutant:
        # self.sequences: dict[str, str] = {}


    def to_dict(self):
        return {
            "name": self.NAME,
            "sequence": self.SEQUENCE,
            "structure": self.STRUCTURE,
            "parent": self.PARENT,
            "notes": self.NOTES,
            "files": self.FILES,
        }
    
    def write_fastas(self, outFasta):
        with open(outFasta, "w") as f:
            f.write(f">{self.NAME}\n")
            for chainId, seq in self.SEQUENCE.items():
                f.write(f"{seq}\n")

    def add_note(self, key: str, value: str):
        self.NOTES[key] = value
            

    def trace_parents(self, zoo: 'MutantZoo', printToConsole:bool=True):
        # from .mutant_zoo import MutantZoo
        mutant = self

        geneology = []
        while True:
            geneology.append(mutant.NAME)
            parentName = mutant.PARENT
            mutant = zoo.get_mutant_by_name(parentName)
            if not mutant:
                break
        if printToConsole:
            print(" --> ".join([mutantName for mutantName in reversed(geneology)]))
        return geneology


    def get_plot_color(self, encoding):
        colorName = self.NAME.split("_")[0]
        colorMap = {
        'red': {'hex': '#FF0000', 'rgb': 'rgb(255, 0, 0)'},
        'blue': {'hex': '#0000FF', 'rgb': 'rgb(0, 0, 255)'},
        'green': {'hex': '#008000', 'rgb': 'rgb(0, 128, 0)'},
        'pink': {'hex': '#FFC0CB', 'rgb': 'rgb(255, 192, 203)'},
        'black': {'hex': '#000000', 'rgb': 'rgb(0, 0, 0)'},
        'white': {'hex': '#FFFFFF', 'rgb': 'rgb(255, 255, 255)'},
        'cyan': {'hex': '#00FFFF', 'rgb': 'rgb(0, 255, 255)'},
        'gold': {'hex': '#FFD700', 'rgb': 'rgb(255, 215, 0)'},
        'yellow': {'hex': '#FFFF00', 'rgb': 'rgb(255, 255, 0)'},
        'purple': {'hex': '#800080', 'rgb': 'rgb(128, 0, 128)'},
        'orange': {'hex': '#FFA500', 'rgb': 'rgb(255, 165, 0)'},
        'silver': {'hex': '#C0C0C0', 'rgb': 'rgb(192, 192, 192)'},
        'violet': {'hex': '#EE82EE', 'rgb': 'rgb(238, 130, 238)'},
        'indigo': {'hex': '#4B0082', 'rgb': 'rgb(75, 0, 130)'},
        'maroon': {'hex': '#800000', 'rgb': 'rgb(128, 0, 0)'},
        'magenta': {'hex': '#FF00FF', 'rgb': 'rgb(255, 0, 255)'},
        'lavender': {'hex': '#E6E6FA', 'rgb': 'rgb(230, 230, 250)'},
        'crimson': {'hex': '#DC143C', 'rgb': 'rgb(220, 20, 60)'}
        }

        return colorMap[colorName][encoding]
    
    def get_plot_shape(self, library):

        shapeMap = {
        'square': {
            'matplotlib': 's',
            'sns': 's',
            'plotly': 'square'
        },
        'circle': {
            'matplotlib': 'o',
            'sns': 'o',
            'plotly': 'circle'
        },
        'oval': {
            'matplotlib': 'o',
            'sns': 'o',
            'plotly': 'circle'
        },
        'star': {
            'matplotlib': '*',
            'sns': '*',
            'plotly': 'star'
        },
        'heart': {
            'matplotlib': "o",  # No direct equivalent
            'sns': "o",       # No direct equivalent
            'plotly': "circle"     # No direct equivalent
        },
        'cube': {
            'matplotlib': 's',
            'sns': 's',
            'plotly': 'square'
        },
        'cone': {
            'matplotlib': '^',
            'sns': '^',
            'plotly': 'triangle-up'
        },
        'line': {
            'matplotlib': '_',
            'sns': '_',
            'plotly': 'line-ew'
        },
        'triangle': {
            'matplotlib': '^',
            'sns': '^',
            'plotly': 'triangle-up'
        },
        'pentagon': {
            'matplotlib': 'p',
            'sns': 'p',
            'plotly': 'pentagon'
        },
        'hexagon': {
            'matplotlib': 'h',
            'sns': 'h',
            'plotly': 'hexagon'
        },
        'octagon': {
            'matplotlib': '8',
            'sns': '8',
            'plotly': 'octagon'
        },
        'diamond': {
            'matplotlib': 'D',
            'sns': 'D',
            'plotly': 'diamond'
        },
        'sphere': {
            'matplotlib': 'o',
            'sns': 'o',
            'plotly': 'circle'
        },
        'cylinder': {
            'matplotlib': 'o',
            'sns': 'o',
            'plotly': 'circle'
        },
        'pyramid': {
            'matplotlib': '^',
            'sns': '^',
            'plotly': 'triangle-up'
        },
        'rhombus': {
            'matplotlib': 'd',
            'sns': 'd',
            'plotly': 'diamond'
        }
        }

        shapeName = self.NAME.split("_")[1]
        return shapeMap[shapeName][library]