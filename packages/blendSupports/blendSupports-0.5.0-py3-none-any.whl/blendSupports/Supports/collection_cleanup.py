import bpy


def collection_cleanup(collection_name):
    """
    Cleanup a collection of objects no longer required

    Source: https://blender.stackexchange.com/questions/153713/removing-all-meshes-from-a-collection-with-python

    :param collection_name: Name of the collection iterate through
    :return: Nothing, delete the objects requested then stop
    """
    # Cleanup the collection
    collection = bpy.data.collections[collection_name]

    meshes = set()
    for obj in collection.objects:
        meshes.add(obj.data)
        if obj.name != "Camera":
            bpy.data.objects.remove(obj)

    # Look at meshes that are orphean after objects removal
    for mesh in [m for m in meshes if m.users == 0]:
        # Delete the meshes
        bpy.data.meshes.remove(mesh)