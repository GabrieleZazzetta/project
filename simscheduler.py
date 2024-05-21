#Zazzetta Gabriele, mat. 347093

class Process:
    def __init__(self, pid, burst_time, priority=None):  #pid=nome processo
        self.pid = pid
        self.burst_time = burst_time
        self.priority = priority
        self.waiting_time = 0

def FCFS(processes):
    current_time = 0
    total_waiting_time = 0
    order_of_execution = []
    for process in processes:
        order_of_execution.append(process.pid)
        process.waiting_time = current_time
        total_waiting_time += current_time
        current_time += process.burst_time
    return total_waiting_time / len(processes), order_of_execution

def SJF(processes):
    current_time = 0
    total_waiting_time = 0
    order_of_execution = []
    remaining_processes = list(processes)
    remaining_processes.sort(key=lambda x: x.burst_time)   #ordinamento lista, "key=lambda x: x.burst_time" funzione che prende un singolo processo e restituisce il burst time
    for process in remaining_processes:
        order_of_execution.append(process.pid)
        process.waiting_time = current_time
        total_waiting_time += current_time
        current_time += process.burst_time
    return total_waiting_time / len(processes), order_of_execution

def Priority(processes):
    current_time = 0
    total_waiting_time = 0
    order_of_execution = []
    remaining_processes = list(processes)
    remaining_processes.sort(key=lambda x: x.priority)
    for process in remaining_processes:
        order_of_execution.append(process.pid)
        process.waiting_time = current_time
        total_waiting_time += current_time
        current_time += process.burst_time
    return total_waiting_time / len(processes), order_of_execution

from collections import deque
def RoundRobin(processes, quantum):
    current_time = 0
    total_waiting_time = 0
    total_burst_time = sum(process.burst_time for process in processes)
    order_of_execution = []
    remaining_processes = deque(processes)
    while remaining_processes:
        process = remaining_processes.popleft()
        if process.burst_time <= quantum:
            total_waiting_time += current_time - process.waiting_time
            current_time += process.burst_time
            order_of_execution.append(process.pid)
            total_burst_time -= process.burst_time
        else:
            total_waiting_time += current_time - process.waiting_time
            current_time += quantum
            process.burst_time -= quantum
            process.waiting_time = current_time  #aggiorno il tempo di attesa
            remaining_processes.append(process)
            order_of_execution.append(process.pid)

        #aggiorno il tempo di attesa per i processi nella coda
        for p in remaining_processes:
            total_waiting_time += min(quantum, p.burst_time)

    return total_waiting_time / len(processes), order_of_execution

def read_processes_from_file(file_path):
    processes = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
        num_processes, quantum = map(int, lines[0].split())  #lettura numero di processi e la durata del quanto
        for line in lines[1:]:
            if not line.startswith('#'):
                parts = line.split()
                pid = parts[0]
                burst_time = int(parts[1])
                priority = int(parts[2])
                processes.append(Process(pid, burst_time, priority))
    return processes, quantum

if __name__ == "__main__":
    file_path = "processi.txt"  
    processes, quantum = read_processes_from_file(file_path)

    algorithms = ["FCFS", "SJF", "Priority", "RoundRobin"]
    for algorithm in algorithms:
        if algorithm == "RoundRobin":
            avg_waiting_time, order_of_execution = RoundRobin(processes, quantum)
            print(f"{algorithm}:")
            print("Order of execution:", "->".join(order_of_execution), end=", ")
            print(f"TMA {avg_waiting_time}")
        else:
            avg_waiting_time, order_of_execution = globals()[algorithm](processes)
            print(f"{algorithm}:")
            print("Order of execution:", "->".join(order_of_execution), end=", ")
            print(f"TMA {avg_waiting_time}")
