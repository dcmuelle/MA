def BatteryDispatch(power_balance, battery_size, eta_discharge, max_c_charge, max_c_discharge):
    
    max_charge_power = max_c_charge*battery_size
    max_discharge_power = max_c_discharge*battery_size

    power_balance['SoC']= 0.0 # Battery state of charge (kWh)
    power_balance['Charging'] = 0.0 # Effective charging (kWh)
    power_balance['Discharging'] = 0.0 # Effective discharging (kWh)
    
    power_balance['PossibleCharging'] = power_balance['to Grid'] 
    power_balance['PossibleCharging'].clip(lower=0.0, upper=max_charge_power, inplace=True)
    power_balance['PossibleDischarging'] = -power_balance['from Grid']
    power_balance['PossibleDischarging'].clip(lower=-max_discharge_power, upper=0.0, inplace=True) 
    
    for i in range(1, len(power_balance)):
        deltaE = 0
        if power_balance['PossibleCharging'].values[i] > 0:
            if power_balance['SoC'].values[i-1] < (battery_size - power_balance['PossibleCharging'].values[i]):
                deltaE =  power_balance['PossibleCharging'].values[i]
                power_balance['Charging'].values[i] = power_balance['PossibleCharging'].values[i]
                            
            elif power_balance['SoC'].values[i-1] < battery_size:
                deltaE = battery_size - power_balance['SoC'].values[i-1]
                power_balance['Charging'].values[i] = deltaE
            power_balance['SoC'].values[i] = power_balance['SoC'].values[i-1] + deltaE  
                
        if -power_balance['PossibleDischarging'].values[i] > 0:                      
            if power_balance['SoC'].values[i-1] > -power_balance['PossibleDischarging'].values[i]/eta_discharge:
                deltaE = deltaE + power_balance['PossibleDischarging'].values[i]
                power_balance['Discharging'].values[i] = power_balance['PossibleDischarging'].values[i]
                power_balance['SoC'].values[i] = power_balance['SoC'].values[i-1] + deltaE/eta_discharge
            elif power_balance['SoC'].values[i-1] > 0:
                deltaE = deltaE - power_balance['SoC'].values[i-1]
                power_balance['Discharging'].values[i] = + eta_discharge*deltaE
                power_balance['SoC'].values[i] = power_balance['SoC'].values[i-1] + deltaE
         
        
    # Postprocess
    # Correct grid feed-in for energy going to or coming from the battery
    power_balance['to Grid New'] = power_balance['to Grid'] - power_balance['Charging']
    power_balance['from Grid New'] = power_balance['from Grid'] + power_balance['Discharging']
        
    return power_balance