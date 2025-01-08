# A/B Testing with Epsilon-Greedy Strategy

This project implements an **A/B testing simulation** using the **epsilon-greedy strategy**. The main goal is to demonstrate how this strategy balances exploration and exploitation when testing multiple options with different probabilities of success (win rates).

---

## Table of Contents
- [Overview](#overview)
- [How It Works](#how-it-works)
- [Key Components](#key-components)
  - [RandomEvent](#randomevent-class)
  - [Experiment](#experiment-class)
- [Usage](#usage)
  - [Example Usage](#example-usage)
  - [Customizing the Experiment](#customizing-the-experiment)

---

## Overview

This project simulates a scenario where multiple "random events" (e.g., variations of a website feature) are tested. Each event has a hidden "win rate" (probability of success), and the experimenter aims to:
1. Identify the event with the highest win rate (exploitation).
2. Gather enough data to ensure confidence in the results (exploration).

The **epsilon-greedy strategy** is employed to balance these two goals by dynamically adjusting how often the experimenter explores new events versus exploiting the best-performing one.

---

## How It Works

1. **Initialization**: Each event has an associated win rate, but this is unknown to the algorithm. Estimates for these win rates are initialized to 0.
2. **Epsilon-Greedy Strategy**:
   - With probability `epsilon`, the algorithm randomly selects an event to explore.
   - Otherwise, it selects the event with the highest estimated win rate to exploit.
   - Over time, `epsilon` decreases, favoring exploitation as more data is gathered.
3. **Updating Estimates**: After each selection, the win rate estimate of the chosen event is updated based on its outcome.
4. **Iteration**: The process repeats for a specified number of iterations, collecting results and refining estimates.

---

## Key Components

### `RandomEvent` Class

This class models an individual event with a specific win rate.

#### Attributes:
- `winrate`: The true probability of success for the event.
- `estimate`: The current estimated win rate based on observed results.
- `N`: The number of times this event has been selected.
- `history`: A list tracking the estimate of the win rate over time.

#### Methods:
- `pull()`: Simulates a success or failure based on the true win rate.
- `update(result)`: Updates the estimated win rate after observing a result.

---

### `Experiment` Class

This class runs the A/B test using the epsilon-greedy strategy.

#### Attributes:
- `probs`: A list of true win rates for each event.
- `initial_epsilon`: The starting exploration rate.
- `iterations`: Total number of iterations for the experiment.
- `num_explored`: Number of exploration steps.
- `num_exploited`: Number of exploitation steps.
- `num_optimal`: Number of times the optimal choice was selected.

#### Methods:
- `epsilon_func(val, t)`: Computes the dynamic epsilon value based on the current iteration.
- `run()`: Runs the experiment, collecting results and updating win rate estimates.
- `plot_results(events)`: Visualizes the estimated win rates over time for all events.

---

### Usage

The experiment can be run with customizable parameters such as the number of events, their true win rates, the initial epsilon value, and the number of iterations.
Example Usage

The following example runs an experiment with 3 events, true win rates of 0.2, 0.5, and 0.75, an initial epsilon of 0.1, and 5000 iterations:

```python
if __name__ == "__main__":
    experiment = Experiment(probs=[0.2, 0.5, 0.75], initial_epsilon=0.1, iterations=5000)
    experiment.run()
```

#### Customizing the Experiment

You can modify the parameters to fit your use case:

- `probs`: Adjust the number of events and their win rates.
- `initial_epsilon`: Set a different starting exploration rate.
- `iterations`: Increase or decrease the number of iterations.