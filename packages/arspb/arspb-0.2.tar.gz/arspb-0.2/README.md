# Augmented Random Search (ARS)

ARS is a random search method for training linear or fully connected neural network policies for continuous control problems, based on the paper ["Simple random search provides a competitive approach to reinforcement learning."](https://arxiv.org/abs/1803.07055) 

## Prerequisites for running ARS

Our ARS implementation relies on Python 3, OpenAI Gym, PyBullet and the Ray library for parallel computing.  

To install OpenAI Gym follow the instructions here:
https://github.com/openai/gym

To install PyBullet, use:
``` 
pip install pybullet
``` 
To install Ray execute:
``` 
pip install ray
```
For more information on Ray see http://ray.readthedocs.io/en/latest/. 

Install this repo using pip or clone using git:
```
pip install arspb
```

## Running ARS

First start Ray by executing a command of the following form:

```
ray start --head
```
or
```
ray start --head --redis-port=6379 --num-workers=18
```

This command starts multiple Python processes on one machine for parallel computations with Ray. 
Set "num_workers=X" for parallelizing ARS across X CPUs.
For parallelzing ARS on a cluster follow the instructions here: http://ray.readthedocs.io/en/latest/using-ray-on-a-large-cluster.html.

We recommend using single threaded linear algebra computations by setting: 
```
export MKL_NUM_THREADS=1
```

To train a policy for InvertedPendulumSwingupBulletEnv-v0, execute the following command: 

```
python arspb/ars.py
```

All arguments passed into ARS are optional and can be modified to train other environments, use different hyperparameters, or use  different random seeds.
For example, to train a policy for InvertedPendulumSwingupBulletEnv-v0, execute the following command:

```
python arspb/ars.py --env_name InvertedPendulumSwingupBulletEnv-v0 --policy_type=linear --n_directions 230 --deltas_used 230 --step_size 0.02 --delta_std 0.0075 --n_workers 48 --shift 5
```

You can also train a fully connected neural network, specifying the sizes of the hidden layers, as follows:

```
python arspb/ars.py --env_name AntBulletEnv-v0 --policy_type=nn --policy_network_size=128,64 --n_directions 230 --deltas_used 230 --step_size 0.02 --delta_std 0.0075 --n_workers 48 --shift 5
```

By default, the activation function is tanh, you can also select clip, by adding this argument:

```
--activation=clip
```

## Rendering Trained Policy

First run a PyBullet GUI window using the following command:
```
python -m pybullet_utils.runServer
```
When running a gym environment, it will automatically connect to this GUI window over shared memory.

To render a trained policy, execute a command of the following form: (--render is not needed, since the env will connect to the running GUI server)

```
python arspb/run_policy.py --expert_policy_file=trained_policies/InvertedPendulumSwingupBulletEnv-v0/lin_policy_plus.npz --envname=InvertedPendulumSwingupBulletEnv-v0 --json_file=trained_policies/InvertedPendulumSwingupBulletEnv-v0/params.json
```

Or enjoy a fully connected neural network policy, AntBulletEnv-v0:

```
python arspb/run_policy.py  --envname=AntBulletEnv-v0 --expert_policy_file=trained_policies/AntBulletEnv-v0/nn_policy_plus.npz --json_file=trained_policies/AntBulletEnv-v0/params.json
```
or a spinning running HumanoidBullet-v0 (click image below for video)
```
python3 arspb/run_policy.py  --envname=HumanoidBulletEnv-v0 --expert_policy_file=arspb/trained_policies/HumanoidBulletEnv-v0/nn_policy_plus.npz --json_file=arspb/trained_policies/HumanoidBulletEnv-v0/params.json --render
```

[![Spinning running HumanoidBullet-v0](https://github.com/erwincoumans/ARS/blob/master/arspb/trained_policies/HumanoidBullet-v0/spin_run.png)](https://www.youtube.com/watch?v=Z08TLBca_so&hd=1 "Spinning running HumanoidBullet-v0")
