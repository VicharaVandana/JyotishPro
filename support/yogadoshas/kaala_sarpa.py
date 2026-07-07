import support.generic as gen
import support.yogadoshas.common as common

def kaalSarpaDosha(charts):
    #Check if kaal sarpa dosha exists. 
    #return value can be ABSENT, ASCENDPRESENT, DESCENDPRESENT

    #For Kaal sarpa dosha to be present, All 7 planets must be on the same side of Rahu Ketu Axis in D1 chart
    #If planets are present right side of Rahu-Ketu axis then its ascending kaala sarpa dosha else its descending

    IsKaalSarpaDoshaPresent = True  #initially assume the dosha is present. 
    #Check distance between Rahu and Sun
    baseplanet = "Rahu"
    dist = gen.get_distancebetweenplanets(charts["D1"], baseplanet, "Sun")
    if (dist > (180*3600)): #If sun is greater than sun is in the right side of rahu ketu axis. so lets make Ketu as base planet
        baseplanet = "Ketu"
    
    #now lets check if all other 6 planets are also same side of rahu ketu axis as sub. 
    #So now distance between any of 6 remaining planets from baseplanet must not be more than 180 degrees for kaal sarpa dosha to exist
    for planet in ["Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]:
        dist = gen.get_distancebetweenplanets(charts["D1"], baseplanet, planet)
        if (dist > (180*3600)): #Rahu ketu axis is broken
            IsKaalSarpaDoshaPresent = False
            break   #end for loop once kaal sarpa dosha is broken
    
    if(IsKaalSarpaDoshaPresent == True):
        if (baseplanet == "Rahu"):
            retval = "DESCENDPRESENT"
        else:
            retval = "ASCENDPRESENT"
    else:
         retval = "ABSENT"
    
    return retval

    #Ananta Kaal sarpa dosha - Kaalsarpa dosha with Rahu in Tan bhav
def AnantaKaalSarpaDosha(charts):
    IsGlobalPresent = False
    IsAnantaKaalSarpaDoshaPresent = False
    Name = ""
    Rule = ""
    Results = ""
    Note = ""
    Remedies = ""
    
    KaalSarpDoshaSts = kaalSarpaDosha(charts)
    if (KaalSarpDoshaSts != "ABSENT") and (charts["D1"]["planets"]["Rahu"]["house-num"] == 1):
        IsAnantaKaalSarpaDoshaPresent = True
        colorlist = ["pink","pink","pink","pink","pink","pink","pink","pink","pink","pink","pink","pink"]
        colorlist[1-1] = "yellow"
        colorlist[7-1] = "yellow"
        #Update the Name and Rule
        if (KaalSarpDoshaSts == "ASCENDPRESENT"):
            Name = "Ascending Ananta Kaala Sarpa"
            typ = "Ascending"
            Rule = f'''All the remaining 7 planets are in the same side of Rahu-Ketu Axis forming Kaala Sarpa Dosha. Since Rahu is in 1st house and Ketu is in 7th house this is Ananta Kaala Sarpa Dosha. All the planets are right side of Rahu-Ketu Axis heading towards Rahu So its Ascending Ananta Kaala Sarpa Dosha.
            '''
        else:
            Name = "Descending Ananta Kaala Sarpa"
            typ = "Descending"
            Rule = f'''All the remaining 7 planets are in the same side of Rahu-Ketu Axis forming Kaala Sarpa Dosha. Since Rahu is in 1st house and Ketu is in 7th house this is Ananta Kaala Sarpa Dosha. All the planets are left side of Rahu-Ketu Axis heading towards Ketu So its Descending Ananta Kaala Sarpa Dosha.
            '''
        #Update the Results of Ananta Kaala Sarpa Dosha
        Results = f'''Kaal Sarp Dosha is a frightful astrological event that affects a person severely with multifaceted catastrophes. It is a result of bad karma done by the native in the previous lives.
        As Kaalsarp dosh veils the planets, the aspects other planets represent may get hampered, which may lead to problems in the life of the native. So the results from aspects of other planets will be blocked by Rahu-Ketu axis and the native will not be ble to get full results of other planets in his kundali.
        The natives with Ananta kaala sarpa dosha will have to struggle for longer to find success. Although you will work very hard in order to succeed, but the results will come to you after a delay. The Anant Kaalsarp dosh will likely test your patience by introducing you to constant obstacles and challenges. Due to this dosha, a person faces problems in all aspects of their lives, but if you don't lose hope, you will find success later. 
        Also, don't indulge in ill deeds such as gambling, lust, etc.
        '''
        #Update the Note
        Note = "The effect of Ananta Kaala Sarpa Dosha will decrease after the age of 27 if other strong Yogas are present in Native's Kundali."
        #update Remedies for Dosha
        Remedies = f'''One of the most effective remedies to reduce the effects of the Kala Sarpa Dosha is visiting shrines of higher spiritual beings. The popular places to visit include Srikalahasti temple, Trimbakeshwar temple, Rameswaram, and Thirunageswaram. The Kalasarpa Dosha Nivaran Puja at Sri Kalahasti mandir, Rameswaram, and Thirunageswaram, is considered the best remedy for Kala Sarpa Dosha. This Dosha can also be remedied by Kal Rudra Yagna performed in these temples.
        Rudra Avisek of Shiva, in any Shiva Temple, and chanting of powerful mantras like the Mrityunjay Mantra, Vishnu Panchakshari Mantra, and Sarp Mantra are the other popular remedies for this Dosha.
        Specifically for Ananta Kaal Sarpa dosha can be solved or atleast impact be reduced by Reading Hanuman Chalisa five times a day for 40 days. If you are a student, you should chant the 'Saraswati Mantra' and 'Saraswatye Namah' for 10-15 minutes daily.'''
        
        relevant_planets = ["Su", "Mo", "Ma", "Me", "Ju", "Ve", "Sa", "Ra", "Ke"]
    
    
    
        #Update the yogadosha sections
        common.yogadoshas_dict["ANANTAKAALSARPA"] = {}
        common.yogadoshas_dict["ANANTAKAALSARPA"]["name"] = Name
        common.yogadoshas_dict["ANANTAKAALSARPA"]["type"] = "Dosha"
        common.yogadoshas_dict["ANANTAKAALSARPA"]["exist"] = IsAnantaKaalSarpaDoshaPresent
        common.yogadoshas_dict["ANANTAKAALSARPA"]["Rule"] = common.iterativeReplace(Rule,"\n ", "\n")
        common.yogadoshas_dict["ANANTAKAALSARPA"]["Result"] = common.iterativeReplace(Results,"\n ", "\n").replace("\n","\n        ") 
        common.yogadoshas_dict["ANANTAKAALSARPA"]["Remedies"] = common.iterativeReplace(Remedies,"\n ", "\n").replace("\n","\n        ")
        common.yogadoshas_dict["ANANTAKAALSARPA"]["Note"] = common.iterativeReplace(Note,"\n ", "\n")
        common.yogadoshas_dict["ANANTAKAALSARPA"]["Source"] = "https://astrotalk.com/kaal-sarp-dosh-12-types"
        if 'relevant_planets' in locals():
            common.yogadoshas_dict["ANANTAKAALSARPA"]["relevant_planets"] = relevant_planets
        elif 'relevant_planets2' in locals():
            common.yogadoshas_dict["ANANTAKAALSARPA"]["relevant_planets"] = relevant_planets2
    
    return IsGlobalPresent

    #Kulika Kaal sarpa dosha - Kaalsarpa dosha with Rahu in Tan bhav
def KulikaKaalSarpaDosha(charts):
    IsGlobalPresent = False
    IsKulikaKaalSarpaDoshaPresent = False
    Name = ""
    Rule = ""
    Results = ""
    Note = ""
    Remedies = ""
    
    KaalSarpDoshaSts = kaalSarpaDosha(charts)
    if (KaalSarpDoshaSts != "ABSENT") and (charts["D1"]["planets"]["Rahu"]["house-num"] == 2):
        IsKulikaKaalSarpaDoshaPresent = True
        colorlist = ["pink","pink","pink","pink","pink","pink","pink","pink","pink","pink","pink","pink"]
        colorlist[2-1] = "yellow"
        colorlist[8-1] = "yellow"
        #Update the Name and Rule
        if (KaalSarpDoshaSts == "ASCENDPRESENT"):
            Name = "Ascending Kulika Kaala Sarpa"
            typ = "Ascending"
            Rule = f'''All the remaining 7 planets are in the same side of Rahu-Ketu Axis forming Kaala Sarpa Dosha. Since Rahu is in 2nd house and Ketu is in 8th house this is Kulika Kaala Sarpa Dosha. All the planets are right side of Rahu-Ketu Axis heading towards Rahu So its Ascending Kulika Kaala Sarpa Dosha.
            '''
        else:
            Name = "Descending Kulika Kaala Sarpa"
            typ = "Descending"
            Rule = f'''All the remaining 7 planets are in the same side of Rahu-Ketu Axis forming Kaala Sarpa Dosha. Since Rahu is in 2nd house and Ketu is in 8th house this is Kulika Kaala Sarpa Dosha. All the planets are left side of Rahu-Ketu Axis heading towards Ketu So its Descending Kulika Kaala Sarpa Dosha.
            '''
        #Update the Results of Kulika Kaala Sarpa Dosha
        Results = f'''Kaal Sarp Dosha is a frightful astrological event that affects a person severely with multifaceted catastrophes. It is a result of bad karma done by the native in the previous lives.
        As Kaalsarp dosh veils the planets, the aspects other planets represent may get hampered, which may lead to problems in the life of the native. So the results from aspects of other planets will be blocked by Rahu-Ketu axis and the native will not be ble to get full results of other planets in his kundali.
        The Kulika kaala sarpa dosha is believed to bring economic losses, humiliation, debt and various other obstacles in the native's life. Hence astrologers suggest that you don't form bondings with people without careful scrutiny. If you are into business, make sure you do it with 100% honesty, especially during the Kulik dosh period. 
        When it comes to married life, it is to remain normal for the native dealing with Kulika dosh. You however may feel that you are getting old before time, thus you must invest in taking care of your health. Do not use intoxicants such as cigarettes, tobacco, etc
        Defamations, scandals, unstable marital life, problems from inheritance, financial issues, etc. are connected with this Dosha.
        '''
        #Update the Note
        Note = "The effect of Kulika Kaala Sarpa Dosha will decrease after the age of 33 if other strong Yogas are present in Native's Kundali."
        #update Remedies for Dosha
        Remedies = f'''One of the most effective remedies to reduce the effects of the Kala Sarpa Dosha is visiting shrines of higher spiritual beings. The popular places to visit include Srikalahasti temple, Trimbakeshwar temple, Rameswaram, and Thirunageswaram. The Kalasarpa Dosha Nivaran Puja at Sri Kalahasti mandir, Rameswaram, and Thirunageswaram, is considered the best remedy for Kala Sarpa Dosha. This Dosha can also be remedied by Kal Rudra Yagna performed in these temples.
        Rudra Avisek of Shiva, in any Shiva Temple, and chanting of powerful mantras like the Mrityunjay Mantra, Vishnu Panchakshari Mantra, and Sarp Mantra are the other popular remedies for this Dosha.
        Specifically, Kulika Kaal Sarpa dosha can be solved or atleast impact be reduced by lighting a lamp of mustard oil in front of the Hanuman idol on every saturday evening. Hold energised Silver Rahu Yantra on Saturday'''
        
        relevant_planets = ["Su", "Mo", "Ma", "Me", "Ju", "Ve", "Sa", "Ra", "Ke"]
    
    
    
        #Update the yogadosha sections
        common.yogadoshas_dict["KULIKAKAALSARPA"] = {}
        common.yogadoshas_dict["KULIKAKAALSARPA"]["name"] = Name
        common.yogadoshas_dict["KULIKAKAALSARPA"]["type"] = "Dosha"
        common.yogadoshas_dict["KULIKAKAALSARPA"]["exist"] = IsKulikaKaalSarpaDoshaPresent
        common.yogadoshas_dict["KULIKAKAALSARPA"]["Rule"] = common.iterativeReplace(Rule,"\n ", "\n")
        common.yogadoshas_dict["KULIKAKAALSARPA"]["Result"] = common.iterativeReplace(Results,"\n ", "\n").replace("\n","\n        ") 
        common.yogadoshas_dict["KULIKAKAALSARPA"]["Remedies"] = common.iterativeReplace(Remedies,"\n ", "\n").replace("\n","\n        ")
        common.yogadoshas_dict["KULIKAKAALSARPA"]["Note"] = common.iterativeReplace(Note,"\n ", "\n")
        common.yogadoshas_dict["KULIKAKAALSARPA"]["Source"] = "https://astrotalk.com/kaal-sarp-dosh-12-types"
        if 'relevant_planets' in locals():
            common.yogadoshas_dict["KULIKAKAALSARPA"]["relevant_planets"] = relevant_planets
        elif 'relevant_planets2' in locals():
            common.yogadoshas_dict["KULIKAKAALSARPA"]["relevant_planets"] = relevant_planets2
    
    return IsGlobalPresent

    #Vasuki Kaal sarpa dosha - Kaalsarpa dosha with Rahu in Tan bhav
def VasukiKaalSarpaDosha(charts):
    IsGlobalPresent = False
    IsVasukiKaalSarpaDoshaPresent = False
    Name = ""
    Rule = ""
    Results = ""
    Note = ""
    Remedies = ""
    
    KaalSarpDoshaSts = kaalSarpaDosha(charts)
    if (KaalSarpDoshaSts != "ABSENT") and (charts["D1"]["planets"]["Rahu"]["house-num"] == 3):
        IsVasukiKaalSarpaDoshaPresent = True
        colorlist = ["pink","pink","pink","pink","pink","pink","pink","pink","pink","pink","pink","pink"]
        colorlist[3-1] = "yellow"
        colorlist[9-1] = "yellow"
        #Update the Name and Rule
        if (KaalSarpDoshaSts == "ASCENDPRESENT"):
            Name = "Ascending Vasuki Kaala Sarpa"
            typ = "Ascending"
            Rule = f'''All the remaining 7 planets are in the same side of Rahu-Ketu Axis forming Kaala Sarpa Dosha. Since Rahu is in 3rd house and Ketu is in 9th house this is Vasuki Kaala Sarpa Dosha. All the planets are right side of Rahu-Ketu Axis heading towards Rahu So its Ascending Vasuki Kaala Sarpa Dosha.
            '''
        else:
            Name = "Descending Vasuki Kaala Sarpa"
            typ = "Descending"
            Rule = f'''All the remaining 7 planets are in the same side of Rahu-Ketu Axis forming Kaala Sarpa Dosha. Since Rahu is in 3rd house and Ketu is in 9th house this is Vasuki Kaala Sarpa Dosha. All the planets are left side of Rahu-Ketu Axis heading towards Ketu So its Descending Vasuki Kaala Sarpa Dosha.
            '''
        #Update the Results of Vasuki Kaala Sarpa Dosha
        Results = f'''Kaal Sarp Dosha is a frightful astrological event that affects a person severely with multifaceted catastrophes. It is a result of bad karma done by the native in the previous lives.
        As Kaalsarp dosh veils the planets, the aspects other planets represent may get hampered, which may lead to problems in the life of the native. So the results from aspects of other planets will be blocked by Rahu-Ketu axis and the native will not be ble to get full results of other planets in his kundali.
        The Vasuki kaala sarpa dosha doesn't only hamper the life of the native but also of the ones related to him, such as his siblings, parents, spouse, etc. You have to face the fact that your family members may cheat on you. There will likely be a lack of peace in the family, and the peace will further shatter with inflating economic problems as the Vasuki Kaalsarp dosh continues. 
        However, the good thing is that the person will have economic success as he continues to put in the hard work in making sure things work out for him. 
        The individual would not get the desired results of their hard work and receive their rewards late in life. This Dosha may cause losses in business too.
        '''
        #Update the Note
        Note = "The effect of Vasuki Kaala Sarpa Dosha will decrease after the age of 36 if other strong Yogas are present in Native's Kundali."
        #update Remedies for Dosha
        Remedies = f'''One of the most effective remedies to reduce the effects of the Kala Sarpa Dosha is visiting shrines of higher spiritual beings. The popular places to visit include Srikalahasti temple, Trimbakeshwar temple, Rameswaram, and Thirunageswaram. The Kalasarpa Dosha Nivaran Puja at Sri Kalahasti mandir, Rameswaram, and Thirunageswaram, is considered the best remedy for Kala Sarpa Dosha. This Dosha can also be remedied by Kal Rudra Yagna performed in these temples.
        Rudra Avisek of Shiva, in any Shiva Temple, and chanting of powerful mantras like the Mrityunjay Mantra, Vishnu Panchakshari Mantra, and Sarp Mantra are the other popular remedies for this Dosha.
        Specifically, Vasuki Kaal Sarpa dosha can be solved or atleast impact be reduced by reading Hanuman Chalisa and Bajrang Baan 5 times for 40 days. Hold energised Silver Rahu Yantra on Saturday. 
        Also every Wednesday keep a handful of Urad dal in a black cloth, and chant the Rahu spell mantra and flow the Urad in the water.'''
        
        relevant_planets = ["Su", "Mo", "Ma", "Me", "Ju", "Ve", "Sa", "Ra", "Ke"]
    
    
    
        #Update the yogadosha sections
        common.yogadoshas_dict["VASUKIKAALSARPA"] = {}
        common.yogadoshas_dict["VASUKIKAALSARPA"]["name"] = Name
        common.yogadoshas_dict["VASUKIKAALSARPA"]["type"] = "Dosha"
        common.yogadoshas_dict["VASUKIKAALSARPA"]["exist"] = IsVasukiKaalSarpaDoshaPresent
        common.yogadoshas_dict["VASUKIKAALSARPA"]["Rule"] = common.iterativeReplace(Rule,"\n ", "\n")
        common.yogadoshas_dict["VASUKIKAALSARPA"]["Result"] = common.iterativeReplace(Results,"\n ", "\n").replace("\n","\n        ") 
        common.yogadoshas_dict["VASUKIKAALSARPA"]["Remedies"] = common.iterativeReplace(Remedies,"\n ", "\n").replace("\n","\n        ")
        common.yogadoshas_dict["VASUKIKAALSARPA"]["Note"] = common.iterativeReplace(Note,"\n ", "\n")
        common.yogadoshas_dict["VASUKIKAALSARPA"]["Source"] = "https://astrotalk.com/kaal-sarp-dosh-12-types"
        if 'relevant_planets' in locals():
            common.yogadoshas_dict["VASUKIKAALSARPA"]["relevant_planets"] = relevant_planets
        elif 'relevant_planets2' in locals():
            common.yogadoshas_dict["VASUKIKAALSARPA"]["relevant_planets"] = relevant_planets2
    
    return IsGlobalPresent

    #Shankhapala Kaal sarpa dosha - Kaalsarpa dosha with Rahu in Tan bhav
def ShankhapalaKaalSarpaDosha(charts):
    IsGlobalPresent = False
    IsShankhapalaKaalSarpaDoshaPresent = False
    Name = ""
    Rule = ""
    Results = ""
    Note = ""
    Remedies = ""
    
    KaalSarpDoshaSts = kaalSarpaDosha(charts)
    if (KaalSarpDoshaSts != "ABSENT") and (charts["D1"]["planets"]["Rahu"]["house-num"] == 4):
        IsShankhapalaKaalSarpaDoshaPresent = True
        colorlist = ["pink","pink","pink","pink","pink","pink","pink","pink","pink","pink","pink","pink"]
        colorlist[4-1] = "yellow"
        colorlist[10-1] = "yellow"
        #Update the Name and Rule
        if (KaalSarpDoshaSts == "ASCENDPRESENT"):
            Name = "Ascending Shankhapala Kaala Sarpa"
            typ = "Ascending"
            Rule = f'''All the remaining 7 planets are in the same side of Rahu-Ketu Axis forming Kaala Sarpa Dosha. Since Rahu is in 4th house and Ketu is in 10th house this is Shankhapala Kaala Sarpa Dosha. All the planets are right side of Rahu-Ketu Axis heading towards Rahu So its Ascending Shankhapala Kaala Sarpa Dosha.
            '''
        else:
            Name = "Descending Shankhapala Kaala Sarpa"
            typ = "Descending"
            Rule = f'''All the remaining 7 planets are in the same side of Rahu-Ketu Axis forming Kaala Sarpa Dosha. Since Rahu is in 4th house and Ketu is in 10th house this is Shankhapala Kaala Sarpa Dosha. All the planets are left side of Rahu-Ketu Axis heading towards Ketu So its Descending Shankhapala Kaala Sarpa Dosha.
            '''
        #Update the Results of Shankhapala Kaala Sarpa Dosha
        Results = f'''Kaal Sarp Dosha is a frightful astrological event that affects a person severely with multifaceted catastrophes. It is a result of bad karma done by the native in the previous lives.
        As Kaalsarp dosh veils the planets, the aspects other planets represent may get hampered, which may lead to problems in the life of the native. So the results from aspects of other planets will be blocked by Rahu-Ketu axis and the native will not be ble to get full results of other planets in his kundali.
        The Shankhapala kaala sarpa dosha is the signal of incoming financial hardship, disease and disorder in the native's life. Hence, he/she should prepare for it. During this period, the happiness in the native's family will plunge to new lows. This may further hamper elements such as love, child's education, etc. 
        If a youngster, the native will find it tough to make the right choices, due to which he or she may find it difficult to settle early in life. The people of this yoga have to face difficulties related to land and property, thus any such deals must be done after proper scrutiny.
        '''
        #Update the Note
        Note = "The effect of Shankhapala Kaala Sarpa Dosha will decrease after the age of 43 if other strong Yogas are present in Native's Kundali."
        #update Remedies for Dosha
        Remedies = f'''One of the most effective remedies to reduce the effects of the Kala Sarpa Dosha is visiting shrines of higher spiritual beings. The popular places to visit include Srikalahasti temple, Trimbakeshwar temple, Rameswaram, and Thirunageswaram. The Kalasarpa Dosha Nivaran Puja at Sri Kalahasti mandir, Rameswaram, and Thirunageswaram, is considered the best remedy for Kala Sarpa Dosha. This Dosha can also be remedied by Kal Rudra Yagna performed in these temples.
        Rudra Avisek of Shiva, in any Shiva Temple, and chanting of powerful mantras like the Mrityunjay Mantra, Vishnu Panchakshari Mantra, and Sarp Mantra are the other popular remedies for this Dosha.
        Specifically, Shankhapala Kaal Sarpa dosha can be solved or atleast impact be reduced by hanging Hanuman Bahuk in red cloth on any Tuesday on the wall towards the south side of the house. On any Friday, flush the water coconut in water during the day. 
        you can also hang Hanuman Bahuk in red cloth on any Tuesday on the wall towards the south side of the house.'''
        
        relevant_planets = ["Su", "Mo", "Ma", "Me", "Ju", "Ve", "Sa", "Ra", "Ke"]
    
    
    
        #Update the yogadosha sections
        common.yogadoshas_dict["SHANKHAPALAKAALSARPA"] = {}
        common.yogadoshas_dict["SHANKHAPALAKAALSARPA"]["name"] = Name
        common.yogadoshas_dict["SHANKHAPALAKAALSARPA"]["type"] = "Dosha"
        common.yogadoshas_dict["SHANKHAPALAKAALSARPA"]["exist"] = IsShankhapalaKaalSarpaDoshaPresent
        common.yogadoshas_dict["SHANKHAPALAKAALSARPA"]["Rule"] = common.iterativeReplace(Rule,"\n ", "\n")
        common.yogadoshas_dict["SHANKHAPALAKAALSARPA"]["Result"] = common.iterativeReplace(Results,"\n ", "\n").replace("\n","\n        ") 
        common.yogadoshas_dict["SHANKHAPALAKAALSARPA"]["Remedies"] = common.iterativeReplace(Remedies,"\n ", "\n").replace("\n","\n        ")
        common.yogadoshas_dict["SHANKHAPALAKAALSARPA"]["Note"] = common.iterativeReplace(Note,"\n ", "\n")
        common.yogadoshas_dict["SHANKHAPALAKAALSARPA"]["Source"] = "https://astrotalk.com/kaal-sarp-dosh-12-types"
        if 'relevant_planets' in locals():
            common.yogadoshas_dict["SHANKHAPALAKAALSARPA"]["relevant_planets"] = relevant_planets
        elif 'relevant_planets2' in locals():
            common.yogadoshas_dict["SHANKHAPALAKAALSARPA"]["relevant_planets"] = relevant_planets2
    
    return IsGlobalPresent

    #Padam Kaal sarpa dosha - Kaalsarpa dosha with Rahu in Santaan bhav
def PadamKaalSarpaDosha(charts):
    IsGlobalPresent = False
    IsPadamKaalSarpaDoshaPresent = False
    Name = ""
    Rule = ""
    Results = ""
    Note = ""
    Remedies = ""
    
    KaalSarpDoshaSts = kaalSarpaDosha(charts)
    if (KaalSarpDoshaSts != "ABSENT") and (charts["D1"]["planets"]["Rahu"]["house-num"] == 5):
        IsPadamKaalSarpaDoshaPresent = True
        colorlist = ["pink","pink","pink","pink","pink","pink","pink","pink","pink","pink","pink","pink"]
        colorlist[5-1] = "yellow"
        colorlist[11-1] = "yellow"
        #Update the Name and Rule
        if (KaalSarpDoshaSts == "ASCENDPRESENT"):
            Name = "Ascending Padam Kaala Sarpa"
            typ = "Ascending"
            Rule = f'''All the remaining 7 planets are in the same side of Rahu-Ketu Axis forming Kaala Sarpa Dosha. Since Rahu is in 5th house and Ketu is in 11th house this is Padam Kaala Sarpa Dosha. All the planets are right side of Rahu-Ketu Axis heading towards Rahu So its Ascending Padam Kaala Sarpa Dosha.
            '''
        else:
            Name = "Descending Padam Kaala Sarpa"
            typ = "Descending"
            Rule = f'''All the remaining 7 planets are in the same side of Rahu-Ketu Axis forming Kaala Sarpa Dosha. Since Rahu is in 5th house and Ketu is in 11th house this is Padam Kaala Sarpa Dosha. All the planets are left side of Rahu-Ketu Axis heading towards Ketu So its Descending Padam Kaala Sarpa Dosha.
            '''
        #Update the Results of Padam Kaala Sarpa Dosha
        Results = f'''Kaal Sarp Dosha is a frightful astrological event that affects a person severely with multifaceted catastrophes. It is a result of bad karma done by the native in the previous lives.
        As Kaalsarp dosh veils the planets, the aspects other planets represent may get hampered, which may lead to problems in the life of the native. So the results from aspects of other planets will be blocked by Rahu-Ketu axis and the native will not be ble to get full results of other planets in his kundali.
        The Padam kaala sarpa dosha is especially harmful to students as they may lose concentration in studies and indulge in detrimental deeds. Hence, parents must keep an eye on their children during this period. You also need to ensure you help your child make the right choices in education or it will simply cost you and him a loss of money and time. 
        For grown-ups, the dosh may hamper your progress in your career. If you are looking for new opportunities or taking risks, you must do it with a partner. Also, health should be a priority as the Padam Kaalsarp dosh progresses.
        The 5th house indicates Purva Punya so this clearly shows the lack of Purva Punya. There will be hindrances in the field of education and career, but the individual could cross all barriers and succeed eventually. Ill health and secret enemies are the biggest adversaries.
        '''
        #Update the Note
        Note = "The effect of Padam Kaala Sarpa Dosha will decrease after the age of 48 if other strong Yogas are present in Native's Kundali."
        #update Remedies for Dosha
        Remedies = f'''One of the most effective remedies to reduce the effects of the Kala Sarpa Dosha is visiting shrines of higher spiritual beings. The popular places to visit include Srikalahasti temple, Trimbakeshwar temple, Rameswaram, and Thirunageswaram. The Kalasarpa Dosha Nivaran Puja at Sri Kalahasti mandir, Rameswaram, and Thirunageswaram, is considered the best remedy for Kala Sarpa Dosha. This Dosha can also be remedied by Kal Rudra Yagna performed in these temples.
        Rudra Avisek of Shiva, in any Shiva Temple, and chanting of powerful mantras like the Mrityunjay Mantra, Vishnu Panchakshari Mantra, and Sarp Mantra are the other popular remedies for this Dosha.
        Specifically, Padam Kaal Sarpa dosha can be solved or atleast impact be reduced by wering a triangular Coral gemstone of seven and a quarter with copper in the middle finger of the right hand on any Tuesday. Keep a Peacock feather in the books on Saturday.
        '''
        
        relevant_planets = ["Su", "Mo", "Ma", "Me", "Ju", "Ve", "Sa", "Ra", "Ke"]
    
    
    
        #Update the yogadosha sections
        common.yogadoshas_dict["PADAMKAALSARPA"] = {}
        common.yogadoshas_dict["PADAMKAALSARPA"]["name"] = Name
        common.yogadoshas_dict["PADAMKAALSARPA"]["type"] = "Dosha"
        common.yogadoshas_dict["PADAMKAALSARPA"]["exist"] = IsPadamKaalSarpaDoshaPresent
        common.yogadoshas_dict["PADAMKAALSARPA"]["Rule"] = common.iterativeReplace(Rule,"\n ", "\n")
        common.yogadoshas_dict["PADAMKAALSARPA"]["Result"] = common.iterativeReplace(Results,"\n ", "\n").replace("\n","\n        ") 
        common.yogadoshas_dict["PADAMKAALSARPA"]["Remedies"] = common.iterativeReplace(Remedies,"\n ", "\n").replace("\n","\n        ")
        common.yogadoshas_dict["PADAMKAALSARPA"]["Note"] = common.iterativeReplace(Note,"\n ", "\n")
        common.yogadoshas_dict["PADAMKAALSARPA"]["Source"] = "https://astrotalk.com/kaal-sarp-dosh-12-types"
        if 'relevant_planets' in locals():
            common.yogadoshas_dict["PADAMKAALSARPA"]["relevant_planets"] = relevant_planets
        elif 'relevant_planets2' in locals():
            common.yogadoshas_dict["PADAMKAALSARPA"]["relevant_planets"] = relevant_planets2
    
    return IsGlobalPresent

    #Mahapadma Kaal sarpa dosha - Kaalsarpa dosha with Rahu in Rog bhav
def MahapadmaKaalSarpaDosha(charts):
    IsGlobalPresent = False
    IsMahapadmaKaalSarpaDoshaPresent = False
    Name = ""
    Rule = ""
    Results = ""
    Note = ""
    Remedies = ""
    
    KaalSarpDoshaSts = kaalSarpaDosha(charts)
    if (KaalSarpDoshaSts != "ABSENT") and (charts["D1"]["planets"]["Rahu"]["house-num"] == 6):
        IsMahapadmaKaalSarpaDoshaPresent = True
        colorlist = ["pink","pink","pink","pink","pink","pink","pink","pink","pink","pink","pink","pink"]
        colorlist[6-1] = "yellow"
        colorlist[12-1] = "yellow"
        #Update the Name and Rule
        if (KaalSarpDoshaSts == "ASCENDPRESENT"):
            Name = "Ascending Mahapadma Kaala Sarpa"
            typ = "Ascending"
            Rule = f'''All the remaining 7 planets are in the same side of Rahu-Ketu Axis forming Kaala Sarpa Dosha. Since Rahu is in 6th house and Ketu is in 12th house this is Mahapadma Kaala Sarpa Dosha. All the planets are right side of Rahu-Ketu Axis heading towards Rahu So its Ascending Mahapadma Kaala Sarpa Dosha.
            '''
        else:
            Name = "Descending Mahapadma Kaala Sarpa"
            typ = "Descending"
            Rule = f'''All the remaining 7 planets are in the same side of Rahu-Ketu Axis forming Kaala Sarpa Dosha. Since Rahu is in 6th house and Ketu is in 12th house this is Mahapadma Kaala Sarpa Dosha. All the planets are left side of Rahu-Ketu Axis heading towards Ketu So its Descending Mahapadma Kaala Sarpa Dosha.
            '''
        #Update the Results of Mahapadma Kaala Sarpa Dosha
        Results = f'''Kaal Sarp Dosha is a frightful astrological event that affects a person severely with multifaceted catastrophes. It is a result of bad karma done by the native in the previous lives.
        As Kaalsarp dosh veils the planets, the aspects other planets represent may get hampered, which may lead to problems in the life of the native. So the results from aspects of other planets will be blocked by Rahu-Ketu axis and the native will not be ble to get full results of other planets in his kundali.
        The Mahapadma kaala sarpa dosha is special as its more of a partial-yoga than a Dosha. The native finds himself the luck to win over all his enemies with ease. There is an enhancement in wisdom and a thrust of will to do something worthwhile and big in life. 
        However, as the dosh period continues, the native tends to lose peace of mind and may make thoughtless choices. In the dosh period, the person earns profit from business from abroad. 
        '''
        #Update the Note
        Note = "The effect of Mahapadma Kaala Sarpa Dosha will decrease after the age of 54 if other strong Yogas are present in Native's Kundali."
        #update Remedies for Dosha
        Remedies = f'''One of the most effective remedies to reduce the effects of the Kala Sarpa Dosha is visiting shrines of higher spiritual beings. The popular places to visit include Srikalahasti temple, Trimbakeshwar temple, Rameswaram, and Thirunageswaram. The Kalasarpa Dosha Nivaran Puja at Sri Kalahasti mandir, Rameswaram, and Thirunageswaram, is considered the best remedy for Kala Sarpa Dosha. This Dosha can also be remedied by Kal Rudra Yagna performed in these temples.
        Rudra Avisek of Shiva, in any Shiva Temple, and chanting of powerful mantras like the Mrityunjay Mantra, Vishnu Panchakshari Mantra, and Sarp Mantra are the other popular remedies for this Dosha.
        Specifically, Mahapadma Kaal Sarpa dosha can be solved or atleast impact be reduced by visiting the Hanuman idol in the morning on Tuesday. Recite Hanuman Chalisa once in a day for 40 days. 
        Also you can recite Sunderkand of Ramcharitmanas on Tuesday or Saturday 108 times.
        '''
        
        relevant_planets = ["Su", "Mo", "Ma", "Me", "Ju", "Ve", "Sa", "Ra", "Ke"]
    
    
    
        #Update the yogadosha sections
        common.yogadoshas_dict["MAHAPADMAKAALSARPA"] = {}
        common.yogadoshas_dict["MAHAPADMAKAALSARPA"]["name"] = Name
        common.yogadoshas_dict["MAHAPADMAKAALSARPA"]["type"] = "Dosha"
        common.yogadoshas_dict["MAHAPADMAKAALSARPA"]["exist"] = IsMahapadmaKaalSarpaDoshaPresent
        common.yogadoshas_dict["MAHAPADMAKAALSARPA"]["Rule"] = common.iterativeReplace(Rule,"\n ", "\n")
        common.yogadoshas_dict["MAHAPADMAKAALSARPA"]["Result"] = common.iterativeReplace(Results,"\n ", "\n").replace("\n","\n        ") 
        common.yogadoshas_dict["MAHAPADMAKAALSARPA"]["Remedies"] = common.iterativeReplace(Remedies,"\n ", "\n").replace("\n","\n        ")
        common.yogadoshas_dict["MAHAPADMAKAALSARPA"]["Note"] = common.iterativeReplace(Note,"\n ", "\n")
        common.yogadoshas_dict["MAHAPADMAKAALSARPA"]["Source"] = "https://astrotalk.com/kaal-sarp-dosh-12-types"
        if 'relevant_planets' in locals():
            common.yogadoshas_dict["MAHAPADMAKAALSARPA"]["relevant_planets"] = relevant_planets
        elif 'relevant_planets2' in locals():
            common.yogadoshas_dict["MAHAPADMAKAALSARPA"]["relevant_planets"] = relevant_planets2
    
    return IsGlobalPresent

    #Takshaka Kaal sarpa dosha - Kaalsarpa dosha with Rahu in Santaan bhav
def TakshakaKaalSarpaDosha(charts):
    IsGlobalPresent = False
    IsTakshakaKaalSarpaDoshaPresent = False
    Name = ""
    Rule = ""
    Results = ""
    Note = ""
    Remedies = ""
    
    KaalSarpDoshaSts = kaalSarpaDosha(charts)
    if (KaalSarpDoshaSts != "ABSENT") and (charts["D1"]["planets"]["Rahu"]["house-num"] == 7):
        IsTakshakaKaalSarpaDoshaPresent = True
        colorlist = ["pink","pink","pink","pink","pink","pink","pink","pink","pink","pink","pink","pink"]
        colorlist[7-1] = "yellow"
        colorlist[1-1] = "yellow"
        #Update the Name and Rule
        if (KaalSarpDoshaSts == "ASCENDPRESENT"):
            Name = "Ascending Takshaka Kaala Sarpa"
            typ = "Ascending"
            Rule = f'''All the remaining 7 planets are in the same side of Rahu-Ketu Axis forming Kaala Sarpa Dosha. Since Rahu is in 7th house and Ketu is in 1st house this is Takshaka Kaala Sarpa Dosha. All the planets are right side of Rahu-Ketu Axis heading towards Rahu So its Ascending Takshaka Kaala Sarpa Dosha.
            '''
        else:
            Name = "Descending Takshaka Kaala Sarpa"
            typ = "Descending"
            Rule = f'''All the remaining 7 planets are in the same side of Rahu-Ketu Axis forming Kaala Sarpa Dosha. Since Rahu is in 7th house and Ketu is in 1st house this is Takshaka Kaala Sarpa Dosha. All the planets are left side of Rahu-Ketu Axis heading towards Ketu So its Descending Takshaka Kaala Sarpa Dosha.
            '''
        #Update the Results of Takshaka Kaala Sarpa Dosha
        Results = f'''Kaal Sarp Dosha is a frightful astrological event that affects a person severely with multifaceted catastrophes. It is a result of bad karma done by the native in the previous lives.
        As Kaalsarp dosh veils the planets, the aspects other planets represent may get hampered, which may lead to problems in the life of the native. So the results from aspects of other planets will be blocked by Rahu-Ketu axis and the native will not be ble to get full results of other planets in his kundali.
        The Takshaka kaala sarpa dosha impacts mainly the marriage. he or she may have to face a delay in marriage. The marriage delay may become the reason for tension and stress for your parents too. If married, there may be disturbances due to the nature of the in-laws. There may also arise situations when you might think of divorce. 
        Also, the ones dealing with Kaalsarp dosh must not consider love marriage during the dosh period. Doing so will hamper the love you share after marriage, and you will have to put extra effort to make things work.
        You find romance difficult and also have trouble receiving their share of ancestral property. They may have good achievements but would show the tendency to renounce everything.
        '''
        #Update the Note
        Note = "The effect of Takshaka Kaala Sarpa Dosha will decrease after the age of 60 if other strong Yogas are present in Native's Kundali."
        #update Remedies for Dosha
        Remedies = f'''One of the most effective remedies to reduce the effects of the Kala Sarpa Dosha is visiting shrines of higher spiritual beings. The popular places to visit include Srikalahasti temple, Trimbakeshwar temple, Rameswaram, and Thirunageswaram. The Kalasarpa Dosha Nivaran Puja at Sri Kalahasti mandir, Rameswaram, and Thirunageswaram, is considered the best remedy for Kala Sarpa Dosha. This Dosha can also be remedied by Kal Rudra Yagna performed in these temples.
        Rudra Avisek of Shiva, in any Shiva Temple, and chanting of powerful mantras like the Mrityunjay Mantra, Vishnu Panchakshari Mantra, and Sarp Mantra are the other popular remedies for this Dosha.
        Specifically, Takshaka Kaal Sarpa dosha can be solved or atleast impact be reduced by reciting Sunderkand of Ramcharitmanas on Tuesday or Saturday 108 times. Read Ganapati Atharvashirsha on every full moon.
        Wear an energized Silver Rahu Yantra around your neck.
        '''
        
        relevant_planets = ["Su", "Mo", "Ma", "Me", "Ju", "Ve", "Sa", "Ra", "Ke"]
    
    
    
        #Update the yogadosha sections
        common.yogadoshas_dict["TAKSHAKAKAALSARPA"] = {}
        common.yogadoshas_dict["TAKSHAKAKAALSARPA"]["name"] = Name
        common.yogadoshas_dict["TAKSHAKAKAALSARPA"]["type"] = "Dosha"
        common.yogadoshas_dict["TAKSHAKAKAALSARPA"]["exist"] = IsTakshakaKaalSarpaDoshaPresent
        common.yogadoshas_dict["TAKSHAKAKAALSARPA"]["Rule"] = common.iterativeReplace(Rule,"\n ", "\n")
        common.yogadoshas_dict["TAKSHAKAKAALSARPA"]["Result"] = common.iterativeReplace(Results,"\n ", "\n").replace("\n","\n        ") 
        common.yogadoshas_dict["TAKSHAKAKAALSARPA"]["Remedies"] = common.iterativeReplace(Remedies,"\n ", "\n").replace("\n","\n        ")
        common.yogadoshas_dict["TAKSHAKAKAALSARPA"]["Note"] = common.iterativeReplace(Note,"\n ", "\n")
        common.yogadoshas_dict["TAKSHAKAKAALSARPA"]["Source"] = "https://astrotalk.com/kaal-sarp-dosh-12-types"
        if 'relevant_planets' in locals():
            common.yogadoshas_dict["TAKSHAKAKAALSARPA"]["relevant_planets"] = relevant_planets
        elif 'relevant_planets2' in locals():
            common.yogadoshas_dict["TAKSHAKAKAALSARPA"]["relevant_planets"] = relevant_planets2
    
    return IsGlobalPresent

    #Karkotak Kaal sarpa dosha - Kaalsarpa dosha with Rahu in Santaan bhav
def KarkotakKaalSarpaDosha(charts):
    IsGlobalPresent = False
    IsKarkotakKaalSarpaDoshaPresent = False
    Name = ""
    Rule = ""
    Results = ""
    Note = ""
    Remedies = ""
    
    KaalSarpDoshaSts = kaalSarpaDosha(charts)
    if (KaalSarpDoshaSts != "ABSENT") and (charts["D1"]["planets"]["Rahu"]["house-num"] == 8):
        IsKarkotakKaalSarpaDoshaPresent = True
        colorlist = ["pink","pink","pink","pink","pink","pink","pink","pink","pink","pink","pink","pink"]
        colorlist[8-1] = "yellow"
        colorlist[2-1] = "yellow"
        #Update the Name and Rule
        if (KaalSarpDoshaSts == "ASCENDPRESENT"):
            Name = "Ascending Karkotak Kaala Sarpa"
            typ = "Ascending"
            Rule = f'''All the remaining 7 planets are in the same side of Rahu-Ketu Axis forming Kaala Sarpa Dosha. Since Rahu is in 8th house and Ketu is in 2nd house this is Karkotak Kaala Sarpa Dosha. All the planets are right side of Rahu-Ketu Axis heading towards Rahu So its Ascending Karkotak Kaala Sarpa Dosha.
            '''
        else:
            Name = "Descending Karkotak Kaala Sarpa"
            typ = "Descending"
            Rule = f'''All the remaining 7 planets are in the same side of Rahu-Ketu Axis forming Kaala Sarpa Dosha. Since Rahu is in 8th house and Ketu is in 2nd house this is Karkotak Kaala Sarpa Dosha. All the planets are left side of Rahu-Ketu Axis heading towards Ketu So its Descending Karkotak Kaala Sarpa Dosha.
            '''
        #Update the Results of Karkotak Kaala Sarpa Dosha
        Results = f'''Kaal Sarp Dosha is a frightful astrological event that affects a person severely with multifaceted catastrophes. It is a result of bad karma done by the native in the previous lives.
        As Kaalsarp dosh veils the planets, the aspects other planets represent may get hampered, which may lead to problems in the life of the native. So the results from aspects of other planets will be blocked by Rahu-Ketu axis and the native will not be ble to get full results of other planets in his kundali.
        The Karkotak kaala sarpa dosha is responsible for causing hindrance in acquiring a fortune. The dosh may also hamper career progress as you may witness several hindrances in acquiring a job and getting a well-deserved promotion. 
        People dealing with Karkotak Kaalsarp dosha also acquire the habit of speaking the truth. This may seem like a good thing, but this habit may bar the native from acquiring good deals for himself. This doesn't mean that you shouldn't speak the truth, but you must surely think before speaking to anyone.
        This Dosha affects mental wellbeing. An irritable nature and outspoken character work detrimentally for individuals who receive no success despite hard work. They would also face ups and downs in finance, legal issues, etc
        '''
        #Update the Note
        Note = "The effect of Karkotak Kaala Sarpa Dosha will decrease after the age of 33 if other strong Yogas are present in Native's Kundali."
        #update Remedies for Dosha
        Remedies = f'''One of the most effective remedies to reduce the effects of the Kala Sarpa Dosha is visiting shrines of higher spiritual beings. The popular places to visit include Srikalahasti temple, Trimbakeshwar temple, Rameswaram, and Thirunageswaram. The Kalasarpa Dosha Nivaran Puja at Sri Kalahasti mandir, Rameswaram, and Thirunageswaram, is considered the best remedy for Kala Sarpa Dosha. This Dosha can also be remedied by Kal Rudra Yagna performed in these temples.
        Rudra Avisek of Shiva, in any Shiva Temple, and chanting of powerful mantras like the Mrityunjay Mantra, Vishnu Panchakshari Mantra, and Sarp Mantra are the other popular remedies for this Dosha.
        Specifically, Karkotak Kaal Sarpa dosha can be solved or atleast impact be reduced by wearing Shiva Yantra made of silver around the neck. 
        Starting from Saturday, feed Boondi Laddoos to the ants for 27 days. Also wear a triangular Coral gemstone in copper on the middle finger of the right hand.
        '''
        
        relevant_planets = ["Su", "Mo", "Ma", "Me", "Ju", "Ve", "Sa", "Ra", "Ke"]
    
    
    
        #Update the yogadosha sections
        common.yogadoshas_dict["KARKOTAKKAALSARPA"] = {}
        common.yogadoshas_dict["KARKOTAKKAALSARPA"]["name"] = Name
        common.yogadoshas_dict["KARKOTAKKAALSARPA"]["type"] = "Dosha"
        common.yogadoshas_dict["KARKOTAKKAALSARPA"]["exist"] = IsKarkotakKaalSarpaDoshaPresent
        common.yogadoshas_dict["KARKOTAKKAALSARPA"]["Rule"] = common.iterativeReplace(Rule,"\n ", "\n")
        common.yogadoshas_dict["KARKOTAKKAALSARPA"]["Result"] = common.iterativeReplace(Results,"\n ", "\n").replace("\n","\n        ") 
        common.yogadoshas_dict["KARKOTAKKAALSARPA"]["Remedies"] = common.iterativeReplace(Remedies,"\n ", "\n").replace("\n","\n        ")
        common.yogadoshas_dict["KARKOTAKKAALSARPA"]["Note"] = common.iterativeReplace(Note,"\n ", "\n")
        common.yogadoshas_dict["KARKOTAKKAALSARPA"]["Source"] = "https://astrotalk.com/kaal-sarp-dosh-12-types"
        if 'relevant_planets' in locals():
            common.yogadoshas_dict["KARKOTAKKAALSARPA"]["relevant_planets"] = relevant_planets
        elif 'relevant_planets2' in locals():
            common.yogadoshas_dict["KARKOTAKKAALSARPA"]["relevant_planets"] = relevant_planets2
    
    return IsGlobalPresent

    #Shankhachur Kaal sarpa dosha - Kaalsarpa dosha with Rahu in Santaan bhav
def ShankhachurKaalSarpaDosha(charts):
    IsGlobalPresent = False
    IsShankhachurKaalSarpaDoshaPresent = False
    Name = ""
    Rule = ""
    Results = ""
    Note = ""
    Remedies = ""
    
    KaalSarpDoshaSts = kaalSarpaDosha(charts)
    if (KaalSarpDoshaSts != "ABSENT") and (charts["D1"]["planets"]["Rahu"]["house-num"] == 9):
        IsShankhachurKaalSarpaDoshaPresent = True
        colorlist = ["pink","pink","pink","pink","pink","pink","pink","pink","pink","pink","pink","pink"]
        colorlist[9-1] = "yellow"
        colorlist[3-1] = "yellow"
        #Update the Name and Rule
        if (KaalSarpDoshaSts == "ASCENDPRESENT"):
            Name = "Ascending Shankhachur Kaala Sarpa"
            typ = "Ascending"
            Rule = f'''All the remaining 7 planets are in the same side of Rahu-Ketu Axis forming Kaala Sarpa Dosha. Since Rahu is in 9th house and Ketu is in 3rd house this is Shankhachur Kaala Sarpa Dosha. All the planets are right side of Rahu-Ketu Axis heading towards Rahu So its Ascending Shankhachur Kaala Sarpa Dosha.
            '''
        else:
            Name = "Descending Shankhachur Kaala Sarpa"
            typ = "Descending"
            Rule = f'''All the remaining 7 planets are in the same side of Rahu-Ketu Axis forming Kaala Sarpa Dosha. Since Rahu is in 9th house and Ketu is in 3rd house this is Shankhachur Kaala Sarpa Dosha. All the planets are left side of Rahu-Ketu Axis heading towards Ketu So its Descending Shankhachur Kaala Sarpa Dosha.
            '''
        #Update the Results of Shankhachur Kaala Sarpa Dosha
        Results = f'''Kaal Sarp Dosha is a frightful astrological event that affects a person severely with multifaceted catastrophes. It is a result of bad karma done by the native in the previous lives.
        As Kaalsarp dosh veils the planets, the aspects other planets represent may get hampered, which may lead to problems in the life of the native. So the results from aspects of other planets will be blocked by Rahu-Ketu axis and the native will not be ble to get full results of other planets in his kundali.
        The Shankhachur kaala sarpa dosha good thing is that the desires of people born in this dosh are usually fulfilled. However, the bad thing is that there may be a delay in fulfilling such desires, which may leave you frustrated. 
        In the family and home of the native dealing with Shankhachur Kaalsarp dosh, there may be a lot of pain and suffering. In this period, it is suggested that you focus on your family and don't indulge in dealings that you will have to regret in the near future.
        The individuals with this Yoga would face troubles in business and sudden downfall from power and position. They may have to fight for their rights. Upon enduring these troubles, these individuals can become increasingly selfish
        '''
        #Update the Note
        Note = "The effect of Shankhachur Kaala Sarpa Dosha will decrease after the age of 36 if other strong Yogas are present in Native's Kundali."
        #update Remedies for Dosha
        Remedies = f'''One of the most effective remedies to reduce the effects of the Kala Sarpa Dosha is visiting shrines of higher spiritual beings. The popular places to visit include Srikalahasti temple, Trimbakeshwar temple, Rameswaram, and Thirunageswaram. The Kalasarpa Dosha Nivaran Puja at Sri Kalahasti mandir, Rameswaram, and Thirunageswaram, is considered the best remedy for Kala Sarpa Dosha. This Dosha can also be remedied by Kal Rudra Yagna performed in these temples.
        Rudra Avisek of Shiva, in any Shiva Temple, and chanting of powerful mantras like the Mrityunjay Mantra, Vishnu Panchakshari Mantra, and Sarp Mantra are the other popular remedies for this Dosha.
        Specifically, Shankhachur Kaal Sarpa dosha can be solved or atleast impact be reduced by reciting Hanuman Chalisa daily
        Regularly recite Mahamrityunjaya Mantra and observe fasting every Monday. Also Wear an energised Silver Rahu Yantra around your neck on Saturday.
        '''
        
        relevant_planets = ["Su", "Mo", "Ma", "Me", "Ju", "Ve", "Sa", "Ra", "Ke"]
    
    
    
        #Update the yogadosha sections
        common.yogadoshas_dict["SHANKACHURKAALSARPA"] = {}
        common.yogadoshas_dict["SHANKACHURKAALSARPA"]["name"] = Name
        common.yogadoshas_dict["SHANKACHURKAALSARPA"]["type"] = "Dosha"
        common.yogadoshas_dict["SHANKACHURKAALSARPA"]["exist"] = IsShankhachurKaalSarpaDoshaPresent
        common.yogadoshas_dict["SHANKACHURKAALSARPA"]["Rule"] = common.iterativeReplace(Rule,"\n ", "\n")
        common.yogadoshas_dict["SHANKACHURKAALSARPA"]["Result"] = common.iterativeReplace(Results,"\n ", "\n").replace("\n","\n        ") 
        common.yogadoshas_dict["SHANKACHURKAALSARPA"]["Remedies"] = common.iterativeReplace(Remedies,"\n ", "\n").replace("\n","\n        ")
        common.yogadoshas_dict["SHANKACHURKAALSARPA"]["Note"] = common.iterativeReplace(Note,"\n ", "\n")
        common.yogadoshas_dict["SHANKACHURKAALSARPA"]["Source"] = "https://astrotalk.com/kaal-sarp-dosh-12-types"
        if 'relevant_planets' in locals():
            common.yogadoshas_dict["SHANKACHURKAALSARPA"]["relevant_planets"] = relevant_planets
        elif 'relevant_planets2' in locals():
            common.yogadoshas_dict["SHANKACHURKAALSARPA"]["relevant_planets"] = relevant_planets2
    
    return IsGlobalPresent

    #Ghatak Kaal sarpa dosha - Kaalsarpa dosha with Rahu in Santaan bhav
def GhatakKaalSarpaDosha(charts):
    IsGlobalPresent = False
    IsGhatakKaalSarpaDoshaPresent = False
    Name = ""
    Rule = ""
    Results = ""
    Note = ""
    Remedies = ""
    
    KaalSarpDoshaSts = kaalSarpaDosha(charts)
    if (KaalSarpDoshaSts != "ABSENT") and (charts["D1"]["planets"]["Rahu"]["house-num"] == 10):
        IsGhatakKaalSarpaDoshaPresent = True
        colorlist = ["pink","pink","pink","pink","pink","pink","pink","pink","pink","pink","pink","pink"]
        colorlist[10-1] = "yellow"
        colorlist[4-1] = "yellow"
        #Update the Name and Rule
        if (KaalSarpDoshaSts == "ASCENDPRESENT"):
            Name = "Ascending Ghatak Kaala Sarpa"
            typ = "Ascending"
            Rule = f'''All the remaining 7 planets are in the same side of Rahu-Ketu Axis forming Kaala Sarpa Dosha. Since Rahu is in 10th house and Ketu is in 4th house this is Ghatak Kaala Sarpa Dosha. All the planets are right side of Rahu-Ketu Axis heading towards Rahu So its Ascending Ghatak Kaala Sarpa Dosha.
            '''
        else:
            Name = "Descending Ghatak Kaala Sarpa"
            typ = "Descending"
            Rule = f'''All the remaining 7 planets are in the same side of Rahu-Ketu Axis forming Kaala Sarpa Dosha. Since Rahu is in 10th house and Ketu is in 4th house this is Ghatak Kaala Sarpa Dosha. All the planets are left side of Rahu-Ketu Axis heading towards Ketu So its Descending Ghatak Kaala Sarpa Dosha.
            '''
        #Update the Results of Ghatak Kaala Sarpa Dosha
        Results = f'''Kaal Sarp Dosha is a frightful astrological event that affects a person severely with multifaceted catastrophes. It is a result of bad karma done by the native in the previous lives.
        As Kaalsarp dosh veils the planets, the aspects other planets represent may get hampered, which may lead to problems in the life of the native. So the results from aspects of other planets will be blocked by Rahu-Ketu axis and the native will not be ble to get full results of other planets in his kundali.
        Since you have Ghatak kaala sarpa dosha, it is highly recommended that you serve your mother, take care of her and never cause her any harm. This will help in bettering your life conditions. However, it has been noticed that in return, you may not get the same kind of affection from your mother. 
        Due to Ghatak Kaalsarp dosha, the person becomes arrogant even if he or she does not have anything to be proud of. Your ego is at the top of your head, which may hamper not only your personal but your professional bondings too.
        Despite the achieved success, the individuals with this Dosha would find it hard to be happy. There would be problems in professional and family lives. Excessive interference from family members may make their life miserable.
        '''
        #Update the Note
        Note = "The effect of Ghatak Kaala Sarpa Dosha will decrease after the age of 42 if other strong Yogas are present in Native's Kundali."
        #update Remedies for Dosha
        Remedies = f'''One of the most effective remedies to reduce the effects of the Kala Sarpa Dosha is visiting shrines of higher spiritual beings. The popular places to visit include Srikalahasti temple, Trimbakeshwar temple, Rameswaram, and Thirunageswaram. The Kalasarpa Dosha Nivaran Puja at Sri Kalahasti mandir, Rameswaram, and Thirunageswaram, is considered the best remedy for Kala Sarpa Dosha. This Dosha can also be remedied by Kal Rudra Yagna performed in these temples.
        Rudra Avisek of Shiva, in any Shiva Temple, and chanting of powerful mantras like the Mrityunjay Mantra, Vishnu Panchakshari Mantra, and Sarp Mantra are the other popular remedies for this Dosha.
        Specifically, Ghatak Kaal Sarpa dosha can be solved or atleast impact be reduced by always reading the Hanuman Chalisa and observe fast each Tuesday.
        Read Ganapati Atharvashirsha on every full moon. Also on Friday, donate coconut, blanket etc. along with epilogue, oil, black cloth, and peel.
        '''
        
        relevant_planets = ["Su", "Mo", "Ma", "Me", "Ju", "Ve", "Sa", "Ra", "Ke"]
    
    
    
        #Update the yogadosha sections
        common.yogadoshas_dict["GHATAKKAALSARPA"] = {}
        common.yogadoshas_dict["GHATAKKAALSARPA"]["name"] = Name
        common.yogadoshas_dict["GHATAKKAALSARPA"]["type"] = "Dosha"
        common.yogadoshas_dict["GHATAKKAALSARPA"]["exist"] = IsGhatakKaalSarpaDoshaPresent
        common.yogadoshas_dict["GHATAKKAALSARPA"]["Rule"] = common.iterativeReplace(Rule,"\n ", "\n")
        common.yogadoshas_dict["GHATAKKAALSARPA"]["Result"] = common.iterativeReplace(Results,"\n ", "\n").replace("\n","\n        ") 
        common.yogadoshas_dict["GHATAKKAALSARPA"]["Remedies"] = common.iterativeReplace(Remedies,"\n ", "\n").replace("\n","\n        ")
        common.yogadoshas_dict["GHATAKKAALSARPA"]["Note"] = common.iterativeReplace(Note,"\n ", "\n")
        common.yogadoshas_dict["GHATAKKAALSARPA"]["Source"] = "https://astrotalk.com/kaal-sarp-dosh-12-types"
        if 'relevant_planets' in locals():
            common.yogadoshas_dict["GHATAKKAALSARPA"]["relevant_planets"] = relevant_planets
        elif 'relevant_planets2' in locals():
            common.yogadoshas_dict["GHATAKKAALSARPA"]["relevant_planets"] = relevant_planets2
    
    return IsGlobalPresent

    #Vishadhara Kaal sarpa dosha - Kaalsarpa dosha with Rahu in Laab bhav
def VishadharaKaalSarpaDosha(charts):
    IsGlobalPresent = False
    IsVishadharaKaalSarpaDoshaPresent = False
    Name = ""
    Rule = ""
    Results = ""
    Note = ""
    Remedies = ""
    
    KaalSarpDoshaSts = kaalSarpaDosha(charts)
    if (KaalSarpDoshaSts != "ABSENT") and (charts["D1"]["planets"]["Rahu"]["house-num"] == 11):
        IsVishadharaKaalSarpaDoshaPresent = True
        colorlist = ["pink","pink","pink","pink","pink","pink","pink","pink","pink","pink","pink","pink"]
        colorlist[11-1] = "yellow"
        colorlist[5-1] = "yellow"
        #Update the Name and Rule
        if (KaalSarpDoshaSts == "ASCENDPRESENT"):
            Name = "Ascending Vishadhara Kaala Sarpa"
            typ = "Ascending"
            Rule = f'''All the remaining 7 planets are in the same side of Rahu-Ketu Axis forming Kaala Sarpa Dosha. Since Rahu is in 11th house and Ketu is in 5th house this is Vishadhara Kaala Sarpa Dosha. All the planets are right side of Rahu-Ketu Axis heading towards Rahu So its Ascending Vishadhara Kaala Sarpa Dosha.
            '''
        else:
            Name = "Descending Vishadhara Kaala Sarpa"
            typ = "Descending"
            Rule = f'''All the remaining 7 planets are in the same side of Rahu-Ketu Axis forming Kaala Sarpa Dosha. Since Rahu is in 11th house and Ketu is in 5th house this is Vishadhara Kaala Sarpa Dosha. All the planets are left side of Rahu-Ketu Axis heading towards Ketu So its Descending Vishadhara Kaala Sarpa Dosha.
            '''
        #Update the Results of Vishadhara Kaala Sarpa Dosha
        Results = f'''Kaal Sarp Dosha is a frightful astrological event that affects a person severely with multifaceted catastrophes. It is a result of bad karma done by the native in the previous lives.
        As Kaalsarp dosh veils the planets, the aspects other planets represent may get hampered, which may lead to problems in the life of the native. So the results from aspects of other planets will be blocked by Rahu-Ketu axis and the native will not be ble to get full results of other planets in his kundali.
        The Vishadhara kaala sarpa dosha is fatal for the one trying to acquire education, especially higher education. There will be a lot of obstacles for such a person to get higher education. However, despite all odds, their patience and commitment will help them in moving forward. 
        These people do better in their professional life if they pursue their career from abroad than from their own country. Their fortune trends in foreign countries. In the family, the person has to suffer from property loss even after the possibility of benefiting from grandparents.
         The issues corresponding to this Dosha begin with memory loss, poor educational experience, and plenty of domestic issues on property and wealth. The individuals with this Dosha may also suffer on account of their child.
        '''
        #Update the Note
        Note = "The effect of Vishadhara Kaala Sarpa Dosha will decrease after the age of 48 if other strong Yogas are present in Native's Kundali."
        #update Remedies for Dosha
        Remedies = f'''One of the most effective remedies to reduce the effects of the Kala Sarpa Dosha is visiting shrines of higher spiritual beings. The popular places to visit include Srikalahasti temple, Trimbakeshwar temple, Rameswaram, and Thirunageswaram. The Kalasarpa Dosha Nivaran Puja at Sri Kalahasti mandir, Rameswaram, and Thirunageswaram, is considered the best remedy for Kala Sarpa Dosha. This Dosha can also be remedied by Kal Rudra Yagna performed in these temples.
        Rudra Avisek of Shiva, in any Shiva Temple, and chanting of powerful mantras like the Mrityunjay Mantra, Vishnu Panchakshari Mantra, and Sarp Mantra are the other popular remedies for this Dosha.
        Specifically, Vishadhara Kaal Sarpa dosha can be solved or atleast impact be reduced by feeding barley grains to the needy for 27 days on Saturday.
        On Saturday, circumambulate the raw coal anti-clockwise around your head 8 times, then throw the coal in the running water. Also dont forget to recite Hanuman Chalisa daily.
        '''
        
        relevant_planets = ["Su", "Mo", "Ma", "Me", "Ju", "Ve", "Sa", "Ra", "Ke"]
    
    
    
        #Update the yogadosha sections
        common.yogadoshas_dict["VISHADHARAKAALSARPA"] = {}
        common.yogadoshas_dict["VISHADHARAKAALSARPA"]["name"] = Name
        common.yogadoshas_dict["VISHADHARAKAALSARPA"]["type"] = "Dosha"
        common.yogadoshas_dict["VISHADHARAKAALSARPA"]["exist"] = IsVishadharaKaalSarpaDoshaPresent
        common.yogadoshas_dict["VISHADHARAKAALSARPA"]["Rule"] = common.iterativeReplace(Rule,"\n ", "\n")
        common.yogadoshas_dict["VISHADHARAKAALSARPA"]["Result"] = common.iterativeReplace(Results,"\n ", "\n").replace("\n","\n        ") 
        common.yogadoshas_dict["VISHADHARAKAALSARPA"]["Remedies"] = common.iterativeReplace(Remedies,"\n ", "\n").replace("\n","\n        ")
        common.yogadoshas_dict["VISHADHARAKAALSARPA"]["Note"] = common.iterativeReplace(Note,"\n ", "\n")
        common.yogadoshas_dict["VISHADHARAKAALSARPA"]["Source"] = "https://astrotalk.com/kaal-sarp-dosh-12-types"
        if 'relevant_planets' in locals():
            common.yogadoshas_dict["VISHADHARAKAALSARPA"]["relevant_planets"] = relevant_planets
        elif 'relevant_planets2' in locals():
            common.yogadoshas_dict["VISHADHARAKAALSARPA"]["relevant_planets"] = relevant_planets2
    
    return IsGlobalPresent

    #Sheshanaga Kaal sarpa dosha - Kaalsarpa dosha with Rahu in Karch bhav
def SheshanagaKaalSarpaDosha(charts):
    IsGlobalPresent = False
    IsSheshanagaKaalSarpaDoshaPresent = False
    Name = ""
    Rule = ""
    Results = ""
    Note = ""
    Remedies = ""
    
    KaalSarpDoshaSts = kaalSarpaDosha(charts)
    if (KaalSarpDoshaSts != "ABSENT") and (charts["D1"]["planets"]["Rahu"]["house-num"] == 12):
        IsSheshanagaKaalSarpaDoshaPresent = True
        colorlist = ["pink","pink","pink","pink","pink","pink","pink","pink","pink","pink","pink","pink"]
        colorlist[12-1] = "yellow"
        colorlist[6-1] = "yellow"
        #Update the Name and Rule
        if (KaalSarpDoshaSts == "ASCENDPRESENT"):
            Name = "Ascending Sheshanaga Kaala Sarpa"
            typ = "Ascending"
            Rule = f'''All the remaining 7 planets are in the same side of Rahu-Ketu Axis forming Kaala Sarpa Dosha. Since Rahu is in 12th house and Ketu is in 6th house this is Sheshanaga Kaala Sarpa Dosha. All the planets are right side of Rahu-Ketu Axis heading towards Rahu So its Ascending Sheshanaga Kaala Sarpa Dosha.
            '''
        else:
            Name = "Descending Sheshanaga Kaala Sarpa"
            typ = "Descending"
            Rule = f'''All the remaining 7 planets are in the same side of Rahu-Ketu Axis forming Kaala Sarpa Dosha. Since Rahu is in 12th house and Ketu is in 6th house this is Sheshanaga Kaala Sarpa Dosha. All the planets are left side of Rahu-Ketu Axis heading towards Ketu So its Descending Sheshanaga Kaala Sarpa Dosha.
            '''
        #Update the Results of Sheshanaga Kaala Sarpa Dosha
        Results = f'''Kaal Sarp Dosha is a frightful astrological event that affects a person severely with multifaceted catastrophes. It is a result of bad karma done by the native in the previous lives.
        As Kaalsarp dosh veils the planets, the aspects other planets represent may get hampered, which may lead to problems in the life of the native. So the results from aspects of other planets will be blocked by Rahu-Ketu axis and the native will not be ble to get full results of other planets in his kundali.
        The Sheshanaga kaala sarpa dosha always fulfils natives desires, however, with a slight delay. The native under the presence of this dosh may develop a habit of spending more than his income. This is why he may usually find himself indebted. After 42 years of age, there is a time in his life when he may find himself a prestigious place in society. This, however, will require your constant hard work and commitment.
        This dosha has debilitating effects, both physically and mentally. The individuals face a life of defamation and find it hard to get rid of the same. They will have a lot of hidden enemies, and will never feel satisfied with their lives.
        '''
        #Update the Note
        Note = "The effect of Sheshanaga Kaala Sarpa Dosha will decrease after the age of 54 if other strong Yogas are present in Native's Kundali."
        #update Remedies for Dosha
        Remedies = f'''One of the most effective remedies to reduce the effects of the Kala Sarpa Dosha is visiting shrines of higher spiritual beings. The popular places to visit include Srikalahasti temple, Trimbakeshwar temple, Rameswaram, and Thirunageswaram. The Kalasarpa Dosha Nivaran Puja at Sri Kalahasti mandir, Rameswaram, and Thirunageswaram, is considered the best remedy for Kala Sarpa Dosha. This Dosha can also be remedied by Kal Rudra Yagna performed in these temples.
        Rudra Avisek of Shiva, in any Shiva Temple, and chanting of powerful mantras like the Mrityunjay Mantra, Vishnu Panchakshari Mantra, and Sarp Mantra are the other popular remedies for this Dosha.
        Specifically, Sheshanaga Kaal Sarpa dosha can be solved or atleast impact be reduced by hanging Hanuman Bahuk wrapped in red cloth on any Tuesday on the wall towards the south side of the house
        Feed the raw bread of barley flour to the birds for 3 months. Also you can wear an energised Shiva Yantra made of silver around the neck.
        '''
        
        relevant_planets = ["Su", "Mo", "Ma", "Me", "Ju", "Ve", "Sa", "Ra", "Ke"]
    
    
    
        #Update the yogadosha sections
        common.yogadoshas_dict["SHESHANAGAKAALSARPA"] = {}
        common.yogadoshas_dict["SHESHANAGAKAALSARPA"]["name"] = Name
        common.yogadoshas_dict["SHESHANAGAKAALSARPA"]["type"] = "Dosha"
        common.yogadoshas_dict["SHESHANAGAKAALSARPA"]["exist"] = IsSheshanagaKaalSarpaDoshaPresent
        common.yogadoshas_dict["SHESHANAGAKAALSARPA"]["Rule"] = common.iterativeReplace(Rule,"\n ", "\n")
        common.yogadoshas_dict["SHESHANAGAKAALSARPA"]["Result"] = common.iterativeReplace(Results,"\n ", "\n").replace("\n","\n        ") 
        common.yogadoshas_dict["SHESHANAGAKAALSARPA"]["Remedies"] = common.iterativeReplace(Remedies,"\n ", "\n").replace("\n","\n        ")
        common.yogadoshas_dict["SHESHANAGAKAALSARPA"]["Note"] = common.iterativeReplace(Note,"\n ", "\n")
        common.yogadoshas_dict["SHESHANAGAKAALSARPA"]["Source"] = "https://astrotalk.com/kaal-sarp-dosh-12-types"
        if 'relevant_planets' in locals():
            common.yogadoshas_dict["SHESHANAGAKAALSARPA"]["relevant_planets"] = relevant_planets
        elif 'relevant_planets2' in locals():
            common.yogadoshas_dict["SHESHANAGAKAALSARPA"]["relevant_planets"] = relevant_planets2
    
    return IsGlobalPresent

    #Gajakesari Yoga - Jupiter is in Kendra with respect to Moon in D1 chart
