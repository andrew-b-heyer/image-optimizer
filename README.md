# image-optimizer
Simple image optimizer.

- It modified images to be under 1600px x 1600px (recommended wordpress image size)
- Reformats images to webp (considering changing this to jog due to late adoption of many tools like Adobe products *headsmack*, Odoo, and probably others. 
- Will not expand images if they are under 1600 x 1600
- Maintains aspect ratio, in other words the script does not simply resize but shrinks and maintains spect ratio to be under 1600px width or height

# How to use
`cd /inside/directory/of/images/to/optimize`
python3 bulk_convert_jpeg.py /directory/to/output/images/
