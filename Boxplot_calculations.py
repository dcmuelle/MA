{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "olympic-particle",
   "metadata": {},
   "outputs": [],
   "source": [
    "def Boxplot_calculations(meteo_data):\n",
    "meteo_data = meteo_data[meteo_data.time.dt.year == year]\n",
    "hourly_average=meteo_data.groupby([meteo_data[\"time\"].dt.month, meteo_data[\"time\"].dt.day, meteo_data[\"time\"].dt.hour]).mean()\n",
    "hourly_average.index.names = [\"month\", \"day\", \"hour\"]\n",
    "hourly_average['Prod/m2'] = hourly_average['G(i)']*0.17/1000\n",
    "hourly_average['Prod'] = hourly_average['Prod/m2']*size\n",
    "yearly_PV_prod = hourly_average['Prod'].sum()\n",
    "PV_production = hourly_average['Prod']\n",
    "power_balance = pd.DataFrame()\n",
    "power_balance['consumption'] = total_elec_load\n",
    "power_balance['from PV'] = PV_production\n",
    "power_balance['exchange grid'] = PV_production - total_elec_load\n",
    "power_balance['to Grid'] = (PV_production - total_elec_load).clip(lower=0)\n",
    "power_balance['from Grid'] = (total_elec_load - PV_production).clip(lower=0)\n",
    "power_balance = power_balance.fillna(0)\n",
    "total_elec_load = load_SFH_modern_full_retrofit['Total Electricity without AC']\n",
    "power_balance = pd.DataFrame()\n",
    "power_balance['consumption'] = total_elec_load\n",
    "power_balance['from PV'] = PV_production\n",
    "power_balance['exchange grid'] = PV_production - total_elec_load\n",
    "power_balance['to Grid'] = (PV_production - total_elec_load).clip(lower=0)\n",
    "power_balance['from Grid'] = (total_elec_load - PV_production).clip(lower=0)\n",
    "power_balance = power_balance.fillna(0)\n",
    "power_balance = BatteryDispatch(power_balance, battery_size, eta_discharge, max_c_charge, max_c_discharge)\n",
    "power_balance['exchange grid new'] = power_balance['to Grid New'] - power_balance['from Grid New']"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.6.9"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
