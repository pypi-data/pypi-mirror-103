import os
from shutil import rmtree, copyfile
from sys import exit

from ase.io import write
from ase.cluster.icosahedron import Icosahedron
from ase.cluster.decahedron import Decahedron
from ase.cluster.octahedron import Octahedron

from NISP.NISP.motif_methods import no_of_atoms_to_make_ico
from NISP.NISP.motif_methods import no_of_atoms_to_make_deca
from NISP.NISP.motif_methods import no_of_atoms_to_make_octa

from NISP.NISP.Create_submitSL_slurm_Main import make_submitSL

atom_writing = 8
details_writing = 12

def write_files_for_manual_mode(element,e_coh,maximum_size,manual_mode,input_information_file,slurm_information=None,sort_manual_mode_by='base details'):
	if manual_mode.lower() == 'vasp':
		manual_mode = 'vasp'
		folder = 'VASP_Clusters'
		filename_suffix = ''
	elif manual_mode.lower() == 'xyz':
		manual_mode = 'xyz'
		folder = 'Clusters'
		filename_suffix = 'xyz'
	else:
		print('Error in def write_files_for_manual_mode, in Manual_Mode.py')
		print('The entry for Manual Mode in the input_information dictionary must be one of the following:')
		print('\t* "VASP" - Obtain clusters as POSCARs.')
		print('\t* "xyz"  - Obtain clusters as xyz files.')
		print('\t* False  - Do not perform manual mode in NISP.')
		print('Sort this out.')
		exit('This program will finished without completing.')
	if os.path.exists(folder):
		rmtree(folder)
	os.mkdir(folder)
	if manual_mode.lower() == 'xyz':
		write_start_of_manual_mode_file(element,maximum_size,input_information_file)
	write_icosahedral_cluster(element,e_coh,maximum_size,manual_mode,filename_suffix,input_information_file,folder,sort_manual_mode_by)
	write_octahedral_cluster (element,e_coh,maximum_size,manual_mode,filename_suffix,input_information_file,folder,sort_manual_mode_by)
	write_decahedral_cluster (element,e_coh,maximum_size,manual_mode,filename_suffix,input_information_file,folder,sort_manual_mode_by)
	if manual_mode.lower() == 'vasp':
		copy_VASP_files(folder,slurm_information)
	print('Have finished making the '+str(input_information_file)+' file.')
	print('Obtain the energies of the clusters that have been added to the '+str(folder)+' folder and then add these energies to associated cluster in the '+str(input_information_file)+' file.')
	print('This program will finish here')
	exit()

def write_start_of_manual_mode_file(element,maximum_size,input_information_file):
	with open(input_information_file,'w') as input_file:
		input_file.write('Element: '+str(element)+' Max_Size: '+str(maximum_size)+'\n')
		input_file.write('Enter the energies of the clusters below to the right most of each line (not the delta energies, NISP can do that for you later)'+'\n')
		input_file.write('------------------------------'+'\n')

def get_diameter(cluster):
	diameter_of_cluster = max(cluster.get_all_distances().flatten())
	'''
	diameter_of_cluster = 0.0
	for index1 in range(len(cluster)):
		for index2 in range(index1+1,len(cluster)):
			distance = cluster.get_distance(index1,index2)
			if distance > diameter_of_cluster:
				diameter_of_cluster = distance
	'''
	return diameter_of_cluster

def post_creating_cluster(cluster):
	diameter_of_cluster = get_diameter(cluster)
	radius_of_cluster = diameter_of_cluster/2.0
	minimum_vacuum = 10.0 #Angstrom
	vacuum = radius_of_cluster if radius_of_cluster > minimum_vacuum else minimum_vacuum
	#vacuum *= 2.0 # same amount of vaccum about all sides of cluster.
	cluster.center(vacuum=vacuum)
	cluster.set_pbc(False)

def save_cluster_to_folder(folder,name,filename_suffix,manual_mode,cluster):
	os.mkdir(folder+'/'+name)
	if manual_mode == 'vasp':
		write(folder+'/'+name+'/'+'POSCAR',cluster,format='vasp')
	else:
		write(folder+'/'+name+'/'+name+'.'+filename_suffix,cluster,format='xyz')

