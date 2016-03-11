import datetime
#from mx import DateTime
from dbfpy import dbf
import subprocess

print "running dbf_file_walker.py"

##################################
#
# set test_mode here
#
#test_mode = 'test'
test_mode = 'real'
#
# define source file as d:\\import\\TEL-test-set.dbf OR d:\\import\\TEL.dbf
# and target import into table C_ClientsCard_test    OR C_ClientsCard
#
##################################

##################################
#
# set truncate_mode here
#
truncate_mode = 'overwrite'
#truncate_mode = 'keepdata'
#
# keep existing data and append
# fresh records to quizz list
#
#sizetest_mode = 'sizetest' # remap source file to d:\\import\\TEL-test-set.dbf and
#                          # import into table C_ClientsCard_test
sizetest_mode = 'real'
#
##################################


#  testing ...
##inp_file = 'src_file_dbf.DBF'
##inp_file = 'src_file_dbf_state102.dbf'
##inp_file = 'src_file_dbf_state_test_set_4rows-2.dbf'

## in 186 line change C_ClientsCard_test -> C_ClientsCard
if test_mode == 'test':
    inp_file = 'd:\\import\\TEL.dbf' ## current test set
    #inp_file = 'd:\\import\\TEL-test-set.dbf' ## current test set
else:
    inp_file = 'd:\\import\\TEL.dbf' ## current REAL set

if sizetest_mode == 'sizetest':
    inp_file = 'd:\\import\\TEL.dbf'
else :
    inp_file = 'd:\\import\\TEL.dbf'
    #inp_file = 'd:\\import\\TEL-test-set.dbf'

##sql_out_file = 'd:\\import\\tel.sql'    ## result file is defined later
##report_file = 'd:\\import\\report.txt'  ## report file is defined later
    

droper = 0
droperstoper = 10
singlelinelist = []
linelist = []
#errorscounter = 0 # format err counter

def lines_couner(inp_file):
    #
    print 'Counting lines in source file ...' 
    droper = 0
    droperstoper = 1000
    linecounter = 0
    try:
        f_inp_handler = dbf.Dbf(inp_file)
        for line in f_inp_handler :
            linecounter += 1
            
        print 'In file ', inp_file ,' lines counted :', linecounter
        return linecounter
        f_inp_handler.close()    
        
##      f_inp_handler = open(inp_file)
##      print f_inp_handler
##      linecounter = 0
##      for line in f_inp_handler:
##          char_counter = 0
##          for char in line :
##              char_counter += 1
##              print char,
##              if char_counter >= droperstoper :
##                  print 
##                  break
##          linecounter += 1
##          if linecounter >= droperstoper :
##              print 'lines couner reach droperstoper = ', droperstoper
##              break
        
##      print line
##        print droper , line
##        singlelinelist = line.split()
##        for singleword in singlelinelist :
##          print 'already items added :' , len(linelist)
##          linelist.append(singleword)
##        print linecounter
          
        
##        print linelist
##    ##    for word in line :
##    ##      print word
##        droper += 1
##        if droper >= droperstoper :
##          print 'reach droperstoper = ', droperstoper
##          break
        
##      print 'in file ', inp_file ,' lines counted :', linecounter
##      f_inp_handler.close()
    except:
      print 'Can not work with file'
      
def sample_line(inp_file) :
    #
    droper = 0
    droperstoper = 4
    linecounter = 0
    try :
        f_inp_handler = dbf.Dbf(inp_file)
        for line in f_inp_handler :
            print
            linecounter += 1
##            print line
            if linecounter >= droperstoper :
                f_inp_handler.close() 
                break
            for f in line :
                print type(f) , f ,  f.decode('cp866') , f.decode('cp866').encode('cp1251')
            print line[0].decode('cp866').encode('cp1251') , line[1].decode('cp866').encode('cp1251')
##            for rec in db:
##            for field in line.fieldData:
##                print 'field'
##                if type(field)==StringType:
##                   field=unicode(f,'utf-8')
##                   field=f.encode('windows-1251')
##                print field,
                
        
##        return linecounter
        f_inp_handler.close() 


    except :
        print 'err'
