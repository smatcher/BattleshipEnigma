import os.path
import subprocess
import sys
import importlib

# High level script configuration
objs_to_export = {
	'Base':         'Models/base.obj',
	'Carrier':      'Models/carrier.obj',
	'DamageMarker': 'Models/damage_marker.obj',
	'BlueDial':     'Models/blue_dial.obj',
	'RedDial':      'Models/red_dial.obj',
	'BlueRadio':    'Models/blue_radio.obj',
	'RedRadio':     'Models/red_radio.obj',
	'RedPeg':       'Models/red_peg.obj',
	'WhitePeg':     'Models/white_peg.obj'
}

blend_file_path = 'Raw/raw.blend'

# Low level script configuration
blender_path = 'C:\\Program Files\\Blender Foundation\\Blender\\blender.exe'
script_path = os.path.realpath(__file__)
repo_path = os.path.join(os.path.dirname(__file__), '..')
blend_absolute_file_path = os.path.join(repo_path, blend_file_path)

def wait_enter(msg):
	print(msg)
	print('Press Enter to continue')
	input() # Wait for input so the user sees the msg

def run_blender():
	if os.path.isfile(blender_path):
		subprocess.run([blender_path, blend_absolute_file_path, '--background', '--python', script_path])	
	else:
		wait_enter('Error: blender not found at {}'.format(blender_path))

def export():
	import bpy
	has_warning = False

	for obj in bpy.context.scene.objects:
		if not obj.name in objs_to_export:
			print('Did not export {}, object not listed'.format(obj.name))
			has_warning = True
			continue
		output_file = objs_to_export[obj.name]
		print('Found {0} : expoting to {1}'.format(obj.name, output_file))
		bpy.ops.object.select_all(action='DESELECT')
		obj.select = True
		bpy.ops.object.location_clear()
		output_absolute_file_path = os.path.join(repo_path, output_file)
		bpy.ops.export_scene.obj(
			filepath=output_absolute_file_path,
			check_existing=True,
			filter_glob="*.obj;*.mtl",
			use_selection=True,
			use_animation=False,
			use_mesh_modifiers=True,
			use_edges=True,
			use_smooth_groups=False,
			use_smooth_groups_bitflags=False,
			use_normals=False,
			use_uvs=True,
			use_materials=False,
			use_triangles=True,
			use_nurbs=False,
			use_vertex_groups=False,
			use_blen_objects=True,
			group_by_object=False,
			group_by_material=False,
			keep_vertex_order=False,
			axis_forward='-Z',
			axis_up='Y',
			global_scale=10,
			path_mode='AUTO'
		)

	wait_enter('Export complete')

# Main (detect if within blender or not)
if importlib.find_loader('bpy'):
	export()
else:
	run_blender()

