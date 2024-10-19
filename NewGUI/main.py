import matplotlib.pyplot as plt
import numpy as np

# Generate sample data
x = np.linspace(0, 10, 100)
y = np.sin(x)

# Create a figure and axis
fig, ax = plt.subplots()

# Set initial axis limits to prevent negative values and stop at (0, 0)
ax.set_xlim(0, None)
ax.set_ylim(0, None)

# Plot the data
ax.plot(x, y)

# Disable automatic scaling to maintain fixed limits
ax.set_autoscale_on(False)

# Add a title and labels
ax.set_title("Example Plot")
ax.set_xlabel("X-axis")
ax.set_ylabel("Y-axis")

# Connect to the pan button event and prevent panning into negative regions
def on_pan(event):
    if event.button == 1:  # Left mouse button
        # Get current axis limits
        x_min, x_max = ax.get_xlim()
        y_min, y_max = ax.get_ylim()

        # Prevent panning into negative regions
        x_min = max(x_min, 0)
        y_min = max(y_min, 0)

        # Set the new limits
        ax.set_xlim(x_min, x_max)
        ax.set_ylim(y_min, y_max)
        plt.draw()

cid = fig.canvas.mpl_connect('button_press_event', on_pan)

# Show the plot
plt.show()