def sample_line_writer(inp_file) :
    #
    droper = 0
    droperstoper = 4
    linecounter = 0

    out_file = 'out_file_plain.txt'
    try: 
      f_out_handler = open(out_file , 'w')
      f_out_handler.write('USE oktell \r\n')
      f_out_handler.write('GO \r\n')
    except:
      print 'cannot open and write to file' , out_file    
    try :
        f_inp_handler = dbf.Dbf(inp_file)
        for line in f_inp_handler :
            print
            linecounter += 1
            if linecounter >= droperstoper :
                f_inp_handler.close() 
                break
            for f in line :
                print type(f) , f ,  f.decode('cp866') , f.decode('cp866').encode('cp1251')
            print line[0].decode('cp866').encode('cp1251') , line[1].decode('cp866').encode('cp1251')
            
            try: 
##                f_out_handler.write('line')
                f_out_handler.write('INSERT INTO [oktell].[dbo].[C_ClientsCard] (Name ,Phone ,Updated) VALUES (\'')
##                f_out_handler.write( line[0].decode('cp866').encode('cp1251') )
                f_out_handler.write(sym_filter(line[0].decode('cp866').encode('cp1251')))
                f_out_handler.write( '\',\'')
                f_out_handler.write( line[1].decode('cp866').encode('cp1251') )
                f_out_handler.write('\',GETDATE() );')
                f_out_handler.write( ' \r\n' )
##                print sym_filter(line[0].decode('cp866').encode('cp1251'))
##                f_out_handler.write('startline', str(linecounter), str(line[0].decode('cp866').encode('cp1251') ), str(line[1].decode('cp866').encode('cp1251') ), ' endline')
            except:
                print 'cannot write to file' , out_file
    
        return 'lines processed ',linecounter
        f_inp_handler.close() 


    except :
        print 'err'
    f_out_handler.close()

## real DEF
def sql_file_writer(inp_file) :
    #
    print 'Starting import lines from DBF to SQL file ... Please wait '
    droper = 0
    droperstoper = 4  # stoper
    linecounter = 0   # counter for stoper
    errorscounter = 0 # format err counter
    report_file = 'd:\\import\\report.txt'
    sql_out_file_splitter = 51000
    
    sql_out_file = 'd:\\import\\tel0.sql'
    try:
      f_out_handler = open(sql_out_file , 'w')
      f_out_handler.write('USE oktell \r\n')
      f_out_handler.write('GO \r\n')
    except:
      print 'cannot open and write to file' , out_file

    sql_out_file2 = 'd:\\import\\tel2.sql'
    try:
      f_out_handler2 = open(sql_out_file2 , 'w')
      f_out_handler2.write('USE oktell \r\n')
      f_out_handler2.write('GO \r\n')
    except:
      print 'cannot open and write to file' , out_file
      
    try :
        f_inp_handler = dbf.Dbf(inp_file)
        for line in f_inp_handler :
            #print
            linecounter += 1
            if linecounter < sql_out_file_splitter :
                # print splitter below sql_out_file_splitter 
                # check mode
                if test_mode == 'test':
                    f_out_handler.write('INSERT INTO [oktell].[dbo].[C_ClientsCard_test] (Name ,Phone ,Updated ,ClientState) VALUES (\'')
                else :
                    f_out_handler.write('INSERT INTO [oktell].[dbo].[C_ClientsCard] (Name ,Phone ,Updated ,ClientState) VALUES (\'')
                f_out_handler.write(sym_filter(line[0].decode('cp866').encode('cp1251')))
                f_out_handler.write( '\',\'')
                f_out_handler.write( line[1].decode('cp866').encode('cp1251') )
                if line[6] :
#                    print 'check line[6] value for True '
                    f_out_handler.write('\',GETDATE(),551);')
                else :
#                    print 'check line[6] value for False '
                    f_out_handler.write('\',GETDATE(),554);')
                f_out_handler.write( ' \r\n' )
                
            elif linecounter == sql_out_file_splitter :
                # print splitter sql_out_file_splitter reached!
                print 'splitter sql_out_file_splitter reached!' , sql_out_file_splitter
                #
                # switch f_out_handler to f_out_handler2
                #
                f_out_handler.close()
                #
                
                # check mode
                if test_mode == 'test':
                    f_out_handler2.write('INSERT INTO [oktell].[dbo].[C_ClientsCard_test] (Name ,Phone ,Updated ,ClientState) VALUES (\'')
                else :
                    f_out_handler2.write('INSERT INTO [oktell].[dbo].[C_ClientsCard] (Name ,Phone ,Updated ,ClientState) VALUES (\'')                    
                f_out_handler2.write(sym_filter(line[0].decode('cp866').encode('cp1251')))
                f_out_handler2.write( '\',\'')
                f_out_handler2.write( line[1].decode('cp866').encode('cp1251') )
                if line[6] :
