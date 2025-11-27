# mutant_zoo.py
import os
from os import path as p
import random
import itertools
from typing import Dict, List, Optional, Set
import datetime
import yaml
from shutil import copy


from typing import Callable
class MutantZoo:
    def __init__(self,
                  seed: Optional[int] = None,
                  zooYaml: Optional[str] = None) -> None:
        
        if zooYaml:
            self.load_class_state(zooYaml)
            return
        else:
            self.DESIGN_ROUNDS: List['DesignRound'] = []
            self.NOTES: Dict = {}
            self.MUTANT_NAMES: Set[str] = set()
            self.TOP_DIR = None
            self.RELATIVE_PATHS = False

        self.TIMESTAMP = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

        if not seed:
            seed = random.randint(0, 1000000)
        self.SEED = seed

    def new_design_round(
        self,
        roundName: str,
        notes: Optional[Dict] = {},
        inputMode: str = "pdbDir",
        inputDir: Optional[str] = None,
        inputFile: Optional[str] = None,
        sharedParent: Optional[str] = None
    ) -> 'DesignRound':
        """
        Create a new design round and register it in the zoo.
        Returns the newly created DesignRound instance.
        """
        # Lazy import to break circular dependency
        from .design_round import DesignRound

        print(f"Creating new design round: {roundName}")
        
        designRound = DesignRound(
            zoo=self,
            roundName=roundName,
            notes=notes or {},
            inputMode=inputMode,
            inputDir=inputDir,
            inputFile=inputFile,
            sharedParent=sharedParent
        )
        
        self.DESIGN_ROUNDS.append(designRound)
        return designRound
    

    def get_round_by_name(self, roundName: str) -> 'DesignRound':
        for round in self.DESIGN_ROUNDS:
            if round.NAME == roundName:
                return round
        raise ValueError(f"Round {roundName} not found in mutant zoo")
    
    def get_mutant_by_name(self, mutantName: str) -> 'Mutant':
        for round in self.DESIGN_ROUNDS:
            if mutantName in round.MUTANTS:
                return round.MUTANTS[mutantName]
            
        return None

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
        stateToSave["notes"] = self.NOTES
        stateToSave["mutant_names"] = list(self.MUTANT_NAMES)
        stateToSave["seed"] = self.SEED
        stateToSave["design_rounds"] = []
        stateToSave["relative_paths"] = self.RELATIVE_PATHS
        stateToSave["top_dir"] = self.TOP_DIR

        for designRound in self.DESIGN_ROUNDS:
            stateToSave["design_rounds"].append(designRound.to_dict())
            
        yaml.Dumper.ignore_aliases = lambda *args : True

        with open(zooYaml, "w") as f:
            yaml.dump(stateToSave, f)

    def load_class_state(self, zooYaml:str):
        with open(zooYaml, "r") as f:
            state = yaml.safe_load(f)
       
        self.NOTES = state["notes"]
        self.MUTANT_NAMES = set(state["mutant_names"])
        self.SEED = state["seed"]
        self.DESIGN_ROUNDS = []
        self.RELATIVE_PATHS = state["relative_paths"]
        if self.RELATIVE_PATHS:
            self.TOP_DIR = p.dirname(zooYaml)
        else:
            self.TOP_DIR = state.get("top_dir", None)
        

        # Lazy import to break circular dependency
        from .design_round import DesignRound
        from .mutant import Mutant

        for designRoundState in state["design_rounds"]:
            designRound = DesignRound(
                zoo=self,
                roundName=designRoundState["name"],
                notes=designRoundState["notes"],
                inputMode=designRoundState["input_mode"],
                inputDir=designRoundState["input_dir"],
                inputFile=designRoundState["input_file"],
            )
            designRoundMutants = designRoundState["mutants"]
            for mutantName, mutantState in designRoundMutants.items():
                mutant = Mutant(name=mutantName)
                mutant.SEQUENCE = mutantState["sequence"]
                mutant.STRUCTURE = mutantState["structure"]
                mutant.PARENT = mutantState.get("parent", None)
                mutant.NOTES = mutantState.get("notes", {})
                mutant.FILES = mutantState.get("files", {})
                designRound.MUTANTS[mutantName] = mutant
                ## make paths un-relative
                if self.RELATIVE_PATHS:
                    if mutant.STRUCTURE:
                        mutant.STRUCTURE = p.join(self.TOP_DIR, mutant.STRUCTURE)
                    if len(mutant.FILES) > 0:
                        for fileTag, filePath in mutant.FILES.items():
                            mutant.FILES[fileTag] = p.join(self.TOP_DIR, filePath)

            self.DESIGN_ROUNDS.append(designRound)
        self.RELATIVE_PATHS = False


    def migrate(self, outDir):

        self.TOP_DIR = outDir
        self.RELATIVE_PATHS = True  

        os.makedirs(outDir, exist_ok=True)
        for designRound in self.DESIGN_ROUNDS:
            roundDir = os.path.join(outDir, designRound.NAME)
            os.makedirs(roundDir, exist_ok=True)
            for mutantName, mutant in designRound.MUTANTS.items():
                if mutant.STRUCTURE:
                    structureDest = p.join(roundDir, f"{mutantName}.pdb")
                    copy(mutant.STRUCTURE, structureDest)
                    structureRelativePath = p.relpath(structureDest, self.TOP_DIR)
                    mutant.STRUCTURE = structureRelativePath
                elif mutant.SEQUENCE:
                    outFasta = p.join(roundDir, f"{mutantName}.fasta")
                    mutant.write_fastas(outFasta)
                    fastaRelativePath = p.relpath(outFasta, self.TOP_DIR)
                    mutant.SEQUENCE = fastaRelativePath
                elif len(mutant.FILES) > 0:
                    for fileTag, filePath in mutant.FILES.items():
                        if " " in fileTag:
                            fileTag = fileTag.replace(" ", "_")
                        fileExt = p.splitext(filePath)[1]
                        fileDest = p.join(roundDir, f"{fileTag}_{mutantName}{fileExt}")
                        copy(filePath, fileDest)
                        fileRelativePath = p.relpath(fileDest, self.TOP_DIR)
                        mutant.FILES[fileTag] = fileRelativePath

        self.save_class_state(p.join(outDir, "zoo.yaml"))