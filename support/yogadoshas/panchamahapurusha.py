import support.generic as gen
import support.yogadoshas.common as common

#function to check for Sasa Panchamahapurusha yoga - Saturn
# ==========================================================================================
# Function Name: SasaYoga
# Purpose: Calculates the presence of SasaYoga in the provided horoscope.
# Description: Evaluates SasaYoga
# Expected Impact: 
# Parameters:
#   - charts (dict): Comprehensive dictionary containing D1, D9 charts and planetary attributes.
# Returns:
#   - Boolean/String: True if the yoga/dosha is present, False otherwise.
# ==========================================================================================
def SasaYoga(charts):
    IsGlobalPresent = False
    IsSasaYogaPresent = False   #initially assume the yoga is not present
    Rule = ""
    Results = ""
    Note = ""
    #two conditions for Sasa yoga to be present
        #cond1 -> Saturn must be in own rashi (Capricorn or Aquarius) OR Saturn must be exhalted(Libra)
        #cond2 -> Saturn must be in Kendra (either from ascendant or from moon)

    #check for Sasa yoga with lagna D1 chart
    lagnasaturn = charts["D1"]["planets"]["Saturn"]
    lagnamoon = charts["D1"]["planets"]["Moon"]

    #For condition 1
    lagna_cond1_exhaltation = False
    lagna_cond1_swarashi = False
    if(lagnasaturn["sign"] == "Libra"):
        lagna_cond1_exhaltation = True
        Rule = Rule + "In Lagna chart, Saturn is exhalted [Libra]"
    elif (lagnasaturn["sign"] == "Capricorn"):
        lagna_cond1_swarashi = True
        Rule = Rule + f'In Lagna chart, Saturn is in Own sign [Capricorn]'
    elif (lagnasaturn["sign"] == "Aquarius"):
        lagna_cond1_swarashi = True
        Rule = Rule + f'In Lagna chart, Saturn is in Own sign [Aquarius]'
    else:
        lagna_cond1_exhaltation = False
        lagna_cond1_swarashi = False
    lagna_cond1 = lagna_cond1_exhaltation or lagna_cond1_swarashi

    #For condition 2
    lagna_cond2_4mAsc = False
    lagna_cond2_4mMoon = False
    #check for Sasa yoga kendra condition from ascendant
    kendranum_4mlagna = lagnasaturn["house-num"]
    if((kendranum_4mlagna % 3) == 1):
        lagna_cond2_4mAsc = True
        Rule = Rule + f' and in Kendra [house number:{lagnasaturn["house-num"]}]'
    else:
        lagna_cond2_4mAsc = False

    #check for Sasa yoga kendra condition from moon
    kendranum_4mmoon = gen.housediff(lagnamoon["house-num"], lagnasaturn["house-num"])
    if((kendranum_4mmoon % 3) == 1):
        lagna_cond2_4mMoon = True
        Rule = Rule + f' and in Kendra with respect to Moon [house number:{kendranum_4mmoon} from moon]'
    else:
        lagna_cond2_4mMoon = False

    lagna_cond2 = lagna_cond2_4mAsc or lagna_cond2_4mMoon
    IsSasaYogaPresent = lagna_cond1 and lagna_cond2

    #detection part of yoga is over. Now if present then update the other details
    if(IsSasaYogaPresent == True):
        #finish the rule. 
        Rule = Rule + f' Hence Sasa Panchamahapurusha yoga is formed.'

        #Update the results
        Results = f'''Sasa Yoga makes the native practical, realistic, responsible and hardworking. They also develop exceptional mass communication skills and bear an air of authority. Embracing the effects of Saturn wholeheartedly is said to be the mark of a successful person. Saturn can bless people under Sasa Yoga with exceptional abilities to produce positive results.
        Persons with Sasa Yoga in their kundali are well placed in society, often in senior bureaucratic positions. They possess superlative intelligence and leadership qualities. The financial benefits are many; they are blessed with every creature comfort known to man. The effects Sasa yoga may become more pronounced as one grows in years when it is time for the hard work to pay off.
        Natives with Sasa Yoga in their horoscope will be elevated to positions of power. They will enjoy success and riches, and their fame will spread far and wide. They are pragmatic by nature. They are hardworking, conscientious and self-made.
        The native is blessed with the good qualities of Saturn. They are devoted to their mothers and often engage in charitable activities.
        Sasa Yoga enables the natives to draw benefits from spiritualism and meditation. Such people have heightened intuition and can become good spiritual healers and yoga teachers.
        '''           

        #update the notes 
        benefics = charts["D1"]["classifications"]["benefics"].copy()
        malefics = charts["D1"]["classifications"]["malefics"].copy()
        malefics.append("Rahu")
        malefics.append("Ketu")
        aspectedby = charts["D1"]["planets"]["Saturn"]["Aspected-by"]
        conjuncts = charts["D1"]["planets"]["Saturn"]["conjuncts"]
        benefics_aspectingSaturn = list(set(benefics).intersection(aspectedby))
        benefics_conjunctSaturn = list(set(benefics).intersection(conjuncts))
        malefics_aspectingSaturn = list(set(malefics).intersection(aspectedby))
        malefics_conjunctSaturn = list(set(malefics).intersection(conjuncts))
        #getting full list of relevant planets for this yoga
        relevant_planets = ["Sa"]
        if (lagna_cond1_exhaltation  == True):
            relevant_planets.append(lagnasaturn["dispositor"][0:2])
        if (lagna_cond2_4mMoon  == True):
            relevant_planets.append("Mo")
        if (lagna_cond2_4mAsc  == True):
            relevant_planets.append(charts["D1"]["ascendant"]["lagna-lord"][0:2])
        for planet in aspectedby:
            relevant_planets.append(planet[0:2])
        for planet in conjuncts:
            relevant_planets.append(planet[0:2])
        colorlist = ["pink","pink","pink","pink","pink","pink","pink","pink","pink","pink","pink","pink"]


        Note = f'''The Sasa Yoga is strengthened by association with Benefics and weakened by association with malefics. Also the results are subject to strength of ascendant or moon with which the saturn is in kendra.
        Benefic planets aspecting Saturn: {benefics_aspectingSaturn} and conjunct benefics: {benefics_conjunctSaturn}.
        Malefic planets aspecting Saturn: {malefics_aspectingSaturn} and conjunct malefics: {malefics_conjunctSaturn}.
        Consider all these points carefully before concluding the results of this panchamahapurusha yoga.'''

        #Update the yogadosha sections
        common.yogadoshas_dict["SASA"] = {}
        common.yogadoshas_dict["SASA"]["name"] = "Sasa Panchamahapurusha"
        common.yogadoshas_dict["SASA"]["type"] = "Yoga"
        common.yogadoshas_dict["SASA"]["exist"] = IsSasaYogaPresent
        common.yogadoshas_dict["SASA"]["Rule"] = common.iterativeReplace(Rule,"\n ", "\n")
        common.yogadoshas_dict["SASA"]["Result"] = common.iterativeReplace(Results,"\n ", "\n").replace("\n","\n        ") 
        common.yogadoshas_dict["SASA"]["Note"] = common.iterativeReplace(Note,"\n ", "\n")
        common.yogadoshas_dict["SASA"]["Source"] = "https://www.astroyogi.com/kundli/yog/sasa/"
        if 'relevant_planets' in locals():
            common.yogadoshas_dict["SASA"]["relevant_planets"] = relevant_planets
        elif 'relevant_planets2' in locals():
            common.yogadoshas_dict["SASA"]["relevant_planets"] = relevant_planets2

    return IsSasaYogaPresent

    #function to check for Bhadra Panchamahapurusha yoga - Mercury