#                    print 'check line[6] value for True '
                    f_out_handler2.write('\',GETDATE(),551);')
                else :
#                    print 'check line[6] value for False '
                    f_out_handler2.write('\',GETDATE(),554);')
                f_out_handler2.write( ' \r\n' )

            else :
                # print splitter is above sql_out_file_splitter !
                # check mode
                if test_mode == 'test':
                    f_out_handler2.write('INSERT INTO [oktell].[dbo].[C_ClientsCard_test] (Name ,Phone ,Updated ,ClientState) VALUES (\'')
                else :
                    f_out_handler2.write('INSERT INTO [oktell].[dbo].[C_ClientsCard] (Name ,Phone ,Updated ,ClientState) VALUES (\'')
                    
                f_out_handler2.write(sym_filter(line[0].decode('cp866').encode('cp1251')))
                f_out_handler2.write( '\',\'')
                f_out_handler2.write( line[1].decode('cp866').encode('cp1251') )
                if line[6] :
#                    print 'check line[6] value for True '
                    f_out_handler2.write('\',GETDATE(),551);')
                else :
#                    print 'check line[6] value for False '
                    f_out_handler2.write('\',GETDATE(),554);')
                    f_out_handler2.write( ' \r\n' )
        if linecounter < sql_out_file_splitter :
            # close opened files
            f_out_handler.close()
            f_out_handler2.close()
            
    #            # shorted import
    #            if linecounter >= droperstoper :
    #                f_inp_handler.close() 
    #                break
                # detailed values of fileds of DBF
    #            for f in line :
    #                if type(f) == 'str' :
    #                    print type(f) , f ,  f.decode('cp866') , f.decode('cp866').encode('cp1251')
    #                else :
    #                    print type(f) , f
    #            # summorized line values of DBF before import
    #            print line[0].decode('cp866').encode('cp1251') , line[1].decode('cp866').encode('cp1251') , line[6]
##                try:
                    
                    #result writing
                    # check mode
##                    if test_mode == 'test':
##                        f_out_handler.write('INSERT INTO [oktell].[dbo].[C_ClientsCard_test] (Name ,Phone ,Updated ,ClientState) VALUES (\'')
##                    else :
##                        f_out_handler.write('INSERT INTO [oktell].[dbo].[C_ClientsCard] (Name ,Phone ,Updated ,ClientState) VALUES (\'')
##                        
##                    f_out_handler.write(sym_filter(line[0].decode('cp866').encode('cp1251')))
##                    f_out_handler.write( '\',\'')
##                    f_out_handler.write( line[1].decode('cp866').encode('cp1251') )
##                    if line[6] :
##    #                    print 'check line[6] value for True '
##                        f_out_handler.write('\',GETDATE(),551);')
##                    else :
##    #                    print 'check line[6] value for False '
##                        f_out_handler.write('\',GETDATE(),554);')
##                    f_out_handler.write( ' \r\n' )
##            except:
##                print 'cannot write to file' , out_file
        
    except :
        print 'error reading inp file and writing out datafile'

        
#  part 2 . not  euought memory for 100K+ lines
   
        

    try:
        # report writing
        report_file_handler = open(report_file , 'w')
        report_file_handler.write('Total lines processed ')
        report_file_handler.write(str(linecounter))
        report_file_handler.write( ' \r\n' )
        report_file_handler.close()
        print 'Total lines get from DBF to SQL file ',linecounter
        print 'End import lines from DBF to SQL file. Done '
    except:
        print 'cannot write report' , report_file 
    return 'Total lines get from DBF to SQL file ',linecounter
#
# sql_importer
def sql_importer():
    print 'SQL_importer to table started'
    if truncate_mode == 'overwrite':
        print 'table C_ClientsCard_test will be erased before importing...'    
        truncate_cmd = 'sqlcmd -S OKTELL\OKTELL -i \"d:\\import\\truncate_test_tables.sql\" -o \"d:\\import\\truncate_test_tables_report.txt\"'
        p = subprocess.Popen(truncate_cmd, shell = True)
        p.wait()
    
    print 'Importer into SQL table started part 1'
    sql_cmd = 'sqlcmd -S OKTELL\OKTELL -i \"d:\\import\\tel0.sql\" -o \"d:\\import\\import_report0.txt\"'
    p = subprocess.Popen(sql_cmd, shell = True)
    p.wait()
    print 'Importer into SQL table started part 2'
    sql_cmd = 'sqlcmd -S OKTELL\OKTELL -i \"d:\\import\\tel2.sql\" -o \"d:\\import\\import_report2.txt\"'
    p = subprocess.Popen(sql_cmd, shell = True)
    p.wait()
    print 'SQL_importer to table finished'