def write_icosahedral_cluster(element,e_coh,maximum_size,manual_mode,filename_suffix,input_information_file,folder,sort_manual_mode_by='base details'):
	print('============================================================')
	print('Starting Obtaining Icosahedral Delta Energies')
	print('no atoms\tno of shells')
	noshells = 2
	all_ico_details = []
	while True:
		no_atoms = no_of_atoms_to_make_ico(noshells)
		if no_atoms > maximum_size:
			break
		#---------------------------------------------------------------------------------
		# Make cluster
		print('Make icosahedral cluster: '+str(no_atoms) + ' \tnoshells: ' + str(noshells))
		cluster = Icosahedron(element,noshells=noshells)
		post_creating_cluster(cluster)
		name = 'Ico_'+str(no_atoms)
		save_cluster_to_folder(folder,name,filename_suffix,manual_mode,cluster)
		#---------------------------------------------------------------------------------
		# make data for details
		no_atoms = len(cluster)
		ico_details = (no_atoms, noshells)
		all_ico_details.append(ico_details)
		#---------------------------------------------------------------------------------
		noshells += 1
		#---------------------------------------------------------------------------------
	print('============================================================')
	with open(input_information_file,'a') as input_file:
		input_file.write('Icosahedron\n')
		if sort_manual_mode_by == 'no of atoms':
			all_ico_details.sort(key=lambda x:x[0])
		elif sort_manual_mode_by == 'base details':
			all_ico_details.sort(key=lambda x:x[1])
		for no_atoms, noshells in all_ico_details:
			no_atoms = str(no_atoms)
			noshells = str(noshells)
			input_file.write(no_atoms+' '*(atom_writing-len(no_atoms))+noshells+' '*(details_writing-len(noshells))+'\n')

def write_decahedral_cluster(element,e_coh,maximum_size,manual_mode,filename_suffix,input_information_file,folder,sort_manual_mode_by='base details'):
	print('============================================================')
	print('Starting Obtaining Decahedral Delta Energies')
	print('no atoms\tp\tq\tr')
	P_START = 2; Q_ORIGINAL = 1; R_ORIGINAL = 0
	
	p = P_START # p is the atom length along the 100_face_normal_to_5_fold_axis
	q = Q_ORIGINAL # q is the atom length along the 100_face_parallel_to_5_fold_axis
	r = R_ORIGINAL # r is the marks_reenterance_depth
	#previous_value_of_r = -1

	all_deca_details = []
	while True:
		no_atoms = no_of_atoms_to_make_deca(p,q,r)
		if (r == R_ORIGINAL and q == Q_ORIGINAL) and (no_atoms > maximum_size):
			break
		previous_value_of_r = r 
		# From now on, at some point r (and potenitally p and q) will be modified to reflect that for the next cluster to sample
		if no_atoms <= maximum_size:
			print('Make decahedral cluster: '+str(no_atoms) + '\t\tp: ' + str(p) + ' \tq: ' + str(q) + ' \tr: ' + str(r))# + '\t,Calculate: ' + str(no_atoms < maximum_size) + '\t,previous r: ' + str(previous_value_of_r)
			#---------------------------------------------------------------------------------
			# Make cluster
			cluster = Decahedron(element,p=p,q=q,r=r)
			post_creating_cluster(cluster)
			name = 'Deca_'+str(p)+'_'+str(q)+'_'+str(r)
			save_cluster_to_folder(folder,name,filename_suffix,manual_mode,cluster)
			#---------------------------------------------------------------------------------
			# make data for details
			deca_parameters = (p,q,r)
			deca_details = (no_atoms, deca_parameters)
			all_deca_details.append(deca_details)
			#---------------------------------------------------------------------------------
			r += 1 # r is now the value of r for the next cluster that will be made using this algorithm.
			if (r > q + 3):
				r = 0; q += 1
		else:
			r = 0; q += 1 # r and q are changed to reflect the next cluster
		if (q > p + 3) or (previous_value_of_r == 0 and r == 0):
			q = 1; p += 1 # p and q are changed to reflect the next cluster
	print('============================================================')
	with open(input_information_file,'a') as input_file:
		input_file.write('Decahedron\n')
		if sort_manual_mode_by == 'no of atoms':
			all_deca_details.sort(key=lambda x:x[0])
		elif sort_manual_mode_by == 'base details':
			all_deca_details.sort(key=lambda x:x[1])
		for no_atoms, details in all_deca_details:
			no_atoms = str(no_atoms)
			details = '('+', '.join([str(detail) for detail in details])+')'
			input_file.write(no_atoms+' '*(atom_writing-len(no_atoms))+details+' '*(details_writing-len(details))+'\n')

