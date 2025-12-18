# ------------------------- IMPORT LIBRARIES -------------------------
import tkinter as tk                 # Tkinter for GUI
from tkinter import messagebox       # For pop-up messages (errors, warnings)

# ------------------------- MAIN WINDOW SETUP -------------------------
root = tk.Tk()                      # Create the main application window
root.title("Animated BMI Dashboard") # Set the window title
root.geometry("950x400")             # Set window size (width x height)
root.configure(bg="#FFD8E8")         # Set soft pink background color

# ------------------------- DATA STORAGE -----------------------------
# This list stores all BMI values entered by the user
# We will use it to show the history graph
bmi_history = []

# ------------------------- FRAMES FOR LAYOUT ------------------------
# Left frame: For inputs, buttons, BMI text & emoji
left_frame = tk.Frame(root, bg="#FFD8E8")
left_frame.pack(side="left", fill="both", expand=True, padx=20, pady=20)

# Right frame: For BMI history graph and vertical meter
right_frame = tk.Frame(root, bg="#FFFFFF", bd=2, relief="ridge")
right_frame.pack(side="right", fill="y", padx=10, pady=20)

# Canvas to draw the history graph
graph_canvas = tk.Canvas(right_frame, width=300, height=300, bg="white")
graph_canvas.pack()

# Canvas to draw the vertical BMI meter
meter_canvas = tk.Canvas(right_frame, width=60, height=300, bg="white")
meter_canvas.pack(side="right", padx=5)

# ------------------------- BACKGROUND ANIMATION ---------------------
# List of background colors to cycle through for a dynamic effect
bg_colors = ["#FFD8E8", "#FFEED4", "#E8FFD8", "#D8F1FF", "#F0D8FF"]
bg_index = 0  # Start with the first color

# Function to animate background color every 800ms
def animate_bg():
    global bg_index
    # Change background color of window and left frame
    root.configure(bg=bg_colors[bg_index])
    left_frame.configure(bg=bg_colors[bg_index])
    # Move to the next color (loop back after last color)
    bg_index = (bg_index + 1) % len(bg_colors)
    # Call this function again after 800 milliseconds
    root.after(800, animate_bg)

animate_bg()  # Start the background animation

# ------------------------- INPUT LABELS & ENTRIES -------------------
title_label = tk.Label(left_frame, text="BMI CALCULATOR", 
                       font=("Arial Rounded MT Bold", 22), bg="#FFD8E8")
title_label.pack(pady=10)

# Weight input field
weight_entry = tk.Entry(left_frame, font=("Arial", 14), width=15, justify="center")
weight_entry.insert(0, "Enter weight (kg)")  # Placeholder text
weight_entry.pack(pady=5)

# Height input field
height_entry = tk.Entry(left_frame, font=("Arial", 14), width=15, justify="center")
height_entry.insert(0, "Enter height (cm)")  # Placeholder text
height_entry.pack(pady=5)

# Functions to remove placeholder text when user clicks on the entry
def clear_weight_placeholder(event):
    if weight_entry.get() == "Enter weight (kg)":
        weight_entry.delete(0, tk.END)

def clear_height_placeholder(event):
    if height_entry.get() == "Enter height (cm)":
        height_entry.delete(0, tk.END)

# Bind the placeholder-clearing functions to focus events
weight_entry.bind("<FocusIn>", clear_weight_placeholder)
height_entry.bind("<FocusIn>", clear_height_placeholder)

# Label to display BMI result text
result_label = tk.Label(left_frame, text="", font=("Arial", 16, "bold"), bg="#FFD8E8")
result_label.pack(pady=5)

# Label to display an emoji based on BMI category
emoji_label = tk.Label(left_frame, text="", font=("Arial", 40), bg="#FFD8E8")
emoji_label.pack(pady=0)

# ------------------------- ANIMATED BMI BAR --------------------------
# Canvas to draw the horizontal animated BMI bar
bar_canvas = tk.Canvas(left_frame, width=300, height=30, bg="#FFFFFF", highlightthickness=0)
bar_canvas.pack(pady=10)
# Rectangle representing the bar (starts at 0 width)
bar_fill = bar_canvas.create_rectangle(0, 0, 0, 30, fill="#6A5ACD")

