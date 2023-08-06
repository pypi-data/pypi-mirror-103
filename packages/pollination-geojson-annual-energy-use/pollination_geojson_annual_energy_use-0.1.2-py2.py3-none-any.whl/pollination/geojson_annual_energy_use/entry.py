from pollination_dsl.dag import Inputs, DAG, task, Outputs
from dataclasses import dataclass
from typing import Dict, List
from pollination.dragonfly_energy.translate import ModelFromGeojson
from pollination.dragonfly_energy.edit import WindowsByRatio
from pollination.dragonfly_energy.translate import ModelToHoneybee
from pollination.honeybee_energy.settings import SimParDefault
from pollination.honeybee_energy.simulate import SimulateModel
from pollination.honeybee_energy.result import EnergyUseIntensity

# input/output alias
from pollination.alias.inputs.ddy import ddy_input
from pollination.alias.inputs.bool_options import filter_des_days_input, \
    use_multiplier_input
from pollination.alias.outputs.eui import parse_eui_results


@dataclass
class GeojsonAnnualEnergyUseEntryPoint(DAG):
    """GeoJSON annual energy use entry point."""

    # inputs
    geojson = Inputs.file(
        description='A geoJSON file with building footprints as Polygons or '
        'MultiPolygons.', path='model.geojson', extensions=['geojson', 'json']
    )

    epw = Inputs.file(
        description='EPW weather file to be used for the annual energy simulation.',
        extensions=['epw']
    )

    ddy = Inputs.file(
        description='A DDY file with design days to be used for the initial '
        'sizing calculation.', extensions=['ddy'],
        alias=ddy_input
    )

    window_ratio = Inputs.str(
        description='A number between 0 and 1 (but not perfectly equal to 1) for the '
        'desired ratio between window area and wall area. If multiple values are '
        'input here (each separated by a space), different WindowParameters will be '
        'assigned based on cardinal direction, starting with north and moving '
        'clockwise.', default='0.4'
    )

    all_to_buildings = Inputs.str(
        description='A switch to indicate if all geometries in the geojson file should '
        'be considered buildings. If buildings-only, this method will only generate '
        'footprints from geometries that are defined as a "Building" in the type '
        'field of its corresponding properties.',
        default='buildings-only',
        spec={'type': 'string', 'enum': ['buildings-only', 'all-to-buildings']}
    )

    existing_to_context = Inputs.str(
        description='A switch to indicate whether polygons possessing a building_status '
        'of "Existing" under their properties should be imported as ContextShade '
        'instead of Building objects.',
        default='existing-to-context',
        spec={'type': 'string', 'enum': ['no-context', 'existing-to-context']}
    )

    separate_top_bottom = Inputs.str(
        description='A switch to indicate whether top/bottom stories of the buildings '
        'should not be separated in order to account for different boundary conditions '
        'of the roof and ground floor.',
        default='separate-top-bottom',
        spec={'type': 'string', 'enum': ['separate-top-bottom', 'no-separation']}
    )

    use_multiplier = Inputs.str(
        description='A switch to note whether the multipliers on each Building story '
        'should be passed along to the generated Honeybee Room objects or if full '
        'geometry objects should be written for each story of each dragonfly building.',
        default='full-geometry',
        spec={'type': 'string', 'enum': ['full-geometry', 'multiplier']},
        alias=use_multiplier_input
    )

    shade_dist = Inputs.str(
        description='A number to note the distance beyond which other buildings shade '
        'should be excluded from a given Honeybee Model. This can include the units of '
        'the distance (eg. 100ft) or, if no units are provided, the value will be '
        'interpreted in the dragonfly model units. If 0, shade from all neighboring '
        'buildings will be excluded from the resulting models.', default='50m'
    )

    filter_des_days = Inputs.str(
        description='A switch for whether the ddy-file should be filtered to only '
        'include 99.6 and 0.4 design days', default='filter-des-days',
        spec={'type': 'string', 'enum': ['filter-des-days', 'all-des-days']},
        alias=filter_des_days_input
    )

    units = Inputs.str(
        description='A switch to indicate whether the data in the final EUI file '
        'should be in SI (kWh/m2) or IP (kBtu/ft2). Valid values are "si" and "ip".',
        default='si', spec={'type': 'string', 'enum': ['si', 'ip']}
    )

    # tasks
    @task(template=ModelFromGeojson)
    def convert_from_geojson(
        self, geojson=geojson, all_to_buildings=all_to_buildings,
        existing_to_context=existing_to_context, separate_top_bottom=separate_top_bottom
    ) -> List[Dict]:
        return [
            {
                'from': ModelFromGeojson()._outputs.model,
                'to': 'model_init.dfjson'
            }
            ]

    @task(template=WindowsByRatio, needs=[convert_from_geojson])
    def assign_windows(
        self, model=convert_from_geojson._outputs.model, ratio=window_ratio
    ) -> List[Dict]:
        return [
            {
                'from': WindowsByRatio()._outputs.new_model,
                'to': 'model.dfjson'
            }
            ]

    @task(template=ModelToHoneybee, needs=[assign_windows])
    def convert_to_honeybee(
        self, model=assign_windows._outputs.new_model, obj_per_model='Story',
        use_multiplier=use_multiplier, shade_dist=shade_dist
    ) -> List[Dict]:
        return [
            {
                'from': ModelToHoneybee()._outputs.output_folder,
                'to': 'models'
            },
            {
                'from': ModelToHoneybee()._outputs.hbjson_list,
                'description': 'Information about exported HBJSONs.'
            }
            ]

    @task(template=SimParDefault)
    def create_sim_par(self, ddy=ddy, filter_des_days=filter_des_days) -> List[Dict]:
        return [
            {'from': SimParDefault()._outputs.sim_par_json,
             'to': 'simulation_parameter.json'}
            ]

    @task(
        template=SimulateModel,
        needs=[create_sim_par, convert_to_honeybee],
        loop=convert_to_honeybee._outputs.hbjson_list,
        sub_folder='results',  # create a subfolder for results
        sub_paths={'model': '{{item.path}}'}  # sub_path for sim_par arg
    )
    def run_simulation(
        self, model=convert_to_honeybee._outputs.output_folder, epw=epw,
        sim_par=create_sim_par._outputs.sim_par_json
    ) -> List[Dict]:
        return [
            {'from': SimulateModel()._outputs.sql, 'to': 'sql/{{item.id}}.sql'},
            {'from': SimulateModel()._outputs.html, 'to': 'html/{{item.id}}.htm'},
            {'from': SimulateModel()._outputs.err, 'to': 'err/{{item.id}}.err'}
            ]

    @task(template=EnergyUseIntensity, needs=[run_simulation])
    def compute_eui(
        self, result_folder='results/sql', units=units
    ) -> List[Dict]:
        return [
            {'from': EnergyUseIntensity()._outputs.eui_json,
             'to': 'eui.json'}
            ]

    # outputs
    eui = Outputs.file(
        source='eui.json', description='A JSON containing energy use intensity '
        'information across the total model floor area. Values are either kWh/m2 '
        'or kBtu/ft2 depending upon the units input.',
        alias=parse_eui_results
    )

    dfjson = Outputs.file(
        source='model.dfjson',
        description='The DFJSON model used for simulation.'
    )

    hbjson = Outputs.folder(
        source='models',
        description='Folder containing the HBJSON models used for simulation.'
    )

    sql = Outputs.folder(
        source='results/sql',
        description='Folder containing the result SQL files output by the simulation.'
    )

    html = Outputs.folder(
        source='results/html',
        description='Folder containing the result HTML pages with summary reports.'
    )

    err = Outputs.folder(
        source='results/err',
        description='Folder containing the error reports output by the simulation.'
    )
