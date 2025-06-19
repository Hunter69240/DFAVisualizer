import networkx as nx
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw
import io

def valid_with_steps(transition, inputstring, start, final):
    """Validates the input string and returns the steps taken."""
    steps = [] 
    try:
        current_state = start
        steps.append((current_state, None))  # Start state
        for char in inputstring:
            next_state = transition.get((current_state, char), "$")
            if next_state == "$":
                return 0, steps  # Invalid transition
            steps.append((current_state, char))
            current_state = next_state
        steps.append((current_state, None))  # Final state
        return 1 if current_state == final else 0, steps
    except KeyError:
        return 0, steps

def plot_to_gif(states, alphabets, transition, final, start, steps, output_filename="dfa_animation.gif"):
    """Creates a GIF showing the transitions in the DFA."""
    graph = nx.DiGraph()

    # Add nodes
    for state in states:

        if state==final:
          graph.add_node(state, color="green")

        elif state==start:
          graph.add_node(state, color="green")
        else:
          graph.add_node(state, color="red")

    # Add edges
    for (state, char), next_state in transition.items():
        graph.add_edge(state, next_state, label=char)

    pos = nx.spring_layout(graph)  # Layout for the graph
    node_colors = {state: data["color"] for state, data in graph.nodes(data=True)}
    edge_labels = nx.get_edge_attributes(graph, "label")

    # Generate frames for GIF
    frames = []
    highlight_color = "blue"

    for step in steps:
        current_state, char = step
        fig, ax = plt.subplots()
        colors = [
            highlight_color if state == current_state else node_colors[state]
            for state in graph.nodes
        ]
        nx.draw(
            graph, pos, with_labels=True, node_color=colors, node_size=2000, font_size=10, ax=ax
        )
        nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, ax=ax)
        ax.set_title(f"Processing: {char if char else 'End'} | Current State: {current_state}")

        # Save the current frame as an image
        buf = io.BytesIO()
        plt.savefig(buf, format="png")
        buf.seek(0)
        frames.append(Image.open(buf))
        plt.close(fig)

    # Save frames as a GIF
    frames[0].save(
        output_filename,
        save_all=True,
        append_images=frames[1:],
        optimize=True,
        duration=1000,  # 1 second per frame
        loop=0,
    )
    print(f"Animation saved as {output_filename}")

def main():
    # Input DFA details
    n = int(input("Enter the number of states: "))
    a = int(input("Enter the number of alphabets: "))

    states = [input(f"Enter state {i+1} name: ") for i in range(n)]
    alphabets = [input(f"Enter alphabet {i+1}: ") for i in range(a)]

    print("States:", ", ".join(states))
    print("Alphabets:", ", ".join(alphabets))

    start = input("Enter the start state: ")
    while start not in states:
        start = input("Invalid state! Enter the start state again: ")

    final = input("Enter the final state: ")
    while final not in states:
        final = input("Invalid state! Enter the final state again: ")

    transition = {}
    print("Define transitions (use '$' for no transition):")
    for state in states:
        for char in alphabets:
            next_state = input(f"Transition {state} -> {char}: ")
            while next_state != "$" and next_state not in states:
                print("Invalid state!")
                next_state = input(f"Transition {state} -> {char}: ")
            if next_state != "$":
                transition[(state, char)] = next_state

    while True:
        inputstring = input("Enter a string to check the DFA or '!q' to exit: ")
        if inputstring == "!q":
            break
        is_accepted, steps = valid_with_steps(transition, inputstring, start, final)
        if is_accepted:
            print(f"String '{inputstring}' is accepted.")
        else:
            print(f"String '{inputstring}' is not accepted.")
        print("Creating GIF animation for DFA transitions...")
        plot_to_gif(states, alphabets, transition, final, start, steps)

if __name__ == "__main__":
    main()