# ==========================================================================================
# Function Name: BhadraYoga
# Purpose: Calculates the presence of BhadraYoga in the provided horoscope.
# Description: Evaluates BhadraYoga
# Expected Impact: 
# Parameters:
#   - charts (dict): Comprehensive dictionary containing D1, D9 charts and planetary attributes.
# Returns:
#   - Boolean/String: True if the yoga/dosha is present, False otherwise.
# ==========================================================================================
def BhadraYoga(charts):
    IsGlobalPresent = False
    IsBhadraYogaPresent = False   #initially assume the yoga is not present
    Rule = ""
    Results = ""
    Note = ""
    #two conditions for Bhadra yoga to be present
        #cond1 -> Mercury must be in own rashi (Gemini) OR Mercury must be exhalted(Virgo)
        #cond2 -> Mercury must be in Kendra (either from ascendant or from moon)

    #check for Bhadra yoga with lagna D1 chart
    lagnamercury = charts["D1"]["planets"]["Mercury"]
    lagnamoon = charts["D1"]["planets"]["Moon"]

    #For condition 1
    lagna_cond1_exhaltation = False
    lagna_cond1_swarashi = False
    if(lagnamercury["sign"] == "Virgo"):
        lagna_cond1_exhaltation = True
        Rule = Rule + "In Lagna chart, Mercury is exhalted [Virgo]"
    elif (lagnamercury["sign"] == "Gemini"):
        lagna_cond1_swarashi = True
        Rule = Rule + f'In Lagna chart, Mercury is in Own sign [Gemini]'
    else:
        lagna_cond1_exhaltation = False
        lagna_cond1_swarashi = False
    lagna_cond1 = lagna_cond1_exhaltation or lagna_cond1_swarashi

    #For condition 2
    lagna_cond2_4mAsc = False
    lagna_cond2_4mMoon = False
    #check for Bhadra yoga kendra condition from ascendant
    kendranum_4mlagna = lagnamercury["house-num"]
    if((kendranum_4mlagna % 3) == 1):
        lagna_cond2_4mAsc = True
        Rule = Rule + f' and in Kendra [house number:{lagnamercury["house-num"]}]'
    else:
        lagna_cond2_4mAsc = False

    #check for Bhadra yoga kendra condition from moon
    kendranum_4mmoon = gen.housediff(lagnamoon["house-num"], lagnamercury["house-num"])
    if((kendranum_4mmoon % 3) == 1):
        lagna_cond2_4mMoon = True
        Rule = Rule + f' and in Kendra with respect to Moon [house number:{kendranum_4mmoon} from moon]'
    else:
        lagna_cond2_4mMoon = False

    lagna_cond2 = lagna_cond2_4mAsc or lagna_cond2_4mMoon
    IsBhadraYogaPresent = lagna_cond1 and lagna_cond2

    #detection part of yoga is over. Now if present then update the other details
    if(IsBhadraYogaPresent == True):
        #finish the rule. 
        Rule = Rule + f' Hence Bhadra Panchamahapurusha yoga is formed.'

        #Update the results
        Results = f'''Bhadra Yoga makes you stand out from the crowd and helps you advance steadily towards the highest level of success. It is believed that if the planet Mercury holds a favourable position in your birth chart and forms the Bhadra Yoga, it will enhance your intelligence and ensure that you achieve success in all your endeavours.
        The native is blessed with superlative intelligence and wisdom to make the right decisions at the right time. Also, it blesses the native with advanced communication skills which enables them to have a deep and lasting influence on people around them.
        This yoga blesses you with a long and healthy life. With the help of Bhadra Yoga, you will have a great career as a journalist, speaker, political person or reformer.
        Bhadra Yoga will improve your mental faculties and make you intelligent and wise. It also gives you a pleasing personality and a flexible mind. You are approachable and easily become a trusted confidant to many.
        '''           

        #update the notes 
        benefics = charts["D1"]["classifications"]["benefics"].copy()
        malefics = charts["D1"]["classifications"]["malefics"].copy()
        malefics.append("Rahu")
        malefics.append("Ketu")
        aspectedby = charts["D1"]["planets"]["Mercury"]["Aspected-by"]
        conjuncts = charts["D1"]["planets"]["Mercury"]["conjuncts"]
        benefics_aspectingMercury = list(set(benefics).intersection(aspectedby))
        benefics_conjunctMercury = list(set(benefics).intersection(conjuncts))
        malefics_aspectingMercury = list(set(malefics).intersection(aspectedby))
        malefics_conjunctMercury = list(set(malefics).intersection(conjuncts))
        #getting full list of relevant planets for this yoga
        relevant_planets = ["Me"]
        if (lagna_cond2_4mMoon  == True):
            relevant_planets.append("Mo")
        if (lagna_cond2_4mAsc  == True):
            relevant_planets.append(charts["D1"]["ascendant"]["lagna-lord"][0:2])
        for planet in aspectedby:
            relevant_planets.append(planet[0:2])
        for planet in conjuncts:
            relevant_planets.append(planet[0:2])
        colorlist = ["pink","pink","pink","pink","pink","pink","pink","pink","pink","pink","pink","pink"]


        Note = f'''The Bhadra Yoga is strengthened by association with Benefics and weakened by association with malefics. Also the results are subject to strength of ascendant or moon with which the mercury is in kendra.
        Benefic planets aspecting Mercury: {benefics_aspectingMercury} and conjunct benefics: {benefics_conjunctMercury}.
        Malefic planets aspecting Mercury: {malefics_aspectingMercury} and conjunct malefics: {malefics_conjunctMercury}.
        Consider all these points carefully before concluding the results of this panchamahapurusha yoga.'''

        #Update the yogadosha sections
        common.yogadoshas_dict["BHADRA"] = {}
        common.yogadoshas_dict["BHADRA"]["name"] = "Bhadra Panchamahapurusha"
        common.yogadoshas_dict["BHADRA"]["type"] = "Yoga"
        common.yogadoshas_dict["BHADRA"]["exist"] = IsBhadraYogaPresent
        common.yogadoshas_dict["BHADRA"]["Rule"] = common.iterativeReplace(Rule,"\n ", "\n")
        common.yogadoshas_dict["BHADRA"]["Result"] = common.iterativeReplace(Results,"\n ", "\n").replace("\n","\n        ") 
        common.yogadoshas_dict["BHADRA"]["Note"] = common.iterativeReplace(Note,"\n ", "\n")
        common.yogadoshas_dict["BHADRA"]["Source"] = "https://www.astroyogi.com/kundli/yog/bhadra/"
        if 'relevant_planets' in locals():
            common.yogadoshas_dict["BHADRA"]["relevant_planets"] = relevant_planets
        elif 'relevant_planets2' in locals():
            common.yogadoshas_dict["BHADRA"]["relevant_planets"] = relevant_planets2

    return IsBhadraYogaPresent

    #function to check for Ruchaka Panchamahapurusha yoga - Mars
