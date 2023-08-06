"""Test plugin model class against hydromt.models.model_api"""

import pytest
from os.path import join, dirname, abspath
import numpy as np
import warnings
import pdb
from hydromt.models import MODELS
from hydromt.cli.cli_utils import parse_config

import logging

TESTDATADIR = join(dirname(abspath(__file__)), "data")
EXAMPLEDIR = join(dirname(abspath(__file__)), "..", "examples")

_models = {
    "wflow": {
        "example": "wflow_piave_subbasin",
        "ini": "wflow_piave_build_subbasin.ini",
    },
    "wflow_sediment": {
        "example": "wflow_sediment_piave_subbasin",
        "ini": "wflow_sediment_piave_build_subbasin.ini",
    },
}


def _compare_wflow_models(mod0, mod1):
    # check maps
    invalid_maps = {}
    if len(mod0._staticmaps) > 0:
        maps = mod0.staticmaps.raster.vars
        assert np.all(mod0.crs == mod1.crs), f"map crs staticmaps"
        for name in maps:
            map0 = mod0.staticmaps[name].fillna(0)
            map1 = mod1.staticmaps[name].fillna(0)
            if not np.allclose(map0, map1):
                notclose = ~np.isclose(map0, map1)
                xy = map0.raster.idx_to_xy(np.where(notclose.ravel())[0])
                ncells = int(np.sum(notclose))
                diff = (map0 - map1).values[notclose].mean()
                xys = ", ".join([f"({x:.6f}, {y:.6f})" for x, y in zip(*xy)])
                invalid_maps[name] = f"diff: {diff:.4f} ({ncells:d} cells: [{xys}])"
    # invalid_map_str = ", ".join(invalid_maps)
    assert len(invalid_maps) == 0, f"invalid maps: {invalid_maps}"
    # check geoms
    if mod0._staticgeoms:
        for name in mod0.staticgeoms:
            geom0 = mod0.staticgeoms[name]
            geom1 = mod1.staticgeoms[name]
            assert geom0.index.size == geom1.index.size and np.all(
                geom0.index == geom1.index
            ), f"geom index {name}"
            assert geom0.columns.size == geom1.columns.size and np.all(
                geom0.columns == geom1.columns
            ), f"geom columns {name}"
            assert geom0.crs == geom1.crs, f"geom crs {name}"
            if not np.all(geom0.geometry == geom1.geometry):
                warnings.warn(f"New geom {name} different than the example one.")
    # check config
    if mod0._config:
        # flatten
        assert mod0._config == mod1._config, f"config mismatch"


@pytest.mark.parametrize("model", list(_models.keys()))
def test_model_class(model):
    _model = _models[model]
    # read model in examples folder
    root = join(EXAMPLEDIR, _model["example"])
    mod = MODELS.get(model)(root=root, mode="r")
    mod.read()
    # run test_model_api() method
    non_compliant_list = mod.test_model_api()
    assert len(non_compliant_list) == 0


@pytest.mark.parametrize("model", list(_models.keys()))
def test_model_build(tmpdir, model):
    logger = logging.getLogger(__name__)
    _model = _models[model]
    # test build method
    # compare results with model from examples folder
    root = str(tmpdir.join(model))
    mod1 = MODELS.get(model)(root=root, mode="w", logger=logger)
    # Build method options
    region = {
        "subbasin": [12.2051, 45.8331],
        "strord": 4,
        "bounds": [11.70, 45.35, 12.95, 46.70],
    }
    res = 0.01666667
    config = join(TESTDATADIR, _model["ini"])
    opt = parse_config(config)
    # Build model
    mod1.build(region=region, res=res, opt=opt)
    # Check if model is api compliant
    non_compliant_list = mod1.test_model_api()
    assert len(non_compliant_list) == 0

    # Compare with model from examples folder
    # (need to read it again for proper staticgeoms check)
    mod1 = MODELS.get(model)(root=root, mode="r", logger=logger)
    mod1.read()
    root = join(EXAMPLEDIR, _model["example"])
    mod0 = MODELS.get(model)(root=root, mode="r")
    mod0.read()
    # compare models
    _compare_wflow_models(mod0, mod1)


def test_model_clip(tmpdir):
    logger = logging.getLogger(__name__)
    model = "wflow"
    # test clip method
    # compare results with model from examples folder
    root = join(EXAMPLEDIR, "wflow_piave_subbasin")

    # Clip method options
    destination = str(tmpdir.join(model))
    region = {
        "subbasin": [12.3006, 46.4324],
        "wflow_streamorder": 4,
    }

    # Clip workflow
    mod1 = MODELS.get(model)(root=root, mode="r", logger=logger)
    mod1.read()
    mod1.set_root(destination, mode="w")
    mod1.clip_staticmaps(region)
    mod1.clip_forcing()
    mod1.write()
    # Check if model is api compliant
    non_compliant_list = mod1.test_model_api()
    assert len(non_compliant_list) == 0

    # Compare with model from examples folder
    # (need to read it again for proper staticgeoms check)
    mod1 = MODELS.get(model)(root=destination, mode="r", logger=logger)
    mod1.read()
    root = join(EXAMPLEDIR, "wflow_piave_clip")
    mod0 = MODELS.get(model)(root=root, mode="r")
    mod0.read()
    # compare models
    _compare_wflow_models(mod0, mod1)
