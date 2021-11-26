"""
Author                      : Drew Heasman
Date(last updated)          : 05 June 2021
Description : Geochemical calculations
"""
elements = {}
elements["O"] = 15.9994
elements["Al"] = 26.981539
elements["Si"] = 28.0855
elements["K"] = 39.0983
elements["Cr"] = 51.9961
elements["Fe"] = 55.845
elements["Nd"] = 144.24


def get_atomic_weight(formula):
    '''
    returns the atomic weight of a formula
    '''
    atomic_weight = 0
    for element in formula:
        atomic_weight = atomic_weight + elements[element]
    return atomic_weight


def get_moles_formula(grams, formula):
    '''
    returns the number of moles of a formula, given grams and the formula
    '''
    return grams/get_atomic_weight(formula)


def get_moles_element(grams, formula, element):
    '''
    get the moles of an element given the grams, formula, and element
    '''
    moles = grams/get_atomic_weight(formula)
    occ = formula.count(element)
    return moles * occ


def y_slope(m, b, x_list):
    y_list = []
    for x in x_list:
        y_list.append(m*x+b)
    return y_list


def get_num_atoms_from_moles(moles):
    '''
    returns the number of atoms, given the number of moles.
    '''
    return moles * 6.022 * 10**23


def convert_molality_to_molarity(molality, atomic_weight, density):
    '''
    Converts molality to molarity given a molality, an atomic weight,
    and a solution density
    '''
    solution_volume = (1 + ((molality*atomic_weight/1000))) / density
    return molality/solution_volume


def get_mass_of_an_atom(atomic_mass):
    '''
    returns the mass of one atom, given the atomic mass of an isotope
    '''
    return atomic_mass / (6.022*10**23)


def get_num_atoms_formula(grams, formula, element):
    '''
    return the number of atoms of an element in a formula
    '''
    moles = get_moles_element(grams, formula, element)
    return get_num_atoms_from_moles(moles)


def get_weight_perc_formula(formula, element, num_occ):
    '''
    return the weight percent of an element given the formula, element, and
    the number of occurences of that element in the formula.
    '''
    formula_atomic_weight = get_atomic_weight(formula)
    element_weight = get_atomic_weight(element)
    return (element_weight * num_occ) / formula_atomic_weight * 100


def get_ppm_formula(formula, element, num_occ):
    '''
    return the ppm of an element given the formula, element, and the number
    of occurences of that element in the formula.
    '''
    return get_weight_perc_formula(formula, element, num_occ) * 10000


def get_atomic_perc(formula, element):
    '''
    return the atomic percentage of an element in a formula
    '''
    return formula.count(element) / len(formula) * 100
