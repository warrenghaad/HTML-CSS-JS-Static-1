
# Create a third table showing ubiquity: where each geometric concept appears
# across scales from subatomic to cosmic

ubiquity_scales = []

# Header
ubiquity_scales.append([
    "Scale Level",
    "Circle",
    "Triangle",
    "Square/Cube",
    "Hexagon",
    "Spiral",
    "Cross-Scale Pattern"
])

# Subatomic
ubiquity_scales.append([
    "SUBATOMIC",
    "Electron orbitals (s-orbitals spherical)",
    "Quark arrangements, 3-particle systems",
    "Cubic symmetry in particle physics",
    "6-fold patterns in particle collisions",
    "Spin angular momentum, helicity",
    "Symmetry groups define particle behavior"
])

# Atomic
ubiquity_scales.append([
    "ATOMIC",
    "Atomic cross-sections, probability clouds",
    "3-electron systems, bond angles (107-109°)",
    "4-electron arrangements, d-orbitals",
    "6-membered rings (benzene), graphene",
    "Electron spin, orbital angular momentum",
    "VSEPR theory: electron repulsion creates geometry"
])

# Molecular
ubiquity_scales.append([
    "MOLECULAR",
    "Cyclic molecules, crown ethers",
    "Tetrahedral (CH4), trigonal (NH3, H2O)",
    "Square planar (coordination compounds)",
    "Benzene, cyclohexane, graphene sheets",
    "DNA helix, protein helices, polymer coils",
    "Molecular geometry drives chemical properties"
])

# Crystal/Materials
ubiquity_scales.append([
    "CRYSTAL/MATERIALS",
    "Close-packed spheres, bubble structures",
    "Crystal facets, cleavage planes",
    "Cubic lattices (NaCl, diamond, metals)",
    "Hexagonal close-packed (HCP), graphite layers",
    "Helical crystal structures, spiral dislocations",
    "Crystal systems: 7 basic lattice types with geometric symmetry"
])

# Cellular/Biological
ubiquity_scales.append([
    "CELLULAR/BIOLOGICAL",
    "Cell membranes, vacuoles, nuclei",
    "Pyramidal neurons, triangular microstructures",
    "Epithelial cell packing, cube-like cells",
    "Honeycomb (bees), compound eyes, turtle shells",
    "DNA double helix, cochlea, tendrils",
    "Efficiency drives biological geometry"
])

# Organism
ubiquity_scales.append([
    "ORGANISM",
    "Eyes, fruits, flowers (radial)",
    "Teeth, claws, dorsal fins, beaks",
    "Vertebrate body plans (bilateral + segments)",
    "Turtle shells, pineapple scales, pinecones",
    "Snail shells, nautilus, horns, tails",
    "Fibonacci/golden ratio appears in growth patterns"
])

# Human-Made Objects
ubiquity_scales.append([
    "HUMAN-MADE OBJECTS",
    "Wheels, plates, coins, clocks, buttons",
    "Roofs, tools, wedges, arrows, pyramids",
    "Buildings, rooms, boxes, books, screens",
    "Nuts, bolts, floor tiles, soccer balls",
    "Springs, screws, drill bits, coiled ropes",
    "Humans copy nature and optimize for function"
])

# Architecture/Urban
ubiquity_scales.append([
    "ARCHITECTURE/URBAN",
    "Domes, arches, rotundas, roundabouts",
    "Gables, trusses, pyramids, A-frames",
    "City grids, blocks, plazas, courtyards",
    "Hexagonal pavers, geodesic domes",
    "Spiral staircases, helical ramps, towers",
    "Urban planning balances efficiency and aesthetics"
])

# Planetary/Astronomical
ubiquity_scales.append([
    "PLANETARY/ASTRONOMICAL",
    "Planets, moons, stars, orbits",
    "Lagrange points (3-body triangular positions)",
    "Cube satellites, orthogonal orbit families",
    "Hexagonal storm (Saturn's north pole)",
    "Spiral galaxies, spiral arms, nebulae",
    "Gravity + rotation create large-scale geometry"
])

# Cosmic/Universal
ubiquity_scales.append([
    "COSMIC/UNIVERSAL",
    "Cosmic horizon (spherical), CMB spherical harmonics",
    "Cosmic web triangular voids",
    "Cosmic grid (large-scale structure)",
    "Hexagonal patterns in cosmic simulations",
    "Spiral structure of galaxies, cosmic filaments twist",
    "Universal laws manifest as repeated geometric patterns"
])

# Write to CSV
with open('geometric_ubiquity_across_scales.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerows(ubiquity_scales)

print("Geometric ubiquity across scales table created!")
print(f"Total scale levels documented: {len(ubiquity_scales) - 1}")
print("\nScale levels covered:")
for row in ubiquity_scales[1:]:
    print(f"  • {row[0]}")