# ==========================================================================================
# Function Name: RuchakaYoga
# Purpose: Calculates the presence of RuchakaYoga in the provided horoscope.
# Description: Evaluates RuchakaYoga
# Expected Impact: It should not reach here. Something wrong in computation. Dont trust this analysis.
# Parameters:
#   - charts (dict): Comprehensive dictionary containing D1, D9 charts and planetary attributes.
# Returns:
#   - Boolean/String: True if the yoga/dosha is present, False otherwise.
# ==========================================================================================
def RuchakaYoga(charts):
    IsGlobalPresent = False
    IsRuchakaYogaPresent = False   #initially assume the yoga is not present
    Rule = ""
    Results = ""
    Note = ""
    #two conditions for ruchaka yoga to be present
        #cond1 -> Mars must be in own rashi (Aries or Scorpio) OR Mars must be exhalted(Capricorn)
        #cond2 -> Mars must be in Kendra

    #check for ruchaka yoga with lagna D1 chart
    lagnamars = charts["D1"]["planets"]["Mars"]
    lagnamoon = charts["D1"]["planets"]["Moon"]

    #For condition 1
    lagna_cond1_exhaltation = False
    lagna_cond1_swarashi = False
    if(lagnamars["sign"] == "Capricorn"):
        lagna_cond1_exhaltation = True
        Rule = Rule + "In Lagna chart, Mars is exhalted [Capricorn]"
    elif (lagnamars["dispositor"] == "Mars"):
        lagna_cond1_swarashi = True
        Rule = Rule + f'In Lagna chart, Mars is in Own sign [{lagnamars["sign"]}]'
    else:
        lagna_cond1_exhaltation = False
        lagna_cond1_swarashi = False
    lagna_cond1 = lagna_cond1_exhaltation or lagna_cond1_swarashi

    #For condition 2
    lagna_cond2_4mAsc = False
    lagna_cond2_4mMoon = False
    #check for ruchaka yoga kendra condition from ascendant
    kendranum_4mlagna = lagnamars["house-num"]
    if((kendranum_4mlagna % 3) == 1):
        lagna_cond2_4mAsc = True
        Rule = Rule + f' and in Kendra [house number:{lagnamars["house-num"]}]'
    else:
        lagna_cond2_4mAsc = False

    #check for ruchaka yoga kendra condition from moon
    kendranum_4mmoon = gen.housediff(lagnamoon["house-num"], lagnamars["house-num"])
    if((kendranum_4mmoon % 3) == 1):
        lagna_cond2_4mMoon = True
        Rule = Rule + f' and in Kendra with respect to Moon [house number:{kendranum_4mmoon} from moon]'
    else:
        lagna_cond2_4mMoon = False

    lagna_cond2 = lagna_cond2_4mAsc or lagna_cond2_4mMoon
    IsRuchakaYogaPresent = lagna_cond1 and lagna_cond2


    if(IsRuchakaYogaPresent == True):
        #finish the rule. 
        Rule = Rule + f' Hence Ruchaka Panchamahapurusha yoga is formed.'

        #Update the results
        if(lagnamoon["house-num"] == 1): #if moon is in lagna thenruchaka is formed with both and same house distance
            #here ruchaka from ascendant is formed and moon also is in lagna so both are covered
            if (kendranum_4mlagna == 1):
                Results = f'''The  native shall become brave and courageous. His personality will be strong, and he would love to say their point straightforwardly. However, sometimes they might speak in a way that their words may hurt people unknowingly.
                Ruchaka yoga would provide immense physical energy. Their physical well-being would be a treat to watch. Therefore, a career in sports shall enhance their personality and make them successful people. Also, joining forces and being in police work would be good domains for them, career-wise.They will be good leaders.
                Ruchaka Yoga in 1st house comes with a con. With Mars in the first house, the native becomes a victim of the Kuja Dosha or Mangal Dosha. It may bring adversities in the person's life. Specifically, he/she may use all its positive points for attaining wrong deeds. Also, it shall lead to problems in the marital life of the person.
                '''
            elif (kendranum_4mlagna == 4):
                Results = f'''This Ruchaka Yoga provides natives with multiple lands and properties. The person might take birth with property in hand. Along with it, he/she shall possess all comforts and luxuries and true and pure love from mother and other family members.
                Natives shall also possess immense opportunities and growth in their professional world. From here, planet Mars forms a direct aspect with the 10th house. It shall help him grow and become successful in the workplace and grab a good job for himself.
                If the native ever faces hard times, he/she may effortlessly earn money and seek the benefit of wealth. Planet Mars acts as a Karak Grah for real estate and lands. Thus, it is a perfect Yoga to attain success in real estate matters.
                Natives would possess qualities like physical appearance, high energy levels, bravery, and courage. There wont be any shortage of support from people.
                On negative side, Mars in the fourth house makes the native Manglik. However, performing remedies for Mangal dosha can wear off the ill impacts of Kuja Dosha in the chart. With the Mangal Dosha, you may get into quarrelsome behavior and possess the same in the house.
                '''
            elif (kendranum_4mlagna == 7):
                Results = f'''This Ruchaka Yoga makes the person a serial entrepreneur. Native shall be fully driven and possess the energy to grow the business.
                The native is utterly competitive and very active in work. They grab jobs and careers that get them success immensely. However, there are chances that these natives wouldnt take criticism positively. It becomes their behavior to defend themselves as much as possible.
                Ruchaka Yoga leads to natives possessing support from external sources. He/she shall get into partnerships and seek a helping hand from his co-workers and employees. Also, during the Mars Mahadasha, his/her career flourishes to heights. Furthermore, it helps the natives in terms of wealth and business.
                Natives energy also uplifts others. The person becomes a great orator and holds the quality to influence the masses with words and speeches.
                On negative side, Mars in 7th house causes Mangal Dosha. The native becomes utterly aggressive, especially towards the spouse. Also, nature turns possessive around the partner. If the spouse is emotional, the native might deem the attitude of the person as angry.
                '''
            elif (kendranum_4mlagna == 10):
                Results = f'''The benefits of Ruchaka Yoga here are maximum. One because, planet Mars does not form a Mangal Dosha here, second because, in the 10th house, it gains the natural strength of the tenth house. Thus, it also forms a Maha Raj Yoga in the Kundli of the native.
                It helps natives enjoy career growth at an active rate. He/she shall be great as a leader and enjoy successful times and steady growth in her professional life. Moreover, Mars positioning here can create high possibilities for government jobs and politics. Natives would enjoy all sorts of comforts and seek many opportunities in the professional sector of life.
                The physical endurance of the native will be noteworthy and stamina unmatched. So, such people wont be afraid of bearing any sort of physical pain and love using their strengths more than anybody. Along with all this, the placement of Mars in the tenth house shall also make the native achieve utter fame and wealth.
                On negative side, Mars here may make the natives lack patience. He/she shall have to put the effort in excess to make things work. And the hasty decision-making skills will highlight with Mars placement in the 10th house. All this might make natives confront problems in the professional environment and lose important and worth taking opportunities too often. 
                However, on the other hand, natives will definitely be intelligent, and wisdom would be something he/she shall use at its best. Along with it, the energy of Mars will be maximum here. Thus, the person would be courageous and daring to do anything in life. Moreover, with their efforts and energy, natives would achieve greatness and success in life, for sure.
                '''
            else:
                Results = "It should not reach here. Something wrong in computation. Dont trust this analysis."

        else:
            #Here ruchaka is formed by either ascendant or/and moon position but not common house.
            if (lagna_cond2_4mAsc  == True):
                #Here ruchak is formed from lagna then
                if (kendranum_4mlagna == 1):
                    Results = f'''The  native shall become brave and courageous. His personality will be strong, and he would love to say their point straightforwardly. However, sometimes they might speak in a way that their words may hurt people unknowingly.
                    Ruchaka yoga would provide immense physical energy. Their physical well-being would be a treat to watch. Therefore, a career in sports shall enhance their personality and make them successful people. Also, joining forces and being in police work would be good domains for them, career-wise.They will be good leaders.
                    Ruchaka Yoga in 1st house comes with a con. With Mars in the first house, the native becomes a victim of the Kuja Dosha or Mangal Dosha. It may bring adversities in the person's life. Specifically, he/she may use all its positive points for attaining wrong deeds. Also, it shall lead to problems in the marital life of the person.
                    '''
                elif (kendranum_4mlagna == 4):
                    Results = f'''This Ruchaka Yoga provides natives with multiple lands and properties. The person might take birth with property in hand. Along with it, he/she shall possess all comforts and luxuries and true and pure love from mother and other family members.
                    Natives shall also possess immense opportunities and growth in their professional world. From here, planet Mars forms a direct aspect with the 10th house. It shall help him grow and become successful in the workplace and grab a good job for himself.
                    If the native ever faces hard times, he/she may effortlessly earn money and seek the benefit of wealth. Planet Mars acts as a Karak Grah for real estate and lands. Thus, it is a perfect Yoga to attain success in real estate matters.
                    Natives would possess qualities like physical appearance, high energy levels, bravery, and courage. There wont be any shortage of support from people.
                    On negative side, Mars in the fourth house makes the native Manglik. However, performing remedies for Mangal dosha can wear off the ill impacts of Kuja Dosha in the chart. With the Mangal Dosha, you may get into quarrelsome behavior and possess the same in the house.
                    '''
                elif (kendranum_4mlagna == 7):
                    Results = f'''This Ruchaka Yoga makes the person a serial entrepreneur. Native shall be fully driven and possess the energy to grow the business.
                    The native is utterly competitive and very active in work. They grab jobs and careers that get them success immensely. However, there are chances that these natives wouldnt take criticism positively. It becomes their behavior to defend themselves as much as possible.
                    Ruchaka Yoga leads to natives possessing support from external sources. He/she shall get into partnerships and seek a helping hand from his co-workers and employees. Also, during the Mars Mahadasha, his/her career flourishes to heights. Furthermore, it helps the natives in terms of wealth and business.
                    Natives energy also uplifts others. The person becomes a great orator and holds the quality to influence the masses with words and speeches.
                    On negative side, Mars in 7th house causes Mangal Dosha. The native becomes utterly aggressive, especially towards the spouse. Also, nature turns possessive around the partner. If the spouse is emotional, the native might deem the attitude of the person as angry.
                    '''
                elif (kendranum_4mlagna == 10):
                    Results = f'''The benefits of Ruchaka Yoga here are maximum. One because, planet Mars does not form a Mangal Dosha here, second because, in the 10th house, it gains the natural strength of the tenth house. Thus, it also forms a Maha Raj Yoga in the Kundli of the native.
                    It helps natives enjoy career growth at an active rate. He/she shall be great as a leader and enjoy successful times and steady growth in her professional life. Moreover, Mars positioning here can create high possibilities for government jobs and politics. Natives would enjoy all sorts of comforts and seek many opportunities in the professional sector of life.
                    The physical endurance of the native will be noteworthy and stamina unmatched. So, such people wont be afraid of bearing any sort of physical pain and love using their strengths more than anybody. Along with all this, the placement of Mars in the tenth house shall also make the native achieve utter fame and wealth.
                    On negative side, Mars here may make the natives lack patience. He/she shall have to put the effort in excess to make things work. And the hasty decision-making skills will highlight with Mars placement in the 10th house. All this might make natives confront problems in the professional environment and lose important and worth taking opportunities too often. 
                    However, on the other hand, natives will definitely be intelligent, and wisdom would be something he/she shall use at its best. Along with it, the energy of Mars will be maximum here. Thus, the person would be courageous and daring to do anything in life. Moreover, with their efforts and energy, natives would achieve greatness and success in life, for sure.
                    '''
                else:
                    Results = "It should not reach here. Something wrong in computation. Dont trust this analysis. "

            if (lagna_cond2_4mMoon  == True):
                #Here ruchak is formed from Moon then
                if (kendranum_4mmoon == 1):
                    Results = f'''{Results}The  native shall become brave and courageous. His personality will be strong, and he would love to say their point straightforwardly. However, sometimes they might speak in a way that their words may hurt people unknowingly.
                    Ruchaka yoga would provide immense physical energy. Their physical well-being would be a treat to watch. Therefore, a career in sports shall enhance their personality and make them successful people. Also, joining forces and being in police work would be good domains for them, career-wise.They will be good leaders.
                    Ruchaka Yoga in 1st house comes with a con. With Mars in the first house, the native becomes a victim of the Kuja Dosha or Mangal Dosha. It may bring adversities in the person's life. Specifically, he/she may use all its positive points for attaining wrong deeds. Also, it shall lead to problems in the marital life of the person.'''
                elif (kendranum_4mmoon == 4):
                    Results = f'''{Results}This Ruchaka Yoga provides natives with multiple lands and properties. The person might take birth with property in hand. Along with it, he/she shall possess all comforts and luxuries and true and pure love from mother and other family members.
                    Natives shall also possess immense opportunities and growth in their professional world. From here, planet Mars forms a direct aspect with the 10th house. It shall help him grow and become successful in the workplace and grab a good job for himself.
                    If the native ever faces hard times, he/she may effortlessly earn money and seek the benefit of wealth. Planet Mars acts as a Karak Grah for real estate and lands. Thus, it is a perfect Yoga to attain success in real estate matters.
                    Natives would possess qualities like physical appearance, high energy levels, bravery, and courage. There wont be any shortage of support from people.
                    On negative side, Mars in the fourth house makes the native Manglik. However, performing remedies for Mangal dosha can wear off the ill impacts of Kuja Dosha in the chart. With the Mangal Dosha, you may get into quarrelsome behavior and possess the same in the house.'''
                elif (kendranum_4mmoon == 7):
                    Results = f'''{Results}This Ruchaka Yoga makes the person a serial entrepreneur. Native shall be fully driven and possess the energy to grow the business.
                    The native is utterly competitive and very active in work. They grab jobs and careers that get them success immensely. However, there are chances that these natives wouldnt take criticism positively. It becomes their behavior to defend themselves as much as possible.
                    Ruchaka Yoga leads to natives possessing support from external sources. He/she shall get into partnerships and seek a helping hand from his co-workers and employees. Also, during the Mars Mahadasha, his/her career flourishes to heights. Furthermore, it helps the natives in terms of wealth and business.
                    Natives energy also uplifts others. The person becomes a great orator and holds the quality to influence the masses with words and speeches.
                    On negative side, Mars in 7th house causes Mangal Dosha. The native becomes utterly aggressive, especially towards the spouse. Also, nature turns possessive around the partner. If the spouse is emotional, the native might deem the attitude of the person as angry.'''
                elif (kendranum_4mmoon == 10):
                    Results = f'''{Results}The benefits of Ruchaka Yoga here are maximum. One because, planet Mars does not form a Mangal Dosha here, second because, in the 10th house, it gains the natural strength of the tenth house. Thus, it also forms a Maha Raj Yoga in the Kundli of the native.
                    It helps natives enjoy career growth at an active rate. He/she shall be great as a leader and enjoy successful times and steady growth in her professional life. Moreover, Mars positioning here can create high possibilities for government jobs and politics. Natives would enjoy all sorts of comforts and seek many opportunities in the professional sector of life.
                    The physical endurance of the native will be noteworthy and stamina unmatched. So, such people wont be afraid of bearing any sort of physical pain and love using their strengths more than anybody. Along with all this, the placement of Mars in the tenth house shall also make the native achieve utter fame and wealth.
                    On negative side, Mars here may make the natives lack patience. He/she shall have to put the effort in excess to make things work. And the hasty decision-making skills will highlight with Mars placement in the 10th house. All this might make natives confront problems in the professional environment and lose important and worth taking opportunities too often. 
                    However, on the other hand, natives will definitely be intelligent, and wisdom would be something he/she shall use at its best. Along with it, the energy of Mars will be maximum here. Thus, the person would be courageous and daring to do anything in life. Moreover, with their efforts and energy, natives would achieve greatness and success in life, for sure.'''
                else:
                    Results = f"{Results}It should not reach here. Something wrong in computation. Dont trust this analysis."


        #update the notes 
        benefics = charts["D1"]["classifications"]["benefics"].copy()
        malefics = charts["D1"]["classifications"]["malefics"].copy()
        malefics.append("Rahu")
        malefics.append("Ketu")
        aspectedby = charts["D1"]["planets"]["Mars"]["Aspected-by"]
        conjuncts = charts["D1"]["planets"]["Mars"]["conjuncts"]
        benefics_aspectingMars = list(set(benefics).intersection(aspectedby))
        benefics_conjunctMars = list(set(benefics).intersection(conjuncts))
        malefics_aspectingMars = list(set(malefics).intersection(aspectedby))
        malefics_conjunctMars = list(set(malefics).intersection(conjuncts))
        #getting full list of relevant planets for this yoga
        relevant_planets = ["Ma"]
        if (lagna_cond1_exhaltation  == True):
            relevant_planets.append(lagnamars["dispositor"][0:2])
        if (lagna_cond2_4mMoon  == True):
            relevant_planets.append("Mo")
        if (lagna_cond2_4mAsc  == True):
            relevant_planets.append(charts["D1"]["ascendant"]["lagna-lord"][0:2])
        for planet in aspectedby:
            relevant_planets.append(planet[0:2])
        for planet in conjuncts:
            relevant_planets.append(planet[0:2])
        colorlist = ["pink","pink","pink","pink","pink","pink","pink","pink","pink","pink","pink","pink"]


        Note = f'''The Ruchaka Yoga is strengthened by association with Benefics and weakened by association with malefics. Also the results are subject to strength of ascendant or moon with which the mars is in kendra.
        Benefic planets aspecting Mars: {benefics_aspectingMars} and conjunct benefics: {benefics_conjunctMars}.
        Malefic planets aspecting Mars: {malefics_aspectingMars} and conjunct malefics: {malefics_conjunctMars}.
        Consider all these points carefully before concluding the results of this panchamahapurusha yoga.'''

        #Update the yogadosha sections
        common.yogadoshas_dict["RUCHAKA"] = {}
        common.yogadoshas_dict["RUCHAKA"]["name"] = "Ruchaka Panchamahapurusha"
        common.yogadoshas_dict["RUCHAKA"]["type"] = "Yoga"
        common.yogadoshas_dict["RUCHAKA"]["exist"] = IsRuchakaYogaPresent
        common.yogadoshas_dict["RUCHAKA"]["Rule"] = common.iterativeReplace(Rule,"\n ", "\n")
        common.yogadoshas_dict["RUCHAKA"]["Result"] = common.iterativeReplace(Results,"\n ", "\n").replace("\n","\n        ") 
        common.yogadoshas_dict["RUCHAKA"]["Note"] = common.iterativeReplace(Note,"\n ", "\n")
        common.yogadoshas_dict["RUCHAKA"]["Source"] = "https://astrotalk.com/astrology-blog/ruchaka-yoga-in-astrology-impacts-and-benefits-in-different-houses/"
        if 'relevant_planets' in locals():
            common.yogadoshas_dict["RUCHAKA"]["relevant_planets"] = relevant_planets
        elif 'relevant_planets2' in locals():
            common.yogadoshas_dict["RUCHAKA"]["relevant_planets"] = relevant_planets2

    return IsRuchakaYogaPresent

    #function to check for Hamsa Panchamahapurusha yoga - Jupiter
