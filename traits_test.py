from nipype.interfaces.base import traits
#from base import PBRBaseInputSpec, PBRBaseInterface



class InventoryItem(traits.HasTraits):
       name  = traits.Str() # String value, default is ''
       stock = traits.Enum(None, 0, 1, 2, 3, 'many')
       lol = traits.List(traits.Any())
       lol2 = traits.Either()
           # Enumerated list, default value is
           #'None'

hats = InventoryItem()
hats.name = 'Stetson'

print('%s: %s' % (hats.name, hats.stock))

hats.stock = 2      # OK
hats.stock = 'many' # OK
print('%s: %s' % (hats.name, hats.stock))

hats.lol = ['a', ['b']]
print(hats.lol, hats.lol2)

"""
class SienaInputSpec(PBRBaseInputSpec):
    mse_id1 = traits.List(traits.List(File(exists = True)))

class Siena(PBRBaseInterface):
    input_spec = SienaInputSpec

    def _run_interface_pbr(self, runtime):
        print(self.inputs)
"""