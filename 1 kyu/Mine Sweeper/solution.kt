import java.lang.RuntimeException
import java.lang.StringBuilder

class MineSweeper(board: String, nMines: Int) {
    val log = true
    val primaryGrid = Grid(board, nMines)

    fun solve(): String {
        log("\n\nInitial State:\n${primaryGrid.gridToString()}")
        primaryGrid.populateNeighbors()
        var solved = primaryGrid.solveLoop()
        if(solved){
            return primaryGrid.gridToStringFinalOutput()
        }
        else{
            return "?"
        }
    }
    fun log(output: String){
        if(log){
            print(output)
        }
    }



}
class Cell constructor(currentValue: String, rowIdx: Int, colIdx: Int){
    companion object{
        const val SYMBOL_UNKNOWN = "?"
        const val SYMBOL_MINE = "x"
        const val SYMBOL_SIM_MINE = "S"
    }
    val perimeterCellList: MutableList<Cell>
    val rowIdx: Int
    val colIdx: Int
    private var symbol = ""
    init{
        perimeterCellList = ArrayList<Cell>()
        this.rowIdx = rowIdx
        this.colIdx = colIdx
        symbol = currentValue
    }
    fun openCell(){
        val newSymbol = Game.open(rowIdx, colIdx).toString()
        symbol = newSymbol;
    }
    fun markMine(){
        symbol = SYMBOL_MINE;
    }
    fun markUnknown(){
        symbol = SYMBOL_UNKNOWN;
    }
    fun getCoordinateString(): String{
        return "[$rowIdx,$colIdx]"
    }

    override fun toString(): String {
        return symbol;
    }
    fun getSymbolAsInt(): Int{
        if(!this.isNumber()){
            throw RuntimeException("Integer value not available for symbol $symbol")
        }
        else{
            return symbol.toInt()
        }
    }
    fun addNeighbor(neighbor: Cell){
        perimeterCellList.add(neighbor)
    }
    fun isNumber(): Boolean{
        if(symbol.toIntOrNull() == null){
            return false
        }
        return true
    }
    fun isZero(): Boolean{
        if(symbol == "0"){
            return true
        }
        return false
    }
    fun isUnknown(): Boolean{
        if(symbol == SYMBOL_UNKNOWN){
            return true
        }
        return false
    }
    fun isMine(): Boolean{
        if(symbol == SYMBOL_MINE){
            return true
        }
        return false
    }

}
class Scenario constructor(){
    val simulatedMineCells: MutableSet<Cell>
    init{
        simulatedMineCells = HashSet<Cell>()
    }
    fun addSimMine(cell: Cell){
        simulatedMineCells.add(cell)
    }
    fun addAllSimMines(mineCellSet: Set<Cell>){
        simulatedMineCells.addAll(mineCellSet)
    }
    fun createNewScenarioOnMerge(subScenario: Scenario): Scenario{
        val newScenario = Scenario()
        newScenario.addAllSimMines(simulatedMineCells)
        newScenario.addAllSimMines(subScenario.simulatedMineCells)
        return newScenario
    }
    fun hasMines(): Boolean{
        return simulatedMineCells.isNotEmpty()
    }
    override fun toString(): String{
        val sb = StringBuilder("Simulated mines at: ")
        for(simMine in simulatedMineCells){
            sb.append(simMine.getCoordinateString())
        }
        return sb.toString()
    }
    fun findScenarioCommonalityForMines(comparisonScenarioList: List<Scenario>): Scenario{
        val agreedSubScenario = Scenario()
        val comparisonScenarioString = StringBuilder()
        for(comparisonScenario in comparisonScenarioList){
            comparisonScenarioString.append("$comparisonScenario\n")
        }
        log("Testing for commonality of scenario mine cells between this scenario: ${this} and \n${comparisonScenarioString.toString()}")
        for(simulatedMineCell in this.simulatedMineCells){
            var agreed = true
            for(comparisonScenario in comparisonScenarioList){
                if(comparisonScenario.simulatedMineCells.contains(simulatedMineCell)){
                    continue
                }
                else{
                    agreed = false
                    break
                }
            }
            if(agreed){
                log("Agreed on mine at [${simulatedMineCell.rowIdx},${simulatedMineCell.colIdx}]")
                agreedSubScenario.addSimMine(simulatedMineCell)
            }
        }
        return agreedSubScenario
    }

    private fun log(output: String){
        println(output)
    }

}

class Grid constructor (board: String, numMines: Int){
    private val grid: MutableList<MutableList<Cell>>
    private val activeNumberedCellList: MutableList<Cell>
    private val activeUnknownCellList: MutableList<Cell>
    private val activeZeroCellList: MutableList<Cell>
    private val unknownCellSet: MutableSet<Cell>
    private val knownMineCellSet: MutableSet<Cell>
    private val rowMaxIdx: Int
    private val colMaxIdx: Int
    private val MAX_NUM_NO_INFO_CELLS_TO_RECURSIVE_EVALUATE = 3

    var numMines = 0
    var numMinesFound = 0