# ==========================================================================================
# Function Name: HamsaYoga
# Purpose: Calculates the presence of HamsaYoga in the provided horoscope.
# Description: Evaluates HamsaYoga
# Expected Impact: 
# Parameters:
#   - charts (dict): Comprehensive dictionary containing D1, D9 charts and planetary attributes.
# Returns:
#   - Boolean/String: True if the yoga/dosha is present, False otherwise.
# ==========================================================================================
def HamsaYoga(charts):
    IsGlobalPresent = False
    IsHamsaYogaPresent = False   #initially assume the yoga is not present
    Rule = ""
    Results = ""
    Note = ""
    #two conditions for Hamsa yoga to be present
        #cond1 -> Jupiter must be in own rashi (Saggitarius or Pisces) OR Jupiter must be exhalted(Cancer)
        #cond2 -> Jupiter must be in Kendra (either from ascendant or from moon)

    #check for Hamsa yoga with lagna D1 chart
    lagnajupiter = charts["D1"]["planets"]["Jupiter"]
    lagnamoon = charts["D1"]["planets"]["Moon"]

    #For condition 1
    lagna_cond1_exhaltation = False
    lagna_cond1_swarashi = False
    if(lagnajupiter["sign"] == "Cancer"):
        lagna_cond1_exhaltation = True
        Rule = Rule + "In Lagna chart, Jupiter is exhalted [Cancer]"
    elif (lagnajupiter["sign"] == "Saggitarius"):
        lagna_cond1_swarashi = True
        Rule = Rule + f'In Lagna chart, Jupiter is in Own sign [Saggitarius]'
    elif (lagnajupiter["sign"] == "Pisces"):
        lagna_cond1_swarashi = True
        Rule = Rule + f'In Lagna chart, Jupiter is in Own sign [Pisces]'
    else:
        lagna_cond1_exhaltation = False
        lagna_cond1_swarashi = False
    lagna_cond1 = lagna_cond1_exhaltation or lagna_cond1_swarashi

    #For condition 2
    lagna_cond2_4mAsc = False
    lagna_cond2_4mMoon = False
    #check for Hamsa yoga kendra condition from ascendant
    kendranum_4mlagna = lagnajupiter["house-num"]
    if((kendranum_4mlagna % 3) == 1):
        lagna_cond2_4mAsc = True
        Rule = Rule + f' and in Kendra [house number:{lagnajupiter["house-num"]}]'
    else:
        lagna_cond2_4mAsc = False

    #check for Hamsa yoga kendra condition from moon
    kendranum_4mmoon = gen.housediff(lagnamoon["house-num"], lagnajupiter["house-num"])
    if((kendranum_4mmoon % 3) == 1):
        lagna_cond2_4mMoon = True
        Rule = Rule + f' and in Kendra with respect to Moon [house number:{kendranum_4mmoon} from moon]'
    else:
        lagna_cond2_4mMoon = False

    lagna_cond2 = lagna_cond2_4mAsc or lagna_cond2_4mMoon
    IsHamsaYogaPresent = lagna_cond1 and lagna_cond2

    #detection part of yoga is over. Now if present then update the other details
    if(IsHamsaYogaPresent == True):
        #finish the rule. 
        Rule = Rule + f' Hence Hamsa Panchamahapurusha yoga is formed.'

        #Update the results
        Results = f'''Incredible Emotional Intelligence & Knowledge for the Welfare of Masses.
        This yoga in your horoscope blesses you with incredible emotional Intelligence and knowledge that brings about the welfare of the masses and underprivileged, drawing great respect for you in society.
        Hamsa Yoga confers respect in society with great knowledge, high rank in educational institution. This yoga has the power to bless you with an incredible amount of emotional intelligence, which can give you strong social connectivity. 
        Hamsa Yoga will help you get support from Jupiter to acquire a good amount of wisdom and knowledge that can lead you towards growth and success with great achievements. It helps the person write great books, accumulate great amount of knowledge for the welfare of society and the underprivileged.
        It is very difficult to stand against a person with Hamsa Yoga and win. Some famous people with Hamsa Yoga are Jayalalitha, Dr APJ Abdul Kalam, Farooq Abdullah etc.'''           

        #update the notes 
        benefics = charts["D1"]["classifications"]["benefics"]
        malefics = charts["D1"]["classifications"]["malefics"]
        malefics.append("Rahu")
        malefics.append("Ketu")
        aspectedby = charts["D1"]["planets"]["Jupiter"]["Aspected-by"]
        conjuncts = charts["D1"]["planets"]["Jupiter"]["conjuncts"]
        benefics_aspectingJupiter = list(set(benefics).intersection(aspectedby))
        benefics_conjunctJupiter = list(set(benefics).intersection(conjuncts))
        malefics_aspectingJupiter = list(set(malefics).intersection(aspectedby))
        malefics_conjunctJupiter = list(set(malefics).intersection(conjuncts))
        #getting full list of relevant planets for this yoga
        relevant_planets = ["Ju"]
        if (lagna_cond2_4mMoon  == True):
            relevant_planets.append("Mo")
        if (lagna_cond2_4mAsc  == True):
            relevant_planets.append(charts["D1"]["ascendant"]["lagna-lord"][0:2])
        for planet in aspectedby:
            relevant_planets.append(planet[0:2])
        for planet in conjuncts:
            relevant_planets.append(planet[0:2])
        colorlist = ["pink","pink","pink","pink","pink","pink","pink","pink","pink","pink","pink","pink"]


        Note = f'''The Hamsa Yoga is strengthened by association with Benefics and weakened by association with malefics. Also the results are subject to strength of ascendant or moon with which the jupiter is in kendra.
        Benefic planets aspecting Jupiter: {benefics_aspectingJupiter} and conjunct benefics: {benefics_conjunctJupiter}.
        Malefic planets aspecting Jupiter: {malefics_aspectingJupiter} and conjunct malefics: {malefics_conjunctJupiter}.
        Consider all these points carefully before concluding the results of this panchamahapurusha yoga.'''

        #Update the yogadosha sections
        common.yogadoshas_dict["HAMSA"] = {}
        common.yogadoshas_dict["HAMSA"]["name"] = "Hamsa Panchamahapurusha"
        common.yogadoshas_dict["HAMSA"]["type"] = "Yoga"
        common.yogadoshas_dict["HAMSA"]["exist"] = IsHamsaYogaPresent
        common.yogadoshas_dict["HAMSA"]["Rule"] = common.iterativeReplace(Rule,"\n ", "\n")
        common.yogadoshas_dict["HAMSA"]["Result"] = common.iterativeReplace(Results,"\n ", "\n").replace("\n","\n        ") 
        common.yogadoshas_dict["HAMSA"]["Note"] = common.iterativeReplace(Note,"\n ", "\n")
        common.yogadoshas_dict["HAMSA"]["Source"] = "https://www.indastro.com/astrology-reports/hamsa-yoga.php"
        if 'relevant_planets' in locals():
            common.yogadoshas_dict["HAMSA"]["relevant_planets"] = relevant_planets
        elif 'relevant_planets2' in locals():
            common.yogadoshas_dict["HAMSA"]["relevant_planets"] = relevant_planets2

    return IsHamsaYogaPresent

    #function to check for Malavya Panchamahapurusha yoga - Venus
