import os
import glob
import ray
import fileinput
import time


# def concate_files(output_file):
#     file_list = glob.glob("*.fastq")

#     with open(output_file, 'w') as file:
#         input_lines = fileinput.input(file_list)
#         file.writelines(input_lines)

class Analysis:
    
    def __init__(self, path, lib):
        self.path = path
        self.lib = lib
                
        if not isinstance(lib, list):
            aux = []
            aux.append(lib)
            lib = aux 
        
        try:
            os.chdir(path)
            print("Creating folders...")
            tic = time.time()
            for i in range(len(lib)):
                try:
                    os.mkdir(path +  '/' + lib[i] + '/Files_barcodes/')
                    print("Folder created with sucess!")
                except:
                    print("Folder needed for analysis already exist.")
                    pass
                try:
                    os.mkdir((path + '/' + lib[i] + '/Files_barcodes/' + lib[i] + '_trim/'))
                    print("Folder created with sucess!")
                except:
                    print("Folder needed for analysis already exist.")
                    pass
                try:
                    os.mkdir((path + '/' + lib[i] + '/Files_barcodes/' + lib[i] + '_alltrim/'))
                    print("Folder created with sucess!")
                except:
                    print("Folder needed for analysis already exist.")
                    pass
                try:
                    os.mkdir((path + '/' + lib[i] + '/Files_barcodes/' + lib[i] + '_barcodes/'))
                    print("Folder created with sucess!")
                except:
                    print("Folder needed for analysis already exist.")
                    pass
                try:
                    os.mkdir((path + '/' + lib[i] + '/Files_barcodes/' + lib[i] + '_filt/'))
                    print("Folder created with sucess!")
                except:
                    print("Folder needed for analysis already exist.")
                    pass 
                try:
                    os.mkdir((path + '/' + lib[i] + '/Files_barcodes/' + lib[i] + '_minimap/'))
                    print("Folder created with sucess!")
                except:
                    print("Folder needed for analysis already exist.")
                    pass                    
                try:
                    os.mkdir((path + '/' + lib[i] + '/Files_barcodes/' + lib[i] + '_minimap/tables'))
                    print("Folder created with sucess!")
                except:
                    print("Folder needed for analysis already exist.")
                    pass                
                tac = time.time()
                
        except KeyError:
            pass
        
    def merge_files(self, cpus):
        ray.shutdown()
        path = self.path
        lib = self.lib
        #self.cpus = cpus
        
        def concate_files(output_file):
            file_list = glob.glob("*.fastq")

            with open(output_file, 'w') as file:
                input_lines = fileinput.input(file_list)
                file.writelines(input_lines)

        
        if not isinstance(lib, list):
            aux = []
            aux.append(lib)
            lib = aux
        
        #try:
        for i in range(len(lib)):
            
            os.chdir(path + '/' + lib[i] + '/')
            
            barcodes_folders = sorted(os.listdir())
            
            if barcodes_folders.count('unclassified') > 0:
                barcodes_folders.remove('unclassified')
                
            barcodes_folders.remove('Files_barcodes')

            tic = time.time()
            ray.init(num_cpus=cpus)

            # parallel method
            @ray.remote
            def concat(files):
                os.chdir(path + '/' + lib[i] + '/{0}/'.format(files))
                concate_files('{0}.fastq'.format(files))

            # putting files in list
            results = []
            for files in barcodes_folders:
                results.append(concat.remote(files))

            # putting n files to process
            ray.get(results) 
            tac = time.time()
            ray.shutdown()

            # move files for a new directory
            for files in barcodes_folders:
                os.chdir(path + '/' + lib[i] + '/{0}/'.format(files))
                os.rename(path + '/' + lib[i] + '/{0}/{0}.fastq'.format(files), path + '/' + lib[i] + '/Files_barcodes/' + lib[i] + '_barcodes/{0}.fastq'.format(files))

            print('Merged files are in folder: ' + path + '/' + lib[i] + '/Files_barcodes/' + lib[i] + '_barcodes/.\nExecution time: ' + str(tac - tic) + ' s')
    
    
    def guppy_barcoder(self, cpus = 1, barcode_kits = None):
        path = self.path
        lib = self.lib
        #self.cpus = cpus
         
        if not isinstance(lib, list):
            aux = []
            aux.append(lib)
            lib = aux
        
        def init_with_barcoder():
            # guppy - trim barcodes
            ray.init(num_cpus = cpus)

            # parallel mode
            @ray.remote
            def barcodes(i):
                command = 'guppy_barcoder -i ' + path + '/' + lib[i] + '/Files_barcodes/' + lib[i] + '_barcodes/ -s' + path + '/' + lib[i] + '/Files_barcodes/' + lib[i] + '_trim/ --barcode_kits ' + barcode_kits + ' --trim_barcodes'
                os.system(command)

            # putting files in list
            results = []
            for i in range(len(lib)):
                results.append(barcodes.remote(i))

            # putting n files to process
            ray.get(results)

        def init_without_barcoder():
            
            ray.init(num_cpus = cpus)

            # parallel mode
            @ray.remote
            def barcodes(i):
                command = 'guppy_barcoder -i ' + path + '/' + lib[i] + '/Files_barcodes/' + lib[i] + '_barcodes/ -s' + path + '/' + lib[i] + '/Files_barcodes/' + lib[i] + '_trim/ --trim_barcodes'
                os.system(command)

            # putting files in list
            results = []
            for i in range(len(lib)):
                results.append(barcodes.remote(i))

            # putting n files to process
            ray.get(results)

         
        for i in range(len(lib)):
            if barcode_kits:
                try:
                    init_with_barcoder()
                except:
                    ray.shutdown()
                    # guppy - trim barcodes
                    init_with_barcoder()
                # close remote mode
                ray.shutdown()

            else:
                try:
                    # guppy - trim barcodes
                    init_without_barcoder()
                except:
                    ray.shutdown()
                    # guppy - trim barcodes
                    init_without_barcoder()
                # close remote mode
                ray.shutdown()

            print('Trimmed barcodes files are in ' + path + '/' + lib[i] + '/Files_barcodes/' + lib[i] + '_trim/')
    
    
    def nanofilt(self, cpus, q = 10, l = 1350, maxlength = 1650, just_filt = False):
        path = self.path
        lib = self.lib
        self.q = q
