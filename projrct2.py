import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt

# List to store processes
processes = []
total_memory = 0

# Function to add a process
def add_process():
    try:
        pid = len(processes) + 1  # Automatically assign Process ID
        arrival_time = int(arrival_time_entry.get())
        burst_time = int(burst_time_entry.get())
        memory_req = int(memory_entry.get())
        processes.append({
            "PID": pid,
            "Arrival Time": arrival_time,
            "Burst Time": burst_time,
            "Memory Requirement": memory_req
        })
        process_list.insert("", "end", values=(pid, arrival_time, burst_time, memory_req))
        arrival_time_entry.delete(0, tk.END)
        burst_time_entry.delete(0, tk.END)
        memory_entry.delete(0, tk.END)
    except ValueError:
        error_label.config(text="Please enter valid integers for Arrival Time, Burst Time, and Memory!")

# Function to simulate First Come First Serve (FCFS) with memory management
def simulate_fcfs():
    try:
        global total_memory
        available_memory = total_memory
        processes.sort(key=lambda x: x["Arrival Time"])  # Sort by arrival time
        time = 0
        waiting_times = []
        turnaround_times = []
        gantt_chart = []
        memory_chart = []

        for process in processes:
            if process["Memory Requirement"] > total_memory:
                results_label.config(
                    text=f"Process P{process['PID']} exceeds total memory capacity and is skipped!"
                )
                continue
            if available_memory < process["Memory Requirement"]:
                results_label.config(
                    text=f"Insufficient memory for Process P{process['PID']}. Skipping process!"
                )
                continue
            available_memory -= process["Memory Requirement"]

            if time < process["Arrival Time"]:
                time = process["Arrival Time"]
            gantt_chart.append((process["PID"], time, time + process["Burst Time"]))
            memory_chart.append((process["PID"], total_memory - available_memory))
            waiting_times.append(time - process["Arrival Time"])
            time += process["Burst Time"]
            turnaround_times.append(time - process["Arrival Time"])
            available_memory += process["Memory Requirement"]

        avg_waiting_time = sum(waiting_times) / len(waiting_times) if waiting_times else 0
        avg_turnaround_time = sum(turnaround_times) / len(turnaround_times) if turnaround_times else 0

        # Show results
        results_label.config(
            text=f"Average Waiting Time: {avg_waiting_time:.2f}\n"
                 f"Average Turnaround Time: {avg_turnaround_time:.2f}"
        )

        # Show Gantt chart
        fig, ax = plt.subplots(2, 1, figsize=(10, 6))
        for pid, start, end in gantt_chart:
            ax[0].barh(0, end - start, left=start, align='center', edgecolor='black', label=f"P{pid}")
        ax[0].set_yticks([])
        ax[0].set_xticks(range(0, max(end for _, _, end in gantt_chart) + 1))
        ax[0].set_title("Gantt Chart")
        ax[0].set_xlabel("Time")
        ax[0].legend()

        # Show memory allocation
        ax[1].barh([0], [memory_chart[-1][1] if memory_chart else 0], align='center', color='green')
        ax[1].set_title("Memory Usage")
        ax[1].set_xlabel("Memory (MB)")
        ax[1].set_xlim(0, total_memory)

        plt.tight_layout()
        plt.show()
    except Exception as e:
        results_label.config(text=f"Error: {str(e)}")

# Function to set total memory
def set_total_memory():
    try:
        global total_memory
        total_memory = int(total_memory_entry.get())
        memory_label.config(text=f"Total Memory: {total_memory} MB")
        total_memory_entry.delete(0, tk.END)
    except ValueError:
        error_label.config(text="Please enter a valid integer for Total Memory!")

# Function to clear all processes
def clear_processes():
    global processes
    processes = []
    process_list.delete(*process_list.get_children())
    results_label.config(text="")
    error_label.config(text="")

# GUI setup
root = tk.Tk()
root.title("CPU Scheduling Simulator with Memory Management")
root.geometry("700x600")

# Total memory input
memory_frame = tk.Frame(root)
memory_frame.pack(pady=10)

tk.Label(memory_frame, text="Total Memory (MB)").grid(row=0, column=0, padx=5, pady=5)
total_memory_entry = tk.Entry(memory_frame)
total_memory_entry.grid(row=0, column=1, padx=5, pady=5)
set_memory_button = tk.Button(memory_frame, text="Set Memory", command=set_total_memory)
set_memory_button.grid(row=0, column=2, padx=5, pady=5)
memory_label = tk.Label(root, text="Total Memory: Not Set")
memory_label.pack()

# Input section
input_frame = tk.Frame(root)
input_frame.pack(pady=10)

tk.Label(input_frame, text="Arrival Time").grid(row=0, column=0, padx=5, pady=5)
arrival_time_entry = tk.Entry(input_frame)
arrival_time_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(input_frame, text="Burst Time").grid(row=1, column=0, padx=5, pady=5)
burst_time_entry = tk.Entry(input_frame)
burst_time_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(input_frame, text="Memory Requirement (MB)").grid(row=2, column=0, padx=5, pady=5)
memory_entry = tk.Entry(input_frame)
memory_entry.grid(row=2, column=1, padx=5, pady=5)

add_button = tk.Button(input_frame, text="Add Process", command=add_process)
add_button.grid(row=3, column=0, columnspan=2, pady=10)

error_label = tk.Label(root, text="", fg="red")
error_label.pack()

# Process list section
process_list_frame = tk.Frame(root)
process_list_frame.pack(pady=10)

process_list = ttk.Treeview(process_list_frame, columns=("PID", "Arrival Time", "Burst Time", "Memory Requirement"), show="headings")
process_list.heading("PID", text="PID")
process_list.heading("Arrival Time", text="Arrival Time")
process_list.heading("Burst Time", text="Burst Time")
process_list.heading("Memory Requirement", text="Memory Requirement")
process_list.pack()

# Simulation and results section
results_frame = tk.Frame(root)
results_frame.pack(pady=10)

simulate_button = tk.Button(results_frame, text="Simulate FCFS", command=simulate_fcfs)
simulate_button.grid(row=0, column=0, padx=10, pady=10)

clear_button = tk.Button(results_frame, text="Clear Processes", command=clear_processes)
clear_button.grid(row=0, column=1, padx=10, pady=10)

results_label = tk.Label(root, text="")
results_label.pack()

# Run the main loop
root.mainloop()
