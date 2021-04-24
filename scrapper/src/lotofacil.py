import requests

lastContest = 2206


def getUrl(contestNumber):
    url = f"http://loterias.caixa.gov.br/wps/portal/loterias/landing/lotofacil/!ut/p/a1/04_Sj9CPykssy0xPLMnMz0vMAfGjzOLNDH0MPAzcDbz8vTxNDRy9_Y2NQ13CDA0sTIEKIoEKnN0dPUzMfQwMDEwsjAw8XZw8XMwtfQ0MPM2I02-AAzgaENIfrh-FqsQ9wBmoxN_FydLAGAgNTKEK8DkRrACPGwpyQyMMMj0VAcySpRM!/dl5/d5/L2dBISEvZ0FBIS9nQSEh/pw/Z7_61L0H0G0J0VSC0AC4GLFAD2003/res/id=buscaResultado/c=cacheLevelPage//p=concurso={contestNumber}?timestampAjax=1619283349708"
    return url


def createContestObject(res):
    data = res.json()
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

    return contest


def createWinnerListObject(res, contestId):
    winners = []
    data = res.json()
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


def scrapp():
    for i in range(1, lastContest + 1):
        url = getUrl(i)
        caixaRes = requests.get(url)
        if caixaRes.status_code == 200:
            constestObject = createContestObject(caixaRes)

            facilyApiRes = requests.post(
                'http://localhost:3000/contest/save-contest', json=constestObject)
            if facilyApiRes.status_code == 200 or facilyApiRes.status_code == 201:
                contestId = facilyApiRes.json()['id']
                print(f'[Contest]: Saved with id: {contestId}')

                winnersList = createWinnerListObject(caixaRes, contestId)
                facilyApiWinnersRes = requests.post(
                    'http://localhost:3000/contest/save-winners', json=winnersList)
                if(facilyApiWinnersRes.status_code == 200 or facilyApiWinnersRes.status_code == 201):
                    print(f'[Winners] Save for contest: {contestId}')

            else:
                print(f'Failure to save contest')
        else:
            print('Failure to get contest')

    print('[Scrapp]: end')
