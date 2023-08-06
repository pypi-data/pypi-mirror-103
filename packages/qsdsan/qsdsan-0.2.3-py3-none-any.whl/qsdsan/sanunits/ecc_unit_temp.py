#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#!!! Smiti/Anna, I expect the complete unit will be more complex that what I
# laid out below, put your names before me if you contribute more, you can add
# your email address if wanted

'''
QSDsan: Quantitative Sustainable Design for sanitation and resource recovery systems

This module is developed by:
    Yalin Li <zoe.yalin.li@gmail.com>
    Smiti Mittal
    Anna Kogler

This module is under the University of Illinois/NCSA Open Source License.
Please refer to https://github.com/QSD-Group/QSDsan/blob/master/LICENSE.txt
for license details.
'''

# %%

import math
from thermosteam import (Reaction as Rxn, ParallelReaction as ParallelRxn)
#!!! Change this to relative importing when compiled into qsdsan
from qsdsan import Equipment, SanUnit, Component, WasteStream
# from .. import SanUnit, Equipment # relative importing

isinstance = isinstance

# __all__ = ('Electrode', 'ElectroChemCell')

# %%


# Be sure to include documentation and examples
class Electrode(Equipment):
    '''
    Electrodes to be used in an electrochemical cell.
    Refer to the example in :class:`ElectroChemCell` for how to use this class.

    Parameters
    ----------
    N : int
        Number of units of the given electrode.
    electrode_type : str
        Type of the electrode, can only be "anode" or "cathode".
    material: str
        Material of the electrode.
    unit_cost: float
        Unit cost of the electrode, will use default cost (if available)
        if not provided.
    surface_area : float
        Surface area of the electrode in m2.

    See Also
    --------
    :class:`ElectroChemCell`

    '''

    # Include all attributes (no properties) in addition to the ones in the
    # parent `Equipment` class
    # Using __slots__ can improve computational efficiency when the class does not
    # have many attributes
    __slots__ = ('_type', '_material', '_N', 'unit_cost', 'surface_area')

    def __init__(self, name=None, # when left as None, will be the same as the class name
                 design_units=None,
                 F_BM=1., #!!! YL BM is now updated to F_BM
                 lifetime=10000, lifetime_unit='hr', N=0,
                 electrode_type='anode', # note that I prefer not to use 'type' because it's a builtin function
                 material='graphite', unit_cost=0.1, surface_area=1):
        Equipment.__init__(self, name, design_units, F_BM, lifetime, lifetime_unit)
        self.N = N
        self.electrode_type = electrode_type
        self.unit_cost = unit_cost
        self.material = material
        self.surface_area = surface_area

    # All subclasses of `Equipment` must have a `_design` and a `_cost` method
    def _design(self):
        design = {
            f'Type of electrode' : self.electrode_type,
            f'Number of {self.electrode_type}': self.N,
            f'Material of {self.electrode_type}': self.material,
            f'Surface area of {self.electrode_type}': self.surface_area
            }
        self.design_units = {f'Surface area of {self.electrode_type}': 'm2'}
        return design

    # All subclasses of `Equipment` must have a `_cost` method, which returns the
    # purchase cost of this equipment
    def _cost(self):
        return self.unit_cost*self.N

    # You can use property to add checks
    @property
    def N(self):
        '''[str] Number of units of the electrode.'''
        return self._N
    @N.setter
    def N(self, i):
        try:
            self._N = int(i)
        except:
            raise ValueError(f'N must be an integer')

    @property
    def electrode_type(self):
        '''[str] Type of the electrode, either "anode" or "cathode".'''
        return self._type
    @electrode_type.setter
    def electrode_type(self, i):
        if i.lower() in ('anode', 'cathode'):
            self._type = i
        else:
            raise ValueError(f'Electrode can only be "anode" or "cathode", not {i}.')

    @property
    def material(self):
        '''[str] Material of the electrode.'''
        return self._material
    @material.setter
    def material(self, i):
        material = i.lower()
        if material == 'graphite':
            # You can have some default unit cost based on the material,
            # I'm just making up numbers
            # But be careful that by doing this, you might overwriter users' input
            if not self.unit_cost:
                self.unit_cost = 50
        self._material = material

