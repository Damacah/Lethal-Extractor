import shutil
import os

files_to_remove = ('.png', '.jpeg', '.jpg', '.ico', '.webp', '.xcf', '.json', '.dm', 'md', '.txt', 'LICENSE', 'manifest.json', 'MANIFEST.JSON')
bep_folders = {'config', 'core', 'patchers', 'plugins'} #? These are the possible 'special' folders that mods may have. These folders aren't placed in BepInEx/plugins.

def start():
    print('Welcome to Lethal Extractor!')
    
    mods_folder = str(input('Please enter the path where the compressed mods are located: '))
    
    delete_zips = str(input('Do you want to delete the compressed mods? yes/no: '))

    main(mods_folder, delete_zips)
    
def main(mods_folder, delete_zips):
    
    if not os.path.exists(mods_folder):
        print('*-ERROR! Please enter a valid path to the compressed mods-*')
        return
    
    if delete_zips != 'yes' and delete_zips != 'no':
        print('*-ERROR! Please enter a valid answer.-*')
        return

    BepInEx_folder = os.path.join(mods_folder, 'BepInEx')
    
    if not os.path.exists(BepInEx_folder):
        os.mkdir(BepInEx_folder)
        
    #? Creates a list containing the names of all the compressed mods.
    compressed_mods = []
    
    for item in os.listdir(mods_folder):
        #? Just to make sure that there are real mods inside the folder.
        if item.endswith('.zip'):
            compressed_mods.append(item)

    #? This is just for the 'progress bar'.
    number_of_mods = len(compressed_mods)
    extracted_mods = 0
    
    for compressed_mod in compressed_mods:
            
        compressed_mod_name = compressed_mod
        compressed_mod_path = os.path.join(mods_folder, compressed_mod_name)
            
        mod_name = compressed_mod_name.replace('.zip', '')
        mod_folder = os.path.join(mods_folder, mod_name)

        if not os.path.exists(mod_folder):
            os.mkdir(mod_folder)

        shutil.unpack_archive(compressed_mod_path, mod_folder)

        if delete_zips == 'yes':
            os.remove(compressed_mod_path)

        clean_folder(mod_folder)
            
        move_mod(mod_folder, mods_folder, BepInEx_folder)
        
        extracted_mods += 1
        
        print(f'*-{extracted_mods}/{number_of_mods} mods extracted-*', end='\r')
    
    print('\n*-Finally, deleting the remaining folders...-*')
              
    remove_mod_folders(mods_folder)
            
    print('\nFinished! Now, move the BepInEx folder to Lethal Company\'s BepInExPack.') 

#? Deletes all unwanted files from the mod folder.
def clean_folder(mod_folder):
    
    unfiltered_files = os.listdir(mod_folder)

    for file in unfiltered_files:

        if(file.endswith(files_to_remove)):
            
            file_path = os.path.join(mod_folder, file)

            os.remove(file_path)

#? Moves the contents of the mod folder to its correct location in the BepInEx folder.
def move_mod(mod_folder, mods_folder, BepInEx_folder):
    
    plugins_folder = os.path.join(BepInEx_folder, 'plugins')
    
    mod_content = os.listdir(mod_folder)
        
    for item in mod_content:
        
        item_path = os.path.join(mod_folder, item)

        if item == 'BepInEx':
            shutil.copytree(item_path, BepInEx_folder, dirs_exist_ok=True)
            
        elif item in bep_folders:
            
            destination_path = os.path.join(BepInEx_folder, item)
                                    
            shutil.copytree(item_path, destination_path, dirs_exist_ok=True)
        
        else:
            if not os.path.isdir(item_path):
                shutil.copy2(item_path, plugins_folder)
                       
            else:
                shutil.copytree(item_path, plugins_folder, dirs_exist_ok=True)

#? Removes all remaining mod folders.
def remove_mod_folders(mods_folder):
    
    for folder in os.listdir(mods_folder):
        
        if folder != 'BepInEx' and not folder.endswith('.zip'):
            
            folder_path = os.path.join(mods_folder, folder)
            shutil.rmtree(folder_path, ignore_errors=True)
        
if __name__ == '__main__':
    start()