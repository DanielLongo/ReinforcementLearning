### MDP Value Iteration and Policy Iteratoin
# You might not need to use all parameters

import numpy as np
import gym
import time
from lake_envs import *

np.set_printoptions(precision=3)

def policy_evaluation(P, nS, nA, policy, gamma=0.9, max_iteration=1000, tol=1e-3):
	"""Evaluate the value function from a given policy.

	Parameters
	----------
	P: dictionary
		It is from gym.core.Environment
		P[state][action] is tuples with (probability, nextstate, reward, terminal)
	nS: int
		number of states
	nA: int
		number of actions
	gamma: float
		Discount factor. Number in range [0, 1)
	policy: np.array
		The policy to evaluate. Maps states to actions.
	max_iteration: int
		The maximum number of iterations to run before stopping. Feel free to change it.
	tol: float
		Determines when value function has converged.
	Returnsv
	-------
	value function: np.ndarray
		The value function from the given policy.
	"""
	############################
	V = np.zeros(nS)
	prev_V = np.copy(V)
	curr_tol = 1
	i = 0
	while i <= max_iteration and curr_tol >= tol:
		for s in range(nS):

			for a in P[s][policy[s]]:
				prob, next_state, reward, _ = a
				Q = prob * (reward +  gamma * prev_V[next_state]) ############ NEXT StATE

			V[s] = Q

		curr_tol = np.abs(V - prev_V).max()
		prev_V = np.copy(V)
		i += 1


	############################
	# return np.zeros(nS)
	return V


def policy_improvement(P, nS, nA, value_from_policy, policy, gamma=0.9):
	"""Given the value function from policy improve the policy.

	Parameters
	----------
	P: dictionary
		It is from gym.core.Environment
		P[state][action] is tuples with (probability, nextstate, reward, terminal)
	nS: int
		number of states
	nA: int
		number of actions
	gamma: float
		Discount factor. Number in range [0, 1)
	value_from_policy: np.ndarray
		The value calculated from the policy
	policy: np.array
		The previous policy.

	Returns
	-------
	new policy: np.ndarray
		An array of integers. Each integer is the optimal action to take
		in that state according to the environment dynamics and the
		given value function.
	"""
	############################
	new_policy = np.zeros(nS, dtype="int")
	for s in range(nS):
		max_Q, max_a = -1, -1
		for a in range(nA):
			next_state_tups = P[s][a]
			for tup in next_state_tups:
				curr_prob, curr_ns, curr_reward, _ = tup
				curr_Q = curr_prob * (curr_reward + gamma * value_from_policy[curr_ns])
				if curr_Q > max_Q:
					max_Q = curr_Q
					max_a = a
		new_policy[s] = max_a

	############################
	return new_policy


def policy_iteration(P, nS, nA, gamma=0.9, max_iteration=20, tol=1e-3):
	"""Runs policy iteration.

	You should use the policy_evaluation and policy_improvement methods to
	implement this method.

	Parameters
	----------
	P: dictionary
		It is from gym.core.Environment
		P[state][action] is tuples with (probability, nextstate, reward, terminal)
	nS: int
		number of states
	nA: int
		number of actions
	gamma: float
		Discount factor. Number in range [0, 1)
	max_iteration: int
		The maximum number of iterations to run before stopping. Feel free to change it.
	tol: float
		Determines when value function has converged.
	Returns:
	----------
	value function: np.ndarray
	policy: np.ndarray
	"""
	V = np.zeros(nS)
	policy = np.zeros(nS, dtype=int)
	############################
	policy = np.random.choice(range(nA), nS)
	prev_policy = np.random.choice(range(nA), nS)
	i = 0 
	while (i == 0) or (np.abs(prev_policy, policy).all() > 0):
		i += 1
		value_from_policy = policy_evaluation(P, nS, nA, policy)
		prev_policy = policy
		policy = policy_improvement(P, nS, nA, value_from_policy, prev_policy)
	V = policy_evaluation(P, nS, nA, policy)
	############################

	print("v", V.shape, "policy", policy.shape)

	return V, policy


def value_iteration(P, nS, nA, gamma=0.9, max_iteration=20, tol=1e-3):
	"""
	Learn value function and policy by using value iteration method for a given
	gamma and environment.

	Parameters:
	----------
	P: dictionary
		It is from gym.core.Environment
		P[state][action] is tuples with (probability, nextstate, reward, terminal)
	nS: int
		number of states
	nA: int
		number of actions
	gamma: float
		Discount factor. Number in range [0, 1)
	max_iteration: int
		The maximum number of iterations to run before stopping. Feel free to change it.
	tol: float
		Determines when value function has converged.
	Returns:
	----------
	value function: np.ndarray
	policy: np.ndarray
	"""
	V = np.zeros(nS)
	policy = np.zeros(nS, dtype=int)
	############################
	V_prev = V
	k = 1
	while(k < max_iteration or np.abs(V, V_prev) < tol):
		V_prev = V
		for s in range(nS):
			max_Q, max_a = -1, -1
			for a in range(nA):
				next_state_tups = P[s][a]
				curr_Q = 0
				for tup in next_state_tups:
					prob, r, next_state, _ = tup
					curr_Q += prob*(r + gamma * V[next_state])
				if curr_Q > max_Q:
					max_Q = curr_Q
					max_a = a
			V[s] = max_Q
			policy[s] = max_a
		k += 1
	############################
	return V, policy

def example(env):
	"""Show an example of gym
	Parameters
		----------
		env: gym.core.Environment
			Environment to play on. Must have nS, nA, and P as
			attributes.
	"""
	env.seed(0);
	from gym.spaces import prng; prng.seed(10) # for print the location
	# Generate the episode
	ob = env.reset()
	for t in range(100):
		env.render()
		a = env.action_space.sample()
		ob, rew, done, _ = env.step(a)
		if done:
			break
	assert done
	env.render();

def render_single(env, policy):
	"""Renders policy once on environment. Watch your agent play!

		Parameters
		----------
		env: gym.core.Environment
			Environment to play on. Must have nS, nA, and P as
			attributes.
		Policy: np.array of shape [env.nS]
			The action to take at a given state
	"""

	episode_reward = 0
	ob = env.reset()
	for t in range(100):
		env.render()
		time.sleep(0.5) # Seconds between frames. Modify as you wish.
		a = policy[ob]
		ob, rew, done, _ = env.step(a)
		episode_reward += rew
		if done:
			break
	assert done
	env.render();
	# print "Episode reward: %f" % episode_reward
	print("Episode reward:", episode_reward)


# Feel free to run your own debug code in main!
# Play around with these hyperparameters.
if __name__ == "__main__":
	env = gym.make("Deterministic-4x4-FrozenLake-v0")
	print(env.__doc__)
	print("Here is an example of state, action, reward, and next state")
	example(env)
	V_vi, p_vi = value_iteration(env.P, env.nS, env.nA, gamma=0.9, max_iteration=20, tol=1e-3)
	V_pi, p_pi = policy_iteration(env.P, env.nS, env.nA, gamma=0.9, max_iteration=20, tol=1e-3)