    init {
        this.numMines = numMines
        log("Input board: \n" + board)
        val rows = board.split("\n")
        val rowNum = rows.count()
        rowMaxIdx = rowNum - 1
        grid = ArrayList<MutableList<Cell>>(rowNum)
        activeNumberedCellList = ArrayList<Cell>()
        activeUnknownCellList = ArrayList<Cell>()
        activeZeroCellList = ArrayList<Cell>()
        knownMineCellSet = HashSet<Cell>()
        unknownCellSet = HashSet<Cell>()
        for ((rowIdx, rowValue) in rows.withIndex()){
            //log("Importing row index $rowIdx with value: $rowValue")
            val values = rowValue.split(" ")
            val gridRow = ArrayList<Cell>(values.size)
            grid.add(gridRow)
            for((colIdx, entry) in values.withIndex()){
                val gridLocation = Cell(entry, rowIdx, colIdx)
                gridRow.add(gridLocation)
                handleUpdatedCellInfo(gridLocation)
            }
        }
        colMaxIdx = grid[0].count() - 1
    }
    // Updates the active lists and sets of the grid based on new info
    private fun handleUpdatedCellInfo(cell: Cell){
        if(cell.isNumber()){
            activeNumberedCellList.add(cell)
            if(cell.isZero()){
                activeZeroCellList.add(cell)
            }
        }
        else if(cell.isMine()){
            knownMineCellSet.add(cell)
        }
        else if(cell.isUnknown()) {
            unknownCellSet.add(cell)
        }
        else{
            throw RuntimeException("Unclear what this cell is: $cell")
        }
    }
    fun getGridLocation(rowIdx: Int, colIdx: Int): Cell{
        return grid[rowIdx][colIdx]
    }
    fun gridToString(): String{
        val gridAsString = StringBuilder()
        for(row in grid){
            for(value in row){
                gridAsString.append(value.toString())
                gridAsString.append(" ")
            }
            gridAsString.append("\n")
        }
        return gridAsString.toString()
    }
    fun gridToStringFinalOutput(): String{
        val gridAsString = StringBuilder()
        for((rowIdx, row) in grid.withIndex()){
            for((colIdx, value) in row.withIndex()){
                gridAsString.append(value.toString())
                if(colIdx != colMaxIdx){
                    gridAsString.append(" ")
                }
            }
            if(rowIdx != rowMaxIdx) {
                gridAsString.append("\n")
            }
        }
        return gridAsString.toString()
    }
    fun populateNeighbors() {
        for((rowIdx, rowValue) in grid.withIndex()){
            for((colIdx, activeGridLocation) in rowValue.withIndex()){// Go to all grid locations, find neighbors, then add yourself to them as a neighbor
                for(rowOffset in -1..1){
                    val neighborRow = rowIdx + rowOffset
                    if((neighborRow < 0) || (neighborRow > rowMaxIdx)){ //If the index is outside of the bounds on the row
                        //log("Neighbor Row of $neighborRow is out of the range, skipping.")
                        continue
                    }
                    for(colOffset in -1..1){
                        val neighborCol = colIdx + colOffset
                        if((neighborCol < 0) || (neighborCol > colMaxIdx)){ //If the index is outside of the bounds on the col
                            //log("Neighbor Column of $neighborCol is out of the range, skipping.")
                            continue
                        }
                        else if((rowOffset == 0) && (colOffset ==0)){
                            //log("Offsets are both zero, skipping.")
                            continue
                        }
                        else {
                            grid[neighborRow][neighborCol].addNeighbor(activeGridLocation)
                            //log("Adding neighbor: [$neighborRow,$neighborCol] to active gridlocation: [$rowIdx,$colIdx]")
                        }
                    }
                }
            }
        }
    }
    private fun log(output: String){
        println(output)
    }
    private fun logIntentionsAndMarkMine(justification: String, cell: Cell, log: Boolean){
        if(log) {
            log("Marking mine at cell [${cell.rowIdx},${cell.colIdx}] with justification of:\n$justification")
        }
        cell.markMine()
        if(log) {
            log("After:\n ${gridToString()}")
        }
        knownMineCellSet.add(cell)
        unknownCellSet.remove(cell)
    }
    private fun logIntentionsAndOpenCell(justification: String, cell: Cell, log: Boolean, updateActiveNumberCellList: Boolean){
        if(log) {
            log("Opening cell [${cell.rowIdx},${cell.colIdx}] with justification of:\n$justification")
        }
        cell.openCell()
        if(log){
            log("After: ${gridToString()}")
        }
        unknownCellSet.remove(cell)
        if(updateActiveNumberCellList){ // Sometimes this can't be allowed as we may be looping over it and it'll cause a concurrent modification exception
            activeNumberedCellList.add(cell)
        }
    }
    private fun zeroSweep(): Boolean{
        var progressMade = false
        val deferredRemovalList = ArrayList<Cell>()
        for(zeroCell in activeZeroCellList){
            for(neighborCell in zeroCell.perimeterCellList){
                if(unknownCellSet.contains(neighborCell)){
                    neighborCell.openCell()
                    unknownCellSet.remove(neighborCell) // It can't be unknown any more
                    activeNumberedCellList.add(neighborCell)
                    progressMade = true
                }
            }
            deferredRemovalList.add(zeroCell) // It can't be active anymore, as it's surrounded by definition
        }
        activeZeroCellList.removeAll(deferredRemovalList)
        activeNumberedCellList.removeAll(deferredRemovalList)
        return progressMade
    }
    private fun possibilityEliminationSweep(): Boolean{
        var progressMade = false
        val deferredRemovalFromActiveNumberList = ArrayList<Cell>()
        val deferredAdditionToActiveNumberList = ArrayList<Cell>()
        for(cell in activeNumberedCellList){
            val numExpectedMines = cell.getSymbolAsInt()
            var numUnknownNeighboringCells = 0
            var numMineNeighboringCells = 0
            val potentialMarkingCellList = ArrayList<Cell>()
            for(neighborCell in cell.perimeterCellList){
                if(knownMineCellSet.contains(neighborCell)){
                    numMineNeighboringCells++
                }
                else if(unknownCellSet.contains(neighborCell)){
                    potentialMarkingCellList.add(neighborCell)
                    numUnknownNeighboringCells++
                }
            }
            // If there are no unknowns in the perimeter, it's surrounded and should no longer be active.
            if(numUnknownNeighboringCells == 0){
                deferredRemovalFromActiveNumberList.add(cell)
            }
            // If all mines are accounted for, but there are still unknowns in the perimeter, then those are safe!
            else if((numExpectedMines == numMineNeighboringCells) && (numUnknownNeighboringCells > 0)){
                for(identifiedSafe in potentialMarkingCellList){
                    logIntentionsAndOpenCell("If all mines are accounted for around a cell ([${cell.rowIdx},${cell.colIdx}]), but there are unknowns in the perimeter, then those are safe.", identifiedSafe, false, false)
                    deferredAdditionToActiveNumberList.add(identifiedSafe)
                    progressMade = true
                }
            }
            // If there are an equal number of unknown neighbors to the number of unaccounted for mines, they are mines.
            else if((numExpectedMines - numMineNeighboringCells) == numUnknownNeighboringCells){
                for(identifiedMine in potentialMarkingCellList){
                    logIntentionsAndMarkMine("If there are an equal number of unknown neighbors to the number of unaccounted for mines, they are mines." +
                            "\nThis was found to be the case while evaluating the neighbors of cell [${cell.rowIdx},${cell.colIdx}]", identifiedMine, false)
                    deferredRemovalFromActiveNumberList.add(identifiedMine)
                    progressMade = true
                }
            }
        }
        activeNumberedCellList.addAll(deferredAdditionToActiveNumberList)
        activeNumberedCellList.removeAll(deferredRemovalFromActiveNumberList)
        return progressMade
    }
    private fun dump(): String{
        val objectString = StringBuilder("\n\n")
        objectString.append("\nactiveNumberedCellList:\n")
        for(cell in activeNumberedCellList){
            objectString.append("\t${cell.getCoordinateString()}")
        }
        objectString.append("\nactiveUnknownCellList:\n")
        for(cell in activeUnknownCellList){
            objectString.append("\t${cell.getCoordinateString()}")
        }
        objectString.append("\nactiveZeroCellList:\n")
        for(cell in activeZeroCellList){
            objectString.append("\t${cell.getCoordinateString()}")
        }
        objectString.append("\nunknownCellSet:\n")
        for(cell in unknownCellSet){
            objectString.append("\t${cell.getCoordinateString()}")
        }
        objectString.append("\nknownMineCellSet:\n")
        for(cell in knownMineCellSet){
            objectString.append("\t${cell.getCoordinateString()}")
        }
        return objectString.toString()
    }

