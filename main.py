from initial_condition import DEFAULT_INITIAL_CONDITION
from rocket_circularization import RocketCircularization
from VPG import PolicyNetworkBaseline
import numpy as np
import wandb
project_name = 'Rocket Circularization'


config_network = {
    'actor_hidden_dims': [32, 32],
    'critic_hidden_dims': [32, 32],
    'lr': 0.001
}
config_init_cond = {
    'function': 'rotated_state',
    'parameters': {'st': [1, 0, 0, 1.1], 'random': True}
}
config_bounds = {
    'rmin_func': 'constant',
    'rmin_strategy': [
        {
            'name': 'constant',
            'parameters': {'const': 0.1}
        }
    ],
    'rmax_func': 'constant',
    'rmax_strategy': [
        {
            'name': 'constant',
            'parameters': {'const': 2}
        }
    ]
}

config_env = {
    'max_iter': 500,
    'evaluation_steps': 0,
    'radius_range': [0.1, 2],
    'target_radius': 1,
    'dt': 0.01,
    'M': 1,
    'm': 0.01,
    'G': 1,
    'init_state': config_init_cond,
    'thrust_vectors': [[.1, 0], [0, .1], [-.1, 0], [0, -.1]],
    'circularization_penalty': 1,
    'evaluation_penalty': 1,
    'inbounds_reward': 1,
    'thrust_penalty': 0,
    't_vec_len': 1,
    'state_output_mode': 'No Theta'
}
config_training = {
    'episodes': 100000,
    'gamma': 1,
    'vdo_rate': 1000,
    'save_rate': 100,
}

with wandb.init(project=project_name, config={**config_network, **config_env, **config_training, **config_bounds}) as run:
    env = RocketCircularization(bound_config=config_bounds, **config_env)
    rocket_policy = PolicyNetworkBaseline(input_dims=env.get_state_dims(),
                                          output_dims=env.get_action_dims(),
                                          **config_network)
    rocket_policy.train(env, **config_training)
