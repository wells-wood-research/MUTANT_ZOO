import os
from os import path as p
from .mutant import Mutant
from mutant_zoo import MutantZoo
from . import utils


class DesignRound:
    def __init__(self,
                 zoo: MutantZoo,                  # ← reference to the zoo
                 roundName: str,
                 notes: dict = {},
                 inputMode: str = "pdbDir",
                 inputDir: str | None = None,
                 inputFile: str | None = None,
                 sharedParent: str | None = None):

        self.ZOO = zoo
        self.NAME = roundName
        self.NOTES = notes.copy()
        self.INPUT_MODE = inputMode
        self.INPUT_DIR = inputDir
        self.INPUT_FILE = inputFile
        self.MUTANTS: dict[str, Mutant] = {}

        if inputMode == "pdbDir":
            if not inputDir or not p.isdir(inputDir):
                raise ValueError(f"input_dir {inputDir} does not exist or not provided")
            self._add_mutants_from_pdb_directory(inputDir, sharedParent=sharedParent)

        # add other input modes here later...

    def _add_mutants_from_pdb_directory(self,
                                input_dir: str,
                                sharedParent: str | None = None,
                                notes: dict  = {}):
        for file in os.listdir(input_dir):
            if file.lower().endswith(".pdb"):
                pdbFile = p.join(input_dir, file)

                # ← THIS is the critical line: use the zoo's generator
                mutantName = self.ZOO.generate_mutant_name()

                mutant = Mutant(name=mutantName)
                mutant.SEQUENCE = utils.pdb_to_sequence(pdbFile)
                mutant.STRUCTURE = pdbFile
                mutant.PARENT = sharedParent
                mutant.NOTES = notes.copy()

                self.MUTANTS[mutantName] = mutant

    def write_fasta(self, outFasta:str):
        with open(outFasta, "w") as f:
            for mutantName, mutant in self.MUTANTS.items():
                f.write(f">{mutantName}\n")
                for key, value in mutant.SEQUENCE.items():
                    f.write(f"{value}\n")


    def to_dict(self):
        return {
            "name": self.NAME,
            "notes": self.NOTES,
            "input_mode": self.INPUT_MODE,
            "input_dir": self.INPUT_DIR,
            "input_file": self.INPUT_FILE,
            "mutants": {mutantName: mutant.to_dict() for mutantName, mutant in self.MUTANTS.items()},
            "notes": self.NOTES
        }
    
    def add_mutants(self,
                 inputMode: str = "pdbDir",
                 inputDir: str | None = None,
                 inputFile: str | None = None,
                 sharedParent: str | None = None,
                 notes: dict = {}):
        if inputMode == "pdbDir":
            if not inputDir or not p.isdir(inputDir):
                raise ValueError(f"input_dir {inputDir} does not exist or not provided")
            self._add_mutants_from_pdb_directory(inputDir, sharedParent=sharedParent, notes=notes)

    def add_note(self, key: str, value: str):
        self.NOTES[key] = value

    def trace_parents(self, zoo: MutantZoo, printToConsole:bool=True):
        geneologies = []
        for mutantName, mutant in self.MUTANTS.items():
            geneology = mutant.trace_parents(zoo, printToConsole)
            geneologies.append(geneology)
        print(geneologies)