    private fun scenarioRunner(): Boolean{

        val unaccountedForMines = numMines - knownMineCellSet.size
        var guessableCellSet = getGuessableCellSet()  // These are the cells that are adjacent to a number cell.
        log("$unaccountedForMines unaccounted for mines exist in the field.  " +
                "${guessableCellSet.size} cells are guessable that may have them.  " +
                "There are ${unknownCellSet.size} total unknown cells.\n" +
                "${gridToString()}")
        if(guessableCellSet.size == unknownCellSet.size){
            log("All unknown cells are in the guessable set.  So long as there is no ambiguity, we can solve this.")
        }
        else if(guessableCellSet.size < unknownCellSet.size){
            log("Very ambiguous.  We don't know how many mines are in the guessable cells and how many are not.  We must try all number of mines from max to min.")
        }
        val numNoInfoCells = unknownCellSet.size - guessableCellSet.size
        val maxNumberMinesInGuessableSet =
            determineMaxNumOfMinesInGuessableSet(guessableCellSet, unaccountedForMines)
        val minNumberMinesInGuessableSet =
            determineMinNumOfMinesInGuessableSet(guessableCellSet, unaccountedForMines, numNoInfoCells)

        val validScenarioList = ArrayList<Scenario>()

        for (numMinesAssumedInGuessableSet in minNumberMinesInGuessableSet..maxNumberMinesInGuessableSet) {
//            if(numMinesAssumedInGuessableSet != unaccountedForMines){
//                log("Temporary bypass of allowing for fewer mines than can be in the set")
//                continue
//            }
            val scenariosAsIntLists = generateCombinations(
                guessableCellSet.size,
                numMinesAssumedInGuessableSet - 1
            )  // Why one less than unaccounted for mines?
            val scenarioList = ArrayList<Scenario>()
            val guessableCellList = guessableCellSet.toList()
            for (scenarioAsInts in scenariosAsIntLists) {
                scenarioList.add(scenarioFromIntList(scenarioAsInts, guessableCellList))
            }
            for (scenario in scenarioList) {
                engageScenario(scenario, true)
                val valid = validateScenario()
                if (valid) {
                    log("Valid scenario: $scenario")
                    validScenarioList.add(scenario)

                }
                disengageScenario(scenario)
            }
        }
        if(validScenarioList.size == 1){
            engageScenario(validScenarioList[0], false)
            return true
        }
        else if(validScenarioList.size > 1){
            val agreedSubScenario = validScenarioList[0].findScenarioCommonalityForMines(validScenarioList.subList(1, (validScenarioList.size))) //Compare the first to all the others, finding anything that's common to all
            if(agreedSubScenario.hasMines()){
                engageScenario(agreedSubScenario, false)
                return true
            }
            else{
                log("No commonality found on mines.  Trying for safe cells")
                val agreedSafeCells = findScenarioCommonalityForSafe(guessableCellSet, validScenarioList)
                if(agreedSafeCells.isNotEmpty()){
                    for(agreedSafeCell in agreedSafeCells){
                        logIntentionsAndOpenCell("Scenarios have agreed that this is a safe cell", agreedSafeCell, true, true)
                    }
                    return true
                }
//                else{
//                    log("No commonality found for safe cells.")
//                    val provisionalSafeCells = findScenarioCommonalityForSafe(unknownCellSet, validScenarioList)
//                    if(provisionalSafeCells.isNotEmpty()){
//                        for(provisionalSafeCell in provisionalSafeCells){
//                            logIntentionsAndOpenCell("Scenarios have agreed that this is a safe cell", provisionalSafeCell, true)
//                        }
//                        return true
//                    }
//                }
            }
        }
        return false
    }
    private fun findScenarioCommonalityForSafe(possibleCellSet: Set<Cell>, comparisonScenarioList: List<Scenario>): List<Cell>{
        val agreedSafeCellList = ArrayList<Cell>()
        for(possibleSafeCell in possibleCellSet){
            log("\"Testing possible cell [${possibleSafeCell.rowIdx},${possibleSafeCell.colIdx}].")
            var agreedSafe = true
            for(comparisonScenario in comparisonScenarioList){
                if(comparisonScenario.simulatedMineCells.contains(possibleSafeCell)){
                    log("\"Cannot agree on safe at [${possibleSafeCell.rowIdx},${possibleSafeCell.colIdx}] as scenario $comparisonScenario has that cell as a mine.")
                    agreedSafe = false
                    break
                }
            }
            if(agreedSafe){
                log("Agreed on safe at [${possibleSafeCell.rowIdx},${possibleSafeCell.colIdx}]")
                agreedSafeCellList.add(possibleSafeCell)
            }
        }
        return agreedSafeCellList
    }

