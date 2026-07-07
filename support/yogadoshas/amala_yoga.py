import support.generic as gen
import support.yogadoshas.common as common

def AmalaYoga(charts):
    IsGlobalPresent = False
    IsAmalaYogaPresent = False
    Name = ""
    Rule = ""
    Title = ""
    Results = ""
    Note = ""

    relevant_planets = []
    colorlist = ["pink","pink","pink","pink","pink","pink","pink","pink","pink","pink","pink","pink"]

    IsAmalaYogaPresent_lagna = False
    IsAmalaYogaPresent_moon = False

    #Only benefic is present in 10th house from lagna or from moon then Amala yoga is formed.
    moonhouse = charts["D1"]["planets"]["Moon"]["house-num"]
    tenthHouse4mMoon = gen.compute_nthsign(moonhouse,10)    
    planets_tenthfromlagna = charts["D1"]["houses"][10-1]["planets"]
    planets_tenthfrommoon = charts["D1"]["houses"][tenthHouse4mMoon-1]["planets"]
    Aspecingplanets_tenthfromlagna = charts["D1"]["houses"][10-1]["aspect-planets"]

    Aspecingplanets_tenthfrommoon = charts["D1"]["houses"][tenthHouse4mMoon-1]["aspect-planets"]

    naturalBenefics = charts["D1"]["classifications"]["natural-benefics"]
    naturalMalefics = charts["D1"]["classifications"]["natural-malefics"]
    #print(f'''moon house = {moonhouse} and 10th from moon : {tenthHouse4mMoon}
    #Planets in 10thfrom moon : {planets_tenthfrommoon} and natural benefics are {naturalBenefics}''')


    #Check if Amala yoga exists with respect to Lagna
    beneficsInTenth4mLagna = gen.list_intersection(naturalBenefics,planets_tenthfromlagna)
    maleficsInTenth4mLagna = gen.list_intersection(naturalMalefics,planets_tenthfromlagna)
    beneficsAspectingTenth4mLagna = gen.list_intersection(naturalBenefics,Aspecingplanets_tenthfromlagna)
    maleficsAspectingTenth4mLagna = gen.list_intersection(naturalMalefics,Aspecingplanets_tenthfromlagna)

    if((len(beneficsInTenth4mLagna)>0) and (len(maleficsInTenth4mLagna)==0)):
        IsAmalaYogaPresent_lagna = True
        Title = "AMALA"
        Name = "Amala"
        Rule = f'''The benefics {beneficsInTenth4mLagna} are placed in 10th house and are not conjoint with any malefics.
        '''
        colorlist[0] = "yellow"
        colorlist[9] = "yellow"
        for p in beneficsInTenth4mLagna:
            relevant_planets.append(p[0:2])
        #Check if any benefic aspects are there
        if(len(beneficsAspectingTenth4mLagna)>0):
            Note = f'''{Note}There is benefic aspect on 10th house from lagna by {beneficsAspectingTenth4mLagna} which strengthens this Yoga.
            '''
            for p in beneficsAspectingTenth4mLagna:
                relevant_planets.append(p[0:2])
        else:
            Note = f'''{Note}There is no benefic aspect on 10th house from lagna.
            '''
        #Check if any malefic aspects are there
        if(len(maleficsAspectingTenth4mLagna)>0):
            Note = f'''{Note}There is malefic aspect on 10th house from lagna by {maleficsAspectingTenth4mLagna} which weakens this Yoga.
            '''
            for p in maleficsAspectingTenth4mLagna:
                relevant_planets.append(p[0:2])
        else:
            Note = f'''{Note}There is no malefic aspect on 10th house from lagna.
            '''

    #Check if Amala yoga exists with respect to Moon
    beneficsInTenth4mMoon = gen.list_intersection(naturalBenefics,planets_tenthfrommoon)
    maleficsInTenth4mMoon = gen.list_intersection(naturalMalefics,planets_tenthfrommoon)
    beneficsAspectingTenth4mMoon = gen.list_intersection(naturalBenefics,Aspecingplanets_tenthfrommoon)
    maleficsAspectingTenth4mMoon = gen.list_intersection(naturalMalefics,Aspecingplanets_tenthfrommoon)

    if((len(beneficsInTenth4mMoon)>0) and (len(maleficsInTenth4mMoon)==0)):
        IsAmalaYogaPresent_moon = True
        Title = "AMALA"
        Name = "Amala"
        Rule = f'''{Rule}The benefics {beneficsInTenth4mMoon} are placed in 10th house from Moon and are not conjoint with any malefics.
        '''
        colorlist[moonhouse-1] = "yellow"
        colorlist[tenthHouse4mMoon-1] = "yellow"
        relevant_planets.append("Mo")
        for p in beneficsInTenth4mMoon:
            relevant_planets.append(p[0:2])
        #Check if any benefic aspects are there
        if(len(beneficsAspectingTenth4mMoon)>0):
            Note = f'''{Note}There is benefic aspect on 10th house from Moon by {beneficsAspectingTenth4mMoon} which strengthens this Yoga.
            '''
            for p in beneficsAspectingTenth4mMoon:
                relevant_planets.append(p[0:2])
        else:
            Note = f'''{Note}There is no benefic aspect on 10th house from Moon.
            '''
        #Check if any malefic aspects are there
        if(len(maleficsAspectingTenth4mMoon)>0):
            Note = f'''{Note}There is malefic aspect on 10th house from Moon by {maleficsAspectingTenth4mLagna} which weakens this Yoga.
            '''
            for p in maleficsAspectingTenth4mMoon:
                relevant_planets.append(p[0:2])
        else:
            Note = f'''{Note}There is no malefic aspect on 10th house from Moon.
            '''

    IsAmalaYogaPresent = IsAmalaYogaPresent_moon or IsAmalaYogaPresent_lagna

    if (IsAmalaYogaPresent == True):   
        Rule = f'''{Rule}Hence Amala Yoga is formed.''' 
        Results = f'''According to Parashara, Amal Yog will confer long lasting fame  and will make the native honoured by the king, enjoy abundant pleasures, charitable, fond of relatives, helpful to others, pious and virtuous.
        According to Phaladeepika, The person born with Amala Yoga at birth will be virtuous, will have faith in religion, will be happy, fortunate, will be honoured by the king, have an amiable nature and will always have a smile on his face.
        '''

        #Update the yogadosha sections
        common.yogadoshas_dict[Title] = {}
        common.yogadoshas_dict[Title]["name"] = Name
        common.yogadoshas_dict[Title]["type"] = "Yoga"
        common.yogadoshas_dict[Title]["exist"] = IsAmalaYogaPresent
        common.yogadoshas_dict[Title]["Rule"] = common.iterativeReplace(Rule,"\n ", "\n")
        common.yogadoshas_dict[Title]["Result"] = common.iterativeReplace(Results,"\n ", "\n").replace("\n","\n        ") 
        common.yogadoshas_dict[Title]["Note"] = common.iterativeReplace(Note,"\n ", "\n")
        common.yogadoshas_dict[Title]["Source"] = ""

    return IsAmalaYogaPresent


    #Main function to load and compute all yogas and doshas and update the json file
