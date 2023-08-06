import dataclasses

from .steeldesign import SteelMaterial


class SteelShape():
    def __init__(self, name: str, material: SteelMaterial):
        self.name = name
        self.material = material


class WideFlangeShape(SteelShape):
    def __init__(self, name: str, material: SteelMaterial = None):
        if material is None:
            material = SteelMaterial.from_name('A992', grade=50)

        super().__init__(name, material)

    def check_seismic_wtr(self):
        pass


class RectangularHssShape(SteelShape):
    def __init__(self, name: str, material: SteelMaterial = None):
        if material is None:
            material = SteelMaterial.from_name('A500', grade='C')

        super().__init__(name, material)


class RoundHssShape(SteelShape):
    def __init__(self, name: str, material: SteelMaterial = None):
        if material is None:
            material = SteelMaterial.from_name('A500', grade='B')

        super().__init__(name, material)
