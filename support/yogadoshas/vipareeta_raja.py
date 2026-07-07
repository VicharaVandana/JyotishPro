import support.generic as gen
import support.yogadoshas.common as common

def HarshaYoga(charts):
    IsHarshaYogaPresent = False
    
    cnt = 0
    Rule = ""
    Results = ""
    Note = f"In D1, the Harsha Yoga is impacted by association with Benefics and malefics. Also the results are subject to strength of ascendant and combustion with Sun\n"
    
    cond_SixthlordInSixth = False
    cond_EighthlordInSixth = False
    cond_TwelfthlordInSixth = False
    
    relevant_planets = set()

    for nth in [6, 8, 12]:
        lord = gen.get_nthLord(charts["D1"], nth)
        if (gen.get_planetPlacedHousenum(charts["D1"], lord) == 6):
            if nth == 6: cond_SixthlordInSixth = True
            if nth == 8: cond_EighthlordInSixth = True
            if nth == 12: cond_TwelfthlordInSixth = True
            
            cnt += 1
            lordsdetails = charts["D1"]["planets"][lord]
            Rule += f"Lord of house {nth} ({lord}) is placed in sixth house. "
            
            benefics = charts["D1"]["classifications"]["benefics"]
            malefics = charts["D1"]["classifications"]["malefics"] + ["Rahu", "Ketu"]
            
            aspectedby = charts["D1"]["planets"][lord]["Aspected-by"]
            conjuncts = charts["D1"]["planets"][lord]["conjuncts"]
            
            benefics_aspectinglord = list(set(benefics).intersection(aspectedby))
            benefics_conjunctlord = list(set(benefics).intersection(conjuncts))
            malefics_aspectinglord = list(set(malefics).intersection(aspectedby))
            malefics_conjunctlord = list(set(malefics).intersection(conjuncts))
            
            relevant_planets.add(lord)
            relevant_planets.add(lordsdetails["dispositor"])
            for planet in aspectedby + conjuncts:
                relevant_planets.add(planet)
                
            Note += f"Benefic planets aspecting {lord}: {benefics_aspectinglord} and conjunct benefics: {benefics_conjunctlord}. Malefic planets aspecting {lord}: {malefics_aspectinglord} and conjunct malefics: {malefics_conjunctlord}. "

    if (cond_SixthlordInSixth or cond_EighthlordInSixth or cond_TwelfthlordInSixth):
        IsHarshaYogaPresent = True
        Rule += f"Hence {cnt} count of Harsha yoga is formed in Native's D1 chart\n"
        Note += f"Consider all these points carefully before concluding the results of this Vipareeta rajayoga."
        
        Results = f'''Harsha Yoga is a Vipreeta Raja Yoga. As its name suggests, it is made up of two words - <Vipreeta> which means reverse and <Raja> which means a ruler. This presents a condition in the kundali of a person where the negatives add up to a positive outcome that can be life-altering. Fortunes are reversed wherein you receive benefits after a spate of bad luck.
        Vipreeta Raj Yoga is a contradictory yoga where you get the positive results from the paapi grahas. These grahas are notorious for causing malice and ill-will with their effects. But they face an advantageous position when they are in each other's houses and this results in positive outcomes.
        According to Phaladeepika, Harsha yoga native will be blessed with happiness, good fortune, and have a strong constitution. He will conquer his enemies and will not do sinful deeds. He will become a friend of illustrious, wealthy, splendorous, famous, and will have many friends.
        Harsha Vipreet Raj Yoga blesses the native with health and wealth. He or she is considered a leader who wins over enemies, earning much fame and glory'''

        key = f"HARSHA_D1"
        common.yogadoshas_dict[key] = {}
        common.yogadoshas_dict[key]["name"] = f"Harsha Vipareeta Raja (D1)"
        common.yogadoshas_dict[key]["type"] = "Yoga"
        common.yogadoshas_dict[key]["exist"] = True
        common.yogadoshas_dict[key]["Rule"] = common.iterativeReplace(Rule,"\n ", "\n")
        common.yogadoshas_dict[key]["Result"] = common.iterativeReplace(Results,"\n ", "\n").replace("\n","\n        ") 
        common.yogadoshas_dict[key]["Note"] = common.iterativeReplace(Note,"\n ", "\n")
        common.yogadoshas_dict[key]["Source"] = "https://www.sanatanveda.com/astrology/vipareeta-raja-yoga-in-vedic-astrology/"
        
        planet_list = list(relevant_planets)
        common.yogadoshas_dict[key]["relevant_planets"] = [p[0:2] for p in planet_list]
        

    return IsHarshaYogaPresent

