import gymnasium as gym
import numpy as np
import mujoco
#env = gym.make("InvertedPendulum-v5", render_mode='human')
env = gym.make("Humanoid-v5", render_mode='human')

observation, info = env.reset()
#print(observation[0])
env.unwrapped.state  = [3,-1,0,0]
model = env.unwrapped

#print(model.data.qM)
M = model.data.qM

print(model.data.efc_J)
#mujoco.mj_jac(M)
print(env.unwrapped.unwrapped.model_path)


#mb = env.unwrapped.model.geom_size
#print('Copy of parameter: ', mb)
#mb[2,0] = .35
#mb[2,1] = .35
#mb[2,2] = .35

#env.unwrapped.model.geom_size = mb
#print('assigned: ',env.unwrapped.model.geom_size)

for _ in range(1000):
    action = np.zeros(1)  # agent policy that uses the observation and info
    F = 0
    action[0] = F
    observation, reward, terminated, truncated, info = env.step(action)
    #print(terminated, truncated)
    #if terminated or truncated:
        #observation, info = env.reset()
    

env.close()
