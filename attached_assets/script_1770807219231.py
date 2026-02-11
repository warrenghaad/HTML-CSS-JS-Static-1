
# Create a comprehensive framework showing connections between geometric elements
# across atomic, molecular, and cultural/universal scales

import csv

# Create a master table showing geometric throughlines
geometric_throughlines = []

# Header
geometric_throughlines.append([
    "Geometric Element",
    "Atomic/Molecular Level",
    "Mathematical Properties",
    "Evolution Path",
    "Pattern Aggregation",
    "Cultural/Universal Applications",
    "STEM Connections"
])

# Circle
geometric_throughlines.append([
    "CIRCLE",
    "Electron orbitals (s-orbitals have spherical symmetry); circular cross-sections in molecules",
    "Center, radius, diameter, circumference; π ratio; rotational symmetry (infinite fold); equal distance from center",
    "Circle → Wheel → Pulley → Gear → Turbine → Rotational engines",
    "Circles aggregate into: Flower of Life pattern, vesica piscis, concentric systems, circular tessellations (limited - only with other shapes)",
    "Sun disks, halos, mandalas, clocks, planetary orbits, wells, roundabouts",
    "Physics: rotational dynamics, angular momentum; Engineering: wheels, turbines, centrifuges"
])

# Triangle
geometric_throughlines.append([
    "TRIANGLE",
    "Tetrahedral molecular geometry (CH4, NH3); triangular arrangements of atoms; 3-fold coordination",
    "3 sides, 3 vertices; angles sum to 180°; structural stability (rigid); can be equilateral, isosceles, scalene",
    "Triangle → Pyramids → Trusses → Geodesic domes → Structural frameworks",
    "Triangles aggregate into: hexagons (6 triangles), tetrahedrons (4 triangles), octahedrons (8 triangles), infinite triangular tessellations",
    "Pyramids, arrowheads, mountain symbolism, trinity symbols, architectural supports",
    "Engineering: trusses, load distribution; Architecture: stable structures; Chemistry: tetrahedral bonds"
])

# Square
geometric_throughlines.append([
    "SQUARE",
    "Cubic crystal lattices (NaCl, diamond); square planar molecular geometry; 4-fold coordination",
    "4 equal sides, 4 right angles; 4-fold rotational symmetry; area = s²; perpendicular diagonals",
    "Square → Grid systems → City planning → Circuit boards → Pixel arrays",
    "Squares aggregate into: cubic lattices, checkerboard patterns, infinite square tessellations, octahedrons (square + triangles)",
    "City grids, agricultural plots, buildings, windows, tiles, compass directions",
    "Urban planning: grid systems; Computing: pixel matrices; Crystallography: cubic structures"
])

# Hexagon
geometric_throughlines.append([
    "HEXAGON",
    "Benzene rings (C6H6); graphene lattice structure; close-packed crystal structures; 6-fold symmetry",
    "6 equal sides (regular); internal angles 120°; tessellates perfectly; maximum area-to-perimeter ratio",
    "Hexagon → Honeycomb → Efficient packing → Composite materials → Hex-grid maps",
    "Hexagons aggregate into: honeycomb tessellations, flower patterns, graphene sheets, columnar basalt",
    "Honeycombs, turtle shells, basalt columns, nuts/bolts, snowflakes, cell structures",
    "Materials science: honeycomb structures for strength; Biology: efficient cellular packing; Chemistry: benzene, graphene"
])

# Spiral
geometric_throughlines.append([
    "SPIRAL",
    "DNA double helix; protein alpha-helix; spiral arrangements in crystal growth; helical symmetry",
    "Logarithmic (constant angle) or Archimedean (constant spacing); self-similar; growth pattern; Fibonacci/golden ratio",
    "Spiral → Screw threads → Springs → Helical gears → DNA sequencing tools",
    "Spirals aggregate into: double helices, coiled structures, nested spirals, spiral galaxies, vortex patterns",
    "Galaxies, nautilus shells, hurricanes, snail shells, fern fronds, spiral staircases, watch springs",
    "Biology: DNA, proteins; Physics: angular momentum, vortices; Engineering: springs, screws, helical antennas"
])

# Star (multi-pointed)
geometric_throughlines.append([
    "STAR (8-point)",
    "Octahedral coordination in crystals; radial symmetry; 8-fold rotational patterns in quasicrystals",
    "Multiple axes of symmetry; combines squares rotated 45°; angle divisions (360°/8 = 45°)",
    "Star → Navigation rose → Radial designs → Star networks → Hub-spoke systems",
    "Stars aggregate into: rosette patterns, star tessellations with polygons, radial mandalas, quasicrystal patterns",
    "Ishtar star, compass roses, snowflakes, starfish, navigation symbols, city gates, Islamic tile work",
    "Navigation: orientation systems; Network theory: hub-spoke topology; Crystallography: quasicrystals"
])

# Crescent
geometric_throughlines.append([
    "CRESCENT",
    "Curved molecular structures; phases of circular cross-sections; arc segments in atomic arrangements",
    "Arc of circle minus smaller arc; curved edges; cyclic patterns; phase representation",
    "Crescent → Sickle blade → Curved tools → Lunar calendar → Arc architecture",
    "Crescents aggregate into: lunar phase sequences, curved arch systems, wave patterns, cyclical diagrams",
    "Moon phases, sickles, arches, horns, Islamic symbols, crescent wrenches, curved blades",
    "Agriculture: sickle design; Architecture: arches, vaults; Astronomy: lunar cycles, orbital phases"
])

# Line/Edge
geometric_throughlines.append([
    "LINE/EDGE",
    "Chemical bonds (molecular edges); crystal axes; linear molecular geometry (CO2, BeH2)",
    "Shortest distance between points; 1-dimensional; directionality; can be straight or curved",
    "Line → Edge tools → Rulers → Rails → Fiber optics → Linear accelerators",
    "Lines aggregate into: grids, meshes, parallel systems, woven fabrics, crystalline edges, geodesic networks",
    "Boundaries, roads, rivers, edges of objects, timelines, musical staves, writing lines",
    "Physics: vectors, force lines; Engineering: beams, cables; Mathematics: coordinate axes, graphs"
])

# Write to CSV
with open('geometric_throughlines.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerows(geometric_throughlines)

print("Geometric throughlines table created successfully!")
print(f"Total geometric elements documented: {len(geometric_throughlines) - 1}")
print("\nGeometric elements covered:")
for row in geometric_throughlines[1:]:
    print(f"  • {row[0]}")
