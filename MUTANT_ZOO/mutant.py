class Mutant:
    def __init__(self, name: str | None = None):
        self.MUTANT_NAME = name
        self.SEQUENCE: str | None = None      # usually one sequence
        self.STRUCTURE: str | None = None     # path to PDB
        self.PARENT: 'Mutant' | None = None
        # If you later want multiple sequences per mutant:
        # self.sequences: dict[str, str] = {}


    def to_dict(self):
        return {
            "name": self.MUTANT_NAME,
            "sequence": self.SEQUENCE,
            "structure": self.STRUCTURE,
            "parent": self.PARENT.MUTANT_NAME if self.PARENT else None,
        }