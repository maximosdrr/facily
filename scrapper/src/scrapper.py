import requests


class Scrapper:
    def __init__(self, contestType, url, lastContest, facilyBaseUrl='http://localhost:3000'):
        self.type = contestType
        self.url = url
        self.lastContest = lastContest
        self.facilySaveContestEndPoint = f'{facilyBaseUrl}/contest/save-contest'
        self.facilySaveWinnersEndPoint = f'{facilyBaseUrl}/contest/save-winners'
        self.totalScrapped = 0

    def getUrl(self, contestNumber):
        url = self.url.replace('concurso=0', f'concurso={contestNumber}')
        return url

    def createContestObject(self, data):
        try:
            contest = {
                "type": "LOTOFACIL",
                "result": data['dezenasSorteadasOrdemSorteio'],
                "location": data['localSorteio'],
                "index": data['numero'],
                "accumulatedSpecialValue": data['valorAcumuladoConcursoEspecial'],
                "accumulatedValueForNextContest": data['valorAcumuladoProximoConcurso'],
                "accumulatedValue": data['valorAcumuladoConcurso_0_5'],
                "collected": data['valorArrecadado'],
                "estimatedValueForNextContest": data['valorEstimadoProximoConcurso'],
            }

            if 'dezenasSorteadasOrdemSorteio' in data:
                contest['result'] = data['dezenasSorteadasOrdemSorteio']
            elif 'listaDezenas' in data:
                contest['result'] = data['listaDezenas']
            else:
                contest['result'] = []

            return contest
        except:
            return None

    def createWinnerListObject(self, data, contestId):
        winners = []
        retrivedWinnerList = data["listaRateioPremio"]

        for i in range(len(retrivedWinnerList)):
            try:
                winner = {
                    "contest": contestId,
                    "amount": retrivedWinnerList[i]["numeroDeGanhadores"],
                    "award": retrivedWinnerList[i]["valorPremio"],
                    "description": retrivedWinnerList[i]["descricaoFaixa"],
                    "range": retrivedWinnerList[i]["faixa"]
                }
                winners.append(winner)
            except:
                return None

        return winners

    def getDataFromCaixaApi(self, contestIndex):
        url = self.getUrl(contestIndex)
        caixaRes = None
        try:
            caixaRes = requests.get(url)
            if caixaRes.status_code == 200 or caixaRes.status_code == 201:
                return caixaRes.json()
            else:
                return None
        except:
            print(
                f'Failure to get response for caixa api with status: {caixaRes.status_code}')
            return None

    def postContestOnFacilyApi(self, contestObject):
        facilApiRes = None
        try:
            facilApiRes = requests.post(
                self.facilySaveContestEndPoint, json=contestObject)
            if(facilApiRes.status_code == 200 or facilApiRes.status_code == 201):
                return facilApiRes.json()['id']
            else:
                return None
        except:
            print(
                f'[CONTEST]: Failure to post contest object on facily api with status: {facilApiRes.status_code}')
            return None

    def postWinnersOnFacilyApi(self, winnersList):
        facilApiRes = None
        try:
            facilApiRes = requests.post(
                self.facilySaveWinnersEndPoint, json=winnersList)
            if(facilApiRes.status_code == 200 or facilApiRes.status_code == 201):
                return facilApiRes.json()
            else:
                return None
        except:
            print(
                f'[WINNERS]: Failure to post contest object on facily api with status: {facilApiRes.status_code}')
            return None

    def scrapp(self):
        caixaRes = None
        for i in range(1, self.lastContest + 1):
            contestData = self.getDataFromCaixaApi(i)
            if not contestData == None:
                contestPostObject = self.createContestObject(contestData)

                if not contestPostObject == None:
                    insertedContestId = self.postContestOnFacilyApi(
                        contestPostObject)
                    winnersPostList = self.createWinnerListObject(
                        contestData, insertedContestId)
                    if not winnersPostList == None:
                        insertedWinnersResult = self.postWinnersOnFacilyApi(
                            winnersPostList)
                        self.totalScrapped += 1
                        print(
                            f'[Scrapp]: Progress: {self.totalScrapped}/{self.lastContest}')
        print(
            f'[Scrapp]: End Scrapp {self.contestType}. Total Scrapped = {self.totalScrapped}/{self.lastContest}')