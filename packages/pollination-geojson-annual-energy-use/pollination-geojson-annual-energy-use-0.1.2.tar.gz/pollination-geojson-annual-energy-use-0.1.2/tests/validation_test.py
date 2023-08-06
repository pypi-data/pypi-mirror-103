from pollination.geojson_annual_energy_use.entry import \
    GeojsonAnnualEnergyUseEntryPoint
from queenbee.recipe.dag import DAG


def test_geojson_annual_energy_use():
    recipe = GeojsonAnnualEnergyUseEntryPoint().queenbee
    assert recipe.name == 'geojson-annual-energy-use-entry-point'
    assert isinstance(recipe, DAG)
