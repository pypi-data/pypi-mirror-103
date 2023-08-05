"""

Code to load a policy and generate rollout data. Adapted from https://github.com/berkeleydeeprlcourse. 
Example usage:
    python run_policy.py ../trained_policies/Humanoid-v1/policy_reward_11600/lin_policy_plus.npz Humanoid-v1 --render \
            --num_rollouts 20
"""
import numpy as np
import gym
import pybullet_envs
import json
from arspb.policies import *
import time
import arspb.trained_policies as tp
import os

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--expert_policy_file', type=str, default="")
    parser.add_argument('--envname', type=str, default="InvertedPendulumSwingupBulletEnv-v0")
    parser.add_argument('--render', action='store_true')
    parser.add_argument('--nosleep', action='store_true')

    parser.add_argument('--num_rollouts', type=int, default=20,
                        help='Number of expert rollouts')
    parser.add_argument('--json_file', type=str, default="")
    args = parser.parse_args()

    #print('create gym environment:', args.envname)
    env = gym.make(args.envname)

    print('loading and building expert policy')
    if len(args.json_file)==0:
      args.json_file = tp.getDataPath()+"/"+ args.envname+"/params.json"    
    with open(args.json_file) as f:
       params = json.load(f)
    print("params=",params)
    if len(args.expert_policy_file)==0:
      args.expert_policy_file=tp.getDataPath()+"/"+args.envname+"/nn_policy_plus.npz" 
      if not os.path.exists(args.expert_policy_file):
        args.expert_policy_file=tp.getDataPath()+"/"+args.envname+"/lin_policy_plus.npz"
    data = np.load(args.expert_policy_file, allow_pickle=True)

    lst = data.files
    weights = data[lst[0]][0]
    mu = data[lst[0]][1]
    print("mu=",mu)
    std = data[lst[0]][2]
    print("std=",std)
        
    ob_dim = env.observation_space.shape[0]
    ac_dim = env.action_space.shape[0]
    ac_lb = env.action_space.low
    ac_ub = env.action_space.high
    
    policy_params={'type': params["policy_type"],
                   'ob_filter':params['filter'],
                   'policy_network_size' : params["policy_network_size"],
                   'ob_dim':ob_dim,
                   'ac_dim':ac_dim,
                   'action_lower_bound' : ac_lb,
                   'action_upper_bound' : ac_ub,
    }
    policy_params['weights'] = weights
    policy_params['observation_filter_mean'] = mu
    policy_params['observation_filter_std'] = std
    
    policy = FullyConnectedNeuralNetworkPolicy(policy_params, update_filter=False)
    
    policy.get_weights()
            
   
    if args.render: 
      env.render('human')
    returns = []
    observations = []
    actions = []
    for i in range(args.num_rollouts):
        print('iter', i)
        obs = env.reset()
        done = False
        totalr = 0.
        steps = 0
        while not done:
            action = policy.act(obs)
            observations.append(obs)
            actions.append(action)
            
            
            obs, r, done, _ = env.step(action)
            totalr += r
            steps += 1
            if args.render:
                env.render()
            if not args.nosleep:
              time.sleep(1./60.)
            #if steps % 100 == 0: print("%i/%i"%(steps, env.spec.timestep_limit))
            #if steps >= env.spec.timestep_limit:
            #    break
        #print("steps=",steps)
        returns.append(totalr)

    print('returns', returns)
    print('mean return', np.mean(returns))
    print('std of return', np.std(returns))
    
if __name__ == '__main__':
    main()