#         cpus = cpus
#         self.q = q
#         self.l = l
#         self.maxlength = maxlength
        
        def concate_files(output_file):
            file_list = glob.glob("*.fastq")

            with open(output_file, 'w') as file:
                input_lines = fileinput.input(file_list)
                file.writelines(input_lines)
                
        def init_concate_files():
            ray.init(num_cpus=cpus)
            #print("iniciou ray")
            # init parallel mode
            @ray.remote
            def concat(folders):
                # concat files
                os.chdir(path + '/'+ lib[i] + '/Files_barcodes/' + lib[i] + '_trim/{0}/'.format(folders))
                #print("first ", path + '/'+ lib[i] + '/Files_barcodes/' + lib[i] + '_trim/{0}/'.format(folders))
                concate_files('{0}_trim.fastq'.format(folders))

            #print("iniciou results")    
            results = []
            for folders in barcodes_folders:
                results.append(concat.remote(folders))

            #print("iniciou get results")
            ray.get(results) 
            #print("finalizou get results")
        
        def init_nanofilt():
            # nanofilt quality control
            ray.init(num_cpus = cpus)

            @ray.remote
            def filt(files):
                command = ('NanoFilt -q ' + str(q) +' -l ' + str(l) +' --maxlength ' + str(maxlength) + ' ' + files +  ' > ' + path + '/' + lib[i] + '/Files_barcodes/' + lib[i] + '_filt/{0}_filt_q'.format(files) + str(q) +'.fastq')
                os.system(command)

            results = []
            for files in trim_files:
                results.append(filt.remote(files))

            ray.get(results)

            
        if not isinstance(lib, list):
            aux = []
            aux.append(lib)
            lib = aux
        
        for i in range(len(lib)):
            if not just_filt:
                print("Started concate files from " + lib[i] + " folder...\n")
                os.chdir(path + '/' + lib[i] + '/Files_barcodes/' + lib[i] + '_trim/')
                barcodes_folders = sorted(os.listdir())
                drop = glob.glob("*.*")
                #print(drop)

                for d in range(len(drop)):
                    barcodes_folders.remove(drop[d])

                barcodes_folders.remove('unclassified')

                # init parallel mode    
                try:
                    init_concate_files()
                except:
                    #print("iniciou ray shutdown")
                    ray.shutdown()
                    
                    init_concate_files()
                    #print("finalizou get results 2")
                ray.shutdown()

                print("Started move files from /" + lib[i] + "_trim folder to /" + lib[i] + "_alltrim folder...\n")
                for folders in barcodes_folders:
                    os.chdir(path + '/' + lib[i] + '/Files_barcodes/' + lib[i] + '_trim/{0}/'.format(folders))
                    #print("first ", path + '/'+ lib[i] + '/Files_barcodes/' + lib[i] + '_trim/{0}/'.format(folders))
                    os.rename(path + '/' + lib[i] + '/Files_barcodes/'+ lib[i] + '_trim/{0}/{0}_trim.fastq'.format(folders), path + '/' + lib[i] + '/Files_barcodes/' + lib[i] + '_alltrim/{0}_trim.fastq'.format(folders))

                print('Trimmed barcodes files are in ' + path + '/' + lib[i] + '/Files_barcodes/' + lib[i] + '_alltrim/\n')

            #else:
                
            os.chdir(path + '/' + lib[i] + '/Files_barcodes/' + lib[i] + '_alltrim/')
            trim_files = sorted(os.listdir())
            print("Filtering ", len(trim_files) , "files in folder /" + lib[i] + '_alltrim\n')


            print("Started filtering files from /" + lib[i] + "_alltrim/ folder...\n")
            try:
                # nanofilt quality control
                init_nanofilt()
            except:
                ray.shutdown()
                # nanofilt quality control
                init_nanofilt()

            ray.shutdown()

            print("Filtered files are in " + path + '/' + lib[i] + '/Files_barcodes/' + lib[i] + '_filt/\n')


    def minimap(self, cpus, refseqpath, nanofilt_q, refseq = 'refseq_16S.fa'):
        path = self.path
        lib = self.lib