class Membrane(Equipment):
    '''
    Membranes to be used in an electrochemical cell.
    Refer to the example in :class:`ElectroChemCell` for how to use this class.

    Parameters
    ----------
    N : int
        Number of units of the given membrane.
    material: str
        Material of the membrane.
    unit_cost: float
        Unit cost of the membrane per m2, will use default cost (if available)
        if not provided.
    surface_area : float
        Surface area of the membrane in m2.

    See Also
    --------
    :class:`ElectroChemCell`

    '''
    __slots__ = ('_N', 'name', 'unit_cost', 'material', 'surface_area')

    def __init__(self, name=None, # when left as None, will be the same as the class name
                 design_units=None,
                 F_BM=1., lifetime=10000, lifetime_unit='hr', N=0,
                 material='polypropylene', unit_cost=0.1, surface_area=1):
        Equipment.__init__(self, name, design_units, F_BM, lifetime, lifetime_unit)
        self.name = name
        self.N = N
        self.unit_cost = unit_cost
        self.material = material
        self.surface_area = surface_area

    # All subclasses of `Membrane` must have a `_design` and a `_cost` method
    def _design(self):
        design = {
            f'Number of {self.name}': self.N,
            f'Material of {self.name}': self.material,
            f'Surface area of {self.name}': self.surface_area
            }
        self.design_units = {f'Surface area of {self.name}': 'm2'}
        return design

    # All subclasses of `Membrane` must have a `_cost` method, which returns the
    # purchase cost of this equipment
    def _cost(self):
        return self.unit_cost*self.N*self.surface_area

    # You can use property to add checks
    @property
    def N(self):
        '''[str] Number of units of the electrode.'''
        return self._N
    @N.setter
    def N(self, i):
        try:
            self._N = int(i)
        except:
            raise ValueError(f'N must be an integer')

class Column(Equipment):
    '''
    Columns to be used in an electrochemical cell.
    Refer to the example in :class:`ElectroChemCell` for how to use this class.

    Parameters
    ----------
    N : int
        Number of units of the given column.
    material: str
        Material of the column.
    unit_cost: float
        Unit cost of the column per m2, will use default cost (if available)
        if not provided.
    surface_area : float
        Surface area of the column in m2.

    See Also
    --------
    :class:`ElectroChemCell`

    '''

    __slots__ = ('_N', 'name', 'unit_cost', 'material', 'surface_area')

    def __init__(self, name=None, # when left as None, will be the same as the class name
                 design_units=None,
                 F_BM=1., lifetime=10000, lifetime_unit='hr', N=0,
                 material='resin', unit_cost=0.1, surface_area=1):
        Equipment.__init__(self, name, design_units, F_BM, lifetime, lifetime_unit)
        self.name = name
        self.N = N
        self.unit_cost = unit_cost
        self.material = material
        self.surface_area = surface_area

    # All subclasses of `Column` must have a `_design` and a `_cost` method
    def _design(self):
        design = {
            f'Number of {self.name}': self.N,
            f'Material of {self.name}': self.material,
            f'Surface area of {self.name}': self.surface_area
            }
        self.design_units = {f'Surface area of {self.name}': 'm2'}
        return design

    # All subclasses of `Column` must have a `_cost` method, which returns the
    # purchase cost of this equipment
    def _cost(self):
        return self.unit_cost*self.N*self.surface_area

    # You can use property to add checks
    @property
    def N(self):
        '''[str] Number of units of the electrode.'''
        return self._N
    @N.setter
    def N(self, i):
        try:
            self._N = int(i)
        except:
            raise ValueError(f'N must be an integer')

