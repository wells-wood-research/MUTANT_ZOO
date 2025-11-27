from pdbUtils.pdbUtils import pdb2df, df2pdb

def _init_3_to_1():
    return {
        "ALA": "A","ARG": "R","ASN": "N","ASP": "D","CYS": "C",
        "GLN": "Q","GLU": "E","GLY": "G","HIS": "H","ILE": "I",
        "LEU": "L","LYS": "K","MET": "M","PHE": "F","PRO": "P",
        "SER": "S","THR": "T","TRP": "W","TYR": "Y","VAL": "V"
    }

def pdb_to_sequence(pdbFile):
    threeToOne = _init_3_to_1()
    pdbDf = pdb2df(pdbFile)
    sequences = {}
    for chainId, chainDf in pdbDf.groupby("CHAIN_ID"):
        chainSeq = ""
        for resId, resDf in chainDf.groupby("RES_ID"):
            resName = resDf.iloc[0]["RES_NAME"]
            aa = threeToOne.get(resName, None)
            if aa is None:
                aa = f"_{resName}_"
            chainSeq += aa

        sequences[chainId] = chainSeq

    return sequences
    
