# mutant_zoo.py
import os
import random
import itertools
from typing import Dict, List, Optional, Set
import datetime
import yaml


from typing import Callable
class MutantZoo:
    def __init__(self,
                  seed: Optional[int] = None,
                  zooYaml: Optional[str] = None) -> None:
        
        if zooYaml:
            self.load_class_state(zooYaml)
        else:
            self.DESIGN_ROUNDS: List['DesignRound'] = []
            self.GLOBAL_METADATA: Dict = {}
            self.MUTANT_NAMES: Set[str] = set()

        self.TIMESTAMP = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

        if not seed:
            seed = random.randint(0, 1000000)
        self.SEED = seed

    def new_design_round(
        self,
        roundName: str,
        roundMetaData: Optional[Dict] = None,
        inputMode: str = "pdbDir",
        inputDir: Optional[str] = None,
        inputFile: Optional[str] = None
    ) -> 'DesignRound':
        """
        Create a new design round and register it in the zoo.
        Returns the newly created DesignRound instance.
        """
        # Lazy import to break circular dependency
        from design_round import DesignRound

        print(f"Creating new design round: {roundName}")
        
        designRound = DesignRound(
            zoo=self,
            roundName=roundName,
            roundMetaData=roundMetaData or {},
            inputMode=inputMode,
            inputDir=inputDir,
            inputFile=inputFile,
        )
        
        self.DESIGN_ROUNDS.append(designRound)
        return designRound
    

    def get_round_by_name(self, roundName: str) -> 'DesignRound':
        for round in self.DESIGN_ROUNDS:
            if round.ROUND_NAME == roundName:
                return round
        raise ValueError(f"Round {roundName} not found in mutant zoo")

    def generate_mutant_name(self) -> str:
        """
        Generate a unique mutant name using color_shape_animal pattern.
        Guaranteed unique across the entire zoo.
        """
        colors = [
            'red', 'blue', 'green', 'pink', 'black', 'white', 'cyan', 'gold',
            'yellow', 'purple', 'orange', 'silver', 'violet', 'indigo', 'maroon',
            'magenta', 'lavender', 'crimson'
        ]
        shapes = [
            'square', 'circle', 'oval', 'star', 'heart', 'cube', 'cone', 'line',
            'triangle', 'pentagon', 'hexagon', 'octagon', 'diamond', 'sphere',
            'cylinder', 'pyramid', 'rhombus'
        ]
        animals = [
            'cat', 'dog', 'bird', 'fish', 'lion', 'bear', 'wolf', 'fox',
            'elephant', 'giraffe', 'monkey', 'rabbit', 'turtle', 'horse',
            'sheep', 'tiger', 'leopard', 'kangaroo', 'panther'
        ]

        random.seed(self.SEED)

        # Shuffle the product to avoid always picking the same first combo
        combinations = list(itertools.product(colors, shapes, animals))
        random.shuffle(combinations)

        for color, shape, animal in combinations:
            candidateName = f"{color.lower()}_{shape.lower()}_{animal.lower()}"
            if candidateName not in self.MUTANT_NAMES:
                self.MUTANT_NAMES.add(candidateName)
                return candidateName

        raise RuntimeError("Exhausted all possible mutant names! (19×18×19 = ~6,500 names)")
    
    def save_class_state(self, zooYaml: str):
        """
        Saves the non-callable attributes of the class instance to a YAML file.
        """
        stateToSave = {}
        stateToSave["GLOBAL_METADATA"] = self.GLOBAL_METADATA
        stateToSave["MUTANT_NAMES"] = list(self.MUTANT_NAMES)
        stateToSave["SEED"] = self.SEED
        stateToSave["DESIGN_ROUNDS"] = []

        for designRound in self.DESIGN_ROUNDS:
            stateToSave["DESIGN_ROUNDS"].append(designRound.to_dict())

        with open(zooYaml, "w") as f:
            yaml.dump(stateToSave, f)

    def load_class_state(self, zooYaml:str):
        with open(zooYaml, "r") as f:
            state = yaml.safe_load(f)
       
        self.GLOBAL_METADATA = state["GLOBAL_METADATA"]
        self.MUTANT_NAMES = set(state["MUTANT_NAMES"])
        self.SEED = state["SEED"]
        self.DESIGN_ROUNDS = []
        # Lazy import to break circular dependency
        from design_round import DesignRound
        from mutant import Mutant

        for designRoundState in state["DESIGN_ROUNDS"]:
            designRound = DesignRound(
                zoo=self,
                roundName=designRoundState["round_name"],
                roundMetaData=designRoundState["round_metadata"],
                inputMode=designRoundState["input_mode"],
                inputDir=designRoundState["input_dir"],
                inputFile=designRoundState["input_file"],
            )
            designRoundMutants = designRoundState["mutants"]
            for mutantName, mutantState in designRoundMutants.items():
                mutant = Mutant(name=mutantName)
                mutant.SEQUENCE = mutantState["sequence"]
                mutant.STRUCTURE = mutantState["structure"]
                mutant.PARENT = mutantState["parent"]
                designRound.MUTANTS[mutantName] = mutant
            self.DESIGN_ROUNDS.append(designRound)