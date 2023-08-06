
import joblib, glob, pathlib, numpy as np, pathlib
selfpath = pathlib.Path(__file__).parent.resolve()
if __name__ == "__main__":
    from utils import JobLibFileClass, tolerance_factor, tau_factor, octahedral_factor, row_add, row_mul
else:
    from .utils import JobLibFileClass, tolerance_factor, tau_factor, octahedral_factor, row_add, row_mul

class AtomDescriptors:
    
    def __init__(self, seq=3):
        joblibs = glob.glob(str(pathlib.Path(selfpath, "*.joblib")))
        joblibs = [ pathlib.Path(i) for i in joblibs]
        self.joblibnames = []
        for joblib_ in joblibs:
            joblibname = joblib_.stem
            data = joblib.load(joblib_)
            self.joblibnames.append(joblibname)
            self.__dict__[joblibname] = data
        self.ionic_radii = None
        self.seq = seq
        
    def __call__(self, atom=None, charge=None, coordination=None, degree=None, descriptor_name=None):
        descriptors = []
        descriptor_names = []
        for i in [self.v, self.m, self.c9tc06632b3][:self.seq]:
            try:
                descriptors.append(i(atom, descriptor_name))
            except:
                descriptors.append(np.array([np.nan for i in range(i.shape[1])]).reshape(1, -1))
            descriptor_names.append(i.descriptor_names)
            
        d = self.m_ionic_radii(atom, descriptor_name, charge, coordination)[:, -1].reshape(1, -1)
        if d.shape[1] == 0:
            d = self.m_ionic_radii(atom, descriptor_name)[:, -1][:1].reshape(1, -1)
        if d.shape[1] > 1:
            d = d[:, 0].reshape(1, -1)
        descriptors.append(d)
        self.ionic_radii = d[0][0]
        descriptor_names.append(np.array(self.m_ionic_radii.descriptor_names[-1]).reshape(1, ))
        
        d = self.m_ionic_energies(atom, descriptor_name, degree)[:-1].reshape(1, -1)
        descriptors.append(d)
        if d.shape[1] != 0:
            descriptor_names.append(np.array(self.m_ionic_energies.descriptor_names[-1]).reshape(1, ))
        return np.concatenate(descriptor_names), np.concatenate(descriptors, axis=1), 

class ABO3Descriptors:
    
    def __init__(self, seq=3):
        self.seq = seq
        pass
    
    def __call__(self, *argvs):
        
        """
        e.g.
        argvs: 
            [
                dict(
                        atom="Cs", descriptor_name=None, charge=1, coordination="VI", degree=1
                    )
            ]
        """
        des = AtomDescriptors(self.seq)
        descriptors = []
        descriptor_names = []
        site_pres = ["A_", "B_", "C_", "D_", "E_", "F_"]
        ionic_radiies = []
        for index, argv in enumerate(argvs):
            if isinstance(argv, dict):
                a, b = des(**argv)
            elif isinstance(argv, str):
                a, b = des(argv)
            ionic_radiies.append(des.ionic_radii)
            descriptors.append(b)
            descriptor_names.append(site_pres[index] + a)
        if len(ionic_radiies) == 3:
            tf = tolerance_factor(*ionic_radiies)
            tau = tau_factor(1, *ionic_radiies)
            of = octahedral_factor(*ionic_radiies[1:])
            descriptor_names.append(np.array(["tf", "tau", "of"]))
            descriptors.append(np.array([[tf, tau, of]]))
        return np.concatenate(descriptor_names), np.concatenate(descriptors, axis=1), 

class SiteDescriptor:
    
    def __init__(self):
        pass
    def __call__(self, ratios, *argvs):
        des = AtomDescriptors()
        if isinstance(argvs[0], dict):
            names, descriptors = des(**argvs[0])
        elif isinstance(argvs[0], str):
            names, descriptors = des(argvs[0])
        descriptors = row_mul(descriptors, ratios[0])
        for ratio, argv in zip(ratios[1:], argvs[1:]):
            if isinstance(argv, dict):
                a, b = des(**argv)
            elif isinstance(argv, str):
                a, b = des(argv)
            b = row_mul(b, ratio)
            descriptors = row_add(descriptors, b)
        return names, descriptors

if __name__ == "__main__":
    des = AtomDescriptors()
    Csdnames, Cs = des("Cs")
    FAdnames, FA = des("FA", 1, "VI")
    dname, deses = ABO3Descriptors()(dict(atom="Cs"), dict(atom="FA"), dict(atom="I"))
    dname, deses = ABO3Descriptors()("Cs", "Pb", "O")
    a, b = SiteDescriptor()([0.1, 0.1, 0.8], dict(atom="Cs"), dict(atom="FA"), dict(atom="MA"))
    v = des.v
    m = des.m
    m_meaning = des.m_meaning
    m_ionradii = des.m_ionic_radii
    m_ionenergy = des.m_ionic_energies
    m_oxi = des.m_ionic_oxidation_states
    og = des.organic_descriptors
    ol = des.organic_list
    b3 = des.c9tc06632b3
    b4 = des.c9tc06632b4