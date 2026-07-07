import support.generic as gen
import support.globalvariables as gvar

#Section for planet colours in gochar chart based on type of results
SHUBHPHAL = "lime"
NEUTRALPHAL = "white"
ASHUBHPHAL = "red"

phaldeepika_planetPhalNature = {
    "Sun" : {
         "shubh"        : [3,6,10,11],
         "vedh"         : [9,12,4,5],
         "vedh_planets" : ["Moon", "Mars", "Mercury", "Jupiter", "Venus", "Rahu", "Ketu"],
         "ashubh_vedh"  : [4,5,9,11],
         "vipareet_vedh": [6,10,6,9]         
        },
    "Moon" : {
         "shubh"        : [1,3,6,7,10,11],
         "vedh"         : [5,9,12,2,4,8],
         "vedh_planets" : ["Sun", "Mars", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"],
         "ashubh_vedh"  : [1,4,5,8,9,12],
         "vipareet_vedh": [2,6,10,2,6,10]         
        },
    "Mars" : {
         "shubh"        : [3,6,11],
         "vedh"         : [12,9,5],
         "vedh_planets" : ["Sun", "Moon", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"],
         "ashubh_vedh"  : [5,9,12],
         "vipareet_vedh": [7,2,10]         
        },
    "Mercury" : {
         "shubh"        : [2,4,6,8,10,11],
         "vedh"         : [5,3,9,1,8,12],
         "vedh_planets" : ["Sun", "Mars", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"],
         "ashubh_vedh"  : [3,6,7,9,12],
         "vipareet_vedh": [4,10,2,6,10]         
        },
    "Jupiter" : {
         "shubh"        : [2,5,7,9,11],
         "vedh"         : [12,4,3,10,8],
         "vedh_planets" : ["Sun", "Moon", "Mars", "Mercury", "Venus", "Saturn", "Rahu", "Ketu"],
         "ashubh_vedh"  : [3,4,10,12],
         "vipareet_vedh": [4,8,6,10]         
        },
    "Venus" : {
         "shubh"        : [1,2,3,4,5,8,9,11,12],
         "vedh"         : [5,7,1,10,9,5,11,3,6],
         "vedh_planets" : ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Saturn", "Rahu", "Ketu"],
         "ashubh_vedh"  : [6,7,10],
         "vipareet_vedh": [7,11,6]         
        },
    "Saturn" : {
         "shubh"        : [3,6,11],
         "vedh"         : [12,9,5],
         "vedh_planets" : ["Moon", "Mars", "Mercury", "Jupiter", "Venus", "Rahu", "Ketu"],
         "ashubh_vedh"  : [5,9,12],
         "vipareet_vedh": [7,2,10]         
        },
    "Rahu" : {
         "shubh"        : [3,6,10,11],
         "vedh"         : [0,0,0,0],
         "vedh_planets" : ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Ketu"],
         "ashubh_vedh"  : [4,5,9,11],
         "vipareet_vedh": [6,10,6,9]         
        },
    "Ketu" : {
         "shubh"        : [3,6,10,11],
         "vedh"         : [0,0,0,0],
         "vedh_planets" : ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu"],
         "ashubh_vedh"  : [4,5,9,11],
         "vipareet_vedh": [6,10,6,9]          
        },    
} 


def get_gocharphaltype(planetName, natalMoonSign, transitAstrodata):
    #Default ashubh phal
    planetColour = ASHUBHPHAL

    ############### From natal moon check if planet is in shubh stan and if vedh occurs.
    # Find in which house the planet is placed in gochar with respect to natal moon
    planet_gochar_hno = gen.housediff(gen.signnum(natalMoonSign),gen.signnum(transitAstrodata["D1"]["planets"][planetName]["sign"]))
    # Check if this house is natural shubh phal or not - If yes then give shubhphal
    if planet_gochar_hno in phaldeepika_planetPhalNature[planetName]["shubh"]:
        planetColour = SHUBHPHAL
        #Now check if the planet is vedh which results in cancellation of shubh phal
        index = phaldeepika_planetPhalNature[planetName]["shubh"].index(planet_gochar_hno)
        vedh_house = phaldeepika_planetPhalNature[planetName]["vedh"][index]
        if (vedh_house == 0):    #if vedh house is mentioned as 0 then vedh is not possible so confirmed shubhphal
            planetColour = SHUBHPHAL
            return planetColour
        vedh_planets = phaldeepika_planetPhalNature[planetName]["vedh_planets"]
        vedh_house_occupants = transitAstrodata["D1"]["houses"][vedh_house-1]["planets"]
        vedhPlanetsInVedhHouse = gen.list_intersection(vedh_planets,vedh_house_occupants)
        if(len(vedhPlanetsInVedhHouse) == 0):   #No vedh planets and hence confirmed shubh phal
            planetColour = SHUBHPHAL
            return planetColour
        else:   #Vedh has occured. So Neutral phal
            planetColour = NEUTRALPHAL

    ############### From natal moon check if planet is in ashubh_vedh stan and if vipareet vedh occurs.
    if planet_gochar_hno in phaldeepika_planetPhalNature[planetName]["ashubh_vedh"]:
        #Planet in ashubh vedh position. Check if vipareet vedh is occuring
        index = phaldeepika_planetPhalNature[planetName]["ashubh_vedh"].index(planet_gochar_hno)
        vipareetvedh_house = phaldeepika_planetPhalNature[planetName]["vipareet_vedh"][index]
        if (vipareetvedh_house == 0):    #if vipareetvedh house is mentioned as 0 then vipareetvedh is not possible so return decided previous result
            return planetColour
        vipareetvedh_house_occupants = transitAstrodata["D1"]["houses"][vipareetvedh_house-1]["planets"]  #.remove(planetName)
        try:
            if(len(vipareetvedh_house_occupants) > 0):  #Vipareet vedh has occured and so planet gives positive results
                planetColour = SHUBHPHAL
        except:
            pass

    return planetColour