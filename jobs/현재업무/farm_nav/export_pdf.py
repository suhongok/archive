"""FreeCAD script to export farm_nav_whole.FCStd as PDF via SVG"""
import sys
import math

import FreeCAD
import TechDraw
import Part

# Paths
fcstd_path = "/Users/a/Documents/archive/jobs/현재업무/farm_nav/farm_nav_whole.FCStd"
svg_path = "/Users/a/Documents/archive/jobs/현재업무/farm_nav/farm_nav_whole.svg"
template_path = "/Applications/FreeCAD.app/Contents/Resources/share/Mod/TechDraw/Templates/ISO/A3_Landscape_ISO5457_minimal.svg"

print(f"Opening document: {fcstd_path}")
doc = FreeCAD.openDocument(fcstd_path)
FreeCAD.setActiveDocument(doc.Name)

# Find the top-level Assembly object
assembly = None
for obj in doc.Objects:
    if obj.TypeId == "Assembly::AssemblyObject" and obj.Name == "Assembly":
        assembly = obj
        break

if assembly is None:
    print("ERROR: Assembly object not found!")
    sys.exit(1)

print(f"Found assembly: {assembly.Label} ({assembly.Name})")

# Get the assembly's combined shape for bounding box
shapes = []
for obj in doc.Objects:
    if hasattr(obj, "Shape") and obj.Shape and not obj.Shape.isNull():
        if obj.TypeId in ("App::Line", "App::Plane", "App::Point", "App::Origin"):
            continue
        if "Joint" in obj.Name or "Joints" in obj.Name:
            continue
        if obj.TypeId in ("Assembly::JointGroup",):
            continue
        shapes.append(obj.Shape)

if shapes:
    compound = Part.makeCompound(shapes)
    bb = compound.BoundBox
    max_dim = max(bb.XLength, bb.YLength, bb.ZLength)
    print(f"Bounding box: {bb.XLength:.0f} x {bb.YLength:.0f} x {bb.ZLength:.0f} mm")
    print(f"Max dimension: {max_dim:.0f} mm")
else:
    max_dim = 2000

# Create TechDraw page
page = doc.addObject("TechDraw::DrawPage", "Page")
template_obj = doc.addObject("TechDraw::DrawSVGTemplate", "Template")
template_obj.Template = template_path
page.Template = template_obj
print("Created TechDraw page with A3 Landscape template")

# Calculate scale to fit A3 (420x297mm, with margins ~360x250mm usable)
usable_width = 360
usable_height = 250
# For isometric, the projected size is roughly max_dim * sqrt(2/3) ≈ 0.816
projected_size = max_dim * 0.82
scale = min(usable_width / projected_size, usable_height / projected_size)
# Round down to nice scale value
nice_scales = [0.5, 0.2, 0.15, 0.1, 0.075, 0.05, 0.02, 0.01]
chosen_scale = 0.01
for s in nice_scales:
    if s <= scale:
        chosen_scale = s
        break
print(f"Calculated scale: {scale:.4f}, using: 1:{int(1/chosen_scale)}")

# Create isometric view
view = doc.addObject("TechDraw::DrawViewPart", "IsoView")
page.addView(view)
view.Source = [assembly]

# Isometric direction
iso = 1.0 / math.sqrt(3.0)
view.Direction = FreeCAD.Vector(iso, -iso, iso)
view.XDirection = FreeCAD.Vector(-1, -1, 0).normalize()

# Position center of A3 page
view.X = 210
view.Y = 148
view.Scale = chosen_scale
view.ScaleType = 0  # Custom

# Visual settings - use CoarseView for faster rendering of complex assembly
view.CoarseView = True

print("Added isometric view, recomputing (this may take a while)...")
doc.recompute()

# Get the SVG content from the view
print("Generating SVG from view...")
svg_content = TechDraw.viewPartAsSvg(view)

# Read the template SVG and combine
with open(template_path, "r") as f:
    template_svg = f.read()

# Write combined SVG: template background + projected view
# The viewPartAsSvg returns just the projected edges as SVG paths
# We need to embed this into the template

# A3 landscape dimensions in SVG units (mm)
page_w = 420
page_h = 297

# Create a complete SVG with the template and view
combined_svg = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg"
     xmlns:xlink="http://www.w3.org/1999/xlink"
     width="{page_w}mm" height="{page_h}mm"
     viewBox="0 0 {page_w} {page_h}">

  <!-- View content -->
  <g transform="translate({view.X},{page_h - view.Y}) scale(1,-1)">
    {svg_content}
  </g>
</svg>
"""

with open(svg_path, "w") as f:
    f.write(combined_svg)
print(f"SVG exported to: {svg_path}")

FreeCAD.closeDocument(doc.Name)
print("FreeCAD processing done. Convert SVG to PDF with rsvg-convert.")
