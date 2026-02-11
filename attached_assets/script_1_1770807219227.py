
# Create a second table showing how shapes evolve and aggregate
# This demonstrates the three key concepts the user mentioned

evolution_aggregation = []

# Header
evolution_aggregation.append([
    "Base Shape",
    "Aggregation Level 1: Simple Combinations",
    "Aggregation Level 2: Complex Patterns",
    "Aggregation Level 3: Systems",
    "Mathematical Principle",
    "Natural Examples"
])

# Circle aggregations
evolution_aggregation.append([
    "Circle",
    "Vesica Piscis (2 circles), Borromean rings (3 circles), Olympic rings",
    "Flower of Life (19 circles), Seed of Life (7 circles), bubble rafts",
    "Atomic orbitals, planetary systems, cell colonies, foam structures",
    "Pi (π), circumference/diameter ratio, packing efficiency",
    "Bubbles, cells, planets, water droplets, pollen grains"
])

# Triangle aggregations
evolution_aggregation.append([
    "Triangle",
    "Star of David (2 triangles), tetrahedron (4 triangles), diamond shape (2 triangles)",
    "Sierpinski triangle (fractal), hexagonal grid (6 triangles per vertex), geodesic sphere facets",
    "Truss systems, crystal structures, molecular geometry (tetrahedral, octahedral)",
    "Angle sum = 180°, structural rigidity, tessellation capacity",
    "Crystal faces, honeycomb junctions, mountain peaks, pine trees"
])

# Square aggregations
evolution_aggregation.append([
    "Square",
    "Cube (6 squares), checkerboard (2-color), cross/plus (5 squares)",
    "Grid systems, pixel arrays, city blocks, periodic tables",
    "Crystal lattices (cubic), integrated circuits, urban planning grids, agricultural plots",
    "Area = s², 4-fold symmetry, orthogonal axes",
    "Salt crystals, window panes, city layouts, woven fabrics"
])

# Hexagon aggregations
evolution_aggregation.append([
    "Hexagon",
    "Honeycomb cell (shared walls), flower petals (6-fold), benzene ring (chemical)",
    "Honeycomb sheets, graphene (infinite hexagonal lattice), turtle shells",
    "Carbon nanostructures, efficient packing systems, composite materials, hex-grid games",
    "Internal angle = 120°, close-packing, maximum efficiency",
    "Honeycombs, snowflakes, basalt columns, compound eyes, graphene"
])

# Pentagon aggregations
evolution_aggregation.append([
    "Pentagon",
    "Pentagonal star, dodecahedron (12 pentagons), 5-petal flowers",
    "Penrose tilings (aperiodic), quasicrystal structures, radiolarians",
    "Quasi-periodic systems, viral capsids (icosahedral with pentagons), starfish symmetry",
    "Internal angle = 108°, golden ratio connections, does NOT tessellate regularly",
    "Starfish, flowers, viral structures, quasicrystals, pentagonal stones"
])

# Spiral aggregations
evolution_aggregation.append([
    "Spiral",
    "Double helix (2 spirals), triple helix (collagen), nested spirals",
    "Fibonacci spirals in phyllotaxis, spiral galaxies, hurricane systems",
    "DNA structure, protein folding, vortex dynamics, spiral galaxies",
    "Fibonacci sequence, golden angle (137.5°), logarithmic growth",
    "Nautilus shells, galaxies, hurricanes, sunflower seeds, DNA, fern fronds"
])

# Star aggregations
evolution_aggregation.append([
    "Star (multi-point)",
    "Star of Ishtar (8-point), compass rose (4/8/16-point), snowflake arms (6-fold)",
    "Islamic geometric patterns, quasicrystal tilings, radial mandalas",
    "Navigation systems, radial city designs, crystal symmetry groups",
    "Rotational symmetry, angle division (360°/n), overlapping polygons",
    "Snowflakes, starfish, asterisk crystals, flower blooms, sea urchins"
])

# Mixed shape aggregations
evolution_aggregation.append([
    "Mixed: Octagons + Squares",
    "One octagon surrounded by 4 squares (semi-regular tessellation 4.8.8)",
    "Truncated square tiling, bathroom floor patterns, Islamic geometric art",
    "Architectural tiling systems, decorative mosaics, game board designs",
    "Vertex configuration: 4.8.8 (angles sum to 360°), semi-regular tessellation",
    "Floor tiles, Islamic art, game boards (like chess variants)"
])

# Write to CSV
with open('shape_evolution_aggregation.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerows(evolution_aggregation)

print("Shape evolution and aggregation table created!")
print(f"Total patterns documented: {len(evolution_aggregation) - 1}")
