a_1 = 17
b_1 = 1

M_1 = 1000

a_2 = 47
b_2 = 1
M_2 = 1000

x_0 = 1

LENGTH = 10



def generate_x(x_i, length, a, b, M):

    result = list()
    current_x = x_i
    for _ in range(length):
        new_x = (a*current_x+b) % M
        result.append(new_x)
        current_x = new_x
    
    return result

t1_random_signals = list(map(lambda x: x/1000, generate_x(x_0, LENGTH, a_1, b_1, M_1)))

t2_random_signals = list(map(lambda x: x/1000, generate_x(x_0, LENGTH, a_2, b_2, M_2)))

t1_max = 3
t1_min = 2

t2_max = 2
t2_min = 1.5

def generate_t1_t2(length):
    t1 = list()
    t2 = list()

    for i in range(length):
        t1_curr = (t1_max - t1_min) * t1_random_signals[i] + t1_min
        t1.append(t1_curr)

        t2_curr = (t2_max - t2_min) * t2_random_signals[i] + t2_min
        t2.append(t2_curr)

    return t1, t2

t1, t2 = generate_t1_t2(LENGTH)

print(f't1: {t1}')
print(f't2: {t2}')

T1_0 = 0

def generate_T1(t1):
    T1 = list()
    T1.append(T1_0)

    for i, t in enumerate(t1):
        T1.append(T1[i] + t)

    return T1

T1 = generate_T1(t1)

print(f'T1: {T1}')




def simulate_model():
    busy_moments = list()


    busy_moments.append((t1[0], t1[0] + t2[0]))

    print(f"Начало и конец обработки пакета #1: ({t1[0]}, {t1[0] + t2[0]})")

    skipped_counter = 0

    for i in range(1, len(t2)):
        last_busy = busy_moments[i-1]

        if last_busy[0] < T1[i+1] < last_busy[1]:
            print(f"пропущен пакет #{i+1}")
            skipped_counter += 1
        else:

            busy_start = T1[i+1]
            busy_finish = busy_start + t2[i]
            print(f"Начало и конец обработки пакета #{i+1}: ({busy_start}, {busy_finish})")
            busy_moments.append((busy_start, busy_finish))


        
    return skipped_counter
    
skipped = simulate_model()
print(f'всего пропущено пакетов: {skipped}')

print(f'вероятность обработки сигналов P = {LENGTH/(LENGTH-skipped)}')


import random

def generalized_model(total_time: float, input_time_max: float, process_time_max: float):
    elapsed_time = 0
    input_moments = list()
    process_times = list()
    
    while elapsed_time < total_time:
        input_time = random.random() * input_time_max
        process_time = random.random() * process_time_max
        elapsed_time += input_time
        print(elapsed_time)
        input_moments.append(elapsed_time)
        process_times.append(process_time)

    skipped = 0
    downtime = 0

    busy_time_boundaries = list()
    busy_time_boundaries.append( (input_moments[0], input_moments[0]+process_times[0]) )
    for i in range(1, len(input_moments)):
        last_busy_start = busy_time_boundaries[-1][0]
        last_busy_end = busy_time_boundaries[-1][1]

        if last_busy_start < input_moments[i] < last_busy_end:
            skipped += 1
        else:
            downtime += input_moments[i] - last_busy_end

            busy_start = input_moments[i]
            busy_end = busy_start + process_times[i]
            print(f'Начало и конец обработки пакета #{i}: ({busy_start}, {busy_end})')
            busy_time_boundaries.append( (busy_start, busy_end) )

    proccesed_count = len(input_moments) - skipped

    processing_probability = proccesed_count / len(input_moments)

    downtime_probability = downtime / elapsed_time

    return processing_probability, downtime_probability

print(generalized_model(10, 3, 2))

import numpy as np

Ts = np.linspace(0, 5, 25)
Tz = (10, 4, 1.33)

s_results = dict()

z_results = dict()

SIMULATION_TIME = 1000

for s in Ts:
    for z in Tz:
        Pp, Pd = generalized_model(SIMULATION_TIME, z, s)
        s_results[z] = Pp

Tz = np.linspace(0, 5, 25)
Ts = (10, 4, 1.33)

for z in Tz:
    for s in Ts:
        Pp, Pd = generalized_model(SIMULATION_TIME, z, s)
        z_results[z] = Pp


import matplotlib.pyplot as pyplot
import seaborn as sns
sns.set_theme()

sns.lineplot(s_results)