def SaralaYoga(charts):
    IsSaralaYogaPresent = False
    
    cnt = 0
    Rule = ""
    Results = ""
    Note = f"In D1, the Sarala Yoga is impacted by association with Benefics and malefics. Also the results are subject to strength of ascendant and combustion with Sun\n"
    
    cond_SixthlordInEighth = False
    cond_EighthlordInEighth = False
    cond_TwelfthlordInEighth = False
    
    relevant_planets = set()

    for nth in [6, 8, 12]:
        lord = gen.get_nthLord(charts["D1"], nth)
        if (gen.get_planetPlacedHousenum(charts["D1"], lord) == 8):
            if nth == 6: cond_SixthlordInEighth = True
            if nth == 8: cond_EighthlordInEighth = True
            if nth == 12: cond_TwelfthlordInEighth = True
            
            cnt += 1
            lordsdetails = charts["D1"]["planets"][lord]
            Rule += f"Lord of house {nth} ({lord}) is placed in eighth house. "
            
            benefics = charts["D1"]["classifications"]["benefics"]
            malefics = charts["D1"]["classifications"]["malefics"] + ["Rahu", "Ketu"]
            
            aspectedby = charts["D1"]["planets"][lord]["Aspected-by"]
            conjuncts = charts["D1"]["planets"][lord]["conjuncts"]
            
            benefics_aspectinglord = list(set(benefics).intersection(aspectedby))
            benefics_conjunctlord = list(set(benefics).intersection(conjuncts))
            malefics_aspectinglord = list(set(malefics).intersection(aspectedby))
            malefics_conjunctlord = list(set(malefics).intersection(conjuncts))
            
            relevant_planets.add(lord)
            relevant_planets.add(lordsdetails["dispositor"])
            for planet in aspectedby + conjuncts:
                relevant_planets.add(planet)
                
            Note += f"Benefic planets aspecting {lord}: {benefics_aspectinglord} and conjunct benefics: {benefics_conjunctlord}. Malefic planets aspecting {lord}: {malefics_aspectinglord} and conjunct malefics: {malefics_conjunctlord}. "

    if (cond_SixthlordInEighth or cond_EighthlordInEighth or cond_TwelfthlordInEighth):
        IsSaralaYogaPresent = True
        Rule += f"Hence {cnt} count of Sarala yoga is formed in Native's D1 chart\n"
        Note += f"Consider all these points carefully before concluding the results of this Vipareeta rajayoga."
        
        Results = f'''Vipreeta Raj Yoga is a contradictory yoga where you get the positive results from the paapi grahas. These grahas are notorious for causing malice and ill-will with their effects. But they face an advantageous position when they are in each other's houses and this results in positive outcomes.
        According to Phaladeepika, Sarala yoga enables the natives to be long-lived, resolute, fearless, prosperous, learned, blessed with children, and wealth. The native with this yoga will achieve success in all his ventures, will be victorious over his enemies, and will be a great celebrity.
        Sarala Vipreeta Raja Yoga blesses the person with wisdom and power. It infuses the native with an air of authority and the sagacity to solve problems'''

        key = f"SARALA_D1"
        common.yogadoshas_dict[key] = {}
        common.yogadoshas_dict[key]["name"] = f"Sarala Vipareeta Raja (D1)"
        common.yogadoshas_dict[key]["type"] = "Yoga"
        common.yogadoshas_dict[key]["exist"] = True
        common.yogadoshas_dict[key]["Rule"] = common.iterativeReplace(Rule,"\n ", "\n")
        common.yogadoshas_dict[key]["Result"] = common.iterativeReplace(Results,"\n ", "\n").replace("\n","\n        ") 
        common.yogadoshas_dict[key]["Note"] = common.iterativeReplace(Note,"\n ", "\n")
        common.yogadoshas_dict[key]["Source"] = "https://www.sanatanveda.com/astrology/vipareeta-raja-yoga-in-vedic-astrology/"
        
        planet_list = list(relevant_planets)
        common.yogadoshas_dict[key]["relevant_planets"] = [p[0:2] for p in planet_list]
        

    return IsSaralaYogaPresent

