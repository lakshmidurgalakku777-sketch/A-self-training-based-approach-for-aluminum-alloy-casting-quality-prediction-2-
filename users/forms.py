from django import forms

class PredictionForm(forms.Form):

    Pouring_Temperature = forms.FloatField(
        label="Pouring Temperature (°C)",
        help_text="The temperature of molten aluminum as it is poured into the mold."
    )

    Mold_Temperature = forms.FloatField(
        label="Mold Temperature (°C)",
        help_text="The initial temperature of the mold before pouring the molten metal."
    )

    Filling_Time = forms.FloatField(
        label="Filling Time (s)",
        help_text="Time taken to fill the mold cavity with molten aluminum."
    )

    Cooling_Time = forms.FloatField(
        label="Cooling Time (s)",
        help_text="Duration the casting is allowed to cool before being removed from the mold."
    )

    Injection_Pressure = forms.FloatField(
        label="Injection Pressure (MPa)",
        help_text="Pressure applied to inject molten metal into the mold cavity."
    )

    Holding_Pressure = forms.FloatField(
        label="Holding Pressure (MPa)",
        help_text="Sustained pressure applied after injection to minimize shrinkage."
    )

    Injection_Speed = forms.FloatField(
        label="Injection Speed (mm/s)",
        help_text="Speed at which molten metal is injected into the mold."
    )

    Cycle_Time = forms.FloatField(
        label="Cycle Time (s)",
        help_text="Total time for one full casting cycle (pouring to ejection)."
    )

    Al = forms.FloatField(
        label="Aluminum (Al %)",
        help_text="Percentage of aluminum in the alloy composition."
    )

    Si = forms.FloatField(
        label="Silicon (Si %)",
        help_text="Percentage of silicon, important for castability and strength."
    )

    Cu = forms.FloatField(
        label="Copper (Cu %)",
        help_text="Copper content, influences strength and machinability."
    )

    Mg = forms.FloatField(
        label="Magnesium (Mg %)",
        help_text="Magnesium content, affects strength and corrosion resistance."
    )

    Zn = forms.FloatField(
        label="Zinc (Zn %)",
        help_text="Zinc content, which can influence mechanical properties."
    )

    Fe = forms.FloatField(
        label="Iron (Fe %)",
        help_text="Iron content, typically kept low to avoid defects like porosity."
    )

    Mn = forms.FloatField(
        label="Manganese (Mn %)",
        help_text="Manganese content, improves ductility and toughness."
    )

    Ambient_Temperature = forms.FloatField(
        label="Ambient Temperature (°C)",
        help_text="Surrounding air temperature during the casting process."
    )

    Humidity = forms.FloatField(
        label="Humidity (%)",
        help_text="Relative humidity in the environment, which can affect cooling and defects."
    )

    Vibration_Level = forms.FloatField(
        label="Vibration Level (mm/s²)",
        help_text="Level of vibration in the machine, which may influence defect formation."
    )

    Tool_Wear_Level = forms.FloatField(
        label="Tool Wear Level (%)",
        help_text="Percentage wear of the casting tool or die, impacting product quality."
    )

    Lubricant_Flow_Rate = forms.FloatField(
        label="Lubricant Flow Rate (ml/min)",
        help_text="Flow rate of lubricant applied to the mold to aid release and reduce defects."
    )