import re, os,sys
#agrs check \*ak
print('This is iss_file_processor with args_checker running, \*ak')
compile_log_file = open('compile_log_file.txt','w')

class iss_file_processor(object):
    #
    def __init__(self , oem_name , file_to_go , version_modifier):
        #
        self.oem_name = oem_name
        self.file_to_go = file_to_go
        self.version_modifier = version_modifier
        self.file_new = file_to_go+'.new'
    def print_file_processor_info(self):
        print('--------------------------------')
        print(' oem_name \t %s \n file_to_go  \t %s \n version_modifier \t %s \n' %(self.oem_name,self.file_to_go,self.version_modifier))
        print('--------------------------------')
    def find_last_version(self):
        #
        last_version = '0000'
        try:
            #
            print('try file %s' %self.file_to_go)
            file_obj = open(self.file_to_go , 'r')
            file_new = open(self.file_new , 'w')
            for line in file_obj:
                if '#define RV' in line :
                    #print('old line is ')
                    #print(line)
                    #last_version =
                    last_version = 'version changed '+str(re.findall('\d\d\d\d', line)) + '->' +'[\''+ self.version_modifier +'\']'
                    #print ('new line is ')
                    #print(re.sub('\d\d\d\d', self.version_modifier , line))
                    file_new.write(re.sub('\d\d\d\d', self.version_modifier , line))
                else:
                    file_new.write(line)
            print( file_obj.readline())
            file_new.close()
            file_obj.close()
            # file renamer
            #file_name_bu = file_obj+'.bu'
            os.rename(self.file_to_go , self.file_to_go+'.bu')
            #os.rename(self.file_new , self.file_new[0:len(self.file_new)-8]+'.xxx')
            os.rename(self.file_new , self.file_to_go)
        except :
            #
            print('file operation error with %s file' %self.file_to_go)
        return last_version


    def change_version_and_compile(self):
        #
        last_version = '0000'
        try:
            #
            print('try file %s' %self.file_to_go)
            file_obj = open(self.file_to_go , 'r')
            file_new = open(self.file_new , 'w')
            for line in file_obj:
                if '#define RV' in line :
                    #print('old line is ')
                    #print(line)
                    #last_version =
                    last_version = 'version changed '+str(re.findall('\d\d\d\d', line)) + '->' +'[\''+ self.version_modifier +'\']'
                    #print ('new line is ')
                    #print(re.sub('\d\d\d\d', self.version_modifier , line))
                    file_new.write(re.sub('\d\d\d\d', self.version_modifier , line))
                else:
                    file_new.write(line)
            print( file_obj.readline())
            file_new.close()
            file_obj.close()
            try:
                #
                print('try file renamie')

                # file renamer
                #file_name_bu = file_obj+'.bu'
                os.rename(self.file_to_go , self.file_to_go+'.bu')
                #os.rename(self.file_new , self.file_new[0:len(self.file_new)-8]+'.xxx')
                os.rename(self.file_new , self.file_to_go)
            except:
                #
                print('file renaming error')
                compile_log_file.write('file renaming and or back up error %s' %self.file_to_go)
                compile_log_file.write('\r\n')

            try:
                print('try to compile file ' + self.file_to_go )
                compile_command = "compil32 /cc " + self.file_to_go
                print(compile_command)
                #print_out = check_output(compile_command, shell=True).decode()
                #print(print_out)
                os.system(compile_command)
                compile_log_file.write('check terminal for output %s' %self.file_to_go)
                compile_log_file.write('\r\n')
                
            except:
                print('not compiled file due to error ' + self.file_to_go)
                compile_log_file.write('not compiled file due to error %s file' %self.file_to_go)
                compile_log_file.write('\r\n')
                

            
        except :
            #
            print('file operation error with %s file' %self.file_to_go)
            compile_log_file.write('file operation error with %s file' %self.file_to_go) # <---
            compile_log_file.write('\r\n')                                               # <---

        return last_version

# end class ----


res = ''
result = ''
found_given_version = False

try:
    compile_log_file.write('looking if given version to compile bases')
    compile_log_file.write('\r\n')
    for argum in sys.argv :
    ##    print(argum)
    ##    print('--------')
        res = re.match('\d\d\d\d' , argum)
        if res is not None :
            found_given_version = True
            result = argum
            print('found_given_version found %s' %result)
            compile_log_file.write('found_given_version found %s' %result)
            compile_log_file.write('\r\n')
    ##    print('res is %s' %res)
    ##    print('--------')
    
except:
    print('error while looking version as an argument')
    compile_log_file.write('error while looking version as an argument to compile off-line bases ')
    compile_log_file.write('\r\n')

# later compilation block should be
try:
    if found_given_version :
        compile_log_file.write('try to compile off-line bases ')
        compile_log_file.write('\r\n')
        #
        # here compilation block should be
        #
        # put version into life
        #
        current_version = result
        #
        print('try to compile offline bases to version %s' %current_version)
        #
        print('--------------------------------')
        print('ed_bases')
        ed_bases = iss_file_processor('ed_bases','ed_bases.iss', current_version)
        ed_bases.change_version_and_compile()
        print('--------------------------------')
        #    
        print('--------------------------------')
        print('a_bases')
        a_bases = iss_file_processor('a_bases','a_bases.iss', current_version)
        a_bases.change_version_and_compile()
        print('--------------------------------')
        #    
        print('--------------------------------')
        print('aav_bases')
        aav_bases = iss_file_processor('aav_bases','aav_bases.iss', current_version)
        aav_bases.change_version_and_compile()
        print('--------------------------------')
        #    
        print('--------------------------------')
        print('e_bases')
        e_bases = iss_file_processor('e_bases','e_bases.iss', current_version)
        e_bases.change_version_and_compile()
        print('--------------------------------')
        #    
        print('--------------------------------')
        print('o')
        o = iss_file_processor('o','o.iss', current_version)
        o.change_version_and_compile()
        print('--------------------------------')
        #    
        print('--------------------------------')
        print('p_bases')
        p_bases = iss_file_processor('p_bases','p_bases.iss', current_version)
        p_bases.change_version_and_compile()
        print('--------------------------------')
        #    
        print('--------------------------------')
        print('s_bases')
        s_bases = iss_file_processor('s_bases','s_bases.iss', current_version)
        s_bases.change_version_and_compile()
        print('--------------------------------')
        #    
        print('--------------------------------')
        print('sw_bases')
        sw_bases = iss_file_processor('sw_bases','sw_bases.iss', current_version)
        sw_bases.change_version_and_compile()
        print('--------------------------------')
        #    
        print('--------------------------------')
        print('sl_bases')
        sl_bases = iss_file_processor('sl_bases','sl_bases.iss', current_version)
        sl_bases.change_version_and_compile()
        print('--------------------------------')
        #
        print('may be compilation over ...')

        print('hope compilation succesfull')
        compile_log_file.write('hope compilation succesfull')
    else:
        print('error while looking version as an argument to compile off-line bases')
        compile_log_file.write('error while looking version as an argument to compile off-line bases ')
        compile_log_file.write('\r\n')
except:
    print('error while compilation off-line bases')
    compile_log_file.write('error while compilation off-line bases')
    compile_log_file.write('\r\n')
    
compile_log_file.close()