##
def file_checker(some_file) :
    #
    check_result = 'not yet definded'
    try: 
      file_handler = open(some_file , 'r')
      print  'open to read OK', some_file
      check_result = 'open to read OK'
      file_handler.close()
    except:
      print 'cannot open and read file' , some_file  
    #
    try: 
      file_handler = open(some_file , 'w')
      file_handler.write('USE oktell \r\n')
      file_handler.write('GO \r\n')
      print  'open and write OK' , some_file
      check_result = 'open and write OK'
      file_handler.close()
    except:
      print 'cannot open and write to file' , some_file
    #
    return check_result

# C:\pyapps\dbf_file_walker_files\
# \"C:\\pyapps\\dbf_file_walker_files\\
#
def put_data_to_quiz_list():
    # empty TRUNCATE TABLE [oktell].[dbo].[testlist071]
    print 'Tables truncater started'
    if truncate_mode == 'overwrite':
        #
        print 'truncate_mode == overwrite'
        print 'table testlist071 will be overwritten'    
        truncate_cmd = 'sqlcmd -S OKTELL\OKTELL -i \"d:\\import\\truncate_testlist071.sql\" -o \"d:\\import\\truncate_quizzqueu_report.txt\"'
        p = subprocess.Popen(truncate_cmd, shell = True)
        p.wait()
##        print 'table C_ClientsCard_test will be overwritten'    
##        truncate_cmd = 'sqlcmd -S OKTELL\OKTELL -i \"d:\\import\\truncate_test_tables.sql\" -o \"d:\\import\\truncate_test_tables_report.txt\"'
##        p = subprocess.Popen(truncate_cmd, shell = True)
##        p.wait()
    else :
        #
        print 'truncate_mode == keep'
        print 'fresh contacts will be added into table testlist071'
    print 'sql truncate testlist071 finished'

    # fill data into INSET TABLE [oktell].[dbo].[testlist071]
    print 'Fill data into table testlist071 (sql insert testlist071 started)'
    if test_mode == 'test':
        #
        print 'test_mode == test'
        print 'wil be used test script testmode_insert_testlist071.sql  '
        print 'with source table [oktell].[dbo].[C_ClientsCard_test]'
        insert_cmd = 'sqlcmd -S OKTELL\OKTELL -i \"d:\\import\\testmode_insert_testlist071.sql\" -o \"d:\\import\\insert_report.txt\"'
        p = subprocess.Popen(insert_cmd, shell = True)
        p.wait()
    else :
        #
        print 'test_mode == real'
        print 'will be used real script insert_testlist071.sql  '
        print 'with source table [oktell].[dbo].[C_ClientsCard]'
        insert_cmd = 'sqlcmd -S OKTELL\OKTELL -i \"d:\\import\\insert_testlist071.sql\" -o \"d:\\import\\insert_report.txt\"'
        p = subprocess.Popen(insert_cmd, shell = True)
        p.wait()        
    print 'sql insert testlist071 finished'


    
def sym_filter(text):
    ftr = ['\\' , '\"' , '\'' , '\#' , '?' , '&' ,'\@' ]
##    print ' get this text', text
    filteredtext = text
##    for fltsynbl in ftr :
##        print fltsynbl,
##    print ftr
##    print
##    for sign in text :
##        print sign
    for item in ftr :
        if item in text :
            print 'fixed forbidden symbol in ' , text , item , text.index(item)
            filteredtext = text.translate(None , '"\\?\/#&\'\@\"')            
##    print 'return this text ' , filteredtext
    return filteredtext


print '-- start main --'
print '--Current mode - :'
print '-test_mode    ' , test_mode
print '-truncate_mode' , truncate_mode
print '-sizetest_mode' , sizetest_mode
print '----------------'

print lines_couner(inp_file)            # count source lines
##sample_line_writer(inp_file)
##print sym_filter('a?"b/&c\\"')
sql_file_writer(inp_file)               # start import from TEL.DBF to TEL.sql
#print file_checker('report.txt')
sql_importer()                          # import from TEL.sql into 
put_data_to_quiz_list()

print '-- end  main --'