class Machine(Equipment):
    '''
    Supplementary machines to be used in an electrochemical process.
    Refer to the example in :class:`ElectroChemCell` for how to use this class.

    Parameters
    ----------
    N : int
        Number of units of the given machine.
    unit_cost: float
        Unit cost of the machine

    See Also
    --------
    :class:`ElectroChemCell`

    '''
    __slots__ = ('_N', 'name', 'unit_cost')

    def __init__(self, name=None, # when left as None, will be the same as the class name
                 design_units=None,
                 F_BM=1., lifetime=10000, lifetime_unit='hr', N=0,
                 unit_cost=0.1):
        Equipment.__init__(self, name, design_units, F_BM, lifetime, lifetime_unit)
        self.name = name
        self.N = N
        self.unit_cost = unit_cost

    # All subclasses of `Machine` must have a `_design` and a `_cost` method
    def _design(self):
        design = {
            f'Number of {self.name}': self.N,
            }
        return design

    # All subclasses of `Membrane` must have a `_cost` method, which returns the
    # purchase cost of this equipment
    def _cost(self):
        return self.unit_cost*self.N

    # You can use property to add checks
    @property
    def N(self):
        '''[str] Number of units of the electrode.'''
        return self._N
    @N.setter
    def N(self, i):
        try:
            self._N = int(i)
        except:
            raise ValueError(f'N must be an integer')

class Compartment(Equipment):
    '''
    Compartments to be used in an electrochemical process.
    Refer to the example in :class:`ElectroChemCell` for how to use this class.

    Parameters
    ----------
    N : int
        Number of units of the compartment per electrochemical cell.
    unit_cost: float
        Unit cost of the compartment.
    volume : int
        Volume of the compartment in m3.
    chem_agents : list
        List of chemical agents present in the compartment,
        (Agents must be objects of the ChemicalAgent or Component classes.)

    See Also
    --------
    :class:`ElectroChemCell`

    '''
    __slots__ = ('_N', 'name', 'unit_cost', 'volume', 'chem_agents')

    def __init__(self, name=None, # when left as None, will be the same as the class name
                 design_units=None,
                 F_BM=1., lifetime=10000, lifetime_unit='hr', N=0,
                 unit_cost=0.1, volume=1, chem_agents=()):
        if isinstance(chem_agents, (ChemicalAgent, Component)):
            chem_agents = (chem_agents,)
        Equipment.__init__(self, name, design_units, F_BM, lifetime, lifetime_unit)
        self.name = name
        self.N = N
        self.unit_cost = unit_cost
        self.volume = volume
        self.chem_agents = chem_agents

    # All subclasses of `Compartment` must have a `_design` and a `_cost` method
    def _design(self):
        design = {
            f'Number of {self.name}': self.N,
            f'Volume of {self.name}': self.volume,
            f'Chemicals in {self.name}': self.chem_agents
            }
        self.design_units = {f'Volume of {self.name}': 'm3'}
        return design

    # All subclasses of `Compartment` must have a `_cost` method, which returns the
    # purchase cost of this equipment
    def _cost(self):
        return self.unit_cost*self.N

    # You can use property to add checks
    @property
    def N(self):
        '''[str] Number of units of the electrode.'''
        return self._N
    @N.setter
    def N(self, i):
        try:
            self._N = int(i)
        except:
            raise ValueError(f'N must be an integer')




# %%

#!!! YL
# It is possible to consider the costs/impacts of chemical agents this way,
# but normally, chemicals/materials that are used in the unit are considered
# as influent streams (emissions are considered as effluent streams),
# components within the streams should be created in a separate script
# by the user when using the unit.

# E.g., assume the electrolyte for this ElectroChemCell is 5 w/w% aqueous H2SO4 solution,
# we want to mix it with the upstream ammonia solution at a rate of 1 L/hr,
# then in the _run function of the ElectroChemCell class, you can have:
    
#     def _run(self):
#         ammonia, acid = self.ins # ins and outs are both list
#         eff = self.outs[0]
        
#         # Assign the mass ratio 
#         acid.imass['H2SO4'] = 0.5
#         acid.imass['H2O'] = 9.5
        
#         # Adjust the total volume, unit of F_vol is in m3/hr
#         acid.F_vol = 0.001

# When users want to use this unit in a system, they should firstly make a
# separate script containing the different components that will be used in the system,
# and a Components object that includes all the Component objects, for example:
    
#     from qsdsan import Component, Components
    
