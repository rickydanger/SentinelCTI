import plotly.graph_objects as go

# ============================================
# EDIT THIS DATA with your real day
# ============================================
labels = [
    "Start of Focused Work",      # 0
    "Deep Work (Coding)",         # 1
    "Debugging & Troubleshooting",# 2
    "Research & Learning",        # 3
    "Testing & Validation",       # 4
    "Documentation & Reporting",  # 5
    "Meetings & Syncs",           # 6
    "Breaks & Admin",             # 7
    "End of Python Day"           # 8
]

# Define flows: (source_index, target_index, hours)
links = [
    # Morning flow
    (0, 1, 3.5),   # Start → Deep Work (Coding)
    (0, 3, 1.0),   # Start → Research & Learning
    (0, 6, 0.5),   # Start → Meetings
    
    # During the day
    (1, 2, 2.0),   # Coding → Debugging
    (1, 4, 1.0),   # Coding → Testing
    (3, 1, 1.5),   # Research → Coding
    (3, 5, 0.75),  # Research → Documentation
    
    # Afternoon / later
    (2, 4, 1.25),  # Debugging → Testing
    (2, 5, 0.5),   # Debugging → Documentation
    (4, 5, 0.75),  # Testing → Documentation
    
    # Collaboration & breaks
    (6, 7, 1.0),   # Meetings → Breaks/Admin
    (7, 8, 2.0),   # Breaks/Admin → End
    (5, 8, 1.5),   # Documentation → End
    (1, 8, 1.0),   # Remaining deep work → End
]

# Build the chart
fig = go.Figure(data=[go.Sankey(
    node = dict(
        pad = 20,
        thickness = 25,
        line = dict(color = "black", width = 0.5),
        label = labels,
        color = ["#2E86AB", "#A23B72", "#F18F01", "#C73E1D", 
                 "#3A7D44", "#6B4C9A", "#E63946", "#457B9D", "#1D3557"]
    ),
    link = dict(
        source = [link[0] for link in links],
        target = [link[1] for link in links],
        value  = [link[2] for link in links],
        hovertemplate = '%{source.label} → %{target.label}<br>Hours: %{value}<extra></extra>'
    )
)])

fig.update_layout(
    title_text = "Garrick's Python Development Day - Time Flow",
    font_size = 14,
    height = 700,
    paper_bgcolor = "#1e1e2e",   # Dark theme (optional)
    font = dict(color = "white")
)

fig.show()