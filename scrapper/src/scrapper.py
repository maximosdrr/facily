import requests
import time


class Scrapper:
    def __init__(self, contestType, url, lastContest, facilyBaseUrl='http://localhost:3000', requestTimeOut=60):
        self.type = contestType
        self.url = url
        self.lastContest = lastContest
        self.facilySaveContestEndPoint = f'{facilyBaseUrl}/contest/save-contest'
        self.facilySaveWinnersEndPoint = f'{facilyBaseUrl}/contest/save-winners'
        self.facilySaveTodoEndPoint = f'{facilyBaseUrl}/contest/save-todo'
        self.totalScrapped = 0
        self.requestTimeOut = requestTimeOut

    def getUrl(self, contestNumber):
        url = self.url.replace('concurso=0', f'concurso={contestNumber}')
        return url

    def createContestObject(self, data):
        contest = {
            "type": self.type,
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

    def createWinnerListObject(self, data, contestId):
        winners = []
        retrivedWinnerList = data["listaRateioPremio"]

        for i in range(len(retrivedWinnerList)):
            winner = {
                "contest": contestId,
                "amount": retrivedWinnerList[i]["numeroDeGanhadores"],
                "award": retrivedWinnerList[i]["valorPremio"],
                "description": retrivedWinnerList[i]["descricaoFaixa"],
                "range": retrivedWinnerList[i]["faixa"]
            }
            winners.append(winner)

        return winners

    def createTodoObject(self, index):
        return {
            'type': self.type,
            'index': index,
        }

    def getDataFromCaixaApi(self, contestIndex):
        url = self.getUrl(contestIndex)
        caixaRes = None
        caixaRes = requests.get(url, timeout=self.requestTimeOut)
        if not caixaRes == None:
            if caixaRes.status_code == 200 or caixaRes.status_code == 201:
                return caixaRes.json()
            else:
                raise '[Caixa]: Error to get data from caixa api'
        else:
            raise '[Caixa]: Error to get data from caixa api'

    def postContestOnFacilyApi(self, contestObject):
        facilApiRes = None
        facilApiRes = requests.post(
            self.facilySaveContestEndPoint, json=contestObject, timeout=self.requestTimeOut)
        if not facilApiRes == None:
            if(facilApiRes.status_code == 200 or facilApiRes.status_code == 201):
                return facilApiRes.json()['id']
            else:
                raise '[Contest]: Error to post data from facily api'
        else:
            return None

    def postTodoItem(self, todoObject):
        contestNumber = todoObject['index']
        try:
            facilApiRes = requests.post(
                self.facilySaveTodoEndPoint, json=todoObject, timeout=self.requestTimeOut)

            print(
                f'[TODO/{self.type}]: Context number {contestNumber} cant be scrapped, todo latter')
        except:
            print(
                f'[TODO/{self.type}]: TODO OBJECT CANT BE SAVED ! ATETTION ! INDEX: {contestNumber}')

    def postWinnersOnFacilyApi(self, winnersList):
        facilApiRes = None
        facilApiRes = requests.post(
            self.facilySaveWinnersEndPoint, json=winnersList, timeout=self.requestTimeOut)
        if not facilApiRes == None:
            if(facilApiRes.status_code == 200 or facilApiRes.status_code == 201):
                return facilApiRes.json()
            else:
                raise '[Winners]: Error to post data from facily api'
        else:
            raise '[Winners]: Error to post data from facily api'

    def scrapp(self):
        currentTime = time.time()
        for i in range(1, self.lastContest + 1):
            try:
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
                            if self.totalScrapped % 100 == 0 or i == 1:
                                print(
                                    f'[Scrapp/{self.type}]: Progress: {self.totalScrapped}/{self.lastContest}. Execution Time: {time.time() - currentTime}')
                                currentTime = time.time()
            except Exception as e:
                print(e)
                todoObject = self.createTodoObject(i)
                self.postTodoItem(todoObject)
        print(
            f'[Scrapp]: End Scrapp {self.type}. Total Scrapped = {self.totalScrapped}/{self.lastContest}')