def VimalaYoga(charts):
    IsVimalaYogaPresent = False
    
    cnt = 0
    Rule = ""
    Results = ""
    Note = f"In D1, the Vimala Yoga is impacted by association with Benefics and malefics. Also the results are subject to strength of ascendant and combustion with Sun\n"
    
    cond_SixthlordInTwelfth = False
    cond_EighthlordInTwelfth = False
    cond_TwelfthlordInTwelfth = False
    
    relevant_planets = set()

    for nth in [6, 8, 12]:
        lord = gen.get_nthLord(charts["D1"], nth)
        if (gen.get_planetPlacedHousenum(charts["D1"], lord) == 12):
            if nth == 6: cond_SixthlordInTwelfth = True
            if nth == 8: cond_EighthlordInTwelfth = True
            if nth == 12: cond_TwelfthlordInTwelfth = True
            
            cnt += 1
            lordsdetails = charts["D1"]["planets"][lord]
            Rule += f"Lord of house {nth} ({lord}) is placed in twelfth house. "
            
            benefics = charts["D1"]["classifications"]["benefics"]
            malefics = charts["D1"]["classifications"]["malefics"] + ["Rahu", "Ketu"]
            
            aspectedby = charts["D1"]["planets"][lord]["Aspected-by"]
            conjuncts = charts["D1"]["planets"][lord]["conjuncts"]
            
            benefics_aspectinglord = list(set(benefics).intersection(aspectedby))
            benefics_conjunctlord = list(set(benefics).intersection(conjuncts))
            malefics_aspectinglord = list(set(malefics).intersection(aspectedby))
            malefics_conjunctlord = list(set(malefics).intersection(conjuncts))
            
            relevant_planets.add(lord)
            relevant_planets.add(lordsdetails["dispositor"])
            for planet in aspectedby + conjuncts:
                relevant_planets.add(planet)
                
            Note += f"Benefic planets aspecting {lord}: {benefics_aspectinglord} and conjunct benefics: {benefics_conjunctlord}. Malefic planets aspecting {lord}: {malefics_aspectinglord} and conjunct malefics: {malefics_conjunctlord}. "

    if (cond_SixthlordInTwelfth or cond_EighthlordInTwelfth or cond_TwelfthlordInTwelfth):
        IsVimalaYogaPresent = True
        Rule += f"Hence {cnt} count of Vimala yoga is formed in Native's D1 chart\n"
        Note += f"Consider all these points carefully before concluding the results of this Vipareeta rajayoga."
        
        Results = f'''Vipreeta Raja Yoga is a contradictory yoga where you get the positive results from the paapi grahas. These grahas are notorious for causing malice and ill-will with their effects. But they face an advantageous position when they are in each other's houses and this results in positive outcomes.
        According to Phaladeepika, The native with Vimala yoga will be clever in saving money, frugal in his expenses, equipped with good behavior towards others, will enjoy happiness, will be independent, will follow a respectable profession or conduct, and will be well known for his good qualities.
        The native with Vimala yoga will be good at accumulating wealth, good in financial management, spend less, enjoy the pleasures, he also charitable in nature, will be famous in the circle. On the other side, he will also spend on hospitalization, hostile to learned people, will get into unnecessary arguments, short-lived. This yoga also blesses the person with a positive attitude, an honourable career and a spiritual approach to life.'''

        key = f"VIMALA_D1"
        common.yogadoshas_dict[key] = {}
        common.yogadoshas_dict[key]["name"] = f"Vimala Vipareeta Raja (D1)"
        common.yogadoshas_dict[key]["type"] = "Yoga"
        common.yogadoshas_dict[key]["exist"] = True
        common.yogadoshas_dict[key]["Rule"] = common.iterativeReplace(Rule,"\n ", "\n")
        common.yogadoshas_dict[key]["Result"] = common.iterativeReplace(Results,"\n ", "\n").replace("\n","\n        ") 
        common.yogadoshas_dict[key]["Note"] = common.iterativeReplace(Note,"\n ", "\n")
        common.yogadoshas_dict[key]["Source"] = "https://www.sanatanveda.com/astrology/vipareeta-raja-yoga-in-vedic-astrology/"
        
        planet_list = list(relevant_planets)
        common.yogadoshas_dict[key]["relevant_planets"] = [p[0:2] for p in planet_list]
        

    return IsVimalaYogaPresent
