import numpy as np
class JobLibFileClass(object):
    
    def __init__(self, df):
        
        self.atoms = df.index.values
        self.unique_atoms = np.unique(self.atoms)
        self.descriptor_names = df.columns.values
        self.data = df.values
        
        for index, atom in enumerate(self.unique_atoms):
            atom_mask = self.atoms == atom
            self.__dict__[atom] = df.values[atom_mask, :]
    
    def __call__(self, atom=None, descriptor_name=None, *argvs):
        
        # atom and descriptor_name both none, should not return anything
        if atom is None and descriptor_name is None:
            return None
        # if atom is None, descriptor_name has something, there is two conditions
        if atom is None and descriptor_name is not None:
            # First is when argvs has nothing, we should return the whole values
            # But REMEMBER, there does exist the condition that one atom 
            # corresponds to multiple values. 
            # But HOW can we do facing theses multiple values? One single method is 
            # just return their mean values. 
            if len(argvs) == 0:
                if len(self.unique_atoms) == len(self.atoms):
                    # if equals, it says that no conditions that multiple values vs one atom
                    descriptor_mask = self.descriptor_names == descriptor_name
                    return self.atoms, self.data[:, descriptor_mask].reshape(-1, )
                elif len(self.unique_atoms) != len(self.atoms):
                    # it says multiple values vs one atom, we must do something !
                    mean_values = np.zeros(len(self.unique_atoms))
                    for index, atom in enumerate(self.unique_atoms):
                        atom_mask = self.atoms == atom
                        descriptor_mask = self.descriptor_names == descriptor_name
                        mean_value = self.mean(self.data[atom_mask, descriptor_mask])
                        if isinstance(mean_value, str):
                            mean_values = mean_values.astype(str)
                        mean_values[int(index)] = mean_value
                    return self.unique_atoms, mean_values
            elif len(argvs) != 0:
                # Second is when argvs have something, which might be e.g. the user want 
                # to filter the return values by the values in argvs
                if len(self.unique_atoms) == len(self.atoms):
                    descriptor_mask = self.descriptor_names == descriptor_name
                    return_data = self.data[:, descriptor_mask].reshape(-1, )
                    return_atoms = self.atoms.copy()
                    for argv in argvs:
                        atom_mask = return_data == argv
                        return_data = return_data[atom_mask]
                        return_atoms = return_atoms[atom_mask]
                        if len(return_data) == 0:
                            break
                    return return_atoms, return_data
                elif len(self.unique_atoms) != len(self.atoms):
                    mean_values = np.zeros(len(self.unique_atoms))
                    for index, atom in enumerate(self.unique_atoms):
                        atom_mask = self.atoms == atom
                        descriptor_mask = self.descriptor_names == descriptor_name
                        mean_value = self.mean(self.data[atom_mask, descriptor_mask])
                        if isinstance(mean_value, str):
                            mean_values = mean_values.astype(str)
                        mean_values[int(index)] = mean_value
                    return_data = mean_values
                    return_atoms = self.unique_atoms.copy()
                    for argv in argvs:
                        atom_mask = return_data == argv
                        return_data = return_data[atom_mask]
                        return_atoms = return_atoms[atom_mask]
                        if len(return_data) == 0:
                            break
                    return return_atoms, return_data
        # If atom is not None, descriptor is None
        # Return the atom's all descriptors
        if atom is not None and descriptor_name is None:
            if len(argvs) == 0:
                return self.__dict__[atom]
            elif len(argvs) > 0:
                return_data = self.__dict__[atom]
                for argv in argvs:
                    atom_mask = (return_data == argv).sum(axis=1).astype(bool)
                    return_data = return_data[atom_mask, :]
                    if len(return_data) == 0:
                        break
                return return_data
        # If atom is not None, descriptor is not None
        if atom is not None and descriptor_name is not None:
            descriptor_mask = self.descriptor_names == descriptor_name
            atom_mask = self.atoms == atom
            return_data = self.data[atom_mask, descriptor_mask]
            if len(return_data.shape) == 1:
                if return_data.shape[0] == 1:
                    return return_data
                elif return_data.shape[0] > 1:
                    return return_data
            elif len(return_data.shape) > 1:
                return self.mean(return_data)
    def __len__(self):
        return len(self.atoms)
    
    @property
    def shape(self):
        return (len(self), len(self.descriptor_names), )
    
    def mean(self, array):
        if len(array.shape) > 1:
            mean_values = np.zeros(array.shape[1])
            for i in range(array.shape[1]):
                col = array[i, :]
                try:
                    mean_values[i] = col.astype(float).mean()
                except:
                    mean_values[i] = "variety_str"
        elif len(array.shape) == 1:
            try:
                mean_values = array.astype(float).mean()
            except:
                mean_values = "variety_str"
        return mean_values

def tolerance_factor(ra, rb, rc):
    return (ra + rc) / (np.sqrt(2) * (rb + rc))

def tau_factor(na, ra, rb, rc):
    left = rc/rb
    right_denominator = np.log(ra/rb)
    right_numerator = ra/rb
    right = na * (na - right_numerator/right_denominator)
    return left - right

def octahedral_factor(rb, rc):
    return rb/rc

def row_mul(row, ratio):
    row = row.reshape(-1, )
    ratio = float(ratio)
    for index, i in enumerate(row):
        
        if isinstance(i, float):
            mul = i * ratio
        elif str(i) == "nan":
            mul = i
        elif isinstance(i, str):
            try:
                i = float(i)
                mul = i 
            except ValueError:
                mul = i
        row[index] = mul
        
    return row.reshape(-1, 1)