# ==========================================================================================
# Function Name: MalavyaYoga
# Purpose: Calculates the presence of MalavyaYoga in the provided horoscope.
# Description: Evaluates MalavyaYoga
# Expected Impact: 
# Parameters:
#   - charts (dict): Comprehensive dictionary containing D1, D9 charts and planetary attributes.
# Returns:
#   - Boolean/String: True if the yoga/dosha is present, False otherwise.
# ==========================================================================================
def MalavyaYoga(charts):
    IsGlobalPresent = False
    IsMalavyaYogaPresent = False   #initially assume the yoga is not present
    Rule = ""
    Results = ""
    Note = ""
    #two conditions for Malavya yoga to be present
        #cond1 -> Venus must be in own rashi (Taurus or Libra) OR Venus must be exhalted(Pisces)
        #cond2 -> Venus must be in Kendra (either from ascendant or from moon)

    #check for Malavya yoga with lagna D1 chart
    lagnavenus = charts["D1"]["planets"]["Venus"]
    lagnamoon = charts["D1"]["planets"]["Moon"]

    #For condition 1
    lagna_cond1_exhaltation = False
    lagna_cond1_swarashi = False
    if(lagnavenus["sign"] == "Pisces"):
        lagna_cond1_exhaltation = True
        Rule = Rule + "In Lagna chart, Venus is exhalted [Pisces]"
    elif (lagnavenus["sign"] == "Taurus"):
        lagna_cond1_swarashi = True
        Rule = Rule + f'In Lagna chart, Venus is in Own sign [Taurus]'
    elif (lagnavenus["sign"] == "Libra"):
        lagna_cond1_swarashi = True
        Rule = Rule + f'In Lagna chart, Venus is in Own sign [Libra]'
    else:
        lagna_cond1_exhaltation = False
        lagna_cond1_swarashi = False
    lagna_cond1 = lagna_cond1_exhaltation or lagna_cond1_swarashi

    #For condition 2
    lagna_cond2_4mAsc = False
    lagna_cond2_4mMoon = False
    #check for Malavya yoga kendra condition from ascendant
    kendranum_4mlagna = lagnavenus["house-num"]
    if((kendranum_4mlagna % 3) == 1):
        lagna_cond2_4mAsc = True
        Rule = Rule + f' and in Kendra [house number:{lagnavenus["house-num"]}]'
    else:
        lagna_cond2_4mAsc = False

    #check for Malavya yoga kendra condition from moon
    kendranum_4mmoon = gen.housediff(lagnamoon["house-num"], lagnavenus["house-num"])
    if((kendranum_4mmoon % 3) == 1):
        lagna_cond2_4mMoon = True
        Rule = Rule + f' and in Kendra with respect to Moon [house number:{kendranum_4mmoon} from moon]'
    else:
        lagna_cond2_4mMoon = False

    lagna_cond2 = lagna_cond2_4mAsc or lagna_cond2_4mMoon
    IsMalavyaYogaPresent = lagna_cond1 and lagna_cond2

    #detection part of yoga is over. Now if present then update the other details
    if(IsMalavyaYogaPresent == True):
        #finish the rule. 
        Rule = Rule + f' Hence Malavya Panchamahapurusha yoga is formed.'

        #Update the results
        Results = f'''The natives having Malavya Yoga in a horoscope will possess a charming and magnetic personality that attracts other people very easily and especially the people from the opposite sex.
        The natives will be good looking, artistic, intelligent, famous, a powerful sense of humor, and possess all materialistic pleasures and richness in life. The natives are praiseworthy, open-minded, determined, powerful, and lucky.
        The natives will be renowned, successful, own many vehicles, highly educated, and lives a life full of luxury and happiness. They will enjoy happiness through life-partner and children along with materialistic happiness.
        Malavya yoga blesses the native with a beautiful and loving wife, success in business, a life full of luxuries and comforts, and fame on the national or international level. It also gives a good home, vehicles, luxury and comfort, and beauty.
        The natives having Malavya yoga can become successful in the professional fields like modeling, cinema, movies and other such fields that require beauty and charm in order to be successful. The natives can excel in the fields of acting, dancing, singing, cosmetics, and fashion.
        Your artistic skills are greatly advanced due to the powerful influence of this yoga in your life. It makes you a visionary and enables you to find solutions to situations with a high level of creativity. The aesthetic part of you shows up in everything you do.
        Some famous persons with this yoga are: Jayalalitha, Sania Mirza, Sonia Gandhi, Jawaharlal Nehru, Mahatma Gandhi etc
        '''           

        #update the notes 
        benefics = charts["D1"]["classifications"]["benefics"]
        malefics = charts["D1"]["classifications"]["malefics"]
        malefics.append("Rahu")
        malefics.append("Ketu")
        aspectedby = charts["D1"]["planets"]["Venus"]["Aspected-by"]
        conjuncts = charts["D1"]["planets"]["Venus"]["conjuncts"]
        benefics_aspectingVenus = list(set(benefics).intersection(aspectedby))
        benefics_conjunctVenus = list(set(benefics).intersection(conjuncts))
        malefics_aspectingVenus = list(set(malefics).intersection(aspectedby))
        malefics_conjunctVenus = list(set(malefics).intersection(conjuncts))
        #getting full list of relevant planets for this yoga
        relevant_planets = ["Ve"]
        if (lagna_cond1_exhaltation  == True):
            relevant_planets.append(lagnavenus["dispositor"][0:2])
        if (lagna_cond2_4mMoon  == True):
            relevant_planets.append("Mo")
        if (lagna_cond2_4mAsc  == True):
            relevant_planets.append(charts["D1"]["ascendant"]["lagna-lord"][0:2])
        for planet in aspectedby:
            relevant_planets.append(planet[0:2])
        for planet in conjuncts:
            relevant_planets.append(planet[0:2])
        colorlist = ["pink","pink","pink","pink","pink","pink","pink","pink","pink","pink","pink","pink"]


        Note = f'''The Malavya Yoga is strengthened by association with Benefics and weakened by association with malefics. Also the results are subject to strength of ascendant or moon with which the venus is in kendra.
        Benefic planets aspecting Venus: {benefics_aspectingVenus} and conjunct benefics: {benefics_conjunctVenus}.
        Malefic planets aspecting Venus: {malefics_aspectingVenus} and conjunct malefics: {malefics_conjunctVenus}.
        Consider all these points carefully before concluding the results of this panchamahapurusha yoga.'''

        #Update the yogadosha sections
        common.yogadoshas_dict["MALAVYA"] = {}
        common.yogadoshas_dict["MALAVYA"]["name"] = "Malavya Panchamahapurusha"
        common.yogadoshas_dict["MALAVYA"]["type"] = "Yoga"
        common.yogadoshas_dict["MALAVYA"]["exist"] = IsMalavyaYogaPresent
        common.yogadoshas_dict["MALAVYA"]["Rule"] = common.iterativeReplace(Rule,"\n ", "\n")
        common.yogadoshas_dict["MALAVYA"]["Result"] = common.iterativeReplace(Results,"\n ", "\n").replace("\n","\n        ") 
        common.yogadoshas_dict["MALAVYA"]["Note"] = common.iterativeReplace(Note,"\n ", "\n")
        common.yogadoshas_dict["MALAVYA"]["Source"] = "https://www.ganeshaspeaks.com/learn-astrology/yogas/malavya-yoga/"
        if 'relevant_planets' in locals():
            common.yogadoshas_dict["MALAVYA"]["relevant_planets"] = relevant_planets
        elif 'relevant_planets2' in locals():
            common.yogadoshas_dict["MALAVYA"]["relevant_planets"] = relevant_planets2

    return IsMalavyaYogaPresent

    #Functions to check for Vipareeta Raja Yogas - Harsha, Sarala , Vimala
    #function to check for Harsha Vipareeta Raja Yoga - 6th/8th/12th Lord in 6th house in lagna
