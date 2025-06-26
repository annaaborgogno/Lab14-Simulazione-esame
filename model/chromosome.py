from dataclasses import dataclass

@dataclass
class Chromosome():
    chr: int

    def __hash__(self):
        return hash(self.chr)

    def __eq__(self, other):
        if not isinstance(other, Chromosome):
            return False
        return self.chr == other.chr

    def __str__(self):
        return f"Chromosome: {self.chr}"