# Function to animate the emoji with a bounce effect
def animate_emoji():
    def bounce(up=True, count=0):
        if count > 6:   # Stop after 6 bounces
            return
        dy = -6 if up else 6  # Move up or down
        emoji_label.place_configure(y=emoji_label.winfo_y() + dy)
        root.after(80, lambda: bounce(not up, count + 1))  # Repeat with opposite direction
    bounce()  # Start bouncing

# Function to animate the BMI bar growing
def animate_bar(target_width):
    bar_canvas.coords(bar_fill, (0, 0, 0, 30))  # Reset bar width to 0
    def grow(current=0):
        if current >= target_width:
            return
        # Increase width gradually
        bar_canvas.coords(bar_fill, (0, 0, current, 30))
        bar_canvas.after(7, lambda: grow(current + 5))  # Repeat after 7ms
    grow()  # Start animation

# ------------------------- HISTORY GRAPH -----------------------------
# Function to determine color based on BMI category
def get_bmi_color(bmi):
    if bmi < 18.5:
        return "#1E90FF"  # Blue → Underweight
    elif bmi < 24.9:
        return "#32CD32"  # Green → Normal
    elif bmi < 29.9:
        return "#FFA500"  # Orange → Overweight
    else:
        return "#FF4500"  # Red → Obese

# Function to draw BMI history graph
def draw_history_graph():
    graph_canvas.delete("all")  # Clear previous graph
    if len(bmi_history) < 1:
        return  # Nothing to draw yet
    
    width = 300
    height = 300
    padding = 50  # Space for axes and labels

    # Draw X-axis and Y-axis
    graph_canvas.create_line(padding, height-padding, width-padding, height-padding, width=2)
    graph_canvas.create_line(padding, padding, padding, height-padding, width=2)

    # Draw Y-axis labels (BMI values)
    for val in range(0, 51, 10):
        y = height - padding - ((val/50)*(height - 2*padding))
        graph_canvas.create_line(padding-5, y, padding, y)
        graph_canvas.create_text(padding-15, y, text=str(val), anchor="e", font=("Arial",9))

    # Y-axis title
    graph_canvas.create_text(15, height/2, text="BMI Value", angle=90, font=("Arial",10,"bold"))

    # Draw X-axis labels (entry numbers)
    if len(bmi_history) > 1:
        for i in range(len(bmi_history)):
            x = padding + (i/(len(bmi_history)-1))*(width - 2*padding)
            graph_canvas.create_line(x, height-padding, x, height-padding+5)
            graph_canvas.create_text(x, height-padding+15, text=str(i+1), anchor="n", font=("Arial",9))
    elif len(bmi_history) == 1:
        graph_canvas.create_text(width/2, height-padding+15, text="1", anchor="n", font=("Arial",9))

    # X-axis title
    graph_canvas.create_text(width/2, height-15, text="Entry Number", font=("Arial",10,"bold"))

    # Prepare points and colors for the line graph
    max_bmi = max(bmi_history)
    min_bmi = min(bmi_history)
    span = max_bmi - min_bmi if max_bmi != min_bmi else 1

    points = []  # Store (x,y) coordinates
    colors = []  # Store color for each point
    for i, val in enumerate(bmi_history):
        x = padding + (i/(len(bmi_history)-1))*(width - 2*padding) if len(bmi_history)>1 else width/2
        y = height - padding - ((val - min_bmi)/span)*(height-2*padding)
        points.append((x,y))
        colors.append(get_bmi_color(val))

    # Animate line connecting points
    speed = 8
    index = 0
    current = list(points[0])
    def animate_line():
        nonlocal index, current
        if index >= len(points)-1:
            # Draw dots at each point after animation
            for (x,y), color in zip(points, colors):
                r = 4
                graph_canvas.create_oval(x-r, y-r, x+r, y+r, fill=color, outline="")
            return
        tx, ty = points[index+1]
        dx = tx-current[0]
        dy = ty-current[1]
        dist = (dx*dx+dy*dy)**0.5
        color = colors[index]
        if dist<=speed:
            graph_canvas.create_line(points[index][0], points[index][1], tx, ty, fill=color, width=3)
            current = [tx, ty]
            index+=1
        else:
            step_x = current[0] + (dx/dist)*speed
            step_y = current[1] + (dy/dist)*speed
            graph_canvas.create_line(current[0], current[1], step_x, step_y, fill=color, width=3)
            current = [step_x, step_y]
        graph_canvas.after(10, animate_line)
    animate_line()

