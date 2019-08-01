import supreme_court
import matplotlib.pyplot as plt

def simpleInfo(caseList):
    unionsList = []
    overturns = []
    for case in caseList:
        #find all cases related to unions
        if case["issue"]["area"] == "Unions":
            unionsList.append(case)
        #find all cases where a precedent was altered
        if case["decision"]["precedent altered?"] == True:
            overturns.append(case)
    
    conservatives = 0
    for case in unionsList:
        #find all unions cases that went conservative
        if case["decision"]["direction"] == "conservative":
            conservatives += 1
    
    narrows = 0
    for case in overturns:
        #find all precedent altering cases with a 5-4 majority
        if case["voting"]["majority"] == 5:
            narrows += 1
    
    print("Percent of conservative decisions in union related cases:", conservatives*100//len(unionsList), "%")
    print("Percent of overturned precedents decided by one justice:", narrows*100//len(overturns), "%")

def plotOverturns(caseList):
    #number of precedents altered per natural court (by id)
    natural_courts = {}
    for case in caseList:
        court = str(case["natural court"]["id"])
        #new entries start at zero
        try:
            natural_courts[court]
        except KeyError:
            natural_courts[court] = 0
        #count up precedents altered per court
        if case["decision"]["precedent altered?"] == True:
            natural_courts[court] += 1

    #plot natural courts against precedent overturns on a bar graph
    plt.figure(figsize=(9,6))
    plt.bar(list(natural_courts.keys()), list(natural_courts.values()))
    plt.xlabel('Natural Court')
    plt.ylabel('Precedents Altered')
    plt.title('Natural Court vs Precedents Altered')
    plt.xticks(list(natural_courts.keys()), rotation='vertical')
    plt.show()

def main():
    print("Loading data...")
    caseList = supreme_court.get_cases(test=False)
    #ask user what type of analysis they want
    answer = ""
    while answer != "graph" and answer != "no graph":
        answer = input("Graph or no graph? ")
    if answer.lower() == "graph":
        plotOverturns(caseList)
    if answer.lower() == "no graph":
        simpleInfo(caseList)

if __name__ == "__main__":
	main()