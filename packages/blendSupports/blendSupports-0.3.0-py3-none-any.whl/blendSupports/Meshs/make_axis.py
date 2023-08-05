from blendSupports.Nodes.emission_node import create_emission_node
import bpy


def make_axis(colour, height_end, x_min, x_max, x_axis_offset, width=0.01):
    """
    Creates the horizontal and vertical axis for tables


    :param colour: Axis colour

    :param height_end: The end value of the height iterator
    :type height_end: float

    :param x_min: Min value of x
    :type x_min: float

    :param x_max: Max value of x
    :type x_max: float

    :param x_axis_offset: Vertical x axis offset
    :type x_axis_offset: float

    :param width: Width of the axis
    :type width: float

    :return: Nothing
    :rtype: None
    """
    # Make the block
    mesh = bpy.data.meshes.new("axis")  # add the new mesh
    obj = bpy.data.objects.new(mesh.name, mesh)
    create_emission_node(obj, colour)
    col = bpy.data.collections.get("Collection")
    col.objects.link(obj)
    bpy.context.view_layer.objects.active = obj

    # 4 verts made with XYZ coords
    verts = [
        # Vertical axis
        (width / 2 + x_axis_offset, 0, -width),
        (width / 2 + x_axis_offset, height_end, -width),
        (-width / 2 + x_axis_offset, height_end, -width),
        (-width / 2 + x_axis_offset, 0, -width),

        # Horizontal axis
        (x_max, height_end, -width),
        (x_max, height_end - width, -width),
        (x_min, height_end - width, -width),
        (x_min, height_end, -width)
    ]
    edges = []
    faces = [[0, 1, 2, 3], [4, 5, 6, 7]]
    mesh.from_pydata(verts, edges, faces)
    bpy.ops.object.select_all(action='DESELECT')