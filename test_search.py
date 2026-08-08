from src.agents.image_analyzer import check_image

# with a public URL (same as notebook 1)
print(check_image("https://images.unsplash.com/photo-1682351888673-9f898b62a1c9?q=80&w=1171&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"))

# with no image at all
print(check_image(None))