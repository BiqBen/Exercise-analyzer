from app.pose.angle_calculator import calculate_angle


angle = calculate_angle(
    (0, 1),
    (0, 0),
    (1, 0)
)

print(f"Winkel: {angle:.2f}°")