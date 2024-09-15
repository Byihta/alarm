import multiprocessing
from playsound import playsound
from time import sleep
import sys
from os import getcwd, system
import ctypes

#NEEDS CLASS WITH ARG_L {VAL : {SHORT: VAL, LONG: VAL}}
TIME_SLEEP_SECONDS = "time_sleep_seconds"
TIME_SLEEP_MINUTES = "time_sleep_minutes"
TIME_SLEEP_HOURS = "time_sleep_hours"
ALARM_SOUND_NAME = "alarm_sound_name"
SILENT_MODE = "alarm_silent_mode"
#Implement default from file

ARG_L = {
    "short": 
        {
            "s": TIME_SLEEP_SECONDS,
            "m": TIME_SLEEP_MINUTES,
            "h": TIME_SLEEP_HOURS,
            "sn": ALARM_SOUND_NAME,
            "q": SILENT_MODE 
        },
        
    "long": 
        {
            "seconds": TIME_SLEEP_SECONDS,
            "minutes": TIME_SLEEP_MINUTES,
            "hours": TIME_SLEEP_HOURS,
            "soundName": ALARM_SOUND_NAME,
            "quiet": SILENT_MODE
        }
}

ARG_TYPE_PARSER = {
    TIME_SLEEP_SECONDS: int,
    TIME_SLEEP_MINUTES: float,
    TIME_SLEEP_HOURS: float,
    ALARM_SOUND_NAME: str,
    SILENT_MODE: bool
}
    


def alarm(sound_name, seconds = 0, minutes = 0, hours = 0, silent_mode = False):
    
    
    time_interval = int((hours * 60 + minutes) * 60 + seconds)
    
    
    currHours = 0
    currMins = 0
    currSecs = 0
    timerHours = time_interval // 3600
    timerMins = (time_interval % 3600 ) // 60
    timerSecs = ((time_interval % 3600 ) % 60 ) % 60
    sys.stdout.write('\033[?25l')
    print("Total Time: ", timerHours, ":", timerMins, ":", timerSecs)
    #print("Current Time: ", currHours, ":", currMins, ":", currSecs, "\nTime Left", 
    #          timerHours, ":", timerMins, ":", timerSecs, end = "\n") 
    for i in range(time_interval):
        currHours = i // 3600
        currMins = i // 60
        currSecs = i % 60
        timerHours = (time_interval - i) // 3600
        timerMins = ((time_interval - i) % 3600 ) // 60
        timerSecs = (((time_interval - i) % 3600 ) % 60 ) % 60
        
        sys.stdout.write('\033[J')
        print("Current Time: ", currHours, ":", currMins, ":", currSecs, "\nTime Left", 
              timerHours, ":", timerMins, ":", timerSecs, "\n", end = "\033[2A")    
        #sys.stdout.write('\033[2A')
        sleep(1)
    
    system('cls')
    
    #Setup playback process:
    print("Timer Completed! Good Work, your deserve a break!")
    file_path = "./sounds/" + sound_name
    
    if silent_mode:
        try:
            MB_OK = 0x00000
            MB_TOPMOST = 0x40000
            MB_SETFOREGROUND = 0x10000
            MB_SERVICE_NOTIFICATION = 0x200000
            uType = MB_OK | MB_SERVICE_NOTIFICATION
            
            MessageBox = ctypes.windll.user32.MessageBoxW
            MessageBox(None, "Timer Completed! Good Work, your deserve a break!", 'Alarm App', uType)
        except KeyboardInterrupt:
            pass
        finally:
            system('cls')
        
    else:
        
        print("Playing: ", sound_name, "\n\n")
    
        
        p = multiprocessing.Process(target = playsound, args = (file_path,))
        
        p.start()
        
        try:
            input("Press Enter to Stop Alarm.")
        
        except KeyboardInterrupt:
            pass
        
        finally:
            p.terminate()
            sys.stdout.write('\033[?25h')
            system('cls')
    
        

#MISSSING: ARGUMENTLESS ARGUMENTS ps -a
def parse_args():
    
    def aux(argv):
        arg_Q = False
        arg_kw = ""
        arg_dict = {}
        arg_path = argv[0]
        
        for arg in argv[1:]:
            
            if arg[:2] == "--":
                #Add argumentless arguments
                arg_kw, arg_val = arg[2:].split('=')
                
                try:
                    arg_kw = ARG_L["long"][arg_kw]
                    arg_dict[arg_kw] = ARG_TYPE_PARSER[arg_kw](arg_val)
                
                except:
                    print("Argument Error: Unkown keyword argument given")
                    arg_dict[arg_kw] = arg_val

            elif arg[0] == "-" and len(arg) != 1:
                try:
                    arg_kw = arg[1:]
                    arg_dict[arg_kw] = None
                    arg_Q = True
                    
                except:
                    arg_Q = False
                    print("ParseArgument Error")
            
            #Proper Arg Value
            elif arg_Q and arg[0] != "-":
                arg_Q = False
                
                arg_val = arg
                
                try:
                    arg_kw = ARG_L["short"][arg_kw]
                    #Raise Type Exception if arg_val is not correct
                    arg_dict[arg_kw] = ARG_TYPE_PARSER[arg_kw](arg_val)
                
                except:
                    print("Argument Error: Unkown keyword argument given or incorrect type given")
                    arg_dict[arg_kw] = arg_val
            
            else:
                arg_Q = False
                print("Invalid argument: Argument has no name, and will be ignored")         
                
        return arg_path, arg_dict
    
    return aux(sys.argv)        
        
    

if __name__ == '__main__':
    
    
    sleep_secs = 0
    sleep_mins = 0
    sleep_hours = 0
    quiet_Q = False


    
    filename, arg_dict = parse_args()  
    arg_dict_keys = arg_dict.keys() 
    
    if TIME_SLEEP_SECONDS in arg_dict_keys:
        sleep_secs = arg_dict[TIME_SLEEP_SECONDS]
    
    if TIME_SLEEP_MINUTES in arg_dict_keys:
        sleep_mins = arg_dict[TIME_SLEEP_MINUTES]
        
    if TIME_SLEEP_HOURS in arg_dict_keys:
        sleep_hours = arg_dict[TIME_SLEEP_HOURS]
        
    if SILENT_MODE in arg_dict_keys:
        quiet_Q = True
        
    if ALARM_SOUND_NAME in arg_dict_keys:
        sound_name = arg_dict[ALARM_SOUND_NAME]
        
        
        #print("Current Working Dir: ", getcwd())
        #print("Filename: ", filename)
        print(quiet_Q)
        system('cls')
        alarm(sound_name, sleep_secs, sleep_mins, sleep_hours, quiet_Q)
        
    else:
        print("Error: No sound name specified")
        