# ------------------------- BMI METER -------------------------------
def draw_bmi_meter(bmi):
    meter_canvas.delete("all")  # Clear previous meter
    # Define BMI categories and colors
    categories = [
        (0,18.5,"#3498db"),    # Underweight
        (18.5,24.9,"#2ecc71"), # Normal
        (25,29.9,"#f1c40f"),   # Overweight
        (30,50,"#e74c3c")      # Obese
    ]
    height = 300
    for start,end,color in categories:
        y1 = height - ((start/50)*height)
        y2 = height - ((end/50)*height)
        meter_canvas.create_rectangle(0,y2,60,y1,fill=color, outline="")
        meter_canvas.create_text(65, (y1+y2)/2, text=f"{round(end,1)}", anchor="w", font=("Arial",8))
    # Draw black triangle showing current BMI
    y = height - ((bmi/50)*height)
    meter_canvas.create_polygon(0,y-5,60,y-5,30,y+10, fill="black")

# ------------------------- CALCULATE BMI ----------------------------
def calculate_bmi():
    try:
        # Get user input
        weight = float(weight_entry.get())
        height_cm = float(height_entry.get())
        if height_cm <= 0:
            messagebox.showerror("Error","Height must be >0")
            return
        height_m = height_cm / 100  # Convert to meters
        bmi = round(weight / (height_m**2), 2)  # BMI formula
        bmi_history.append(bmi)  # Add to history

        # Determine BMI category and emoji
        if bmi < 18.5:
            text = f"Underweight ({bmi})"; color="#1E90FF"; emoji="😐"
        elif bmi < 24.9:
            text = f"Normal ({bmi})"; color="#32CD32"; emoji="😄"
        elif bmi < 29.9:
            text = f"Overweight ({bmi})"; color="#FFA500"; emoji="😯"
        else:
            text = f"Obese ({bmi})"; color="#FF4500"; emoji="😟"

        # Update UI
        result_label.config(text=text, fg=color)
        emoji_label.config(text=emoji)

        # Animate elements
        animate_emoji()
        animate_bar(min(int(bmi*12),300))  # Limit max width to 300
        draw_history_graph()
        draw_bmi_meter(bmi)

    except:
        messagebox.showerror("Error","Enter valid numbers!")

# ------------------------- CLEAR HISTORY ---------------------------
def clear_history():
    if messagebox.askyesno("Clear History","Delete all BMI history?"):
        bmi_history.clear()  # Remove all stored BMI
        graph_canvas.delete("all")  # Clear graph
        graph_canvas.create_text(150,150,text="History Cleared",fill="gray", font=("Arial",14))

# Button to clear history
clear_btn = tk.Button(left_frame,text="CLEAR HISTORY", font=("Arial",12,"bold"),
                      command=clear_history,bg="#444",fg="white", padx=15,pady=5)
clear_btn.pack(pady=5)

# ------------------------- CALCULATE BUTTON ------------------------
calc_btn = tk.Button(left_frame,text="CALCULATE", font=("Arial",14,"bold"),
                     command=calculate_bmi,bg="#FF69B4",fg="white",
                     activebackground="#FF1493", padx=20,pady=5)
calc_btn.pack(pady=10)  # Visible from the start

# ------------------------- ENTER KEY SUBMIT ------------------------
root.bind("<Return>", lambda event: calculate_bmi())  # Press Enter to calculate

# ------------------------- RUN THE APP -----------------------------
root.mainloop()  # Start the GUI loop