    /*
    If the guessableset size is equal to the number of unknown cells, it should be solvable unless there is ambiguity
    Determine minimum and maximum number of mines that can be in the guessableSet
    Start from minimum, run scenario, if valid, recur.
     */
    private fun generationalRecursiveScenarioRunner(): ArrayList<Scenario>{
        val unaccountedForMines = numMines - knownMineCellSet.size
        var guessableCellSet = getGuessableCellSet()  // These are the cells that are adjacent to a number cell.
        log("$unaccountedForMines unaccounted for mines exist in the field.  " +
                "${guessableCellSet.size} cells are guessable that may have them.  " +
                "There are ${unknownCellSet.size} total unknown cells.")
        val numNoInfoCells = unknownCellSet.size - guessableCellSet.size
        if(guessableCellSet.size == unknownCellSet.size){   // Base Case!
            log("All unknown cells are in the guessable set.  So long as there is no ambiguity, we can solve this.")

        }
        else if(guessableCellSet.size < unknownCellSet.size) {
            log("Very ambiguous.  We don't know how many mines are in the guessable cells and how many are not.")
        }

        val maxNumberMinesInGuessableSet =
            determineMaxNumOfMinesInGuessableSet(guessableCellSet, unaccountedForMines)
        val minNumberMinesInGuessableSet =
            determineMinNumOfMinesInGuessableSet(guessableCellSet, unaccountedForMines, numNoInfoCells)

        val validScenarioList = ArrayList<Scenario>()
        for (numMinesAssumedInGuessableSet in minNumberMinesInGuessableSet..maxNumberMinesInGuessableSet) {
            val scenariosAsIntLists = generateCombinations(
                guessableCellSet.size,
                unaccountedForMines - 1
            )  // Why one less than unaccounted for mines?
            val scenarioList = ArrayList<Scenario>()
            val guessableCellList = guessableCellSet.toList()
            for (scenarioAsInts in scenariosAsIntLists) {
                scenarioList.add(scenarioFromIntList(scenarioAsInts, guessableCellList))
            }

            // Now we have the scenario combinations as Scenarios.  Time to test them out.

            for (scenario in scenarioList) {
                engageScenario(scenario, true)
                val valid = validateScenario()
                if (valid) {
                    log("Valid scenario at this point. Recursively calling generationalRecursiveScenarioRunner\"): ${scenario.toString()}")
                    log("Recursively calling generationalRecursiveScenarioRunner")
                    val validSubScenarios = generationalRecursiveScenarioRunner()
                    if (validSubScenarios.size == 0) {   // There are no valid subscenarios.  That means this scenario is no good.
                        continue
                    } else if (validSubScenarios.size == 1) {  // There is one valid subscenario.  This means no ambiguity and that we can use this scenario
                        validScenarioList.add(scenario.createNewScenarioOnMerge(validSubScenarios[0]))
                    } else { // Ambiguity!
                        //throw AmbiguityException("More than one possible solution.")
                    }
                }
                disengageScenario(scenario)
            }
        }
        return validScenarioList  // We can never know if we're the first called.  The parent of this will have to handle that.
    }
    private fun determineMinNumOfMinesInGuessableSet(guessableCellSet: Set<Cell>, numUnaccountedForMines: Int, numNoInfoCells: Int): Int{
        if(numNoInfoCells > numUnaccountedForMines){
            return 0
        }
        else{
            return numUnaccountedForMines - numNoInfoCells
        }
         // TODO
    }
    private fun determineMaxNumOfMinesInGuessableSet(guessableCellSet: Set<Cell>, numUnaccountedForMines: Int): Int{
        return guessableCellSet.size.coerceAtMost(numUnaccountedForMines) // TODO
    }
    private fun scenarioFromIntList(scenarioIndexes: ArrayList<Int>, guessableCellList: List<Cell>): Scenario{
        val scenario = Scenario()
        for(simMineIndex in scenarioIndexes){
            scenario.addSimMine(guessableCellList[simMineIndex])
        }
        return scenario
    }
    private fun validateScenario(): Boolean{
        for(cell in activeNumberedCellList){
            val numExpectedMines = cell.getSymbolAsInt()
            var numMineNeighboringCells = 0
            for(neighborCell in cell.perimeterCellList){
                if(knownMineCellSet.contains(neighborCell)){
                    numMineNeighboringCells++
                }
            }
            if(numExpectedMines != numMineNeighboringCells){
                return false
            }
        }
        return true

    }
    private fun engageScenario(scenario: Scenario, simulationInd: Boolean){
        for(simMine in scenario.simulatedMineCells){
            if(simulationInd){
                logIntentionsAndMarkMine("Simulation", simMine, false)
            }
            else{
                logIntentionsAndMarkMine("Validated Simulation for application", simMine, true)
            }
        }
    }
    private fun disengageScenario(scenario: Scenario){
        for(simMine in scenario.simulatedMineCells){
            simMine.markUnknown()
            knownMineCellSet.remove(simMine)
            unknownCellSet.add(simMine)
        }
    }
    private fun generateCombinations(spots: Int, mines: Int): ArrayList<ArrayList<Int>>{
        val combinations = ArrayList<ArrayList<Int>>()
        val combinationData = ArrayList<Int>()
        for(i in 0..mines){
            combinationData.add(-1)
        }
        combinationHelper(combinations, combinationData, 0, spots - 1, 0)
        return combinations

    }
    private fun combinationHelper(combinations: ArrayList<ArrayList<Int>>, data: ArrayList<Int>, start: Int, end: Int, index: Int){
        if (index == data.size) {
            val combination = data.clone() as (ArrayList<Int>)
            combinations.add(combination)
        } else if (start <= end) {
            data[index] = start
            combinationHelper(combinations, data, start + 1, end, index + 1)
            combinationHelper(combinations, data, start + 1, end, index)
        }
    }
    private fun getGuessableCellSet(): MutableSet<Cell>{
        val guessableCellSet = HashSet<Cell>()
        for(numberCell in activeNumberedCellList){
            for(neighborCell in numberCell.perimeterCellList){
                if(unknownCellSet.contains(neighborCell)){
                    guessableCellSet.add(neighborCell);
                }
            }
        }
        return guessableCellSet
    }
    fun solveLoop(): Boolean{
        var progressMade = true
        while(progressMade){
            if((knownMineCellSet.size == numMines) && (unknownCellSet.size == 0)){
                log("\n\nThere are no more unknown cells and we have found all the mines.  This is successful.\n" +
                        "${gridToString()}")
                return true
            }
            else if((numMines - knownMineCellSet.size) == 0){ // Are there no more mines, but there are unknown cells?  They're safe!
                 val safeCellList = unknownCellSet.toList()
                 for(safeCell in safeCellList){
                     logIntentionsAndOpenCell("No more mines exist", safeCell, true, true)
                 }
                return true
            }
            else if((numMines - knownMineCellSet.size) == unknownCellSet.size) { // Are there an equal number of unknown cells and mines? They're mines!
                val mineCellList = unknownCellSet.toList()
                for(mineCell in mineCellList){
                    logIntentionsAndMarkMine("No more safe cells exist", mineCell, true)
                }
                return true
            }
            else if(activeNumberedCellList.size == 0){ // Are there no active number cells, and the above solvings won't work?  We can't do anything.
                log("There no active number cells, and we can't make any sweeping solutions?  We can't do anything.")
                return false
            }
            progressMade = zeroSweep()
            if(progressMade){
                //log("\n\nProgress was made in zeroSweep.  Continuing. \n${gridToString()}")
                continue
            }
            else {
                //log("\n\nProgress was not made in zeroSweep.  Escalating. \n${gridToString()}")
                progressMade = possibilityEliminationSweep()
                if (progressMade) {
                    //log("\n\nProgress was made in possibilityEliminationSweep.  Continuing. \n${gridToString()}")
                    continue
                }
                else {
                    //log("\n\nProgress was not made in possibilityEliminationSweep. Escalating. \n${gridToString()}")
                    progressMade = scenarioRunner()
                    if(progressMade){
                        //log("\n\nProgress was made in scenarioRunner.  Continuing. \n${gridToString()}")
                        continue
                }
                    else {
                        //log("\n\nProgress was not made in scenarioRunner. Escalating. \n${gridToString()}")
                    }
                }
            }
        }
        log("Unable to make progress for a full loop. \n${gridToString()} ${dump()}")
        return false
    }
}
____________________________________________________________________________________
typealias PartialSolutions<T> = List<Map<T, Char>>