def write_octahedral_cluster(element,e_coh,maximum_size,manual_mode,filename_suffix,input_information_file,folder,sort_manual_mode_by='base details'):
	def get_max_cutoff_value(length):
		max_cutoff = (length-1.0)/2.0 - 0.5*((length-1.0)%2.0)
		if not max_cutoff%1 == 0:
			print('Error in Get_Interpolation_Data, at def Get_Energies_Of_Octahedrals, at def get_max_cutoff_value: max_cutoff did not come out as an interger.\nCheck this.\nmax_cutoff = '+str(max_cutoff))
			import pdb; pdb.set_trace()
			exit()
		return int(max_cutoff)
	print('============================================================')
	print('Starting Obtaining Octahedral Delta Energies')
	print('no atoms\tlength\tcutoff')
	length = 2; cutoff = get_max_cutoff_value(length); cutoff_max = cutoff

	all_octa_details = []
	while True:
		no_atoms = no_of_atoms_to_make_octa(length,cutoff)
		if (no_atoms > maximum_size) and (cutoff == cutoff_max):
			break
		if no_atoms <= maximum_size:
			print(str(no_atoms)+' \tlength: ' + str(length) + ' \tcutoff = ' + str(cutoff))
			#---------------------------------------------------------------------------------
			# Make cluster
			cluster = Octahedron(element,length=length,cutoff=cutoff)
			post_creating_cluster(cluster)
			name = 'Octa_'+str(length)+'_'+str(cutoff)
			save_cluster_to_folder(folder,name,filename_suffix,manual_mode,cluster)
			#---------------------------------------------------------------------------------
			# make data for details
			octa_parameters = (length,cutoff)
			octa_details = (no_atoms, octa_parameters)
			all_octa_details.append(octa_details)
			#---------------------------------------------------------------------------------
		cutoff -= 1
		if cutoff < 0 or no_atoms > maximum_size:
			length += 1
			cutoff = get_max_cutoff_value(length)
			cutoff_max = cutoff
	print('============================================================')
	with open(input_information_file,'a') as input_file:
		input_file.write('Octahedron\n')
		if sort_manual_mode_by == 'no of atoms':
			all_octa_details.sort(key=lambda x:x[0])
		elif sort_manual_mode_by == 'base details':
			all_octa_details.sort(key=lambda x:x[1])
		for no_atoms, details in all_octa_details:
			no_atoms = str(no_atoms)
			details = '('+', '.join([str(detail) for detail in details])+')'
			input_file.write(no_atoms+' '*(atom_writing-len(no_atoms))+details+' '*(details_writing-len(details))+'\n')

def copy_VASP_files(folder,slurm_information):
	vasp_files_folder = 'VASP_Files'
	if not os.path.exists(vasp_files_folder):
		print('Error in copying VASP files to cluster folder')
		print('There is no folder called "VASP_Files" in your working directory.')
		print('This folder is where you should place your VASP files in for DFT local optimisations.')
		print('Make this folder and place your "POTCAR", INCAR", "KPOINTS" files for VASP local optimisations')
		print('This program will exit without completing.')
		exit()
	VASP_Files_files = os.listdir(vasp_files_folder)
	have_POTCAR  = 'POTCAR'  in VASP_Files_files
	have_INCAR   = 'INCAR'   in VASP_Files_files
	have_KPOINTS = 'KPOINTS' in VASP_Files_files
	if not (have_POTCAR and have_INCAR and have_KPOINTS):
		print('Error in copying VASP files to cluster folder')
		print('You need the following files when you are performing VASP calculations:')
		print()
		print('\tPOTCAR:\t' +('You have this' if have_POTCAR  else 'You do not have this'))
		print('\tINCAR:\t'  +('You have this' if have_INCAR   else 'You do not have this'))
		print('\tKPOINTS:\t'+('You have this' if have_KPOINTS else 'You do not have this'))
		print()
		print('Check this out. This program will now end without completing.')
		exit()
	for root, dirs, files in os.walk(folder):
		dirs.sort()
		if not ('POSCAR' in files):
			continue
		print('Copying VASP files to '+root)
		for file in ['POTCAR', 'INCAR', 'KPOINTS']:
			copyfile(vasp_files_folder+'/'+file, root+'/'+file)
		project = slurm_information['project']
		time = slurm_information['time']
		nodes = slurm_information['nodes']
		ntasks_per_node = slurm_information['ntasks_per_node']
		mem_per_cpu = slurm_information['mem-per-cpu']
		partition = slurm_information['partition']
		email = slurm_information['email']
		vasp_version = slurm_information['vasp_version']
		vasp_execution = slurm_information['vasp_execution']
		make_submitSL(root,project,time,nodes,ntasks_per_node,mem_per_cpu,partition=partition,email=email,vasp_version=vasp_version,vasp_execution=vasp_execution)