#         self.cpus = cpus
#         self.refseqpath = refseqpath
#         self.refseq = refseq
        
        
        def init_minimap():
            
            ray.init(num_cpus = cpus)

            @ray.remote
            def filt(files):
                command = ('minimap2 -cx map-ont ' + refseqpath + '/ncbi/' + refseq + ' {0}'.format(files) + ' > ' + path + '/' + lib[i] + '/Files_barcodes/' + lib[i] + '_minimap/{0}_align'.format(files.replace('_trim.fastq_filt'+ str(nanofilt_q) + '.fastq', 'q'+ str(nanofilt_q))))
                os.system(command)

            results = []
            for files in filt_files:
                results.append(filt.remote(files))

            ray.get(results)

            
                
        if not isinstance(lib, list):
            aux = []
            aux.append(lib)
            lib = aux 
        
        for i in range(len(lib)):
            os.chdir(path + '/' + lib[i] + '/Files_barcodes/' + lib[i] + '_filt/')
            filt_files = glob.glob('*.fastq')
            filt_files = sorted(filt_files)
            
            try:
                init_minimap()
            except:
                ray.shutdown()
                init_minimap()
                
            ray.shutdown()
        
        
    def taxonomy(self, cpus):
        path = self.path
        lib = self.lib
         
        def init_taxonomy():
            os.chdir(path)
            ray.init(num_cpus = cpus)

            @ray.remote
            def taxonomy(libs):
                command = ('Rscript --vanilla paf_R.R ' + path + ' ' + libs)
                os.system(command)

            results = []
            for libs in lib:
                results.append(taxonomy.remote(libs))

            ray.get(results)
            
        #for libs in lib:
        #try:
        init_taxonomy()
        #except:
#             ray.shutdown()
#             init_taxonomy()

        ray.shutdown()