#     H2O = Component.from_chemical('H2O', tmo.Chemical('H2O'),
#                                   phase='l', particle_size='Soluble',
#                                   degradability='Undegradable', organic=False)
    
    
#     # Alternatively, when search_ID is given, QSDsan will try to search the database
#     # H2O = Component('H2O', search_ID='H2O',
#     #                 phase='l', particle_size='Soluble',
#     #                 degradability='Undegradable', organic=False)
    
    
    
#     H2SO4 = Component.from_chemical('H2SO4', tmo.Chemical('H2SO4'),
#                                     phase='l', particle_size='Soluble',
#                                     degradability='Undegradable', organic=False)
    
#     cmps = Components((H2O, H2SO4))
#     cmps.compile() # After compiling, the Components object is ready to be used in the system

# For example, in the PitLatrine unit (subclass of Toilet),
# a tp (toilet paper) stream is one of the influents, and it contains the Component Tissue.
# In the _cmps.py, properties related to the Tissue component are defined.

# Links:
#     Toilet: https://github.com/QSD-Group/QSDsan/blob/main/qsdsan/sanunits/_toilet.py (line 109)
#     _cmps.py (in bwaise system): https://github.com/QSD-Group/EXPOsan/blob/main/exposan/bwaise/_cmps.py (lines 95-100)
#     Use of the PitLatrine unit: https://github.com/QSD-Group/EXPOsan/blob/main/exposan/bwaise/systems.py (lines 220-229)



class ChemicalAgent(Component):
    '''
    Chemical agents (cleaning agenta, electrolytes etc.) to be used in an electrochemical process.
    Refer to the example in :class:`ElectroChemCell` for how to use this class.

    Parameters
    ----------
    rate : float
        Rate of usage of the agent.
    rate_unit : str
        Unit in which the rate of usage is specified.
    unit_cost : float
        Unit cost of the agent.

    See Also
    --------
    :class:`ElectroChemCell`

    '''
    __slots__ = ('name', 'rate', 'rate_unit', 'unit_cost')

    def __init__(self, 
                 # !!! For the ``Component`` class, ID must be provided
                 ID, # when left as None, will be the same as the class name
                 formula=None, particle_size=None,
                 degradability = 'Slowly', i_mass=None, measured_as=None, organic = True,
                 rate=1, rate_unit='Litre per hr',
                 unit_cost=0.1):
        #!!! YL
        # When keywords of the parameters are not provided,
        # the values will be passed in the order of the parameters
        # defined in the Component.from_chemical function (part of the codes below)
        # def from_chemical(cls, ID, chemical=None, phase=None, measured_as=None, 
        #                   i_C=None, i_N=None, i_P=None, i_K=None, i_Mg=None, i_Ca=None,
        #                   i_mass=None, i_charge=None, i_COD=None, i_NOD=None,
        #                   f_BOD5_COD=None, f_uBOD_COD=None, f_Vmass_Totmass=None, 
        #                   description=None, particle_size=None, degradability=None, 
        #                   organic=None, **data):
        
        # Becuase in your previous code:
        # Component.from_chemical(ID, formula, particle_size, degradability, i_mass, measured_as, organic)
        # you did not specify the parameters, so the value are passed to the
        # wrong parameters, e.g., your formula, which is the second,
        # is interpreted as chemical in the function
        
        # Below are the codes for the from_chemical function, I specified
        # the keyward of the parameters, so the valuse are corrected passed to
        # the function
        Component.from_chemical(ID=ID, formula=formula,
                                particle_size=particle_size,
                                degradability=degradability,
                                i_mass=i_mass,
                                measured_as=measured_as, organic=organic)
        self.name = ID
        self.rate = rate
        self.rate_unit = rate_unit
        self.unit_cost = unit_cost

    # All subclasses of `ChemicalAgent` must have a `_cost` method, which returns the
    # purchase cost of this chemical
    # time must be specified in units compatible with rate_unit
    def _cost(self, time):
        return time*self.rate*self.unit_cost

chem = ChemicalAgent(ID='H2O')
costout = chem._cost(2)
print(costout)



