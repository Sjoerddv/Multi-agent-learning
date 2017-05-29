import math
import random
import time
import matplotlib.pyplot as plt
T1 = time.time()
N = 8
max_iterations = (5*10**5)
no_collision_reward, collision_reward = 100, 10
w, h = 12, 12
# speed should be greater than r in order to avoid 'traffic jams'
# speed should also be co-prime with w and h
speed = 3
# k is not as defined
k = 4
e = .1
# r is squared because: (x**2 + y**2) < r**2.
r =1
r = r*r
sin_angles = [speed * math.sin(i*2 * math.pi / k) for i in range(k)]
cos_angles = [speed * math.cos(i*2 * math.pi / k) for i in range(k)]
sin_angles2 = [0.0, 3.0, 0, -3.0 ]
cos_angles2 = [3.0, 0, -3.0, 0]
print(sin_angles)
print(cos_angles)
initial_value = 0
range_reduce = 5000

class Agent:
    def __init__(self, n):
        self.n = n
        self.x = random.randint(0, w - 1)
        self.y = random.randint(0, h - 1)
        # amount of times, mean
        # adjusted for optimanl initial values
        self.history = [(0, initial_value) for _ in range(k)]
        # angle is a value between 0 and k - 1
        self.current_angle = random.randint(0, k - 1)
        self.best_angle = self.current_angle
        self.collisions = 0

    def decide_angle(self):
        if random.random() < e:
            self.current_angle = random.randint(0, k - 1)
        else:
            self.current_angle = self.best_angle

    def decide_angle_optimistic(self):
        from random import shuffle
        x = list(range(k))
        shuffle(x)
        current_val = 0
        temp_angle = 0
        for j in x:
            if self.history[j][1] > current_val:
                current_val = self.history[j][1]
                temp_angle = j
        self.current_angle = temp_angle;

    def move(self):
        self.x += cos_angles[self.current_angle]
        self.y += sin_angles[self.current_angle]
        self.x, self.y = self.x % w, self.y % h

    def undo_move(self):
        self.x -= cos_angles[self.current_angle]
        self.y -= sin_angles[self.current_angle]
        self.x, self.y = self.x % w, self.y % h

    def collision(self, pop):
        for other_skater in pop:
            if other_skater.n != self.n:
                if ((other_skater.x - self.x) ** 2 +
                            (other_skater.y - self.y) ** 2) < r:
                    # print(other_skater.x, self.x, other_skater.y, self.y, r)
                    self.collisions += 1
                    return True
        return False

    def update_history(self, value, iterate):
        amount, mean = self.history[self.current_angle]
        amount += 1
        mean *= (amount - 1) / amount
        mean += value/amount
        self.history[self.current_angle] = amount, mean

        #check if current angle is best
        if mean > self.history[self.best_angle][1]:
            self.best_angle = self.current_angle
        #   print(iterate)


population = [Agent(n) for n in range(N)]
current_angles = [0 for _ in range(k)]
current_rewards = [0 for _ in range(k)]
last_collision = 0
total_collisions = 0
plot_vector = [[0 for _ in range(k)] for _ in range(max_iterations // range_reduce)]
collision_vector = [[0 for _ in range(k)] for _ in range(max_iterations // range_reduce)]
reward_vector = [[0 for _ in range(k)] for _ in range(max_iterations // range_reduce)]
for iteration in range(max_iterations):
    if iteration % 1000 == 0:
        print (iteration)
    line = [None for _ in range(N)]
    random.shuffle(population)
    for skater in population:
        skater.decide_angle()
        plot_vector[iteration // range_reduce][skater.current_angle] += 1/range_reduce
        skater.move()
        if not skater.collision(population):
            reward = no_collision_reward
        else:
            collision_vector[iteration//range_reduce][skater.current_angle] += 1/range_reduce
            last_collision = iteration
            skater.undo_move()
            reward = collision_reward
            total_collisions += 1
        skater.update_history(reward, iteration)
        current_angles[skater.current_angle] += 1
        current_rewards[skater.current_angle] += reward
    for i in range(0, k):
        if not current_angles[i] == 0:
            reward_vector[iteration // range_reduce][i] += current_rewards[i] / (current_angles[i] * range_reduce)
        # line[skater.n] = (int(skater.x), int(skater.y), skater.current_angle)
print("Last collisions at", last_collision)
print("Total collisions,", total_collisions)
line = [None for _ in range(N)]
for skater in population:
    line[skater.n] = (int(skater.x), int(skater.y), skater.current_angle)

print(line)
for skater in population:
    print(skater.best_angle, skater.history, skater.collisions)
#plt.plot(collision_vector)

#for i in plot_vector:
#    print(i)
print(time.time() - T1)
plt.figure(1)
plt.plot(plot_vector)
plt.xlabel('Generation (x %s)'%range_reduce)
plt.ylabel('Number of skaters')
plt.legend()


plt.figure(2)
plt.plot(reward_vector)
plt.xlabel('Generation (x %s)'%range_reduce)
plt.ylabel('Mean reward')
plt.legend()
plt.show()
print("done")