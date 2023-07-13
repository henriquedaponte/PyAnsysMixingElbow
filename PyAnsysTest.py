# Importing the PyFluent libraries required
import ansys.fluent.core as pyfluent
from ansys.fluent.core import examples
from ansys.fluent.visualization.pyvista import Graphics


# Downloading the mixing elbow sample .cas file from the repository
import_filename = examples.download_file('mixing_elbow.cas.h5', 'pyfluent/mixing_elbow')

# Starting the fluent session with a visible GUI
solver = pyfluent.launch_fluent(precision='double', processor_count=2, show_gui=True, mode='solver')


# Importing the mixing elbow sample .cas file
solver.file.read(file_type='case', file_name=import_filename)

# Configuring the turbulence model
solver.setup.models.viscous = {'model' : 'k-epsilon'}
solver.setup.models.viscous.near_wall_treatment.wall_function = 'standard-wall-fn'


# Initializing the Solution
solver.solution.initialization.hybrid_initialize()

# Running the Solver
solver.solution.run_calculation.iterate(iter_count=100)

# Loading the graphics from the session
graphics = Graphics(session=solver)

# Creating a contour of Temperature on the simmetry plane
temperature_contour = graphics.Contours['contour-temperature']
temperature_contour.field = 'temperature'
temperature_contour.surfaces_list = ['symmetry-xyplane']
temperature_contour.display()

# Creating a vector plot of velocity on the symmetry plane
vector = graphics.Vectors['velocity']
vector.surfaces_list = ['symmetry-xyplane']
vector.scale = 3
vector.display()

# Add an input prompt to keep the Python interpreter running
input("Press enter to exit...")