bl_info = {
    "name": "New Deformed Pipe Mesh",
    "author": "Rasim Labibov",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Add > Mesh > New Deformed Pipe Mesh",
    "description": "Adds a new Deformed Pipe Mesh",
    "warning": "",
    "doc_url": "",
    "category": "Add Mesh",
}


import bpy
from bpy.types import Operator
from bpy.props import FloatVectorProperty, FloatProperty, IntProperty
from bpy_extras.object_utils import AddObjectHelper, object_data_add
from mathutils import Vector
from math import sqrt, tau, pi, sin, cos


def add_object(self, context):
    # Generate vertices
    verts = []

    da = tau / self.sectors
    dy = self.length / self.chunks
    
    Y_POINTS = self.chunks+1

    for i in range(self.sectors+1):
        angle = i * da
        for j in range(Y_POINTS):
            y = -self.length / 2 + j * dy

            t = angle * self.radius

            a = cos(pi * y / self.length)
            b = cos(self.form * (t + pi/4 * y) / self.radius)
            w = self.deformation * a * b

            x = cos(angle) * (self.radius + w)
            z = sin(angle) * (self.radius + w)

            verts.append(Vector( (x * self.scale.x, y * self.scale.y, z * self.scale.z) ))

    # Mesh data
    edges = []
    faces = []


    #
    # Start mesh generation
    #

    for i in range(self.sectors):
        k = i * Y_POINTS  # Row start index
        for j in range(self.chunks):
            faces.append([k + j, k + j+1, k + j+Y_POINTS+1, k + j+Y_POINTS])


    #
    # Finish mesh generation
    #

    mesh = bpy.data.meshes.new(name="New Deformed Pipe")
    mesh.from_pydata(verts, edges, faces)
    # useful for development when the mesh may be invalid.
    # mesh.validate(verbose=True)
    object_data_add(context, mesh, operator=self)


class OBJECT_OT_add_object(Operator, AddObjectHelper):
    """Create a new Deformed Pipe Mesh"""
    bl_idname = "mesh.add_deformed_pipe"
    bl_label = "Add Deformed Pipe Mesh"
    bl_options = {'REGISTER', 'UNDO'}

    scale: FloatVectorProperty(
        name="scale",
        default=(1.0, 1.0, 1.0),
        subtype='TRANSLATION',
        description="scaling",
    )

    length: FloatProperty(
        name="length",
        default=2.0,
        subtype='DISTANCE',
        description="length of a deformed pipe"
    )

    radius: FloatProperty(
        name="radius",
        default=0.5,
        min=0.1,
        subtype='DISTANCE',
        description="radius of a deformed pipe"
    )

    deformation: FloatProperty(
        name="deformation",
        default=0.05,
        min=0,
        subtype='DISTANCE',
        description="deformation of a deformed pipe"
    )

    form: IntProperty(
        name="form",
        default=5,
        min=0,
        max=20,
        subtype='DISTANCE',
        description="form of a deformed pipe"
    )

    sectors: IntProperty(
        name="sectors",
        default=40,
        min=1,
        max=100,
        description="sectors of a deformed pipe"
    )

    chunks: IntProperty(
        name="chunks",
        default=40,
        min=1,
        max=100,
        description="chunks of a deformed pipe"
    )

    def execute(self, context):

        add_object(self, context)

        return {'FINISHED'}


# Registration

def add_object_button(self, context):
    self.layout.operator(
        OBJECT_OT_add_object.bl_idname,
        text="Add Deformed Pipe Mesh",
        icon='PLUGIN')


# This allows you to right click on a button and link to documentation
def add_object_manual_map():
    url_manual_prefix = "https://docs.blender.org/manual/en/latest/"
    url_manual_mapping = (
        ("bpy.ops.mesh.add_object", "scene_layout/object/types.html"),
    )
    return url_manual_prefix, url_manual_mapping


def register():
    bpy.utils.register_class(OBJECT_OT_add_object)
    bpy.utils.register_manual_map(add_object_manual_map)
    bpy.types.VIEW3D_MT_mesh_add.append(add_object_button)


def unregister():
    bpy.utils.unregister_class(OBJECT_OT_add_object)
    bpy.utils.unregister_manual_map(add_object_manual_map)
    bpy.types.VIEW3D_MT_mesh_add.remove(add_object_button)


if __name__ == "__main__":
    register()
