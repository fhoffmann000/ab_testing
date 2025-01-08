import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import random


class RandomEvent:
    """
    Represents a random event with a specified win rate.

    Attributes:
        winrate (float): The true win rate of the event.
        estimate (float): The current estimated win rate based on observed results.
        N (int): The number of times this event has been selected.
        history (list): A list of tuples tracking (iteration, estimate).
    """

    def __init__(self, winrate):
        self.winrate = winrate
        self.estimate = 0  # Estimated win rate
        self.N = 0  # Number of pulls
        self.history = []  # Track estimates over time

    def update(self, result):
        """
        Updates the estimated win rate based on a new result.
        
            result (bool): The outcome of the event (1 for success, 0 for failure).
        """
        self.N += 1
        self.estimate += (result - self.estimate) / self.N
        self.history.append((self.N, self.estimate))

    def pull(self):
        """
        Simulates pulling the lever for this event.
        
            bool: True if the event is successful, False otherwise.
        """
        return np.random.random() < self.winrate


class Experiment:
    """
    Conducts an A/B test experiment using the epsilon-greedy strategy.

    Attributes:
        probs (list): The true probabilities (win rates) for each event.
        initial_epsilon (float): The initial exploration rate.
        iterations (int): The number of iterations to run the experiment.
        num_explored (int): Number of times exploration occurred.
        num_exploited (int): Number of times exploitation occurred.
        num_optimal (int): Number of times the optimal choice was selected.
    """

    def __init__(self, probs, initial_epsilon=0.1, iterations=5000):
        """
        Initializes the experiment with given probabilities, epsilon, and iterations.

            probs (list): A list of win probabilities for the events.
            initial_epsilon (float): Initial exploration rate.
            iterations (int): Number of iterations for the experiment.
        """
        self.probs = probs
        self.initial_epsilon = initial_epsilon
        self.iterations = iterations
        self.num_explored = 0
        self.num_exploited = 0
        self.num_optimal = 0

    @staticmethod
    def epsilon_func(val, t):
        """
        Calculates the epsilon value for a given iteration.

            val (float): Initial epsilon value.
            t (int): Current iteration.
        
        Returns:
            float: Adjusted epsilon value for the current iteration.
        """
        return val / (0.01 * t + 1)

    def run(self):
        """
        Runs the experiment using the epsilon-greedy strategy.
        """
        optimal_index = np.argmax(self.probs)  # Index of the optimal event
        events = [RandomEvent(prob) for prob in self.probs]
        results = np.zeros(self.iterations)

        for t in range(self.iterations):
            epsilon = self.epsilon_func(self.initial_epsilon, t)
            if random.random() < epsilon:
                selected_event = random.choice(range(len(events)))  # Explore
                self.num_explored += 1
            else:
                selected_event = np.argmax([event.estimate for event in events])  # Exploit
                self.num_exploited += 1

            if selected_event == optimal_index:
                self.num_optimal += 1

            result = events[selected_event].pull()
            results[t] = result
            events[selected_event].update(result)

        # Print experiment summary
        print(f"Explorations: {self.num_explored}, Exploitations: {self.num_exploited}, Optimal Selections: {self.num_optimal}")
        print(f"Overall Success Rate: {np.mean(results):.2f}")

        # Plot results
        self.plot_results(events)

    def plot_results(self, events):
        """
        Plots the estimated win rates over iterations for all events.
        
            events (list): A list of RandomEvent objects.
        """
        plt.figure(figsize=(12, 8))
        for i, event in enumerate(events):
            df = pd.DataFrame(event.history, columns=["Iteration", "Estimate"])
            sns.lineplot(x="Iteration", y="Estimate", data=df, label=f"Event {i+1} (Winrate: {event.winrate})")
        
        plt.title("Estimated Win Rates Over Iterations")
        plt.xlabel("Iterations")
        plt.ylabel("Estimated Win Rate")
        plt.legend(loc="best")
        plt.grid(True)
        plt.show()


# Example usage
if __name__ == "__main__":
    # Define a test case
    # probs should be between 0 and 1
    experiment = Experiment(probs=[0.2, 0.5, 0.75], initial_epsilon=0.1, iterations=5000)
    experiment.run()
