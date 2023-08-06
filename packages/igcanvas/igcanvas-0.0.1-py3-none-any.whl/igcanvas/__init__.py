
def genImage(
    src: str, 
    size=(800, 800),
    fillSize=.7,
    color='white',
    shadow=True,
    shadow_color='gray',
    shadow_offset=[5, 10],
    shadow_blur=3
    ):
  from PIL import Image, ImageDraw, ImageFilter
  with Image.open(src, 'r') as img:
    bg = Image.new('RGB', size, color)
    max_size = [int(i * fillSize) for i in bg.size]
    scale = max([x//y for x, y in zip(img.size, max_size)])
    canvas = img.resize([i // scale for i in img.size])
    position = [(a - b)//2 for a, b in zip(bg.size, canvas.size)]
    if(shadow):
      draw = ImageDraw.Draw(bg)
      offset = shadow_offset * 2
      shadow_pos = [*position, *[i + j for i, j in zip(position, canvas.size)]]
      shadow_pos = [a + b for a, b in zip(offset, shadow_pos)]
      draw.rectangle(shadow_pos, shadow_color)
      bg = bg.filter(ImageFilter.GaussianBlur(shadow_blur))
    bg.paste(canvas, position)
    return bg