def row_add(site_data, new_row):
    site_data = site_data.reshape(-1, )
    new_row = new_row.reshape(-1, )
    for index, i in enumerate(site_data):
        
        if str(new_row[index]) == "nan" or str(i) == "nan":
            add = np.nan
        else:
            try:
                i = float(i)
                j = float(new_row[index])
                add = j + i
            except:
                add = new_row[index]
        try:
            site_data[index] = add
        except:
            site_data[index] = i
    
    return site_data.reshape(-1, 1)

if __name__ == "__main__":
    import pathlib, glob, joblib
    selfpath = pathlib.Path(__file__).parent.resolve()
    joblibs = glob.glob(str(pathlib.Path(selfpath, "*.joblib")))
    joblibnames = []
    jobdict = {}
    for joblib_ in joblibs:
        joblibname = pathlib.Path(joblib_.split(".")[0]).parts[-1]
        data = joblib.load(joblib_)
        joblibnames.append(joblibname)
        jobdict[joblibname] = data
    
    v = jobdict["v"]
    m = jobdict["m"]
    m_ionic_energies = jobdict["m_ionic_energies"]
    m_ionic_oxidation_states = jobdict["m_ionic_oxidation_states"]
    m_ionic_radii = jobdict["m_ionic_radii"]
    m_meaning = jobdict["m_meaning"]
    organic_descriptors = jobdict["organic_descriptors"]
    organic_list = jobdict["organic_list"]
    c9tc06632b3 = jobdict["c9tc06632b3"]
    c9tc06632b4 = jobdict["c9tc06632b4"]
    for i in v.descriptor_names:
        v(descriptor_name=i)
    print("v des done")
    for i in m.descriptor_names:
        m(descriptor_name=i)
    print("m des done")
    for i in m_ionic_energies.descriptor_names:
        a, b = m_ionic_energies(descriptor_name=i)
    print("m_ionic_energies des done")
    for i in m_ionic_oxidation_states.descriptor_names:
        a, b = m_ionic_oxidation_states(descriptor_name=i)
    print("m_ionic_oxidation_states des done")
    for i in m_ionic_radii.descriptor_names:
        a, b = m_ionic_radii(descriptor_name=i)
    print("m_ionic_radii des done")
    for i in m_meaning.descriptor_names:
        a, b = m_meaning(descriptor_name=i)
    print("m_meaning des done")
    for i in organic_descriptors.descriptor_names:
        a, b = organic_descriptors(descriptor_name=i)
    print("organic_descriptors des done")
    for i in organic_list.descriptor_names:
        a, b = organic_list(descriptor_name=i)
    print("organic_list des done")
    for i in c9tc06632b3.descriptor_names:
        a, b = c9tc06632b3(descriptor_name=i)
    print("c9tc06632b3 des done")
    for i in c9tc06632b4.descriptor_names:
        a, b = c9tc06632b4(descriptor_name=i)
    print("c9tc06632b4 des done")
    
    for i in v.descriptor_names:
        dvalues = list(set(v(descriptor_name=i)[1].tolist()))
        for dvalue in dvalues:
            v(None, i, *[dvalue])
    print("v des done")
    for i in m.descriptor_names:
        dvalues = list(set(m(descriptor_name=i)[1].tolist()))
        for dvalue in dvalues:
            m(None, i, *[dvalue])
    print("m des done")
    for i in m_ionic_energies.descriptor_names:
        dvalues = list(set(m_ionic_energies(descriptor_name=i)[1].tolist()))
        for dvalue in dvalues:
            m_ionic_energies(None, i, *[dvalue])
    print("m_ionic_energies des done")
    for i in m_ionic_oxidation_states.descriptor_names:
        dvalues = list(set(m_ionic_oxidation_states(descriptor_name=i)[1].tolist()))
        for dvalue in dvalues:
            m_ionic_oxidation_states(None, i, *[dvalue])
    print("m_ionic_oxidation_states des done")
    for i in m_ionic_radii.descriptor_names:
        dvalues = list(set(m_ionic_radii(descriptor_name=i)[1].tolist()))
        for dvalue in dvalues:
            a = m_ionic_radii(None, i, *[dvalue])
    print("m_ionic_radii des done")
    for i in m_meaning.descriptor_names:
        dvalues = list(set(m_meaning(descriptor_name=i)[1].tolist()))
        for dvalue in dvalues:
            a = m_meaning(None, i, *[dvalue])
    print("m_meaning des done")
    for i in organic_descriptors.descriptor_names:
        dvalues = list(set(organic_descriptors(descriptor_name=i)[1].tolist()))
        for dvalue in dvalues:
            a = organic_descriptors(None, i, *[dvalue])
    print("organic_descriptors des done")
    for i in organic_list.descriptor_names:
        dvalues = list(set(organic_list(descriptor_name=i)[1].tolist()))
        for dvalue in dvalues:
            a = organic_list(None, i, *[dvalue])
    print("m_meaning des done")
    for i in c9tc06632b3.descriptor_names:
        dvalues = list(set(c9tc06632b3(descriptor_name=i)[1].tolist()))
        for dvalue in dvalues:
            a = c9tc06632b3(None, i, *[dvalue])
    print("c9tc06632b3 des done")
    for i in c9tc06632b4.descriptor_names:
        dvalues = list(set(c9tc06632b4(descriptor_name=i)[1].tolist()))
        for dvalue in dvalues:
            a = c9tc06632b4(None, i, *[dvalue])
    print("c9tc06632b4 des done")
    
    for i in v.descriptor_names:
        dvalues = list(set(v(descriptor_name=i)[1].tolist()))
        for dvalue in dvalues:
            v("Cs", i, *[dvalue])