class MineSweeper(board: String, nMines: Int) {
    val nMines = nMines
    val tiles = build(board)
    val unsolveable = listOf<Map<Tile, Char>>()

    fun solve(): String {
        tiles
            .filter { x -> x.status == Status.Clear }
            .forEach { t -> t.openRecursive(force = true) }
            
        while (true) {
            val nextMove = step(tiles, nMines)
            if (nextMove.isEmpty()) return "?"
            nextMove.forEach { m -> 
                m.forEach { (t, isMine) -> 
                    if (isMine == '1') t.markMine() else t.openRecursive()
                }
            }
            if (tiles.count { x -> x.status == Status.Unknown } == 0) {
                return output(tiles)
            }
        }
    }
    
    fun step(tiles: List<Tile>, nMines: Int): List<Map<Tile, Char>> {
        // Look at each numbered tile adjacent to an unknown
        // Generate a set of all possible placements satisfying the number of adjacent mines
        val placements = tiles
            .filter { t -> t.status == Status.Danger }
            .filter { t -> t.adjacent.any { a -> a.status == Status.Unknown }}
            .map(::partials)
        
        // No numbered squares next to unknowns: use the total number of mines to deduce 
        // whether all the remaining squares are empty or mines, or the map is unsolveable
        if (placements.size == 0) {
            val knownMines = tiles.knownMines()
            val unknown = tiles.unknown()
            return when {
               nMines == knownMines -> completeRemaining(tiles, '0')
               nMines == unknown + knownMines -> completeRemaining(tiles, '1')
               else -> unsolveable
            }
        }
        
        // Any placements that only have a single valid configuration can be applied immediately
        val certain = placements.filter { m -> m.size == 1 }
        if (certain.any()) { return certain.flatten() }
        
        // All overlapping placements must be consistent with each other
        val distinct = mergeConnected(placements)
        if (distinct.size == 0) {
            return unsolveable
        }
        
        // Merged groups that only have a single consistent result can be applied immediately
        if (distinct.any { x -> x.size == 1 }) {
            return distinct
                .filter { x -> x.size == 1 }
                .flatten()
        }
        
        // The overall next move must not introduce too many mines or not leave enough space for remaining mines
        // Cross-join the distinct areas to get all possible sets of next moves
        val knownMines = tiles.knownMines()
        val unknown = tiles.unknown()
        val combined = expandNextMoves<Tile>(distinct)
            .filter { x -> 
                x.values.count { it == '1' } <= nMines - knownMines 
                &&
                x.values.count { it == '1' } + (unknown - x.values.size) >= (nMines - knownMines)
            }
        
        // All tiles for which all scenarios agree can be applied
        // If none agree, the map cannot be solved
        val commonBits = extractCommonTiles<Tile>(combined)
        return if (commonBits.size > 0) {
            listOf(commonBits)
        } else { 
            unsolveable 
        }
    }
    
