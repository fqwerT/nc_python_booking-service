from PIL import Image, ImageDraw
import random
from io import BytesIO
import base64

def random_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


width, height = 300, 300
image = Image.new("RGB", (width, height), (30, 30, 40))
draw = ImageDraw.Draw(image)

def generate_background():
    for y in range(height):
        for x in range(width):
            
            r = random.randint(0, 255)
            g = random.randint(0, 255)
            b = random.randint(0, 255)
            image.putpixel((x, y), (r, g, b))

# ─── Голова ───
def generate_head(center_x, center_y):
    head_radius = random.randint(50, 70)
    draw.ellipse(
        (center_x - head_radius, center_y - head_radius,
         center_x + head_radius, center_y + head_radius),
        fill=random_color(),
        outline=random_color()
    )

    eye_r = head_radius // 8
    draw.ellipse((center_x - head_radius//3 - eye_r, center_y - head_radius//4 - eye_r,
                  center_x - head_radius//3 + eye_r, center_y - head_radius//4 + eye_r),
                 fill=(255,255,255))
    draw.ellipse((center_x + head_radius//3 - eye_r, center_y - head_radius//4 - eye_r,
                  center_x + head_radius//3 + eye_r, center_y - head_radius//4 + eye_r),
                 fill=(255,255,255))


def generate_body(center_x, center_y):
    body_width  = random.randint(50, 90)
    body_length = random.randint(90, 160)
    

    draw.rectangle(
        (center_x - body_width//2, center_y,
         center_x + body_width//2, center_y + body_length),
        fill=random_color()
    )

    arm_width = random.randint(15, 28)
    arm_length = random.randint(50, 110)
    arm_angle_factor = random.uniform(0.6, 1.4)  # немного случайный наклон

    draw.rectangle(
        (center_x - body_width//2 - arm_width,
         center_y + 10,
         center_x - body_width//2,
         center_y + int(arm_length * arm_angle_factor)),
        fill=random_color()
    )

    draw.rectangle(
        (center_x + body_width//2,
         center_y + 10,
         center_x + body_width//2 + arm_width,
         center_y + int(arm_length * arm_angle_factor)),
        fill=random_color()
    )


def generate_legs(center_x, center_y):
    leg_length = random.randint(70, 140)
    leg_width  = random.randint(25, 45)
    

    draw.rectangle(
        (center_x - leg_width//2 - 15, center_y,
         center_x - 15,              center_y + leg_length),
        fill=random_color()
    )

    draw.rectangle(
        (center_x + 15,             center_y,
         center_x + leg_width//2 + 15, center_y + leg_length),
        fill=random_color()
    )


def draw_random_avatar():
    center_x = width // 2 + random.randint(-40, 40)
    head_y   = random.randint(80, 140)
    generate_head(center_x, head_y)
    generate_body(center_x, head_y + 60)
    generate_legs(center_x, head_y + random.randint(110, 180))
    
    buffer = BytesIO()
    image.save(buffer, format='PNG')
    img_str = base64.b64encode(buffer.getvalue()).decode('utf-8')
    return img_str
