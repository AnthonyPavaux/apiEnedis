from custom_components.apiEnedis import myClientEnedis
from custom_components.apiEnedis.sensorEnedis import manageSensorState
import json, datetime

__version__ = "test_saniho"

from custom_components.apiEnedis.const import (
    _consommation,
    _production,
)

def writeDataJson( myDataEnedis ):
    directory = "../myCredential/20210428/"
    for clef in myDataEnedis.getDataJsonKey():
        nomfichier = directory+clef+".json"
        data = myDataEnedis.getDataJson(clef)
        with open(nomfichier, 'w') as outfile:
            json.dump(data, outfile)

def readDataJson():
    import glob, os
    data = {}
    directory = "../myCredential/20210428/*.json"
    listeFile = glob.glob(directory)
    for nomFichier in listeFile:
        with open(nomFichier) as json_file:
            clef = os.path.basename(nomFichier).split(".")[0]
            data[clef] = json.load(json_file)
    return data

def testMulti():
    import configparser
    mon_conteneur = configparser.ConfigParser()
    mon_conteneur.read("../myCredential/security.txt")
    #for qui in ["ENEDIS","ENEDIS2","ENEDIS3","ENEDIS4"]:
    #for qui in ["ENEDIS","ENEDIS7"]:
    #for qui in ["ENEDIS9"]:
    #for qui in ["ENEDIS","ENEDIS2","ENEDIS3","ENEDIS4","ENEDIS15"]:
    #for qui in ["ENEDIS18"]:
    #for qui in ["ENEDIS19"]:
    #for qui in ["ENEDIS"]:
    #for qui in ["ENEDIS21"]:
    for qui in ["ENEDIS"]:
        print("*** traitement de %s " %(qui))
        token = mon_conteneur[qui]['TOKEN']
        PDL_ID = mon_conteneur[qui]['CODE']
        #PDL_ID = "09764109908395"
        #print(qui , "*", token, PDL_ID)
        heureCreusesCh = eval("[['00:00','05:00'], ['22:00', '24:00']]")
        #heureCreusesCh = None
        heuresCreusesON = True
        #heuresCreusesON = False

        # Lecture fichier Json de sortie
        dataJson = {} #readDataJson()
        myDataEnedis = myClientEnedis.myClientEnedis( token=token, PDL_ID=PDL_ID, delai=10,
            heuresCreuses=heureCreusesCh, heuresCreusesCost=0.0797, heuresPleinesCost=0.1175,
            version = __version__, heuresCreusesON=heuresCreusesON, dataJson= dataJson )
        myDataEnedis.getData()

        #myDataEnedis.updateContract()
        #myDataEnedis.updateHCHP()
        #myDataEnedis.updateYesterday()
        #print("myDataEnedis.getContract() : ", myDataEnedis.getContract())
        #print("myDataEnedis.getContract() : ", myDataEnedis.getContract()['usage_point_status'])
        #print("myDataEnedis.getContract() : ", myDataEnedis.getTypePDL())
        #print("myDataEnedis.getLastActivationDate() : ", myDataEnedis.getLastActivationDate())
        #print("myDataEnedis.getHeuresCreuses() : ", myDataEnedis.getHeuresCreuses())

        #print("cnosommation : %s" %myDataEnedis.getYesterday() )
        #myDataEnedis.updateProductionYesterday()
        #print("production : %s" %myDataEnedis.getProductionYesterday() )
        #myDataEnedis.updateLastYear()

        # myDataEnedis._serverName = "http://localhost:5500" # pour mockserver
        # myDataEnedis._serverName = "http://localhost:5501" # pour record
        #myDataEnedis.updateDataYesterdayHCHP()


        # SORTIE OUTPUT
        #writeDataJson( myDataEnedis )

        # ***********************************
        # ***********************************
        myDataSensorEnedis = manageSensorState()
        myDataSensorEnedis.init(myDataEnedis)
        typeSensor = _consommation
        status_counts, state = myDataSensorEnedis.getStatus( typeSensor )
        print("****")
        print(status_counts)

        laDate = datetime.datetime.today() - datetime.timedelta(2)
        status_counts, state = myDataSensorEnedis.getStatusHistory(laDate, "ALL")
        print("****")
        print(status_counts, "/", state)


def testMono():
    import configparser
    mon_conteneur = configparser.ConfigParser()
    mon_conteneur.read("../../../myCredential/security.txt")
    qui = "ENEDIS"
    token = mon_conteneur[qui]['TOKEN']
    PDL_ID = mon_conteneur[qui]['CODE']
    print(token, PDL_ID)

    heureCreusesCh = "[['00:00','05:00'], ['22:00', '24:00']]"
    myDataEnedis = myClientEnedis.myClientEnedis(token=token, PDL_ID=PDL_ID, delai=10, \
                                       heuresCreuses=eval(heureCreusesCh),
                                       heuresCreusesCost=0.20,
                                       heuresPleinesCost=1.30,
                                       version = __version__)
    myDataEnedis.getData()
    print(myDataEnedis.getContract())
    #myDataEnedis.updateProductionYesterday()
    #retour = myDataEnedis.getProductionYesterday()
    #print("retour", retour)
    myDataEnedis.updateYesterday()
    retour = myDataEnedis.getYesterday()
    print("retour", retour)

def testGitInformation():
    from custom_components.apiEnedis import gitinformation
    git = gitinformation.gitinformation( "saniho/apiEnedis" )
    git.getInformation()
    print(git.getVersion())

def main():
    testMulti()
    testGitInformation()
    #testMono()

if __name__ == '__main__':
    main()
""" get all update and charge l'instance et utilisation avec get after ....."""