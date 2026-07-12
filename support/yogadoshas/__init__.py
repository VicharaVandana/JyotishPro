import support.generic as gen
import support.astrochart as ac
import support.lordinhouses as lh
from .panchamahapurusha import SasaYoga, BhadraYoga, HamsaYoga, MalavyaYoga, RuchakaYoga
from .vipareeta_raja import HarshaYoga, SaralaYoga, VimalaYoga
from .kaala_sarpa import kaalSarpaDosha, AnantaKaalSarpaDosha, KulikaKaalSarpaDosha, VasukiKaalSarpaDosha, ShankhapalaKaalSarpaDosha, PadamKaalSarpaDosha, MahapadmaKaalSarpaDosha, TakshakaKaalSarpaDosha, KarkotakKaalSarpaDosha, ShankhachurKaalSarpaDosha, GhatakKaalSarpaDosha, VishadharaKaalSarpaDosha, SheshanagaKaalSarpaDosha
from .chandra_yogadoshas import ChandraYogaDoshas
from .kuja_dosha import KujaDosha
from .other_yogas import GajaKesariYoga, ChandraMangalaYoga
from .amala_yoga import AmalaYoga
from .nabhasa_yogas import ParivarthanaYoga, AashrayaYoga, DalaYoga, AakritiYoga, SankhyaYoga
from .raja_yogas import DharmaKarmadhipatiYoga, NeechaBhangaRajaYoga, KendraTrikonaYoga, SreenathaYoga

# Note: Placeholder for dhana_yogas will be imported here when functions are added.


# ==========================================================================================
# Function Name: ComputeYogaDoshas
# Purpose: Calculates the presence of ComputeYogaDoshas in the provided horoscope.
# Description: Evaluates standard planetary configurations.
# Expected Impact: Returns boolean indicating presence.
# Parameters:
#   - charts (dict): Comprehensive dictionary containing D1, D9 charts and planetary attributes.
# Returns:
#   - Boolean/String: True if the yoga/dosha is present, False otherwise.
# ==========================================================================================
def ComputeYogaDoshas(charts):

    # This is to reset the globas if Compute is called consecutively for different chart selections 
    # instead of appending on top of it resulting duplicate appending
    import support.yogadoshas.common as common
    common.reset_globals()

    charts["yogadoshas"] = []

    # Panchamahapurusha yogas
    SasaYoga(charts)
    BhadraYoga(charts)
    HamsaYoga(charts)
    MalavyaYoga(charts)
    RuchakaYoga(charts)
    
    # Vipareeta Raja yogas
    HarshaYoga(charts)
    SaralaYoga(charts)
    VimalaYoga(charts)

    # Major Raja Yogas
    DharmaKarmadhipatiYoga(charts)
    NeechaBhangaRajaYoga(charts)
    KendraTrikonaYoga(charts)
    SreenathaYoga(charts)
    
    # Gaja Kesari Yoga
    GajaKesariYoga(charts)
    
    ChandraMangalaYoga(charts)
    AmalaYoga(charts)
    ChandraYogaDoshas(charts)   # Sunapha / Anapha / Durdhara / Kemadruma
    KujaDosha(charts)
    
    # Nabhasa Yogas
    ParivarthanaYoga(charts)
    AashrayaYoga(charts)
    DalaYoga(charts)
    AakritiYoga(charts)
    SankhyaYoga(charts)

    #Kaalasarpa

    AnantaKaalSarpaDosha(charts)
    KulikaKaalSarpaDosha(charts)
    VasukiKaalSarpaDosha(charts)
    ShankhapalaKaalSarpaDosha(charts)
    PadamKaalSarpaDosha(charts)
    MahapadmaKaalSarpaDosha(charts)
    TakshakaKaalSarpaDosha(charts)
    KarkotakKaalSarpaDosha(charts)
    ShankhachurKaalSarpaDosha(charts)
    GhatakKaalSarpaDosha(charts)
    VishadharaKaalSarpaDosha(charts)
    SheshanagaKaalSarpaDosha(charts)


    # Reconstruct the string array for backward compatibility and list display
    for key, data in common.yogadoshas_dict.items():
        if data.get("exist", False):
            # For list of strings just display the name (append division info if you want)
            # if it was SasaYoga_D9, its name is already updated to "Sasa Panchamahapurusha Yoga (D9)" by the function
            charts["yogadoshas"].append(data["name"])

    return charts["yogadoshas"]