    fun partials(tile: Tile): PartialSolutions<Tile> {
        if (tile.status != Status.Danger) error("Only use for mine-adjacent tiles")
        val u = tile.adjacent.filter { x -> x.status == Status.Unknown }
        val m = tile.adjacent.count { x -> x.status == Status.Mine }
        return combinations(u.size, tile.n - m).map { com -> u.zip(com.toList()).toMap() }
    }

    fun <T> mergeConnected(partials: List<PartialSolutions<T>>): List<PartialSolutions<T>> {
        val merged = mutableSetOf<Int>()
        val nextSet = partials.mapIndexedNotNull { i, p1 ->
            // If a partial is merged, it is removed from the pool
            if (i in merged) {
                return@mapIndexedNotNull null
            }
            // Check every other non-merged partial and merge if they overlap
            partials.forEachIndexed { j, p2 ->
                if (j in (merged + i)) return@forEachIndexed
                val overlap = p1[0].keys.intersect(p2[0].keys)
                if (overlap.any()) {
                    merged.add(i)
                    merged.add(j)
                    // The merged partial should contain only the set of potential solutions 
                    // that are consistent with each other
                    return@mapIndexedNotNull p1.flatMap { group ->
                        p2.mapNotNull { nextGroup ->
                            if (overlap.all { t -> group[t] == nextGroup[t] }) {
                                group + nextGroup
                            } else {
                                null
                            }
                        }
                    }
                }
            }
            // No overlaps, it's an island
            return@mapIndexedNotNull p1
        }
        if (nextSet.size < partials.size) return mergeConnected(nextSet)
        return nextSet
    }
    
