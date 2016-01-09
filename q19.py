import re

input = ['Al => ThF','Al => ThRnFAr','B => BCa','B => TiB','B => TiRnFAr','Ca => CaCa','Ca => PB','Ca => PRnFAr','Ca => SiRnFYFAr','Ca => SiRnMgAr','Ca => SiTh','F => CaF','F => PMg','F => SiAl','H => CRnAlAr','H => CRnFYFYFAr','H => CRnFYMgAr','H => CRnMgYFAr','H => HCa','H => NRnFYFAr','H => NRnMgAr','H => NTh','H => OB','H => ORnFAr','Mg => BF','Mg => TiMg','N => CRnFAr','N => HSi','O => CRnFYFAr','O => CRnMgAr','O => HP','O => NRnFAr','O => OTi','P => CaP','P => PTi','P => SiRnFAr','Si => CaSi','Th => ThCa','Ti => BP','Ti => TiTi','e => HF','e => NAl','e => OMg']
molecule = 'CRnCaCaCaSiRnBPTiMgArSiRnSiRnMgArSiRnCaFArTiTiBSiThFYCaFArCaCaSiThCaPBSiThSiThCaCaPTiRnPBSiThRnFArArCaCaSiThCaSiThSiRnMgArCaPTiBPRnFArSiThCaSiRnFArBCaSiRnCaPRnFArPMgYCaFArCaPTiTiTiBPBSiThCaPTiBPBSiRnFArBPBSiRnCaFArBPRnSiRnFArRnSiRnBFArCaFArCaCaCaSiThSiThCaCaPBPTiTiRnFArCaPTiBSiAlArPBCaCaCaCaCaSiRnMgArCaSiThFArThCaSiThCaSiRnCaFYCaSiRnFYFArFArCaSiRnFYFArCaSiRnBPMgArSiThPRnFArCaSiRnFArTiRnSiRnFYFArCaSiRnBFArCaSiRnTiMgArSiThCaSiThCaFArPRnFArSiRnFArTiTiTiTiBCaCaSiRnCaCaFYFArSiThCaPTiBPTiBCaSiThSiRnMgArCaF'

class q19(object):
    def __init__(self, transformations):
        self.transformations = []

        for t in transformations:
            tmp = t.split('=>')
            self.transformations.append((tmp[0].strip(), tmp[1].strip()))

    def _transform(self, molecule):
        possible_molecules = set()

        for source, destination in self.transformations:
            i = 0
            while i >= 0:
                i = molecule.find(source, i)

                if i >= 0:
                    possible_molecules.add(molecule[0:i] + molecule[i:i+len(source)].replace(source, destination) + molecule[i+len(source):])
                    i += 1

        return possible_molecules

    def _molecule_closeness(self,m1, m2):
        i = 0
        while i < min(len(m1), len(m2)):
            if m1[i] != m2[i]:
                break
            i += 1
        return i

    def part_one(self, molecule):
        return len(self._transform(molecule))

    def part_two(self, starting_molecule, target_molecule):
        # don't think this solution will always find the "shortest" steps to ANY molecule. it just happens to reverse engineer the algorithm
        # the question used to generate the target molecule
        repl_r = {destination:source for source, destination in self.transformations}
        molecules = [target_molecule]
        while molecules[-1] != starting_molecule:
            molecules.append(re.sub('^(.*)(' + '|'.join(repl_r.keys()) + ')(.*?)$',
                                lambda x: x.group(1) + repl_r[x.group(2)] + x.group(3),
                                molecules[-1]))
        return len(molecules) - 1
