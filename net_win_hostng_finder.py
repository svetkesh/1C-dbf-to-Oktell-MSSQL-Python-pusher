import os,sys
from subprocess import check_output
list_out= []
print ('echo')
class iprange(object):
    #pass
    def __init__(self, ipaddress):
        self.ipaddress = ipaddress
    def print_test_ipaddress(self):
        print ('get it test as ' ,self.ipaddress)
    def divide_test_ipaddress(self):
##        pass
        ip_oct_list = self.ipaddress.split('.')
##        print ('-'.join(ip_oct_list))
        for oct_d in range (1,255):
            ip_oct_list[3] = str(oct_d)
            print ('-'.join(ip_oct_list))

    def nbt_test_ipaddress(self):
##        pass
        dict_ip_info = {}
        ip_oct_list = self.ipaddress.split('.')
##        print ('-'.join(ip_oct_list))
        for oct_d in range (104,106):
            ip_oct_list[3] = str(oct_d)
            print ('.'.join(ip_oct_list))
            command = "nbtstat -A " +'.'.join(ip_oct_list)
##            print (command)
##            os.system(command)
##            raw_input()
##            os.system("CLS")
            print_out = check_output(command, shell=True).decode()
            dict_ip_info = {'.'.join(ip_oct_list) : print_out }
##            list_out.append(print_out)
##            print (print_out)
            if "Host not found" in print_out :
                print ('can not connect to host', '.'.join(ip_oct_list) )
            else:
                print ('get useful data from host', '.'.join(ip_oct_list))
                list_out.append(dict_ip_info)

            
    def pretty_print(self):
        #pretty print
        print('----')
        list_splitted_info = []
        list_of_groups = []
        list_of_pc = []
        dict_summury = {}
        for item in list_out :
            print ('item--',item)
            print('----')
            for item_element in item :
                list_splitted_info = []
##                print (itemsting ,' ; ' , item[itemsting])
                print ('item_element--',item_element)
                print('----')
                print ('item[item_element]--' , item[item_element])
                print('----')
##                for item_string in item[item_element] :
##                    if 'UNIQUE' in item_string :
##                        print ('item_string--' , item_string.split())
##                    else:
##                        print ('no UNIQUE here ' , item_string)
##                print ('item[item_element].split()--' , item[item_element].replace('\r\n','\n').split('\n'))
                list_splitted_info = item[item_element].replace('\r\n','\n').split('\n')
                # printing compressed and splitted info
                print ('printing compressed and splitted info')
                for item_splitted in list_splitted_info :
                    if len(str(item_splitted)) >2 :
##                        print (item_splitted)
                        if 'UNIQUE' in item_splitted :
##                            print ('UNIQUE' , item_splitted.split())
                            UNIQUE_name = item_splitted.split()[0]
                        if 'GROUP' in item_splitted :
                            GROUP_name = item_splitted.split()[0]
                        if 'MAC' in item_splitted :
                            MAC_name = item_splitted.split()[3]
                print('UNIQUE_name',UNIQUE_name)
                print('GROUP_name ',GROUP_name)
                print('MAC_name   ',MAC_name)
                        
                # printing UNIQUE info
##                print ('printing UNIQUE info')                
##                print (list_splitted_info[8])
                # printing count info
##                print ('printing count info list_splitted_info.count')                
##                print (list_splitted_info.count())
                
    def get_info_for_ip_range(self):
        # get ingo for ip and put to dict
##        pass
        # declare empty data
        
        
        ip_oct_list = self.ipaddress.split('.')
        for oct_d in range (1,255):
            UNIQUE_name = ''
            GROUP_name = ''
            MAC_name= ''
            status = 'nodata' # could be winok or notwin or errdata
            dict_ip_info = {}
            dict_info = {}
            ip_oct_list[3] = str(oct_d)
            print ('.'.join(ip_oct_list))
            command = "nbtstat -A " +'.'.join(ip_oct_list)
            # command_out = check_output(command, shell=True).decode() # get err UnicodeDecodeError:
                                                                     #'utf-8' codec can't decode byte 0x8f
                                                                     # in position 232: invalid start byte
            try:
                command_out = check_output(command, shell=True).decode()
                if "Host not found" in command_out :
                    print ('can not connect to host', '.'.join(ip_oct_list) )
                else:
                    print ('get useful data from host', '.'.join(ip_oct_list))
                    list_splitted_info = command_out.replace('\r\n','\n').split('\n')
    ##                print (list_splitted_info)
                    print ('-------------')
                    for item_splitted in list_splitted_info :
                        if len(str(item_splitted)) >2 :
                            if 'UNIQUE' in item_splitted :
                                UNIQUE_name = item_splitted.split()[0]
                            if 'GROUP' in item_splitted :
                                GROUP_name = item_splitted.split()[0]
                            if 'MAC' in item_splitted :
                                MAC_name = item_splitted.split()[3]
                    print('UNIQUE_name',UNIQUE_name)
                    print('GROUP_name ',GROUP_name)
                    print('MAC_name   ',MAC_name)
                    if len(UNIQUE_name) > 1 and len(GROUP_name) > 1 and len(MAC_name) > 1 :
                        status = 'winok'
                    else :
                        status = 'notwin'
                    print('status     ',status)
                    print ('-------------')
                #
            #
                dict_ip_info = {'UNIQUE_name' : UNIQUE_name , 'GROUP_name': GROUP_name , 'MAC_name' : MAC_name , 'status': status}
            
    ##            print ('dict_ip_info:-------------')
    ##            print (dict_ip_info)
                
                # end command_out <- .decode()pass
            except:
                # fill dict_ip_info with some safe but fake info with status errdata
                print ('error while processing reply from host', '.'.join(ip_oct_list))
                dict_ip_info = {'UNIQUE_name' : '' , 'GROUP_name': '' , 'MAC_name' : '' , 'status': 'errdata'}
            
            dict_info = {'.'.join(ip_oct_list) : dict_ip_info }
##            print ('dict_info:-------------')
##            print (dict_info)
        #
            # 
            list_out.append(dict_info)
            
##            print ('list_out:-------------')
##            print(list_out)
##            list_out= []
                
                
            
        
    
loc19216810 = iprange('192.168.0.1')
##loc19216810.nbt_test_ipaddress()
##loc19216810.pretty_print()
loc19216810.get_info_for_ip_range()
print ('list_out:-------------')
for item in list_out :
    print(item)
try :
    with open('host_finder_report.txt','w') as report_out :
        for item in list_out :
            try :
                report_out.write(str(item))
            except:
                print ('--writting item error--')
            
    report_out.close()
    print ('-- report written to host_finder_report.txt --')
except:
    print ('--writing report error--')