    fun <T> expandNextMoves(partials: List<PartialSolutions<T>>): PartialSolutions<T> {
        return partials.reduce { acc, next -> 
            acc.flatMap { s -> 
                next.map { n -> n + s }
            }
        }
    }
    
    fun <T> extractCommonTiles(partials: PartialSolutions<T>): Map<T, Char> =
        partials[0].mapNotNull { (k, v) ->
            if (partials.all { p -> p[k] == v }) { Pair(k, v) } else { null }
        }.toMap()
        
    fun <T> trimSolutionWithTooManyMines(partial: PartialSolutions<T>, mLimit: Int) =
        partial.filter { x -> x.values.count { it == '1' } <= mLimit }
        
    fun completeRemaining(tiles: List<Tile>, isMine: Char) = listOf(
        tiles
            .filter { x -> x.status == Status.Unknown }
            .associateWith { isMine }
    )
    
    fun build(board: String): List<Tile> {
        val tiles = board
            .split("\n")
            .mapIndexed { y, row -> 
                row.split(" ").mapIndexed { x, c -> 
                    Tile(x, y, if (c == "?") Status.Unknown else Status.Clear)
                }
            }
        val offsets = listOf(
            Pair(-1, -1), Pair(0, -1), Pair(1, -1), 
            Pair(-1, 0),               Pair(1, 0), 
            Pair(-1, 1),  Pair(0, 1),  Pair(1, 1)
        )
        return tiles.also {
            val maxX = it[0].size - 1
            val maxY = it.size - 1
            it.forEachIndexed { y, row ->
                row.forEachIndexed { x, t ->
                    t.adjacent = offsets.mapNotNull { o -> 
                        if (x + o.first in 0..maxX && y + o.second in 0..maxY) {
                            tiles[y + o.second][x + o.first]
                        } else {
                            null
                        }
                    }
                }
            }
        }.flatten()
    }
    
    data class Tile(val x: Int, val y: Int, var status: Status) {
        lateinit var adjacent: List<Tile>
        var n = 0
        fun openRecursive(force: Boolean = false) {
            if (!force && status != Status.Unknown) return
            n = Game.open(y, x)
            status = if (n > 0) Status.Danger else Status.Clear
            if (status == Status.Clear) adjacent.forEach { t ->
                t.openRecursive()
            }
        }
        fun markMine() {
            status = Status.Mine
        }
        fun toMapString() = when (status) {
            Status.Unknown -> "?"
            Status.Clear -> "0"
            Status.Danger -> "$n"
            Status.Mine -> "x"
        }
        override fun toString() = "($x, $y)"
    }
    
    fun List<Tile>.knownMines() = this.count { x -> x.status == Status.Mine }
    
    fun List<Tile>.unknown() = this.count { x -> x.status == Status.Unknown }
    
    fun output(tiles: List<Tile>) = tiles
        .groupBy { t -> t.y }
        .toList()
        .joinToString("\n") { row -> row.second.joinToString(" ") { t -> t.toMapString() } }
    
    enum class Status { Unknown, Clear, Danger, Mine }
    
    // Generate all valid combinations of n mines in m places: ["011", "101", "110"]
    companion object Helper {
        val memo = mutableMapOf<Pair<Int, Int>, List<String>>()
        fun combinations(places: Int, mines: Int): List<String> {
            return memo.getOrPut(Pair(places, mines)) {
                (0..(255 shr (8 - places)))
                .map { x -> x.toString(2) }
                .filter { x -> x.count { l -> l == '1' } == mines }
                .map { x -> x.padStart(places, '0') }
            }
        }
    }
}
______________________________________________________________________________
class MineSweeper(board: String, targetMines: Int) {
    val board = Board(board, targetMines)

    fun solve(): String {
        while (true) {
            board.simplify()
            if (board.complete) {
                return board.desc
            }
            if (!board.hypothesise()) {
                return "?"
            }
        }
    }

    class BoardSlot(data: String) {
        var contents = when(data) {
            "x" -> Mine()
            "?" -> Unknown()
            else -> Clue(data.toInt())
        }
        var x = -1
        var y = -1
        lateinit var links: Array<BoardSlot>

        private val surrounding get() = links.map { it.contents }

        val shouldOpen get(): List<BoardSlot>? {
            val clue = contents as? Clue ?: return null
            if (!clue.isSatisfied(surrounding)) return null
            return links.filter { it.contents is Unknown }
        }

        val shouldMarkMine get(): List<BoardSlot>? {
            val clue = contents as? Clue ?: return null
            if (!clue.allElseBombs(surrounding)) return null
            return links.filter { it.contents is Unknown }
        }

        fun isContradiction(remainingMines: Int): Boolean {
            val clue = contents as? Clue ?: return false
            return clue.isContradicted(surrounding, remainingMines)
        }
    }

    abstract class GameObject(val confirmed: Boolean, val finalAnswer: Boolean, val desc: String)
    
