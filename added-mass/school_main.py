import json
import tempfile
import os
import numpy as np
from fish import Fish
from environment import Environment

# Template shared by every fish in the school
BASE_FISH_CONFIG = {
    "N": 7,
    "fish_length": 1.0,
    "bvs_N": 21,
    "thickness_parameter": 0.2,

    "head_velocity_x": -1.0,
    "head_velocity_y": 0.0,
    "initial_heading": 180,

    "desired_heading": 180,
    "max_offset_rate": 0.1,

    "normalized_wave_number": -6,
    "wave_frequency": 6.283185307179586,
    "wave_amplitude": 0.4,
    "wave_phase": 0,
    "wave_offset": 0,
    "c1": 1,
    "c2": 0.2,

    "E": 10000,
    "rho": 2000,
    "d_b": 0.5,
    "d_s": 1.0,

    "fluid_density": 1000,
    "CF": 1e-3,
    "CD": 0.5,
    "CA": 1.5,
}


def make_fish_config(x_start: float, y_start: float = 0.0, overrides: dict = None) -> dict:
    
    config = dict(BASE_FISH_CONFIG)
    config["head_position_x"] = x_start
    config["head_position_y"] = y_start
    if overrides:
        config.update(overrides)
    return config


def build_inline_school(n_fish: int, x_spacing: float = 2.0, y_line: float = 0.0,
                         lead_x: float = 0.0, overrides_per_fish: list = None):
   
    if overrides_per_fish is None:
        overrides_per_fish = [{}] * n_fish

    configs = []
    for k in range(n_fish):
        x_start = lead_x - k * x_spacing
        configs.append(make_fish_config(x_start=x_start, y_start=y_line,
                                          overrides=overrides_per_fish[k]))
    return configs


def write_configs_to_tempfiles(configs: list, tmpdir: str) -> list:
    
    paths = []
    for ii, config in enumerate(configs):
        path = os.path.join(tmpdir, f"school_fish_{ii}.json")
        with open(path, "w") as f:
            json.dump(config, f, indent=4)
        paths.append(path)
    return paths


def build_school(n_fish: int, x_spacing: float = 2.0, y_line: float = 0.0,
                  lead_x: float = 0.0, overrides_per_fish: list = None,
                  config_dir: str = None) -> list:
    
    configs = build_inline_school(n_fish, x_spacing, y_line, lead_x, overrides_per_fish)

    if config_dir is None:
        config_dir = tempfile.mkdtemp(prefix="school_configs_")
    os.makedirs(config_dir, exist_ok=True)

    paths = write_configs_to_tempfiles(configs, config_dir)
    school = [Fish(path) for path in paths]
    return school


if __name__ == "__main__":
    import pickle
    import time


    '''
    one line of fish (inline)
    '''
    n_fish = 10
    x_spacing = 4.0  
    y_line = 0.0    

    '''
    new
    '''
    overrides_per_fish = [
    {"goal_points": [[-10.0, 15.0], [-20.0, -3.0], [-15.0, 5.0]]},
    {"goal_points": [[-20.0, -3.0], [-15.0, 5.0], [-10.0, 15.0]]},
    {"goal_points": [[-15.0, 5.0], [-10.0, 15.0], [-20.0, -3.0]]},
    {"goal_points": [[-10.0, 15.0], [-20.0, -3.0], [-15.0, 5.0]]},
    {"goal_points": [[-20.0, -3.0], [-15.0, 5.0], [-10.0, 15.0]]},
    {"goal_points": [[-15.0, 5.0], [-10.0, 15.0], [-20.0, -3.0]]},
    {"goal_points": [[-10.0, 15.0], [-20.0, -3.0], [-15.0, 5.0]]},
    {"goal_points": [[-20.0, -3.0], [-15.0, 5.0], [-10.0, 15.0]]},
    {"goal_points": [[-15.0, 5.0], [-10.0, 15.0], [-20.0, -3.0]]},
    {"desired_heading": 160}
    ]
    '''
    new
    '''

    school = build_school(n_fish=10, x_spacing=4.0, y_line=0.0, lead_x=6.0,
                       overrides_per_fish=overrides_per_fish,
                       config_dir="school_configs")

    '''
    school = build_school(n_fish=n_fish, x_spacing=x_spacing, y_line=y_line, lead_x=6.0,
                           config_dir="school_configs")
    '''

    print(f"Built {len(school)} fish, head positions:")
    for ii, fish in enumerate(school):
        print(f"  fish {ii}: head = {fish.positions[:, 0]}")

    fish_tank = Environment(school, controller=True)
    #fish_tank = Environment(school, controller=True, time_N=8001)

    t_start = time.perf_counter()
    fish_tank.run_simulation()
    t_end = time.perf_counter()

    elapsed = t_end - t_start
    minutes = int(elapsed // 60)
    seconds = int(elapsed % 60)
    centiseconds = int((elapsed % 1) * 100)
    print(f"\nTotal time: {minutes:02d}m {seconds:02d}s {centiseconds:02d}cs")

    prefix = f"{n_fish}_fish_inline_school"
    with open(f"{prefix}.pkl", "wb") as f:
        pickle.dump(fish_tank.output, f)
    with open(f"{prefix}_Gamma.pkl", "wb") as f:
        pickle.dump(fish_tank.output_Gamma, f)
    with open(f"{prefix}_bvs.pkl", "wb") as f:
        pickle.dump(fish_tank.output_bvs, f)
    with open(f"{prefix}_bvs_gamma.pkl", "wb") as f:
        pickle.dump(fish_tank.output_bvs_gamma, f)

    #fish_tank.save_animation(f"{prefix}.mp4")
    #fish_tank.save_animation("new.mp4")
    fish_tank.save_animation(
        "new.mp4",
        output=fish_tank.output,
        output_Gamma=fish_tank.output_Gamma,
        output_bvs=fish_tank.output_bvs,
        output_bvs_gamma=fish_tank.output_bvs_gamma
    )
