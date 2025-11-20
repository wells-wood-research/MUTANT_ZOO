import os
from os import path as p
from mutant import Mutant
from mutant_zoo import MutantZoo
import utils


class DesignRound:
    def __init__(self,
                 zoo: MutantZoo,                  # ← reference to the zoo
                 roundName: str,
                 roundMetaData: dict | None = None,
                 inputMode: str = "pdbDir",
                 inputDir: str | None = None,
                 inputFile: str | None = None):

        self.ZOO = zoo
        self.ROUND_NAME = roundName
        self.ROUND_METADATA = roundMetaData or {}
        self.INPUT_MODE = inputMode
        self.INPUT_DIR = inputDir
        self.INPUT_FILE = inputFile
        self.MUTANTS: dict[str, Mutant] = {}

        if inputMode == "pdbDir":
            if not inputDir or not p.isdir(inputDir):
                raise ValueError(f"input_dir {inputDir} does not exist or not provided")
            self._init_from_pdb_directory(inputDir)

        # add other input modes here later...

    def _init_from_pdb_directory(self, input_dir: str):
        for file in os.listdir(input_dir):
            if file.lower().endswith(".pdb"):
                pdb_file = p.join(input_dir, file)

                # ← THIS is the critical line: use the zoo's generator
                mutantName = self.ZOO.generate_mutant_name()

                mutant = Mutant(name=mutantName)
                mutant.SEQUENCE = utils.pdb_to_sequence(pdb_file)
                mutant.STRUCTURE = pdb_file
                mutant.PARENT = None

                self.MUTANTS[mutantName] = mutant

    def write_fasta(self, outFasta:str):
        with open(outFasta, "w") as f:
            for mutantName, mutant in self.MUTANTS.items():
                f.write(f">{mutantName}\n")
                for key, value in mutant.SEQUENCE.items():
                    f.write(f"{value}\n")


    def to_dict(self):
        return {
            "round_name": self.ROUND_NAME,
            "round_metadata": self.ROUND_METADATA,
            "input_mode": self.INPUT_MODE,
            "input_dir": self.INPUT_DIR,
            "input_file": self.INPUT_FILE,
            "mutants": {mutantName: mutant.to_dict() for mutantName, mutant in self.MUTANTS.items()},
        }
    
