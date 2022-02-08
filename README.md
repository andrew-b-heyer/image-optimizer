# image-optimizer
A simple image optimizer.

- It modifies images to be under 1600px x 1600px (recommended wordpress image size)
- Reformats images to webp (considering changing this to jog due to late adoption of many tools like Adobe products *headsmack*, Odoo, and probably others. 
- Will not expand images if they are under 1600 x 1600
- Maintains aspect ratio, in other words the script does not simply resize but shrinks and maintains spect ratio to be under 1600px width or height

# How to use
1. `brew install pillow`
1. `pip install -r requirements.txt`
2. `cd /inside/directory/of/images/to/optimize`
3. `python3 /path/to/bulk_convert_jpeg.py /directory/to/output/images/`