    class Clue(val value: Int): GameObject(true, true, value.toString()) {
        fun isSatisfied(surrounding: List<GameObject>) = surrounding.mines == value
        fun allElseBombs(surrounding: List<GameObject>) = surrounding.clear == surrounding.size - value
        fun isContradicted(surrounding: List<GameObject>, remainingMines: Int) = 
            surrounding.mines > value 
                || surrounding.clear > surrounding.size - value 
                || surrounding.mines + remainingMines < value
        
    }
    class Unknown: GameObject(true, false, "?")
    class Mine: GameObject(true, true, "x")
    class HypotheticalClear: GameObject(false, false, " ")
    class HypotheticalMine: GameObject(false, false, "!")

    class Board(raw: String, private val targetMines: Int) {
        val data = raw.split("\n").map { row ->
            row.split(" ").map {
                BoardSlot(it)
            }
        }

        val mines get() = data.sumBy{row -> row.count { it.contents is Mine || it.contents is HypotheticalMine}}
        val height = data.size
        val width = data[0].size
        val complete get(): Boolean {
            var complete = true
            forEach { x, y ->
                if (!this[x, y].contents.finalAnswer) {
                    complete = false
                }
            }
            return complete
        }

        operator fun get(x: Int, y: Int) = data[y][x]

        init {
            //Link slots
            forEach { x, y ->
                val links = ArrayList<BoardSlot>()
                val sX = if (x == 0) x else x - 1
                val eX = if (x == width - 1) x else x + 1
                val sY = if (y == 0) y else y - 1
                val eY = if (y == height - 1) y else y + 1
                for (i in sX..eX) {
                    for (j in sY..eY) {
                        if (i == x && j == y) continue
                        links.add(this[i,j])
                    }
                }
                this[x,y].links = links.toTypedArray()
                this[x,y].x = x
                this[x,y].y = y
            }
        }

        val desc get() = data.joinToString("\n") {
            it.joinToString(" ") { space -> space.contents.desc }
        }

        fun simplify() {
            clearHypotheticals()
            performSimpleLogic(
                { reveal(it) },
                { Mine() }
            )

            if (data.sumBy { row -> row.count { it.contents is Unknown }} + mines == targetMines) {
                forEach { x, y ->
                    if (this[x,y].contents is Unknown) {
                        this[x,y].contents = Mine()
                    }
                }
            }
        }

        fun hypothesise(): Boolean {
            val unknowns = ArrayList<BoardSlot>()
            forEach { x, y ->
                if (this[x, y].contents is Unknown) {
                    unknowns.add(this[x,y])
                }
            }

            for (unknown in unknowns) {
                if (hypothesise(unknown)) {
                    return true
                }
            }

            return false
        }

        private fun hypothesise(slot: BoardSlot): Boolean {
            val canBeMine = !causesContradiction(slot, HypotheticalMine())
            val canBeClear = !causesContradiction(slot, HypotheticalClear())

            if (canBeMine && !canBeClear) {
                slot.contents = Mine()
                return true
            }
            else if (canBeClear && !canBeMine) {
                slot.contents = reveal(slot)
                return true
            }

            return false
        }

        private fun causesContradiction(b: BoardSlot, state: GameObject): Boolean {
            clearHypotheticals()
            b.contents = state
            performSimpleLogic(
                { HypotheticalClear() },
                { HypotheticalMine() }
            )
            
            return isContradiction()
        }
        
        private fun performSimpleLogic(clear: (BoardSlot) -> GameObject, mine: () -> GameObject) {
            var updated = true
            while (updated) {
                updated = false
                forEach { x, y ->
                    val slot = this[x, y]
                    val shouldOpen = slot.shouldOpen
                    if (shouldOpen != null && shouldOpen.isNotEmpty()) {
                        updated = true
                        shouldOpen.forEach {
                            it.contents = clear(it)
                        }
                    }

                    val shouldMarkMine = slot.shouldMarkMine
                    if (shouldMarkMine != null && shouldMarkMine.isNotEmpty()) {
                        updated = true
                        shouldMarkMine.forEach {
                            it.contents = mine()
                        }
                    }
                }
            }
        }

        private fun isContradiction(): Boolean {
            val remainingMines = targetMines - mines
            if (remainingMines < 0) {
                return true
            }

            var contradiction = false
            var allComplete = true
            forEach { x, y ->
                if (this[x,y].isContradiction(remainingMines)) {
                    contradiction = true
                }

                if (this[x,y].contents is Unknown) {
                    allComplete = false
                }
            }

            return contradiction || (allComplete && mines < targetMines)
        }

        fun clearHypotheticals() {
            forEach { x, y ->
                if (!this[x,y].contents.confirmed) {
                    this[x,y].contents = Unknown()
                }
            }
        }

        fun reveal(slot: BoardSlot) = reveal(slot.x, slot.y)
        fun reveal(x: Int, y: Int) = Clue(Game.open(y, x))

        private fun forEach(action: (Int, Int) -> Unit) {
            (0 until width).forEach { x ->
                (0 until height).forEach { y ->
                    action(x, y)
                }
            }
        }
    }
}

val List<MineSweeper.GameObject>.mines get() = count { it is MineSweeper.Mine || it is MineSweeper.HypotheticalMine }
val List<MineSweeper.GameObject>.clear get() = count { it is MineSweeper.Clue || it is MineSweeper.HypotheticalClear }
